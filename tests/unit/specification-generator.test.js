const { SpecificationGenerator } = require('../../src/services/specification-generator');
const fs = require('fs').promises;
const path = require('path');

jest.mock('fs', () => ({
  promises: {
    writeFile: jest.fn(),
    mkdir: jest.fn()
  }
}));

describe('SpecificationGenerator', () => {
  let specGenerator;

  beforeEach(() => {
    specGenerator = new SpecificationGenerator();
    jest.clearAllMocks();
  });

  describe('generateSpecification', () => {
    it('should generate complete specification from analysis', async () => {
      const analysis = {
        projectType: 'web application',
        features: ['user authentication', 'CRUD operations', 'responsive design'],
        requirements: ['secure login', 'data persistence', 'mobile-friendly']
      };

      const result = await specGenerator.generateSpecification(analysis);

      expect(result).toEqual({
        title: 'Web Application Specification',
        overview: expect.stringContaining('web application'),
        features: analysis.features,
        requirements: analysis.requirements,
        technicalSpecs: expect.objectContaining({
          architecture: expect.any(String),
          database: expect.any(String),
          security: expect.any(String)
        }),
        timeline: expect.objectContaining({
          phases: expect.any(Array),
          estimatedDuration: expect.any(String)
        }),
        generatedAt: expect.any(Date)
      });
    });

    it('should handle missing analysis fields gracefully', async () => {
      const analysis = {
        projectType: 'mobile app'
        // Missing features and requirements
      };

      const result = await specGenerator.generateSpecification(analysis);

      expect(result.features).toEqual([]);
      expect(result.requirements).toEqual([]);
      expect(result.title).toBe('Mobile App Specification');
    });

    it('should reject invalid analysis input', async () => {
      await expect(specGenerator.generateSpecification(null)).rejects.toThrow('Analysis data is required');
      await expect(specGenerator.generateSpecification({})).rejects.toThrow('Project type is required');
    });
  });

  describe('saveSpecification', () => {
    it('should save specification to file', async () => {
      const specification = {
        title: 'Test App Specification',
        overview: 'A test application',
        features: ['feature1', 'feature2'],
        generatedAt: new Date()
      };

      fs.mkdir.mockResolvedValue();
      fs.writeFile.mockResolvedValue();

      const filePath = await specGenerator.saveSpecification(specification);

      expect(fs.mkdir).toHaveBeenCalledWith(
        expect.stringContaining('specifications'),
        { recursive: true }
      );
      expect(fs.writeFile).toHaveBeenCalledWith(
        filePath,
        expect.stringContaining('# Test App Specification'),
        'utf8'
      );
      expect(filePath).toMatch(/\.md$/);
    });

    it('should handle file system errors', async () => {
      const specification = {
        title: 'Test Spec',
        overview: 'Test',
        features: [],
        generatedAt: new Date()
      };

      fs.mkdir.mockRejectedValue(new Error('Permission denied'));

      await expect(specGenerator.saveSpecification(specification)).rejects.toThrow('Permission denied');
    });
  });

  describe('formatAsMarkdown', () => {
    it('should format specification as markdown', () => {
      const specification = {
        title: 'Todo App Specification',
        overview: 'A simple todo application',
        features: ['Add tasks', 'Mark complete', 'Delete tasks'],
        requirements: ['User-friendly', 'Fast performance'],
        technicalSpecs: {
          architecture: 'MVC pattern',
          database: 'SQLite',
          security: 'JWT authentication'
        },
        timeline: {
          phases: [
            { name: 'Planning', duration: '1 week' },
            { name: 'Development', duration: '4 weeks' }
          ],
          estimatedDuration: '5 weeks'
        },
        generatedAt: new Date('2024-01-01')
      };

      const markdown = specGenerator.formatAsMarkdown(specification);

      expect(markdown).toContain('# Todo App Specification');
      expect(markdown).toContain('## Overview');
      expect(markdown).toContain('A simple todo application');
      expect(markdown).toContain('## Features');
      expect(markdown).toContain('- Add tasks');
      expect(markdown).toContain('## Requirements');
      expect(markdown).toContain('- User-friendly');
      expect(markdown).toContain('## Technical Specifications');
      expect(markdown).toContain('**Architecture:** MVC pattern');
      expect(markdown).toContain('## Timeline');
      expect(markdown).toContain('**Planning** - 1 week');
    });
  });
});