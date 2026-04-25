import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageSquare, X, Send, Bot, User } from 'lucide-react';

interface ChatSidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ChatSidebar = ({ isOpen, onClose }: ChatSidebarProps) => {
  const [messages, setMessages] = useState([
    { id: 1, sender: 'agent', text: 'Hi! I can answer any questions you have about this specific report. What would you like to know?' }
  ]);
  const [inputValue, setInputValue] = useState('');

  const handleSend = () => {
    if (!inputValue.trim()) return;
    
    // Add user message
    const newMessages = [...messages, { id: Date.now(), sender: 'user', text: inputValue }];
    setMessages(newMessages);
    setInputValue('');
    
    // Mock agent response after short delay
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        id: Date.now(), 
        sender: 'agent', 
        text: 'Based on the report context, the risk factors are primarily associated with supply chain disruptions as noted in section 3.' 
      }]);
    }, 1000);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ width: 0, opacity: 0 }}
          animate={{ width: 320, opacity: 1 }}
          exit={{ width: 0, opacity: 0 }}
          transition={{ duration: 0.3, ease: 'easeInOut' }}
          className="h-full bg-white border-l border-gray-200 shadow-xl flex flex-col overflow-hidden shrink-0"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-gray-100 bg-[#f8fafc]">
            <div className="flex items-center space-x-2">
              <MessageSquare size={18} className="text-[#1e3a8a]" />
              <h3 className="font-semibold text-gray-800">Report Assistant</h3>
            </div>
            <button 
              onClick={onClose}
              className="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-200 rounded-lg transition-colors"
            >
              <X size={18} />
            </button>
          </div>

          {/* Chat Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((msg) => (
              <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`flex max-w-[85%] ${msg.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                  <div className={`shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                    msg.sender === 'user' ? 'bg-gray-100 ml-2' : 'bg-[#1e3a8a] mr-2'
                  }`}>
                    {msg.sender === 'user' ? <User size={14} className="text-gray-600" /> : <Bot size={14} className="text-white" />}
                  </div>
                  <div className={`p-3 rounded-2xl text-[14px] leading-relaxed ${
                    msg.sender === 'user' 
                      ? 'bg-[#1e3a8a] text-white rounded-tr-sm' 
                      : 'bg-[#f1f5f9] text-gray-800 rounded-tl-sm border border-gray-200'
                  }`}>
                    {msg.text}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Input Area */}
          <div className="p-4 border-t border-gray-100 bg-white">
            <div className="flex items-center border border-gray-300 rounded-xl bg-gray-50 px-2 py-1 focus-within:ring-2 focus-within:ring-blue-100 focus-within:border-blue-400 transition-all">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Ask about this report..."
                className="flex-1 bg-transparent border-none focus:ring-0 text-sm py-2 px-2 text-gray-700 placeholder-gray-400"
              />
              <button 
                onClick={handleSend}
                disabled={!inputValue.trim()}
                className={`p-2 rounded-lg transition-colors ${
                  inputValue.trim() ? 'bg-[#1e3a8a] text-white hover:bg-[#2e4a9a]' : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                }`}
              >
                <Send size={16} />
              </button>
            </div>
            <p className="text-center text-xs text-gray-400 mt-2">
              Context-aware assistant
            </p>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
