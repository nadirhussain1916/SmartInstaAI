import React from 'react';
import { Heart, MessageCircle, Calendar } from 'lucide-react';
import { InstagramPost as InstagramPostType } from '../types';

interface InstagramPostProps {
  post: InstagramPostType;
}

const InstagramPost: React.FC<InstagramPostProps> = ({ post }) => {
  const formatNumber = (num: number) => {
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'k';
    }
    return num.toString();
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric' 
    });
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-all duration-300 hover:scale-[1.02]">
      {/* Media Preview */}
      <div className="relative aspect-square overflow-hidden">
        <img 
          src={post.mediaUrl} 
          alt={post.title}
          className="w-full h-full object-cover"
        />
        {post.mediaType === 'video' && (
          <div className="absolute inset-0 bg-black bg-opacity-20 flex items-center justify-center">
            <div className="w-12 h-12 bg-white bg-opacity-80 rounded-full flex items-center justify-center">
              <div className="w-0 h-0 border-l-[8px] border-l-gray-800 border-y-[6px] border-y-transparent ml-1"></div>
            </div>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-4">
        <h3 className="font-semibold text-gray-900 text-sm mb-2 line-clamp-2">
          {post.title}
        </h3>
        <p className="text-gray-600 text-xs mb-3 line-clamp-2">
          {post.caption}
        </p>

        {/* Metrics */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-1">
              <Heart className="w-4 h-4 text-red-500" />
              <span className="text-xs font-medium text-gray-700">
                {formatNumber(post.likes)}
              </span>
            </div>
            <div className="flex items-center space-x-1">
              <MessageCircle className="w-4 h-4 text-blue-500" />
              <span className="text-xs font-medium text-gray-700">
                {formatNumber(post.comments)}
              </span>
            </div>
          </div>
          <div className="flex items-center space-x-1">
            <Calendar className="w-3 h-3 text-gray-400" />
            <span className="text-xs text-gray-500">
              {formatDate(post.date)}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InstagramPost;