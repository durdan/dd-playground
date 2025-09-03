class BookController {
  constructor(bookService) {
    this.bookService = bookService;
  }

  createBook = async (req, res) => {
    try {
      const book = this.bookService.createBook(req.body);
      res.status(201).json(book);
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  };

  getAllBooks = async (req, res) => {
    try {
      const books = this.bookService.getAllBooks();
      res.status(200).json(books);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  };

  getBookById = async (req, res) => {
    try {
      const id = parseInt(req.params.id);
      if (isNaN(id)) {
        return res.status(400).json({ error: 'Invalid book ID' });
      }
      
      const book = this.bookService.getBookById(id);
      res.status(200).json(book);
    } catch (error) {
      res.status(404).json({ error: error.message });
    }
  };

  updateBook = async (req, res) => {
    try {
      const id = parseInt(req.params.id);
      if (isNaN(id)) {
        return res.status(400).json({ error: 'Invalid book ID' });
      }
      
      const book = this.bookService.updateBook(id, req.body);
      res.status(200).json(book);
    } catch (error) {
      if (error.message === 'Book not found') {
        res.status(404).json({ error: error.message });
      } else {
        res.status(400).json({ error: error.message });
      }
    }
  };

  deleteBook = async (req, res) => {
    try {
      const id = parseInt(req.params.id);
      if (isNaN(id)) {
        return res.status(400).json({ error: 'Invalid book ID' });
      }
      
      this.bookService.deleteBook(id);
      res.status(204).send();
    } catch (error) {
      res.status(404).json({ error: error.message });
    }
  };
}

module.exports = BookController;