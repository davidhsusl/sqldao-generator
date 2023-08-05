from example import dao, entity
from sqldaogenerator.generator.mysql_generator import generate

if __name__ == '__main__':
    generate('daniel', '0614', 'localhost', 3306, 'database_test',
             datasource_package=dao, datasource_name='Datasource',
             base_dao_package=dao, base_dao_name='BaseDao', dao_package=dao,
             entity_package=entity, entity_name='Sample', table='t_sample',
             override_datasource=True)
