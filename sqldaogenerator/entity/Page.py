from dataclasses import dataclass


@dataclass
class Page:
    order_by = 'id desc'
    page = None
    page_size: int = None
