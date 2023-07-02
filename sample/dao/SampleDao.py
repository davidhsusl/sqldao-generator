from sample.dao.BaseDao import BaseDao
from sample.entity.Sample import SampleE, Sample
from sqldaogenerator.common.Criterion import Criterion
from sqldaogenerator.common.transaction_holder import transactional, get_transaction


class SampleDao(BaseDao):

    def select(self, condition: Sample) -> tuple[list[SampleE], int]:
        criterion = Criterion.builder() \
            .equals_filter(condition.equals_filters()).in_filter(condition.in_filters()).gte_filter(condition.gte_filters()) \
            .lte_filter(condition.lte_filters()).date_filter(condition.date_filters()).build()
        with self.Session() as session:
            orders = condition.order_by.split(' ')
            query = session.query(SampleE).filter(*criterion.to_list()).order_by(eval(f"SampleE.{orders[0]}.{orders[1]}()"))
            total = None
            if condition.page is not None and condition.page_size is not None:
                query = query.offset((condition.page - 1) * condition.page_size).limit(condition.page_size)
                total = session.query(SampleE).filter(*criterion).count()
            entities = query.all()
        return entities, len(entities) if total is None else total

    @transactional
    def insert(self, sample: Sample):
        session = get_transaction()
        entity = SampleE(col_var=sample.col_var, col_text=sample.col_text, col_tinyint=sample.col_tinyint, col_int=sample.col_int,
                         col_double=sample.col_double, col_datetime=sample.col_datetime)
        session.add(entity)

    @transactional
    def update(self, condition: Sample, sample: Sample):
        session = get_transaction()
        criterion = Criterion.builder() \
            .equals_filter(condition.equals_filters()).in_filter(condition.in_filters()).gte_filter(condition.gte_filters()) \
            .lte_filter(condition.lte_filters()).date_filter(condition.date_filters()).build()
        entities = session.query(SampleE).filter(*criterion.to_list()).all()
        for entity in entities:
            self.set_not_none(entity, sample, 'col_var', 'col_text', 'col_tinyint', 'col_int', 'col_double', 'col_datetime')

    @transactional
    def delete(self, condition: Sample):
        session = get_transaction()
        criterion = Criterion.builder() \
            .equals_filter(condition.equals_filters()).in_filter(condition.in_filters()).gte_filter(condition.gte_filters()) \
            .lte_filter(condition.lte_filters()).date_filter(condition.date_filters()).build()
        entities = session.query(SampleE).filter(*criterion.to_list()).all()
        for entity in entities:
            session.delete(entity)


sample_dao = SampleDao()
