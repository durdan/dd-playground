// Test that linting and formatting configs are valid
const fs = require('fs');
const path = require('path');

describe('Repository Policy Files', () => {
  test('prettier config exists and is valid JSON', () => {
    const prettierConfig = path.join(__dirname, '.prettierrc.json');
    expect(fs.existsSync(prettierConfig)).toBe(true);
    
    const config = JSON.parse(fs.readFileSync(prettierConfig, 'utf8'));
    expect(config).toHaveProperty('semi');
    expect(config).toHaveProperty('singleQuote');
  });

  test('eslint config exists and is valid JSON', () => {
    const eslintConfig = path.join(__dirname, '.eslintrc.json');
    expect(fs.existsSync(eslintConfig)).toBe(true);
    
    const config = JSON.parse(fs.readFileSync(eslintConfig, 'utf8'));
    expect(config).toHaveProperty('extends');
    expect(config).toHaveProperty('rules');
  });

  test('commitlint config exists', () => {
    const commitlintConfig = path.join(__dirname, 'commitlint.config.js');
    expect(fs.existsSync(commitlintConfig)).toBe(true);
  });

  test('editorconfig exists', () => {
    const editorConfig = path.join(__dirname, '.editorconfig');
    expect(fs.existsSync(editorConfig)).toBe(true);
  });

  test('husky hooks exist', () => {
    const preCommit = path.join(__dirname, '.husky', 'pre-commit');
    const commitMsg = path.join(__dirname, '.husky', 'commit-msg');
    
    expect(fs.existsSync(preCommit)).toBe(true);
    expect(fs.existsSync(commitMsg)).toBe(true);
  });
});