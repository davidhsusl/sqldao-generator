import inspect
import unittest
import uuid
from datetime import datetime, timedelta

from example.dao.SampleDao import sample_dao
from example.entity.SampleCriterion import SampleCriterion
from sqldaogenerator.common.TransactionManager import transactional

date_format = "%Y-%m-%d %H:%M:%S"


class SampleTest(unittest.TestCase):

    @transactional()
    def test_crud(self):
        # create
        uuid_str = str(uuid.uuid4()).replace("-", "")
        now = datetime.now()
        now_str = now.strftime(date_format)
        sample = (SampleCriterion.builder()
                  .set_col_var("a")
                  .set_col_char(uuid_str)
                  .set_col_text("b")
                  .set_col_tinyint(0)
                  .set_col_int(1)
                  .set_col_double(2.5)
                  .set_col_datetime(now_str)
                  .build())
        entity = sample_dao.insert(sample)
        self.assertIsNotNone(entity.id)

        # read
        criterion_builder = (SampleCriterion.builder()
                             .col_var_like("a")
                             .col_text_in(["b"])
                             .col_tinyint_gte(0)
                             .col_int_lte(1)
                             .col_double(2.5)
                             .col_datetime_start(now_str)
                             .col_datetime_end(now_str)
                             .page_no(1)
                             .page_size(10))
        criterion = criterion_builder.build()
        entities, total = sample_dao.select(criterion)
        self.assertEqual(1, total)
        self.assertEqual(entity.id, entities[0].id)
        self.assertEqual(uuid_str, entities[0].col_char)

        # update
        one_day_later = (now + timedelta(days=1)).strftime(date_format)
        criterion = (criterion_builder
                     .set_col_var("c")
                     .set_col_tinyint(2)
                     .set_col_double(3.5)
                     .set_col_datetime(one_day_later)
                     .build())
        row_count = sample_dao.update(criterion)
        self.assertEqual(1, row_count)
        criterion = (SampleCriterion.builder()
                     .col_var_like("c")
                     .col_text_in(["b"])
                     .col_tinyint_gte(2)
                     .col_int_lte(1)
                     .col_double(3.5)
                     .col_datetime_start(one_day_later)
                     .col_datetime_end(one_day_later)
                     .page_no(1)
                     .page_size(10)
                     .build())
        entities, total = sample_dao.select(criterion)
        self.assertEqual(1, total)
        self.assertEqual(entity.id, entities[0].id)
        self.assertEqual("c", entities[0].col_var)

        # delete
        criterion_for_delete = (SampleCriterion.builder()
                                .id(entity.id)
                                .build())
        row_count = sample_dao.delete(criterion_for_delete)
        self.assertEqual(1, row_count)
        entities, total = sample_dao.select(criterion)
        self.assertEqual(0, total)

    @transactional()
    def test_transactional(self):
        # create
        now = datetime.now()
        now_str = now.strftime(date_format)
        sample = (SampleCriterion.builder()
                  .set_col_var("a")
                  .set_col_text("b")
                  .set_col_tinyint(0)
                  .set_col_int(1)
                  .set_col_double(2.5)
                  .set_col_datetime(now_str)
                  .build())
        entity = sample_dao.insert(sample)
        self.assertIsNotNone(entity.id)

        # read
        criterion_builder = (SampleCriterion.builder()
                             .col_var_like("a")
                             .col_text_in(["b"])
                             .col_tinyint_gte(0)
                             .col_int_lte(1)
                             .col_double(2.5)
                             .col_datetime_start(now_str)
                             .col_datetime_end(now_str)
                             .page_no(1)
                             .page_size(10))
        criterion = criterion_builder.build()
        entities, total = sample_dao.select(criterion)
        self.assertEqual(0, total)

        # delete
        criterion_for_delete = (SampleCriterion.builder()
                                .id(entity.id)
                                .build())
        sample_dao.delete(criterion_for_delete)
        entities, total = sample_dao.select(criterion)
        self.assertEqual(0, total)

    def test_select(self):
        criterion = (SampleCriterion.builder()
                     .col_var_like("a")
                     .col_text_in(["6"])
                     .col_tinyint_gte(1)
                     .col_int_lte(5)
                     .col_double_in([3.5, 4.5])
                     .col_datetime_start("2023-07-04 08:26:40")
                     .col_datetime_end("2023-08-05 18:26:40")
                     .page_no(1)
                     .page_size(10)
                     .order_by("id desc")
                     .build())
        # criterion = SampleCriterion.builder()
        #     .col_tinyint_null(reverse=False)
        #     .build()
        entities, total = sample_dao.select(criterion)
        for entity in entities:
            print([item for item in inspect.getmembers(entity) if
                   isinstance(item[1], (str, int, float, datetime))])
        self.assertEqual(2, total)

    def test_insert(self):
        now = datetime.now().strftime(date_format)
        sample = (SampleCriterion.builder()
                  .set_col_var("abc")
                  .set_col_text("6")
                  .set_col_tinyint(1)
                  .set_col_int(5)
                  .set_col_double(4.5)
                  .set_col_datetime(now)
                  .build())
        entity = sample_dao.insert(sample)
        print(entity.id)
        criterion = (SampleCriterion.builder()
                     .col_datetime(now)
                     .build())
        entities, total = sample_dao.select(criterion)
        print([item for item in inspect.getmembers(entities[0]) if
               isinstance(item[1], (str, int, float, datetime))])
        self.assertEqual(1, total)

    def test_update(self):
        criterion = (SampleCriterion.builder()
                     .id_in([13, 15])
                     .set_col_var("g")
                     .set_col_text("m")
                     .set_col_tinyint(3)
                     .set_col_int(9)
                     .set_col_double(6.5)
                     .set_col_datetime(datetime.fromisoformat("2023-07-04T21:30:56"))
                     .build())
        sample_dao.update(criterion)
        entities, total = sample_dao.select(criterion)
        print([item for item in inspect.getmembers(entities[0]) if
               isinstance(item[1], (str, int, float, datetime))])
        self.assertEqual(2, total)

    def test_delete(self):
        criterion = (SampleCriterion.builder()
                     .id(8)
                     .build())
        sample_dao.delete(criterion)
        entities, total = sample_dao.select(criterion)
        self.assertEqual(0, total)


if __name__ == "__main__":
    unittest.main()
