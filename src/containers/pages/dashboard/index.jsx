import { Box, Button } from '@mui/material';
import React from 'react';
import InstagramPostsList from './components/InstagramPostsList';
import ChatInterface from './components/ChatInterface';

function Dashboard() {
  return (
    <Box sx={{ height: '100vh', display: 'flex', bgcolor: 'grey.100', position: 'relative' }}>
      <Box
        sx={{
          width: 360,
          flexShrink: 0,
          display: { xs: 'none', lg: 'block' },
          bgcolor: 'white',
        }}
      >
        <InstagramPostsList />
      </Box>

      {/* Right Panel - Chat Interface */}
      <Box sx={{ flex: 1, minWidth: 0 }}>
        <ChatInterface />
      </Box>

      {/* Mobile Toggle Button for Posts */}
      <Box
        sx={{
          display: { lg: 'none' },
          position: 'absolute',
          top: 16,
          left: 16,
          zIndex: 20,
        }}
      >
        <Button
          sx={{
            width: 40,
            height: 40,
            minWidth: 0,
            p: 0,
            bgcolor: 'white',
            borderRadius: 2,
            boxShadow: 3,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Box
            sx={{
              width: 20,
              height: 20,
              borderRadius: '50%',
              background: 'linear-gradient(to right, #ec4899, #f97316)',
            }}
          />
        </Button>
      </Box>
    </Box>
  );
}

export default Dashboard;
