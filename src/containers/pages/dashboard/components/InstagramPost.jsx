import React from 'react';
import { Box, Typography, Card, CardMedia, CardContent } from '@mui/material';
import { CalendarMonth, FavoriteBorder, Message } from '@mui/icons-material';
import dayjs from 'dayjs';
import image from '@assets/dummy.jpg';

function InstagramPost({ post }) {

    return (
        <Card
            elevation={1}
            sx={{
                borderRadius: 3,
                overflow: 'hidden',
                border: '1px solid #f3f4f6',
                transition: 'all 0.3s ease',
                '&:hover': {
                    boxShadow: 3,
                    transform: 'scale(1.02)',
                },
            }}
        >
            {/* Media Preview */}
            <Box sx={{ position: 'relative', aspectRatio: '1 / 1', overflow: 'hidden' }}>
                <CardMedia
                    component="img"
                    image={`http://127.0.0.1:8000/${post?.thumbnail_url}`}
                    alt=''
                    sx={{ width: '100%', height: '100%', objectFit: 'cover' }}
                />
                {post.post_type === 'video' && (
                    <Box
                        sx={{
                            position: 'absolute',
                            inset: 0,
                            bgcolor: 'rgba(0, 0, 0, 0.2)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                        }}
                    >
                        <Box
                            sx={{
                                width: 48,
                                height: 48,
                                bgcolor: 'rgba(255, 255, 255, 0.8)',
                                borderRadius: '50%',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                            }}
                        >
                            <Box
                                sx={{
                                    width: 0,
                                    height: 0,
                                    borderLeft: '8px solid #1f2937',
                                    borderTop: '6px solid transparent',
                                    borderBottom: '6px solid transparent',
                                    ml: '2px',
                                }}
                            />
                        </Box>
                    </Box>
                )}
            </Box>

            {/* Content */}
            <CardContent sx={{ p: 2 }}>
                <Typography
                    variant="body1"
                    sx={{
                        color: 'text.primary',
                        fontWeight: 600,
                        mb: 0.5,
                        display: '-webkit-box',
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: 'vertical',
                        overflow: 'hidden',
                    }}
                >
                    {post?.title}
                </Typography>
                <Typography
                    variant="caption"
                    sx={{
                        color: 'text.secondary',
                        mb: 1.5,
                        display: '-webkit-box',
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: 'vertical',
                        overflow: 'hidden',
                    }}
                >
                    {post?.caption}
                </Typography>

                {/* Metrics */}
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box sx={{ display: 'flex', gap: 2, alignItems:'center' }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                            <FavoriteBorder sx={{ fontSize: 16, color: '#FF0000' }} />
                            <Typography variant="caption" sx={{ fontWeight: 500, color: 'text.secondary' }}>
                                {post.likes}
                            </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                            <Message sx={{ fontSize: 16, color: '#ADD8E6.' }} />
                            <Typography variant="caption" sx={{ fontWeight: 500, color: 'text.secondary' }}>
                                {post.comments}
                            </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                            <CalendarMonth sx={{ fontSize: 16, color: '#6b7280' }} />
                            <Typography variant="caption" sx={{ color: '#9ca3af' }}>
                                {dayjs(post.timestamp).format('MMMM D')}
                            </Typography>
                        </Box>
                    </Box>
                </Box>
            </CardContent>
        </Card>
    );
}

export default InstagramPost;
