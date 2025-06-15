import { configureStore } from '@reduxjs/toolkit';
import chatReducer from './slices/chatSlice';
import postsReducer from './slices/postsSlice';
import userReducer from './slices/userSlice';

export const store = configureStore({
  reducer: {
    chat: chatReducer,
    posts: postsReducer,
    user: userReducer,
  },
});