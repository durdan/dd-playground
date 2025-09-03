const Book = require('../models/Book');

class BookService {
  constructor(storage) {
    this.storage = storage;
  }

  createBook(bookData) {
    const errors = Book.validate(bookData);
    if (errors.length > 0) {
      throw new Error(`Validation failed: ${errors.join(', ')}`);
    }
    return this.storage.create(bookData);
  }

  getAllBooks() {
    return this.storage.findAll();
  }

  getBookById(id) {
    const book = this.storage.findById(id);
    if (!book) {
      throw new Error('Book not found');
    }
    return book;
  }

  updateBook(id, bookData) {
    const errors = Book.validate(bookData);
    if (errors.length > 0) {
      throw new Error(`Validation failed: ${errors.join(', ')}`);
    }
    
    const updatedBook = this.storage.update(id, bookData);
    if (!updatedBook) {
      throw new Error('Book not found');
    }
    return updatedBook;
  }

  deleteBook(id) {
    const deleted = this.storage.delete(id);
    if (!deleted) {
      throw new Error('Book not found');
    }
  }
}

module.exports = BookService;