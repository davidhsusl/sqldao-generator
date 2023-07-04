import importlib.resources as pkg_resources
import re
from types import ModuleType

from sqlalchemy import create_engine, text

from sample import dao, entity
from sqldaogenerator import resources
from sqldaogenerator.generator.enums.MySqlTypeEnum import MySqlTypeEnum

primary_key_template = "{column} = Column({type}, autoincrement=True, primary_key=True, comment='{comment}')"
column_template = "{column} = Column({type}, comment='{comment}')"
set_template = """def set_{column}(self, value: {type}):
        self.values['{column}'] = value
        return self"""
filter_template = """def {column}{suffix}(self, value: {type} = None{other}):
        if value is not None{condition}:
            self.filters.append({entity_name}.{column}{expression})
        return self"""
insert_template = "{column}=criterion.get('{column}', None)"


def add_set(sets: list[str], column: str, type: str):
    sets.append(set_template.format(column=column, type=type))


def add_equal(filters: list[str], column: str, type: str, entity_name: str):
    filters.append(filter_template.format(column=column, suffix='', type=type, entity_name=entity_name,
                                          condition=" and value != ''", expression=' == value', other=''))
    filters.append(filter_template.format(column=column, suffix='_in', type=f"list[{type}]", entity_name=entity_name,
                                          condition=" and len(value) > 0", expression='.in_(value)', other=''))


def add_num(filters: list[str], column: str, type: str, entity_name: str):
    filters.append(filter_template.format(column=column, suffix='_gte', type=type, entity_name=entity_name,
                                          condition="", expression=' >= value', other=''))
    filters.append(filter_template.format(column=column, suffix='_lte', type=type, entity_name=entity_name,
                                          condition="", expression=' <= value', other=''))


def add_datetime(filters: list[str], column: str, type: str, entity_name: str):
    filters.append(filter_template.format(column=column, suffix='_start', type=type, entity_name=entity_name,
                                          condition=" and value != ''", expression=' >= value', other=''))
    filters.append(filter_template.format(column=column, suffix='_end', type=type, entity_name=entity_name,
                                          condition=" and value != ''", expression=' <= value', other=''))


def add_like(filters: list[str], column: str, type: str, entity_name: str):
    filters.append(filter_template.format(column=column, suffix='_like', type=type, entity_name=entity_name,
                                          condition=" and value != ''", expression='.like(f"{left}{value}{right}")',
                                          other=", left='%', right='%'"))


def generate(user: str, password: str, host: str, port: int, database: str, base_dao_package: ModuleType, base_dao_name: str,
             entity_package: ModuleType, dao_package: ModuleType, table: str, entity_name: str, override_base_dao=False):
    # create a BaseDao
    base_dao_file = pkg_resources.files(base_dao_package).joinpath(f"{base_dao_name}.py")
    if override_base_dao or not base_dao_file.is_file():
        template = pkg_resources.files(resources).joinpath('base_dao_template.txt').read_text()
        template = template.format(name=base_dao_name, user=user, password=password, host=host, port=port, dbname=database)
        with base_dao_file.open('w', encoding='utf-8') as file:
            file.write(template)

    connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_string, echo=True, pool_recycle=270)
    with engine.connect() as connection:
        results = connection.execute(text(f"""
            select COLUMN_NAME, DATA_TYPE, COLUMN_KEY, COLUMN_COMMENT
            from information_schema.columns
            where table_name = '{table}'
            """)).all()

    # create entity, dao
    camelcased_word = re.findall('[A-Z][a-z0-9]*', entity_name)
    underlined_word = '_'.join(camelcased_word).lower()
    columns = []
    sets = []
    filters = []
    insert_columns = []
    for result in results:
        column_name = result.COLUMN_NAME.lower()
        data_type = result.DATA_TYPE

        # column
        if result.COLUMN_KEY == 'PRI':
            template = primary_key_template
        else:
            template = column_template
        columns.append(template.format(
            column=column_name, comment=result.COLUMN_COMMENT, type=MySqlTypeEnum[data_type].value))

        # fields, filters
        match [column_name, data_type]:
            case [_, ('varchar' | 'text')]:
                py_type = 'str'
                add_set(sets, column_name, py_type)
                add_equal(filters, column_name, py_type, entity_name)
                add_like(filters, column_name, py_type, entity_name)
            case [_, ('tinyint' | 'int' | 'double' | 'bigint') as db_type]:
                py_type = 'float' if db_type == 'double' else 'int'
                add_set(sets, column_name, py_type)
                add_equal(filters, column_name, py_type, entity_name)
                add_num(filters, column_name, py_type, entity_name)
            case [_, ('datetime')]:
                py_type = 'datetime | str'
                add_set(sets, column_name, py_type)
                add_equal(filters, column_name, py_type, entity_name)
                add_datetime(filters, column_name, py_type, entity_name)
        if column_name != 'id':
            insert_columns.append(insert_template.format(column=column_name, entity_variable=underlined_word))

    # entity
    tab = '    '
    filter_intent = f"\n\n{tab}"
    for template_name, file_name in [('entity_template.txt', entity_name), ('criterion_template.txt', f"{entity_name}Criterion")]:
        template = pkg_resources.files(resources).joinpath(template_name).read_text()
        template = template.format(entity_name=entity_name, table=table, columns=f'\n{tab}'.join(columns),
                                   sets=filter_intent.join(sets), filters=filter_intent.join(filters),
                                   entity_package=entity_package.__package__)
        entity_file = pkg_resources.files(entity_package).joinpath(f"{file_name}.py")
        with entity_file.open('w', encoding='utf-8') as file:
            file.write(template)

    # dao
    template = pkg_resources.files(resources).joinpath('dao_template.txt').read_text()
    template = template.format(base_dao_package=base_dao_package.__package__, base_dao_name=base_dao_name,
                               entity_package=entity_package.__package__, entity_name=entity_name, entity_variable=underlined_word,
                               insert_columns=", ".join(f"\n{tab * 4}{item}" if index % 2 == 0 else item
                                                        for index, item in enumerate(insert_columns)))
    entity_file = pkg_resources.files(dao_package).joinpath(f"{entity_name}Dao.py")
    with entity_file.open('w', encoding='utf-8') as file:
        file.write(template)


if __name__ == '__main__':
    generate('daniel', '0614', 'localhost', 3306, 'database_test',
             base_dao_package=dao, base_dao_name='BaseDao', override_base_dao=True,
             entity_package=entity, dao_package=dao, table='t_sample', entity_name='Sample')
