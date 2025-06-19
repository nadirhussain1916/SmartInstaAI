import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles } from 'lucide-react';
import ChatMessage from './ChatMessage';
import { mockUser, mockChatMessages } from '../utils/mockData';
import { ChatMessage as ChatMessageType, FilterType } from '../types';

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessageType[]>(mockChatMessages);
  const [inputValue, setInputValue] = useState('');
  const [selectedFilter, setSelectedFilter] = useState<FilterType>('History');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSendMessage = () => {
    if (!inputValue.trim()) return;

    const newUserMessage: ChatMessageType = {
      id: Date.now().toString(),
      type: 'user',
      content: inputValue,
      timestamp: new Date().toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: false 
      })
    };

    setMessages(prev => [...prev, newUserMessage]);
    setInputValue('');
    setIsTyping(true);

    // Simulate bot response
    setTimeout(() => {
      const botResponse: ChatMessageType = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: getBotResponse(inputValue, selectedFilter),
        timestamp: new Date().toLocaleTimeString('en-US', { 
          hour: '2-digit', 
          minute: '2-digit',
          hour12: false 
        })
      };
      setMessages(prev => [...prev, botResponse]);
      setIsTyping(false);
    }, 1500);
  };

  const getBotResponse = (userInput: string, filter: FilterType) => {
    const responses = {
      History: [
        "Based on your post history, I can see coffee and morning routines perform really well. Let me create a carousel that builds on this theme!",
        "Your audience loves lifestyle content! I'll design a carousel that captures that same energy.",
        "Looking at your top posts, visual storytelling is your strength. Let's create something amazing!"
      ],
      Origin: [
        "I'll create an authentic carousel that tells your brand story from the beginning. What's the origin story you want to share?",
        "Origin stories create deep connections. Let me craft a carousel that shows your journey authentically.",
        "Your audience wants to know the real you. I'll create a carousel that showcases your authentic beginnings."
      ],
      Product: [
        "Let me create a product-focused carousel that highlights features and benefits in an engaging way.",
        "I'll design a carousel that showcases your product through compelling visuals and copy that converts.",
        "Product carousels work best with social proof. I'll include testimonials and real use cases."
      ]
    };
    
    return responses[filter][Math.floor(Math.random() * responses[filter].length)];
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Header */}
      <div className="p-6 border-b border-gray-200 bg-white">
        {/* User Profile */}
        <div className="flex items-center space-x-3 mb-4">
          <img 
            src={mockUser.avatar} 
            alt={mockUser.name}
            className="w-10 h-10 rounded-full object-cover ring-2 ring-pink-100"
          />
          <div>
            <h3 className="font-semibold text-gray-900">{mockUser.name}</h3>
            <p className="text-sm text-gray-600">Content Creator</p>
          </div>
        </div>

        {/* Filter Radio Buttons */}
        <div className="flex space-x-1">
          {(['History', 'Origin', 'Product'] as FilterType[]).map((filter) => (
            <label key={filter} className="relative cursor-pointer">
              <input
                type="radio"
                name="filter"
                value={filter}
                checked={selectedFilter === filter}
                onChange={(e) => setSelectedFilter(e.target.value as FilterType)}
                className="sr-only"
              />
              <div className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                selectedFilter === filter
                  ? 'bg-gradient-to-r from-pink-500 to-orange-500 text-white shadow-md'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}>
                {filter}
              </div>
            </label>
          ))}
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((message, index) => (
          <ChatMessage 
            key={message.id} 
            message={message} 
            isLatest={index === messages.length - 1}
          />
        ))}
        
        {/* Typing Indicator */}
        {isTyping && (
          <div className="flex justify-start mb-4">
            <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3 mr-4 shadow-sm">
              <div className="flex items-center space-x-2">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
                <span className="text-xs text-gray-500">AI is typing...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-6 border-t border-gray-200 bg-white">
        <div className="flex items-center space-x-3">
          <div className="flex-1 relative">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Describe the carousel you want to create..."
              className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-xl resize-none focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-all duration-200"
              rows={1}
              style={{ minHeight: '48px', maxHeight: '120px' }}
            />
            <Sparkles className="absolute right-3 top-3 w-5 h-5 text-gray-400" />
          </div>
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isTyping}
            className="w-12 h-12 bg-gradient-to-r from-pink-500 to-orange-500 rounded-xl flex items-center justify-center text-white hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 hover:scale-105"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;