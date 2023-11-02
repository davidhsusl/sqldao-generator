"""
This file is generated by sqldao-generator; don't modify anything.
If you need to do it, you should create another class.
"""

from sqldaogenerator.common.Criterion import Criterion
from sqldaogenerator.common.TransactionManager import transactional
from example.dao.BaseDao import BaseDao
from example.entity.Sample import Sample


class SampleDao(BaseDao):

    @transactional(auto_commit=False)
    def select(self, criterion: Criterion) -> tuple[list[Sample], int]:
        assert self.is_in_modules(criterion.filters, Sample), \
            'The expressions must be created by the Sample entity.'
        query = self.get_query(criterion, Sample)
        page = criterion.page
        if page.order_by:
            orders = page.order_by.split(' ')
            query = query.order_by(eval(f"Sample.{orders[0]}.{orders[1]}()"))
        total = None
        if page.page_no and page.page_size:
            query = query.offset((page.page_no - 1) * page.page_size).limit(page.page_size)
            total = self.get_query(criterion, Sample).count()
        entities = query.all()
        if entities and criterion.labels:
            entities = self.convert(entities, criterion.labels, Sample)
        return entities, total or len(entities)

    @transactional()
    def insert(self, criterion: Criterion):
        session = self.get_transaction()
        entity = Sample(**criterion.values)
        session.add(entity)
        session.flush()
        session.refresh(entity)
        session.expunge(entity)
        return entity

    @transactional()
    def update(self, criterion: Criterion):
        criterion_list = criterion.filters
        assert criterion_list, 'Must have at least one condition in the update statement.'
        assert self.is_in_modules(criterion_list, Sample), \
            'The expressions must be created by the Sample entity.'
        session = self.get_transaction()
        entities = session.query(Sample).filter(*criterion_list).all()
        for entity in entities:
            for key, value in criterion.items():
                setattr(entity, key, value)
        return len(entities)

    @transactional()
    def delete(self, criterion: Criterion):
        criterion_list = criterion.filters
        assert criterion_list, 'Must have at least one condition in the delete statement.'
        assert self.is_in_modules(criterion_list, Sample), \
            'The expressions must be created by the Sample entity.'
        session = self.get_transaction()
        entities = session.query(Sample).filter(*criterion_list).all()
        for entity in entities:
            session.delete(entity)
        return len(entities)


sample_dao = SampleDao()
