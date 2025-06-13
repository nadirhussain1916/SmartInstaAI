import React from 'react';
import { TrendingUp } from 'lucide-react';
import InstagramPost from './InstagramPost';
import { mockInstagramPosts } from '../utils/mockData';

const InstagramPostsList: React.FC = () => {
  return (
    <div className="bg-gray-50 border-r border-gray-200 h-full overflow-y-auto">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-center space-x-3 mb-6">
          <div className="w-10 h-10 bg-gradient-to-r from-pink-500 to-orange-500 rounded-lg flex items-center justify-center">
            <TrendingUp className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Top Posts</h2>
            <p className="text-sm text-gray-600">Your best performing content</p>
          </div>
        </div>

        {/* Posts List */}
        <div className="space-y-4">
          {mockInstagramPosts.map((post, index) => (
            <div key={post.id} className="relative">
              {/* Ranking Badge */}
              <div className="absolute -top-2 -left-2 z-10 w-6 h-6 bg-gradient-to-r from-pink-500 to-orange-500 rounded-full flex items-center justify-center">
                <span className="text-white text-xs font-bold">{index + 1}</span>
              </div>
              <InstagramPost post={post} />
            </div>
          ))}
        </div>

        {/* Performance Summary */}
        <div className="mt-6 p-4 bg-white rounded-xl border border-gray-100">
          <h3 className="font-medium text-gray-900 text-sm mb-2">Performance Summary</h3>
          <div className="grid grid-cols-2 gap-4 text-center">
            <div>
              <div className="text-lg font-bold text-pink-600">8.4k</div>
              <div className="text-xs text-gray-600">Total Likes</div>
            </div>
            <div>
              <div className="text-lg font-bold text-blue-600">448</div>
              <div className="text-xs text-gray-600">Total Comments</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InstagramPostsList;