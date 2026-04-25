import { useState } from 'react';
import { Search, Sparkles, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

export const SmartInput = () => {
  const [query, setQuery] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const navigate = useNavigate();

  const handleSearch = () => {
    if (query.trim()) {
      navigate('/report');
    }
  };

  const suggestions = [
    "Tóm tắt tin tức công nghệ mới nhất",
    "Giải thích máy tính lượng tử",
    "So sánh hiệu suất React và Vue",
    "Thực hành tốt nhất về thiết kế API"
  ];

  return (
    <div className="w-full max-w-4xl mx-auto mt-8 mb-12">
      {/* Search Input Area */}
      <motion.div 
        className={`relative flex items-center bg-white rounded-2xl shadow-sm border transition-all duration-300 ${
          isFocused ? 'border-blue-500 shadow-blue-100 shadow-lg ring-4 ring-blue-50' : 'border-gray-200 hover:border-gray-300'
        }`}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="pl-6 pr-3 py-4 flex items-center justify-center">
          <Search className={`h-6 w-6 transition-colors ${isFocused ? 'text-blue-500' : 'text-gray-400'}`} />
        </div>
        
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          placeholder="Hỏi InfoAgent bất cứ điều gì..."
          className="flex-1 bg-transparent border-none py-5 text-lg text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-0 w-full"
        />
        
        <div className="pr-4 pl-2 py-3 flex items-center">
          <button 
            onClick={handleSearch}
            className={`p-3 rounded-xl flex items-center justify-center transition-all ${
              query.length > 0 
                ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-md' 
                : 'bg-gray-100 text-gray-400 cursor-not-allowed'
            }`}
            disabled={query.length === 0}
          >
            <ArrowRight size={20} />
          </button>
        </div>
      </motion.div>

      {/* Quick Suggestions */}
      <motion.div 
        className="mt-6 flex flex-wrap gap-3 justify-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3, duration: 0.5 }}
      >
        <div className="flex items-center mr-2 text-sm font-medium text-gray-500">
          <Sparkles size={16} className="mr-1.5 text-blue-500" />
          Gợi ý:
        </div>
        {suggestions.map((suggestion, index) => (
          <button
            key={index}
            onClick={() => {
              setQuery(suggestion);
              navigate('/report');
            }}
            className="px-4 py-2 bg-white border border-gray-200 rounded-full text-sm text-gray-600 hover:bg-blue-50 hover:border-blue-200 hover:text-blue-700 transition-colors shadow-sm flex items-center group"
          >
            {suggestion}
          </button>
        ))}
      </motion.div>
    </div>
  );
};
