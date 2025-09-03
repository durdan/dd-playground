from typing import List, Optional
from models import Book
from database import Database

class BookNotFoundError(Exception):
    pass

class BookRepository:
    def __init__(self, database: Database):
        self.db = database
    
    def create(self, book: Book) -> Book:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO books (title, author, isbn, publication_year) VALUES (?, ?, ?, ?)",
                (book.title, book.author, book.isbn, book.publication_year)
            )
            book.id = cursor.lastrowid
            conn.commit()
            return book
    
    def get_by_id(self, book_id: int) -> Book:
        with self.db.get_connection() as conn:
            row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
            if not row:
                raise BookNotFoundError(f"Book with id {book_id} not found")
            return self._row_to_book(row)
    
    def get_all(self) -> List[Book]:
        with self.db.get_connection() as conn:
            rows = conn.execute("SELECT * FROM books ORDER BY title").fetchall()
            return [self._row_to_book(row) for row in rows]
    
    def update(self, book: Book) -> Book:
        if not book.id:
            raise ValueError("Book ID is required for update")
        
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "UPDATE books SET title = ?, author = ?, isbn = ?, publication_year = ? WHERE id = ?",
                (book.title, book.author, book.isbn, book.publication_year, book.id)
            )
            if cursor.rowcount == 0:
                raise BookNotFoundError(f"Book with id {book.id} not found")
            conn.commit()
            return book
    
    def delete(self, book_id: int) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
            if cursor.rowcount == 0:
                raise BookNotFoundError(f"Book with id {book_id} not found")
            conn.commit()
    
    def search(self, query: str) -> List[Book]:
        if not query or not query.strip():
            return []
        
        search_term = f"%{query.strip()}%"
        with self.db.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? ORDER BY title",
                (search_term, search_term)
            ).fetchall()
            return [self._row_to_book(row) for row in rows]
    
    def _row_to_book(self, row) -> Book:
        return Book(
            id=row['id'],
            title=row['title'],
            author=row['author'],
            isbn=row['isbn'],
            publication_year=row['publication_year']
        )