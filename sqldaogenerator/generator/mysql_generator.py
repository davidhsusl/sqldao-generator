from sqldaogenerator.logger.logger import info


def generate(host: str, port: int, user: str, password: str, database: str, entity_package: str, dao_package: str):
    info('This is test')


if __name__ == '__main__':
    generate()
