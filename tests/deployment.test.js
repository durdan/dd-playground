const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

describe('Staging Deployment', () => {
  const baseUrl = 'http://localhost:3000';
  
  beforeAll(async () => {
    // Ensure services are running
    await new Promise(resolve => setTimeout(resolve, 5000));
  });

  test('health endpoint returns healthy status', async () => {
    try {
      const { stdout } = await execAsync(`curl -s ${baseUrl}/health`);
      const response = JSON.parse(stdout);
      
      expect(response.status).toBe('healthy');
      expect(response.environment).toBe('staging');
      expect(response.database).toBe('connected');
    } catch (error) {
      throw new Error(`Health check failed: ${error.message}`);
    }
  });

  test('config endpoint shows staging environment', async () => {
    try {
      const { stdout } = await execAsync(`curl -s ${baseUrl}/config`);
      const response = JSON.parse(stdout);
      
      expect(response.environment).toBe('staging');
      expect(response.hasApiKey).toBe(true);
      expect(response.databaseConnected).toBe(true);
    } catch (error) {
      throw new Error(`Config check failed: ${error.message}`);
    }
  });

  test('metrics endpoint is accessible', async () => {
    try {
      const { stdout } = await execAsync(`curl -s ${baseUrl}/metrics`);
      expect(stdout).toContain('http_requests_total');
      expect(stdout).toContain('http_request_duration_seconds');
    } catch (error) {
      throw new Error(`Metrics check failed: ${error.message}`);
    }
  });

  test('prometheus is scraping metrics', async () => {
    try {
      const { stdout } = await execAsync('curl -s http://localhost:9090/api/v1/targets');
      const response = JSON.parse(stdout);
      
      const webAppTarget = response.data.activeTargets.find(
        target => target.labels.job === 'web-app'
      );
      
      expect(webAppTarget).toBeDefined();
      expect(webAppTarget.health).toBe('up');
    } catch (error) {
      throw new Error(`Prometheus check failed: ${error.message}`);
    }
  });

  test('environment variables are properly loaded', async () => {
    try {
      const { stdout } = await execAsync('docker-compose -f docker-compose.staging.yml exec -T web printenv NODE_ENV');
      expect(stdout.trim()).toBe('staging');
    } catch (error) {
      throw new Error(`Environment variable check failed: ${error.message}`);
    }
  });
});