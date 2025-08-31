const express = require('express');
const router = express.Router();
const { User, Product } = require('./models');

router.get('/users', (req, res) => res.json([new User('Alice', 'alice@example.com'), new User('Bob', 'bob@example.com')]));
router.get('/products', (req, res) => res.json([new Product('Laptop', 999), new Product('Mouse', 29)]));
router.get('/health', (req, res) => res.json({ status: 'healthy', timestamp: new Date() }));

module.exports = router;