import React from 'react';
import LoadingSpinner from './LoadingSpinner';

const withLoading = (WrappedComponent) => {
  return function WithLoadingComponent(props) {
    const { isLoading, loadingMessage, ...restProps } = props;

    if (isLoading) {
      return <LoadingSpinner overlay message={loadingMessage} />;
    }

    return <WrappedComponent {...restProps} />;
  };
};

export default withLoading;