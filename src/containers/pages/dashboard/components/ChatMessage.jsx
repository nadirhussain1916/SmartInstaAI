import React, { useEffect, useState, useRef } from 'react';
import { Box, Typography, useTheme } from '@mui/material';
import { motion } from 'framer-motion';
import dayjs from 'dayjs';

function ChatMessage({ message, isLatest }) {
  console.log(message);
  
  const theme = useTheme();
  const isUser = message.type === 'user';
  const [typedText, setTypedText] = useState('');
  const messageRef = useRef();
  const fullText = removeSquareBrackets(message.content);

  useEffect(() => {
    if (isLatest && messageRef.current) {
      messageRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [isLatest]);

  useEffect(() => {
    if (isUser) {
      setTypedText(fullText); // instantly show for user messages
      return;
    }

    setTypedText('');
    let index = 0;

    const interval = setInterval(() => {
      setTypedText((prev) => prev + fullText.charAt(index));
      index++;

      if (index >= fullText.length) clearInterval(interval);
    }, 20); // typing speed in ms

    return () => clearInterval(interval);
  }, [fullText]);

  function removeSquareBrackets(text) {
    if (text.startsWith('[') && text.endsWith(']')) {
      return text.slice(1, -1).trim();
    }
    return text.trim();
  }

  return (
    <Box
      ref={messageRef}
      display="flex"
      justifyContent={isUser ? 'flex-end' : 'flex-start'}
      mb={2}
    >
      <Box
        component={motion.div}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        sx={{
          maxWidth: { xs: '70%', lg: '60%' },
          px: 2,
          py: 1.5,
          borderRadius: 4,
          ml: isUser ? 2 : 0,
          mr: isUser ? 0 : 2,
          background: isUser
            ? 'linear-gradient(to right, #ec4899, #f97316)'
            : '#fff',
          color: isUser ? '#fff' : theme.palette.text.primary,
          border: isUser ? 'none' : `1px solid ${theme.palette.grey[300]}`,
          boxShadow: isUser ? 'none' : theme.shadows[1],
          whiteSpace: 'pre-wrap',
        }}
      >
        <Typography
          variant="body2"
          sx={{ lineHeight: 1.6, whiteSpace: 'pre-wrap' }}
        >
          {typedText}
          {!isUser && typedText.length < fullText.length && (
            <motion.span
              animate={{ opacity: [0, 1, 0] }}
              transition={{ repeat: Infinity, duration: 1 }}
              style={{ display: 'inline-block' }}
            >
              |
            </motion.span>
          )}
        </Typography>
        <Typography
          variant="caption"
          display="block"
          mt={1}
          sx={{ color: isUser ? '#fce7f3' : theme.palette.grey[500] }}
        >
          {message?.timestamp}
        </Typography>
      </Box>
    </Box>
  );
}

export default ChatMessage;
