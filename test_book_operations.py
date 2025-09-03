import unittest
import tempfile
import os
from models import Book
from database import Database
from repository import BookRepository, BookNotFoundError

class TestBookOperations(unittest.TestCase):
    def setUp(self):
        # Create temporary database for testing
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.database = Database(self.db_path)
        self.repo = BookRepository(self.database)
    
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def test_book_validation(self):
        # Valid book
        book = Book("1984", "George Orwell", "978-0-452-28423-4", 1949)
        self.assertEqual(book.title, "1984")
        
        # Invalid books
        with self.assertRaises(ValueError):
            Book("", "Author", "ISBN", 2000)  # Empty title
        
        with self.assertRaises(ValueError):
            Book("Title", "", "ISBN", 2000)  # Empty author
        
        with self.assertRaises(ValueError):
            Book("Title", "Author", "ISBN", -1)  # Invalid year
    
    def test_create_book(self):
        book = Book("1984", "George Orwell", "978-0-452-28423-4", 1949)
        created_book = self.repo.create(book)
        
        self.assertIsNotNone(created_book.id)
        self.assertEqual(created_book.title, "1984")
    
    def test_get_book_by_id(self):
        book = Book("1984", "George Orwell", "978-0-452-28423-4", 1949)
        created_book = self.repo.create(book)
        
        retrieved_book = self.repo.get_by_id(created_book.id)
        self.assertEqual(retrieved_book.title, "1984")
        self.assertEqual(retrieved_book.author, "George Orwell")
    
    def test_get_book_not_found(self):
        with self.assertRaises(BookNotFoundError):
            self.repo.get_by_id(999)
    
    def test_update_book(self):
        book = Book("1984", "George Orwell", "978-0-452-28423-4", 1949)
        created_book = self.repo.create(book)
        
        created_book.title = "Nineteen Eighty-Four"
        updated_book = self.repo.update(created_book)
        
        self.assertEqual(updated_book.title, "Nineteen Eighty-Four")
        
        # Verify in database
        retrieved_book = self.repo.get_by_id(created_book.id)
        self.assertEqual(retrieved_book.title, "Nineteen Eighty-Four")
    
    def test_update_nonexistent_book(self):
        book = Book("1984", "George Orwell", "978-0-452-28423-4", 1949)
        book.id = 999
        
        with self.assertRaises(BookNotFoundError):
            self.repo.update(book)
    
    def test_delete_book(self):
        book = Book("1984", "George Orwell", "978-0-452-28423-4", 1949)
        created_book = self.repo.create(book)
        
        self.repo.delete(created_book.id)
        
        with self.assertRaises(BookNotFoundError):
            self.repo.get_by_id(created_book.id)
    
    def test_delete_nonexistent_book(self):
        with self.assertRaises(BookNotFoundError):
            self.repo.delete(999)
    
    def test_get_all_books(self):
        books = [
            Book("1984", "George Orwell", "978-0-452-28423-4", 1949),
            Book("Animal Farm", "George Orwell", "978-0-452-28424-1", 1945),
        ]
        
        for book in books:
            self.repo.create(book)
        
        all_books = self.repo.get_all()
        self.assertEqual(len(all_books), 2)
        self.assertEqual(all_books[0].title, "1984")  # Ordered by title
    
    def test_search_books(self):
        books = [
            Book("1984", "George Orwell", "978-0-452-28423-4", 1949),
            Book("Animal Farm", "George Orwell", "978-0-452-28424-1", 1945),
            Book("Brave New World", "Aldous Huxley", "978-0-06-085052-4", 1932),
        ]
        
        for book in books:
            self.repo.create(book)
        
        # Search by title
        results = self.repo.search("1984")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "1984")
        
        # Search by author
        results = self.repo.search("Orwell")
        self.assertEqual(len(results), 2)
        
        # Search with no results
        results = self.repo.search("Nonexistent")
        self.assertEqual(len(results), 0)
        
        # Empty search
        results = self.repo.search("")
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()