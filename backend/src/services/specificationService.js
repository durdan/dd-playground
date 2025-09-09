const { v4: uuidv4 } = require('uuid');
const integrationService = require('./integrationService');

class SpecificationService {
  constructor() {
    this.jobs = new Map();
  }

  async generateSpecification(chatHistory, requirements) {
    const jobId = uuidv4();
    
    // Validate input
    if (!chatHistory || !Array.isArray(chatHistory)) {
      throw new Error('Invalid chat history provided');
    }
    
    if (!requirements || typeof requirements !== 'object') {
      throw new Error('Invalid requirements provided');
    }

    // Start async processing
    this.processSpecificationGeneration(jobId, chatHistory, requirements);
    
    return { jobId, status: 'started' };
  }

  async processSpecificationGeneration(jobId, chatHistory, requirements) {
    try {
      this.jobs.set(jobId, { status: 'processing', progress: 0 });

      // Simulate specification generation steps
      const steps = [
        { name: 'Analyzing chat history', duration: 1000 },
        { name: 'Processing requirements', duration: 1500 },
        { name: 'Generating specification', duration: 2000 },
        { name: 'Validating output', duration: 500 }
      ];

      let totalProgress = 0;
      const progressIncrement = 100 / steps.length;

      for (let i = 0; i < steps.length; i++) {
        const step = steps[i];
        
        // Simulate processing time
        await this.delay(step.duration);
        
        totalProgress += progressIncrement;
        
        // Send progress update
        integrationService.broadcast('spec_progress', {
          jobId,
          progress: Math.round(totalProgress),
          currentStep: step.name
        });
      }

      // Generate the actual specification
      const specification = this.createSpecification(chatHistory, requirements);
      
      // Mark job as complete
      this.jobs.set(jobId, { status: 'completed', result: specification });
      
      // Send completion notification
      integrationService.broadcast('spec_complete', {
        jobId,
        specification
      });

    } catch (error) {
      console.error('Specification generation failed:', error);
      
      this.jobs.set(jobId, { status: 'failed', error: error.message });
      
      integrationService.broadcast('spec_error', {
        jobId,
        error: error.message
      });
    }
  }

  createSpecification(chatHistory, requirements) {
    // Extract key information from chat history
    const userMessages = chatHistory.filter(msg => msg.role === 'user');
    const features = this.extractFeatures(userMessages);
    
    return {
      id: uuidv4(),
      title: requirements.title || 'Generated Specification',
      description: requirements.description || 'Auto-generated from chat conversation',
      features,
      technicalRequirements: this.extractTechnicalRequirements(chatHistory),
      userStories: this.generateUserStories(features),
      createdAt: new Date().toISOString()
    };
  }

  extractFeatures(messages) {
    // Simple feature extraction logic
    const features = [];
    messages.forEach(msg => {
      if (msg.content.toLowerCase().includes('need') || 
          msg.content.toLowerCase().includes('want') ||
          msg.content.toLowerCase().includes('should')) {
        features.push({
          id: uuidv4(),
          description: msg.content.substring(0, 100) + '...',
          priority: 'medium'
        });
      }
    });
    return features;
  }

  extractTechnicalRequirements(chatHistory) {
    return {
      platform: 'web',
      technologies: ['React', 'Node.js'],
      database: 'PostgreSQL',
      authentication: 'required'
    };
  }

  generateUserStories(features) {
    return features.map(feature => ({
      id: uuidv4(),
      story: `As a user, I want ${feature.description.toLowerCase()}`,
      acceptanceCriteria: ['Feature works as expected', 'Error handling is implemented']
    }));
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  getJobStatus(jobId) {
    return this.jobs.get(jobId) || { status: 'not_found' };
  }
}

module.exports = new SpecificationService();