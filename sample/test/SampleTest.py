import inspect
import unittest
from datetime import datetime

from sample.dao.SampleDao import sample_dao
from sample.entity.Sample import Sample


class SampleTest(unittest.TestCase):

    def test_select(self):
        criterion = Sample(col_var='n', col_text_in=['m'], col_tinyint_gte=3, col_int_lte=9, col_double=6.5,
                           col_datetime_start='2023-07-01 21:30:55', col_datetime_end='2023-07-01 21:30:57', page=1, page_size=10)
        entities, total = sample_dao.select_sample(criterion)
        for entity in entities:
            print([item for item in inspect.getmembers(entity) if isinstance(item[1], (str, int, float, datetime))])
        self.assertEqual(2, total)

    def test_insert(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sample = Sample(col_var='i', col_text='6', col_tinyint=1, col_int=5, col_double=3.5, col_datetime=now)
        entity = sample_dao.insert_sample(sample)
        print(entity.id)
        entities, total = sample_dao.select_sample(sample)
        print([item for item in inspect.getmembers(entities[0]) if isinstance(item[1], (str, int, float, datetime))])
        self.assertEqual(1, total)

    def test_update(self):
        criterion = Sample(id_in=[13, 15])
        sample = Sample(col_var='n', col_text='m', col_tinyint=3, col_int=9, col_double=6.5,
                        col_datetime=datetime.fromisoformat('2023-07-01T21:30:56'))
        sample_dao.update_sample(criterion, sample)
        entities, total = sample_dao.select_sample(sample)
        print([item for item in inspect.getmembers(entities[0]) if isinstance(item[1], (str, int, float, datetime))])
        self.assertEqual(2, total)

    def test_delete(self):
        criterion = Sample(id_in=[3])
        sample_dao.delete_sample(criterion)
        entities, total = sample_dao.select_sample(criterion)
        self.assertEqual(0, total)


if __name__ == '__main__':
    unittest.main()
