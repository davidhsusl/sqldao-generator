from dataclasses import dataclass


@dataclass
class Page:
    order_by = 'id desc'
    page: int = None
    page_size: int = None
