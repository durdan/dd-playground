const request = require('supertest');
const app = require('../app');

describe('Book Validation Middleware', () => {
  describe('POST /api/books', () => {
    it('should create a book with valid data', async () => {
      const validBook = {
        title: 'The Great Gatsby',
        author: 'F. Scott Fitzgerald',
        isbn: '978-0-7432-7356-5',
        publishedYear: 1925,
        genre: 'Fiction'
      };

      const response = await request(app)
        .post('/api/books')
        .send(validBook)
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data.title).toBe(validBook.title);
      expect(response.body.data.isbn).toBe('9780743273565'); // Clean ISBN
    });

    it('should reject book with missing required fields', async () => {
      const invalidBook = {
        title: 'Incomplete Book'
        // Missing author, isbn, publishedYear
      };

      const response = await request(app)
        .post('/api/books')
        .send(invalidBook)
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.errors).toHaveLength(3);
      expect(response.body.errors.some(e => e.field === 'author')).toBe(true);
      expect(response.body.errors.some(e => e.field === 'isbn')).toBe(true);
      expect(response.body.errors.some(e => e.field === 'publishedYear')).toBe(true);
    });

    it('should reject book with invalid ISBN', async () => {
      const invalidBook = {
        title: 'Test Book',
        author: 'Test Author',
        isbn: '123-invalid-isbn',
        publishedYear: 2023
      };

      const response = await request(app)
        .post('/api/books')
        .send(invalidBook)
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.errors.some(e => e.field === 'isbn')).toBe(true);
    });

    it('should reject book with invalid published year', async () => {
      const invalidBook = {
        title: 'Future Book',
        author: 'Time Traveler',
        isbn: '978-0-7432-7356-5',
        publishedYear: 2050
      };

      const response = await request(app)
        .post('/api/books')
        .send(invalidBook)
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.errors.some(e => e.field === 'publishedYear')).toBe(true);
    });

    it('should accept valid ISBN-10 format', async () => {
      const validBook = {
        title: 'Test Book',
        author: 'Test Author',
        isbn: '0-7432-7356-X',
        publishedYear: 2020
      };

      const response = await request(app)
        .post('/api/books')
        .send(validBook)
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data.isbn).toBe('074327356X');
    });
  });

  describe('PUT /api/books/:id', () => {
    it('should update book with valid partial data', async () => {
      // First create a book
      const book = {
        title: 'Original Title',
        author: 'Original Author',
        isbn: '978-0-7432-7356-5',
        publishedYear: 2020
      };

      const createResponse = await request(app)
        .post('/api/books')
        .send(book);

      const bookId = createResponse.body.data.id;

      // Then update it
      const updates = {
        title: 'Updated Title',
        genre: 'Mystery'
      };

      const response = await request(app)
        .put(`/api/books/${bookId}`)
        .send(updates)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.title).toBe('Updated Title');
      expect(response.body.data.author).toBe('Original Author'); // Unchanged
    });

    it('should reject update with invalid data', async () => {
      const updates = {
        publishedYear: 3000 // Invalid future year
      };

      const response = await request(app)
        .put('/api/books/999')
        .send(updates)
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.errors.some(e => e.field === 'publishedYear')).toBe(true);
    });
  });
});