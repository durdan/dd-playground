const request = require('supertest');
const { app, server } = require('../server');

describe('Books API', () => {
  afterAll(() => {
    server.close();
  });

  describe('POST /api/books', () => {
    it('should create a new book', async () => {
      const bookData = {
        title: 'Test Book',
        author: 'Test Author',
        year: 2023
      };

      const response = await request(app)
        .post('/api/books')
        .send(bookData)
        .expect(201);

      expect(response.body).toMatchObject(bookData);
      expect(response.body.id).toBeDefined();
    });

    it('should return 400 for invalid book data', async () => {
      const response = await request(app)
        .post('/api/books')
        .send({ title: '' })
        .expect(400);

      expect(response.body.error).toContain('Validation failed');
    });
  });

  describe('GET /api/books', () => {
    it('should return all books', async () => {
      const response = await request(app)
        .get('/api/books')
        .expect(200);

      expect(Array.isArray(response.body)).toBe(true);
    });
  });

  describe('GET /api/books/:id', () => {
    it('should return a book by id', async () => {
      // First create a book
      const createResponse = await request(app)
        .post('/api/books')
        .send({ title: 'Test Book', author: 'Test Author' });

      const bookId = createResponse.body.id;

      const response = await request(app)
        .get(`/api/books/${bookId}`)
        .expect(200);

      expect(response.body.id).toBe(bookId);
    });

    it('should return 404 for non-existent book', async () => {
      const response = await request(app)
        .get('/api/books/999')
        .expect(404);

      expect(response.body.error).toBe('Book not found');
    });

    it('should return 400 for invalid id', async () => {
      await request(app)
        .get('/api/books/invalid')
        .expect(400);
    });
  });

  describe('PUT /api/books/:id', () => {
    it('should update a book', async () => {
      // First create a book
      const createResponse = await request(app)
        .post('/api/books')
        .send({ title: 'Original Title', author: 'Original Author' });

      const bookId = createResponse.body.id;
      const updatedData = { title: 'Updated Title', author: 'Updated Author' };

      const response = await request(app)
        .put(`/api/books/${bookId}`)
        .send(updatedData)
        .expect(200);

      expect(response.body).toMatchObject(updatedData);
    });

    it('should return 404 for non-existent book', async () => {
      await request(app)
        .put('/api/books/999')
        .send({ title: 'Test', author: 'Test' })
        .expect(404);
    });
  });

  describe('DELETE /api/books/:id', () => {
    it('should delete a book', async () => {
      // First create a book
      const createResponse = await request(app)
        .post('/api/books')
        .send({ title: 'To Delete', author: 'Test Author' });

      const bookId = createResponse.body.id;

      await request(app)
        .delete(`/api/books/${bookId}`)
        .expect(204);

      // Verify it's deleted
      await request(app)
        .get(`/api/books/${bookId}`)
        .expect(404);
    });

    it('should return 404 for non-existent book', async () => {
      await request(app)
        .delete('/api/books/999')
        .expect(404);
    });
  });
});