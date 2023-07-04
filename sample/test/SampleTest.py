import inspect
import unittest
from datetime import datetime

from sample.dao.SampleDao import sample_dao
from sample.entity.SampleCriterion import SampleCriterion


class SampleTest(unittest.TestCase):

    def test_select(self):
        criterion = SampleCriterion.builder().col_var('n').col_text_in(['m']).col_tinyint_gte(3).col_int_lte(9).col_double(6.5)\
            .col_datetime_start('2023-07-01 21:30:55').col_datetime_end('2023-07-01 21:30:57').page_no(1).page_size(10).build()
        entities, total = sample_dao.select_sample(criterion)
        for entity in entities:
            print([item for item in inspect.getmembers(entity) if isinstance(item[1], (str, int, float, datetime))])
        self.assertEqual(2, total)

    def test_insert(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sample = SampleCriterion.builder().set_col_var('i').set_col_text('6').set_col_tinyint(1).set_col_int(5).set_col_double(3.5)\
            .set_col_datetime(now).build()
        entity = sample_dao.insert_sample(sample)
        print(entity.id)
        criterion = SampleCriterion.builder().col_datetime(now).build()
        entities, total = sample_dao.select_sample(criterion)
        print([item for item in inspect.getmembers(entities[0]) if isinstance(item[1], (str, int, float, datetime))])
        self.assertEqual(1, total)

    def test_update(self):
        criterion = SampleCriterion.builder().id_in([13, 15]).set_col_var('g').set_col_text('m').set_col_tinyint(3).set_col_int(9)\
            .set_col_double(6.5).set_col_datetime(datetime.fromisoformat('2023-07-04T21:30:56')).build()
        sample_dao.update_sample(criterion)
        entities, total = sample_dao.select_sample(criterion)
        print([item for item in inspect.getmembers(entities[0]) if isinstance(item[1], (str, int, float, datetime))])
        self.assertEqual(2, total)

    def test_delete(self):
        criterion = SampleCriterion.builder().id(8).build()
        sample_dao.delete_sample(criterion)
        entities, total = sample_dao.select_sample(criterion)
        self.assertEqual(0, total)


if __name__ == '__main__':
    unittest.main()
