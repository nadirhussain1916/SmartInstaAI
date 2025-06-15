import React from 'react';

const ChatMessage = ({ message, isLatest = false }) => {
  const isUser = message.type === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 ${isLatest ? 'animate-fade-in' : ''}`}>
      <div className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl ${
        isUser 
          ? 'bg-gradient-to-r from-pink-500 to-orange-500 text-white ml-4' 
          : 'bg-white border border-gray-200 text-gray-800 mr-4 shadow-sm'
      }`}>
        <p className="text-sm leading-relaxed">{message.content}</p>
        <p className={`text-xs mt-2 ${
          isUser ? 'text-pink-100' : 'text-gray-500'
        }`}>
          {message.timestamp}
        </p>
      </div>
    </div>
  );
};

export default ChatMessage;