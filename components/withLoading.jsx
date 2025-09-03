import React from 'react';
import LoadingSpinner from './LoadingSpinner';

const withLoading = (WrappedComponent) => {
  return function WithLoadingComponent({ isLoading, loadingMessage, ...props }) {
    if (isLoading) {
      return <LoadingSpinner overlay message={loadingMessage} />;
    }
    
    return <WrappedComponent {...props} />;
  };
};

export default withLoading;