module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
<<<<<<< HEAD
  testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|test).ts'],
=======
  testMatch: [
    '**/__tests__/**/*.ts',
    '**/?(*.)+(spec|test).ts'
  ],
>>>>>>> fix-setup-testing-1756912222
  transform: {
    '^.+\\.ts$': 'ts-jest',
  },
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
<<<<<<< HEAD
  ],
  setupFilesAfterEnv: ['<rootDir>/src/test/setup.ts']
=======
    '!src/**/__tests__/**',
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
>>>>>>> fix-setup-testing-1756912222
};