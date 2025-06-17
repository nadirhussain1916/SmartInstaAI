import React from 'react';
import { Box, Typography, useTheme } from '@mui/material';

function ChatMessage({ message, isLatest }) {
  const theme = useTheme();
  const isUser = message.type === 'user';

  function removeSquareBrackets(text) {
  // Remove starting [ and ending ] if present
  if (text.startsWith('[') && text.endsWith(']')) {
    return text.slice(1, -1).trim();
  }
  return text.trim();
}
  return (
    <Box
      display="flex"
      justifyContent={isUser ? 'flex-end' : 'flex-start'}
      mb={2}
      className={isLatest ? 'animate-fade-in' : ''}
    >
      <Box
        sx={{
          maxWidth: { xs: '70%', lg: '60%' },
          px: 2,
          py: 1.5,
          borderRadius: 4,
          ml: isUser ? 2 : 0,
          mr: isUser ? 0 : 2,
          background: isUser
            ? 'linear-gradient(to right, #ec4899, #f97316)' // from-pink-500 to-orange-500
            : '#fff',
          color: isUser ? '#fff' : theme.palette.text.primary,
          border: isUser ? 'none' : `1px solid ${theme.palette.grey[300]}`,
          boxShadow: isUser ? 'none' : theme.shadows[1],
        }}
      >
        <Typography variant="body2" sx={{ lineHeight: 1 }}>
          {removeSquareBrackets(message.content)}
        </Typography>
        <Typography
          variant="caption"
          display="block"
          mt={1}
          sx={{ color: isUser ? '#fce7f3' : theme.palette.grey[500] }} // pink-100 or gray-500
        >
          {message.timestamp}
        </Typography>
      </Box>
    </Box>
  );
}

export default ChatMessage;
