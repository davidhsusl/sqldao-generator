from setuptools import setup, find_packages

setup(
    name='sqldao-generator',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'mysql-connector-python==8.0.33',
        'SQLAlchemy==2.0.17'
    ],
    author='Daniel Hsu',
    author_email='',
    description='SqlAlchemy DAO generator',
    url='https://github.com/davidhsusl/sqldao-generator',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
