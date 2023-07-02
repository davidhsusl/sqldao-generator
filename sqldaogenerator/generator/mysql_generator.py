import importlib.resources as pkg_resources
import re
from types import ModuleType

from sqlalchemy import create_engine, text

from sample import dao, entity
from sqldaogenerator import resources
from sqldaogenerator.generator.enums.MySqlTypeEnum import MySqlTypeEnum

primary_key_template = "{column} = Column({type}, autoincrement=True, primary_key=True, comment='{comment}')"
column_template = "{column} = Column({type}, comment='{comment}')"
field_template = "{name}: {type} = None"
filter_template = "({name}E.{column}, self.{field})"
date_filter_template = "({name}E.{column}, (self.{column}_start, self.{column}_end))"
insert_template = "{column}={entity_variable}.{column}"


def generate(user: str, password: str, host: str, port: int, database: str, base_dao_package: ModuleType, base_dao_name: str,
             entity_package: ModuleType, dao_package: ModuleType, table: str, entity_name: str):
    # create a BaseDao
    base_dao_file = pkg_resources.files(base_dao_package).joinpath(f"{base_dao_name}.py")
    if not base_dao_file.is_file():
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
            """))

    # create entity, dao
    camelcased_word = re.findall('[A-Z][a-z0-9]*', entity_name)
    underlined_word = '_'.join(camelcased_word).lower()
    columns = []
    fields = []
    equals_filters = []
    in_filters = []
    gte_filters = []
    lte_filters = []
    date_filters = []
    insert_columns = []
    update_columns = []
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
                fields.append(field_template.format(name=column_name, type='str'))
                fields.append(field_template.format(name=f"{column_name}_in", type='list[str]'))
            case [name, ('tinyint' | 'int' | 'double' | 'bigint') as db_type]:
                py_type = 'float' if db_type == 'double' else 'int'
                if name != 'id':
                    fields.append(field_template.format(name=column_name, type=py_type))
                    fields.append(field_template.format(name=f"{column_name}_in", type=f'list[{py_type}]'))
                    fields.append(field_template.format(name=f"{column_name}_gte", type=py_type))
                    fields.append(field_template.format(name=f"{column_name}_lte", type=py_type))
                gte_filters.append(filter_template.format(name=entity_name, column=column_name, field=f"{column_name}_gte"))
                lte_filters.append(filter_template.format(name=entity_name, column=column_name, field=f"{column_name}_lte"))
            case [_, ('datetime')]:
                fields.append(field_template.format(name=column_name, type='datetime | str'))
                fields.append(field_template.format(name=f"{column_name}_in", type='datetime | str'))
                fields.append(field_template.format(name=f"{column_name}_start", type='datetime | str'))
                fields.append(field_template.format(name=f"{column_name}_end", type='datetime | str'))
                date_filters.append(date_filter_template.format(name=entity_name, column=column_name))
        equals_filters.append(filter_template.format(name=entity_name, column=column_name, field=column_name))
        in_filters.append(filter_template.format(name=entity_name, column=column_name, field=f"{column_name}_in"))
        if column_name != 'id':
            insert_columns.append(insert_template.format(column=column_name, entity_variable=underlined_word))
            update_columns.append(f"'{column_name}'")

    # entity
    tab = '    '
    filter_intent = f",\n{tab * 4}"
    template = pkg_resources.files(resources).joinpath('entity_template.txt').read_text()
    template = template.format(name=entity_name, table=table, columns=f'\n{tab}'.join(columns), fields=f'\n{tab}'.join(fields),
                               equals_filters=filter_intent.join(equals_filters), in_filters=filter_intent.join(in_filters),
                               gte_filters=filter_intent.join(gte_filters), lte_filters=filter_intent.join(lte_filters),
                               date_filters=filter_intent.join(date_filters))
    entity_file = pkg_resources.files(entity_package).joinpath(f"{entity_name}.py")
    with entity_file.open('w', encoding='utf-8') as file:
        file.write(template)

    # dao
    template = pkg_resources.files(resources).joinpath('dao_template.txt').read_text()
    template = template.format(base_dao_package=base_dao_package.__package__, base_dao_name=base_dao_name,
                               entity_package=entity_package.__package__, entity_name=entity_name, entity_variable=underlined_word,
                               insert_columns=", ".join(f"\n{tab * 4}{item}" if index % 3 == 0 else item
                                                        for index, item in enumerate(insert_columns)),
                               update_columns=", ".join(f"\n{tab * 7}  {item}" if index % 3 == 0 else item
                                                        for index, item in enumerate(update_columns)))
    entity_file = pkg_resources.files(dao_package).joinpath(f"{entity_name}Dao.py")
    with entity_file.open('w', encoding='utf-8') as file:
        file.write(template)


if __name__ == '__main__':
    generate('daniel', '0614', 'localhost', 3306, 'database_test',
             base_dao_package=dao, base_dao_name='BaseDao',
             entity_package=entity, dao_package=dao, table='t_sample', entity_name='Sample')
