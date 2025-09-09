const express = require('express');
const specificationService = require('../services/specificationService');
const router = express.Router();

router.post('/generate', async (req, res) => {
  try {
    const { chatHistory, requirements } = req.body;
    
    if (!chatHistory || !requirements) {
      return res.status(400).json({ 
        error: 'Missing required fields: chatHistory and requirements' 
      });
    }

    const result = await specificationService.generateSpecification(chatHistory, requirements);
    res.json(result);
  } catch (error) {
    console.error('Specification generation error:', error);
    res.status(500).json({ error: error.message });
  }
});

router.get('/status/:jobId', (req, res) => {
  const { jobId } = req.params;
  const status = specificationService.getJobStatus(jobId);
  res.json(status);
});

module.exports = router;