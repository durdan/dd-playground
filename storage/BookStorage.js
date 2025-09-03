class BookStorage {
  constructor() {
    this.books = new Map();
    this.nextId = 1;
  }

  create(bookData) {
    const id = this.nextId++;
    const book = { id, ...bookData };
    this.books.set(id, book);
    return book;
  }

  findAll() {
    return Array.from(this.books.values());
  }

  findById(id) {
    return this.books.get(id) || null;
  }

  update(id, bookData) {
    if (!this.books.has(id)) {
      return null;
    }
    const updatedBook = { id, ...bookData };
    this.books.set(id, updatedBook);
    return updatedBook;
  }

  delete(id) {
    return this.books.delete(id);
  }
}

module.exports = BookStorage;