import inspect
import unittest
from datetime import datetime

from sample.dao.SampleDao import sample_dao
from sample.entity.Sample import Sample


class SampleTest(unittest.TestCase):

    def test_select(self):
        criterion = Sample(col_var='n', col_text_in=['j'], col_tinyint_gte=3, col_int_lte=9, col_double=6.5,
                           col_datetime_start='2023-07-01 21:30:55', col_datetime_end='2023-07-01 21:30:57')
        entities, total = sample_dao.select(criterion)
        for entity in entities:
            print([item for item in inspect.getmembers(entity) if isinstance(item[1], (str, int, float, datetime))])
        self.assertEqual(2, total)

    def test_insert(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sample = Sample(col_var='h', col_text='b', col_tinyint=1, col_int=5, col_double=3.5, col_datetime=now)
        sample_dao.insert(sample)
        entities, total = sample_dao.select(sample)
        print([item for item in inspect.getmembers(entities[0]) if isinstance(item[1], (str, int, float, datetime))])
        self.assertEqual(1, total)

    def test_update(self):
        criterion = Sample(id_in=[13, 15])
        sample = Sample(col_var='n', col_text='j', col_tinyint=3, col_int=9, col_double=6.5,
                        col_datetime=datetime.fromisoformat('2023-07-01T21:30:56'))
        sample_dao.update(criterion, sample)
        entities, total = sample_dao.select(sample)
        print([item for item in inspect.getmembers(entities[0]) if isinstance(item[1], (str, int, float, datetime))])
        self.assertEqual(2, total)

    def test_delete(self):
        criterion = Sample(id_in=[6])
        sample_dao.delete(criterion)
        entities, total = sample_dao.select(criterion)
        self.assertEqual(0, total)


if __name__ == '__main__':
    unittest.main()
