from example import dao, entity
from sqldaogenerator.generator.model.EntityCreateReq import EntityCreateReq
from sqldaogenerator.generator.mysql_generator import generate

username = 'daniel'
password = '0614'
host = 'localhost'
port = 3306
dbname = 'database_test'

if __name__ == "__main__":
    entity_tables = [
        ('Sample', 't_sample'),
    ]

    entities = []
    for entity_name, table in entity_tables:
        entities.append(EntityCreateReq(entity, entity_name, table, dao))
        # entities.append(EntityCreateReq('my.package.entity', entity_name, table, 'my.package.dao'))

    generate(username, password, host, port, dbname,
             datasource_package=dao, datasource_name='Datasource',
             base_dao_package=dao, base_dao_name='BaseDao', entities=entities,
             override_datasource=True)
    # generate(username, password, host, port, dbname,
    #          datasource_package='my.package.dao', datasource_name='Datasource',
    #          base_dao_package='my.package.dao', base_dao_name='BaseDao', entities=entities,
    #          override_datasource=True, source_root=r'D:\my\project')
