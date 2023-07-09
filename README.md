# sqldao-generator

## Easily generate DAOs and Entities from tables

## Notice

- Currently, only MySQL and one database are supported.

## Usage

- See example/test/generator.py, SampleTest.py
- Generate a dao and entity from a table

```python
from example import dao, entity
from sqldaogenerator.generator.mysql_generator import generate

generate('user', 'password', 'host', port, 'database',
         datasource_package=dao, datasource_name='Datasource', base_dao_package=dao, base_dao_name='BaseDao',
         dao_package=dao, entity_package=entity, entity_name='Sample', table='t_sample', override_datasource=True)
```

- Select

```python
criterion = SampleCriterion.builder().col_var_like('df').col_text_in(['6']).col_tinyint_gte(1).col_int_lte(5).col_double(3.5)
.col_datetime_start('2023-07-04 08:26:40').col_datetime_end('2023-07-04 08:26:40').page_no(1).page_size(10).build()
entities, total = sample_dao.select_sample(criterion)
```

- Insert

```python
now = datetime.now().strftime(date_format)
sample = SampleCriterion.builder().set_col_var('i').set_col_text('6').set_col_tinyint(1).set_col_int(5).set_col_double(3.5)
.set_col_datetime(now).build()
entity = sample_dao.insert_sample(sample)
print(entity.id)
```

- Update

```python
criterion = SampleCriterion.builder().id_in([13, 15]).set_col_var('g').set_col_text('m').set_col_tinyint(3).set_col_int(9)
.set_col_double(6.5).set_col_datetime(datetime.fromisoformat('2023-07-04T21:30:56')).build()
sample_dao.update_sample(criterion)
```

- Delete

```python
criterion = SampleCriterion.builder().id(8).build()
sample_dao.delete_sample(criterion)
```

- Execute in the same transaction

```python
from sqldaogenerator.common.TransactionManager import transactional


@transactional
def test_transactional(self):
    insert...
    update...
    delete...
```