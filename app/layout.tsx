import React from 'react';

const Layout = ({ children }) => (
  <div className="min-h-screen bg-gray-100">
    <main>{children}</main>
  </div>
);

export default Layout;