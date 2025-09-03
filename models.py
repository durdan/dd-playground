from dataclasses import dataclass
from typing import Optional

@dataclass
class Book:
    title: str
    author: str
    isbn: str
    publication_year: int
    id: Optional[int] = None
    
    def __post_init__(self):
        if not self.title or not self.title.strip():
            raise ValueError("Title is required")
        if not self.author or not self.author.strip():
            raise ValueError("Author is required")
        if not self.isbn or not self.isbn.strip():
            raise ValueError("ISBN is required")
        if not isinstance(self.publication_year, int) or self.publication_year < 0:
            raise ValueError("Publication year must be a positive integer")