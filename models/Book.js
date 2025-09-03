class Book {
  constructor(id, title, author, year) {
    this.id = id;
    this.title = title;
    this.author = author;
    this.year = year;
  }

  static validate(bookData) {
    const errors = [];
    
    if (!bookData.title || bookData.title.trim() === '') {
      errors.push('Title is required');
    }
    
    if (!bookData.author || bookData.author.trim() === '') {
      errors.push('Author is required');
    }
    
    if (bookData.year && (!Number.isInteger(bookData.year) || bookData.year < 0)) {
      errors.push('Year must be a positive integer');
    }
    
    return errors;
  }
}

module.exports = Book;