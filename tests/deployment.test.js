const { execSync } = require('child_process');
const fs = require('fs');

describe('Deployment Configuration', () => {
  test('staging environment file exists', () => {
    expect(fs.existsSync('.env.staging')).toBe(true);
  });

  test('docker-compose file is valid', () => {
    expect(() => {
      execSync('docker-compose -f docker-compose.staging.yml config', { stdio: 'pipe' });
    }).not.toThrow();
  });

  test('required environment variables are defined', () => {
    const envContent = fs.readFileSync('.env.staging', 'utf8');
    
    const requiredVars = [
      'DB_NAME',
      'DB_USER', 
      'DB_PASSWORD',
      'DATABASE_URL',
      'REDIS_URL'
    ];
    
    requiredVars.forEach(varName => {
      expect(envContent).toContain(varName);
    });
  });
});