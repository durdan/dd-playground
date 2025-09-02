import React from 'react';
import { SplitPane } from 'react-split-pane';
import useMediaQuery from '@mui/material/useMediaQuery';
import { useTheme } from '@mui/material/styles';

const Layout = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  return (
    <div style={{ height: '100vh', overflow: 'hidden' }}>
      <SplitPane
        split={isMobile ? 'horizontal' : 'vertical'}
        minSize={50}
        defaultSize={parseInt(localStorage.getItem('splitPos'), 10) || (isMobile ? 100 : '50%')}
        onChange={size => localStorage.setItem('splitPos', size)}
        style={{ position: 'relative' }}
      >
        <div>Editor</div>
        <div>Preview</div>
      </SplitPane>
    </div>
  );
};

export default Layout;
