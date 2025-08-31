const express = require('express');
const app = express();
const config = require('../config/config');
const middleware = require('./middleware');
const routes = require('./routes');

app.use(express.json());
app.use(middleware.logger);
app.use('/api', routes);
app.use(middleware.errorHandler);

app.listen(config.port, () => {
  console.log(`Server running on port ${config.port} in ${config.env} mode`);
});

module.exports = app;