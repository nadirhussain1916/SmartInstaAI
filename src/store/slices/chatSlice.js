import { createSlice } from '@reduxjs/toolkit';

const initialMessages = [
  {
    id: '1',
    type: 'bot',
    content: 'Hi! I\'m your Instagram Carousel Content Generator. I can help you create amazing carousel posts based on your top-performing content. What kind of carousel would you like to create today?',
    timestamp: '10:30'
  },
  {
    id: '2',
    type: 'user',
    content: 'I want to create a carousel about morning routines that will engage my audience',
    timestamp: '10:32'
  },
  {
    id: '3',
    type: 'bot',
    content: 'Perfect! I can see you have some great content about morning coffee rituals. Let me create a 5-slide carousel that builds on that theme. Would you like me to focus on productivity tips, wellness aspects, or lifestyle inspiration?',
    timestamp: '10:33'
  }
];

const chatSlice = createSlice({
  name: 'chat',
  initialState: {
    messages: initialMessages,
    isTyping: false,
    selectedFilter: 'History',
  },
  reducers: {
    addMessage: (state, action) => {
      state.messages.push(action.payload);
    },
    setTyping: (state, action) => {
      state.isTyping = action.payload;
    },
    setSelectedFilter: (state, action) => {
      state.selectedFilter = action.payload;
    },
    clearMessages: (state) => {
      state.messages = [];
    },
  },
});

export const { addMessage, setTyping, setSelectedFilter, clearMessages } = chatSlice.actions;
export default chatSlice.reducer;