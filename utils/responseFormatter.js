const formatResponse = (data, message = 'Success', status = 'success') => {
  return {
    status,
    message,
    data,
    timestamp: new Date().toISOString()
  };
};

const formatError = (message, statusCode = 500, details = null) => {
  return {
    status: 'error',
    message,
    statusCode,
    details,
    timestamp: new Date().toISOString()
  };
};

module.exports = {
  formatResponse,
  formatError
};