import React from 'react';
import { Provider } from 'react-redux';
import { store } from './store/store';
import InstagramPostsList from './components/InstagramPostsList';
import ChatInterface from './components/ChatInterface';

function App() {
  return (
    <Provider store={store}>
      <div className="h-screen flex bg-gray-100">
        {/* Left Panel - Instagram Posts */}
        <div className="w-80 flex-shrink-0 hidden lg:block">
          <InstagramPostsList />
        </div>

        {/* Right Panel - Chat Interface */}
        <div className="flex-1 min-w-0">
          <ChatInterface />
        </div>

        {/* Mobile Toggle Button for Posts (if needed) */}
        <div className="lg:hidden absolute top-4 left-4 z-20">
          <button className="w-10 h-10 bg-white rounded-lg shadow-md flex items-center justify-center">
            <div className="w-5 h-5 bg-gradient-to-r from-pink-500 to-orange-500 rounded"></div>
          </button>
        </div>
      </div>
    </Provider>
  );
}

export default App;