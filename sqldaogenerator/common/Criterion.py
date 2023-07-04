from dataclasses import dataclass, field

from sqldaogenerator.entity.Page import Page


@dataclass
class Criterion:
    page: Page
    filters: list[any] = field(default_factory=list)
    values: dict[any] = field(default_factory=dict)

    def __getitem__(self, item):
        return self.values[item]

    def get(self, key, default):
        return self.values.get(key, default)

    def items(self):
        return self.values.items()

    def to_list(self):
        return self.filters
