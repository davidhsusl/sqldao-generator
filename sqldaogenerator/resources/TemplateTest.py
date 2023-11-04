import os

import unittest

from datetime import datetime

from example.test.generator import username, password, host, port, dbname

os.environ['username'] = username
os.environ['password'] = password
os.environ['host'] = host
os.environ['port'] = str(port)
os.environ['dbname'] = dbname
os.environ['echo'] = 'True'
os.environ['transaction_name'] = 'default'

from sqldaogenerator.resources.CriterionTemplate import SampleCriterion

ignore_fields = ['_sa_instance_state']


def to_dict(obj):
    if isinstance(obj, list):
        for i, o in enumerate(obj):
            obj[i] = _to_dict(o)
        return obj
    return _to_dict(obj)


def _to_dict(obj):
    return {key: value for key, value in obj.__dict__.items() if key not in ignore_fields and value is not None}


class SampleTest(unittest.TestCase):

    def test_select(self):
        samples, total = (SampleCriterion.builder()
                          .where()
                          .column_char('char2')
                          .column_varchar('varchar')
                          .column_text('text')
                          # .column_json({'abc': 'json'})
                          .column_tinyint(1)
                          .column_int(9)
                          .column_double(123.456)
                          .column_datetime('2023-11-02 09:00:00')
                          .column_timestamp('2023-11-02 09:16:27')
                          .page_no(1)
                          .page_size(10)
                          .order_by('column_datetime desc')
                          .select())
        self.assertIsNotNone(samples)
        self.assertIsNotNone(total)
        self.assertGreater(len(samples), 0)
        print(total)
        print(len(samples))
        print(to_dict(samples))

    def test_select_distinct(self):
        samples, total = (SampleCriterion.builder()
                          .distinct()
                          .column()
                          .column_text()
                          # .column_int()
                          # .column_datetime()
                          # .column_double()
                          .where()
                          .column_tinyint(1)
                          .select())
        self.assertIsNotNone(samples)
        self.assertIsNotNone(total)
        print(total)
        print(to_dict(samples))

    def test_select_group_by(self):
        samples, total = (SampleCriterion.builder()
                          .column()
                          .column_text(group=True)
                          # .column_datetime(group=True)
                          .column_double(sum=True)
                          .where()
                          .column_tinyint(1)
                          .select())
        self.assertIsNotNone(samples)
        self.assertIsNotNone(total)
        print(total)
        print(to_dict(samples))

    def test_insert(self):
        sample = (SampleCriterion.builder()
                  .modify()
                  .column_char('char3')
                  .column_varchar('varchar')
                  .column_text('text')
                  .column_json({'abc': 'json'})
                  .column_tinyint(1)
                  .column_int(10)
                  .column_double(123.456)
                  .column_datetime('2023-11-02 09:00:00')
                  .column_timestamp(datetime.now())
                  .insert())
        self.assertIsNotNone(sample)
        self.assertIsNotNone(sample.id)
        print(to_dict(sample))

    def test_update(self):
        updated_count = (SampleCriterion.builder()
                         .modify()
                         .column_char('char0')
                         .column_varchar('varchar0')
                         .column_text('text0')
                         .column_json({'abc': 'json0'})
                         .column_tinyint(10)
                         .column_int(100)
                         .column_double(1230.456)
                         .column_datetime('2023-12-02 09:00:00')
                         .column_timestamp(datetime.now())
                         .where()
                         .id(5)
                         .update())
        self.assertIsNotNone(updated_count)
        print(updated_count)

    def test_delete(self):
        deleted_count = (SampleCriterion.builder()
                         .where()
                         .id(5)
                         .delete())
        self.assertIsNotNone(deleted_count)
        print(deleted_count)


if __name__ == '__main__':
    unittest.main()
