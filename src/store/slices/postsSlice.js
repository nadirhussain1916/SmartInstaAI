import { createSlice } from '@reduxjs/toolkit';

const initialPosts = [
  {
    id: '1',
    mediaUrl: 'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=400',
    mediaType: 'image',
    title: 'Morning Coffee Ritual',
    caption: 'Starting my day with the perfect cup of coffee and some peaceful moments...',
    likes: 2847,
    comments: 156,
    date: '2025-01-15'
  },
  {
    id: '2',
    mediaUrl: 'https://images.pexels.com/photos/1580271/pexels-photo-1580271.jpeg?auto=compress&cs=tinysrgb&w=400',
    mediaType: 'image',
    title: 'Sunset Vibes',
    caption: 'Golden hour hits different when you find the perfect spot...',
    likes: 3921,
    comments: 203,
    date: '2025-01-14'
  },
  {
    id: '3',
    mediaUrl: 'https://images.pexels.com/photos/1133957/pexels-photo-1133957.jpeg?auto=compress&cs=tinysrgb&w=400',
    mediaType: 'image',
    title: 'Creative Workspace',
    caption: 'Sometimes the best ideas come from the most inspiring spaces...',
    likes: 1654,
    comments: 89,
    date: '2025-01-13'
  }
];

const postsSlice = createSlice({
  name: 'posts',
  initialState: {
    posts: initialPosts,
    totalLikes: 8422,
    totalComments: 448,
    loading: false,
    error: null,
  },
  reducers: {
    setPosts: (state, action) => {
      state.posts = action.payload;
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
    },
    updatePostMetrics: (state, action) => {
      const { postId, likes, comments } = action.payload;
      const post = state.posts.find(p => p.id === postId);
      if (post) {
        post.likes = likes;
        post.comments = comments;
      }
    },
  },
});

export const { setPosts, setLoading, setError, updatePostMetrics } = postsSlice.actions;
export default postsSlice.reducer;