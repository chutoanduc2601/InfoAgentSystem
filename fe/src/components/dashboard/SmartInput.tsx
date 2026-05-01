import { useState } from 'react';
import { Search, Sparkles, ArrowRight, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useQueryContext } from '../../context/QueryContext';

export const SmartInput = () => {
  const [inputText, setInputText] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const navigate = useNavigate();
  const { submitQuery, isLoading } = useQueryContext();

  const handleSearch = async () => {
    const trimmed = inputText.trim();
    if (!trimmed || isLoading) return;

    navigate('/report');
    await submitQuery(trimmed);
  };

  const handleSuggestionClick = async (suggestion: string) => {
    if (isLoading) return;
    setInputText(suggestion);
    navigate('/report');
    await submitQuery(suggestion);
  };

  const suggestions = [
    "Tóm tắt tin tức công nghệ mới nhất",
    "Giải thích máy tính lượng tử",
    "So sánh hiệu suất React và Vue",
    "Thực hành tốt nhất về thiết kế API"
  ];

  return (
    <div className="w-full max-w-4xl mx-auto mt-8 mb-12">
      <motion.div 
        className={`relative flex items-center bg-white rounded-2xl shadow-sm border transition-all duration-300 ${
          isFocused ? 'border-blue-500 shadow-blue-100 shadow-lg ring-4 ring-blue-50' : 'border-gray-200 hover:border-gray-300'
        }`}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="pl-6 pr-3 py-4 flex items-center justify-center">
          <Search className={`h-6 w-6 transition-colors ${isFocused ? 'text-blue-500' : 'text-gray-400'}`} />
        </div>
        
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          placeholder="Hỏi InfoAgent bất cứ điều gì..."
          disabled={isLoading}
          className="flex-1 bg-transparent border-none py-5 text-lg text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-0 w-full"
        />
        
        <div className="pr-4 pl-2 py-3 flex items-center">
          <button 
            onClick={handleSearch}
            className={`p-3 rounded-xl transition-all ${
              inputText.length > 0 && !isLoading
                ? 'bg-blue-600 hover:bg-blue-700 text-white' 
                : 'bg-gray-100 text-gray-400'
            }`}
            disabled={inputText.length === 0 || isLoading}
          >
            {isLoading ? <Loader2 size={20} className="animate-spin" /> : <ArrowRight size={20} />}
          </button>
        </div>
      </motion.div>

      <div className="mt-6 flex flex-wrap gap-3 justify-center">
        {suggestions.map((suggestion, index) => (
          <button
            key={index}
            onClick={() => handleSuggestionClick(suggestion)}
            disabled={isLoading}
            className="px-4 py-2 bg-white border border-gray-200 rounded-full text-sm text-gray-600 hover:bg-blue-50 transition-colors"
          >
            {suggestion}
          </button>
        ))}
      </div>
    </div>
  );
};
