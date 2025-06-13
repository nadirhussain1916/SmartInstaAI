import { createSlice } from '@reduxjs/toolkit';

const userSlice = createSlice({
  name: 'user',
  initialState: {
    name: 'Sarah Johnson',
    avatar: 'https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=400',
    role: 'Content Creator',
    isAuthenticated: true,
  },
  reducers: {
    setUser: (state, action) => {
      return { ...state, ...action.payload };
    },
    updateProfile: (state, action) => {
      state.name = action.payload.name || state.name;
      state.avatar = action.payload.avatar || state.avatar;
      state.role = action.payload.role || state.role;
    },
    logout: (state) => {
      state.isAuthenticated = false;
      state.name = '';
      state.avatar = '';
      state.role = '';
    },
  },
});

export const { setUser, updateProfile, logout } = userSlice.actions;
export default userSlice.reducer;