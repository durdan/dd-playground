module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',     // new feature
        'fix',      // bug fix
        'docs',     // documentation
        'style',    // formatting, missing semicolons, etc
        'refactor', // code change that neither fixes a bug nor adds a feature
        'perf',     // performance improvement
        'test',     // adding tests
        'chore',    // updating build tasks, package manager configs, etc
        'ci',       // continuous integration
        'build',    // build system or external dependencies
        'revert'    // revert previous commit
      ]
    ],
    'subject-case': [2, 'never', ['start-case', 'pascal-case', 'upper-case']],
    'subject-max-length': [2, 'always', 72],
    'body-max-line-length': [2, 'always', 100]
  }
};