import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Bot, 
  Plus, 
  MessageSquare, 
  Settings, 
  ChevronLeft, 
  ChevronRight, 
  User 
} from 'lucide-react';

interface SidebarProps {
  isCollapsed: boolean;
  setIsCollapsed: (collapsed: boolean) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ isCollapsed, setIsCollapsed }) => {
  const [history] = useState([
    "How does quantum computing work?",
    "Latest AI trends in 2026",
    "React vs Vue performance",
    "Explain black holes simply",
    "Best practices for API design"
  ]);
  const location = useLocation();

  return (
    <aside 
      className={`relative flex flex-col h-screen bg-[#16275c] text-white transition-all duration-300 ${
        isCollapsed ? 'w-20' : 'w-72'
      }`}
    >
      {/* Collapse Toggle */}
      <button 
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="absolute -right-2 top-6 bg-[#1e3a8a] border border-gray-600 rounded-full p-1 z-10 hover:bg-[#2e4a9a] transition-colors"
      >
        {isCollapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
      </button>

      {/* Logo */}
      <Link to="/" className="flex items-center h-20 px-5 border-b border-[#2a4590] hover:bg-[#1e3a8a] transition-colors">
        <Bot className="text-blue-400 shrink-0" size={32} />
        {!isCollapsed && (
          <span className="ml-3 text-xl font-bold tracking-wide">InfoAgent</span>
        )}
      </Link>

      {/* New Question Button */}
      <div className="p-4">
        <Link 
          to="/"
          className="flex items-center justify-center w-full bg-blue-600 hover:bg-blue-500 text-white rounded-lg p-3 transition-colors shadow-md"
          title="New Question"
        >
          <Plus size={20} />
          {!isCollapsed && <span className="ml-2 font-medium">New Question</span>}
        </Link>
      </div>

      {/* Search History */}
      <div className="flex-1 overflow-y-auto px-3 py-2 scrollbar-thin scrollbar-thumb-[#2a4590]">
        {!isCollapsed && (
          <h3 className="text-xs font-semibold text-blue-300 uppercase tracking-wider mb-3 px-2">
            History
          </h3>
        )}
        <ul className="space-y-1">
          {history.map((item, index) => {
            // Mock active state for the first item when on /report
            const isActive = index === 0 && location.pathname === '/report';
            return (
              <li key={index}>
                <Link 
                  to="/report"
                  className={`flex items-center w-full p-2 rounded-lg transition-colors text-left ${
                    isActive ? 'bg-[#2a4590]' : 'hover:bg-[#2a4590]'
                  } ${isCollapsed ? 'justify-center' : ''}`}
                  title={item}
                >
                  <MessageSquare size={18} className={`${isActive ? 'text-blue-400' : 'text-gray-400'} shrink-0`} />
                  {!isCollapsed && (
                    <span className={`ml-3 text-sm truncate ${isActive ? 'text-white font-medium' : 'text-gray-200'}`}>
                      {item}
                    </span>
                  )}
                </Link>
              </li>
            );
          })}
        </ul>
      </div>

      {/* User Profile */}
      <div className="p-4 border-t border-[#2a4590]">
        <button 
          className={`flex items-center w-full p-2 rounded-lg hover:bg-[#2a4590] transition-colors ${
            isCollapsed ? 'justify-center' : ''
          }`}
        >
          <div className="bg-blue-800 rounded-full p-1.5 shrink-0">
            <User size={20} />
          </div>
          {!isCollapsed && (
            <div className="ml-3 text-left">
              <p className="text-sm font-medium">Alex Developer</p>
              <p className="text-xs text-blue-300">Free Plan</p>
            </div>
          )}
        </button>
        <button 
          className={`flex items-center w-full p-2 mt-1 rounded-lg hover:bg-[#2a4590] transition-colors ${
            isCollapsed ? 'justify-center' : ''
          }`}
          title="Settings"
        >
          <Settings size={20} className="text-gray-400 shrink-0" />
          {!isCollapsed && <span className="ml-3 text-sm text-gray-200">Settings</span>}
        </button>
      </div>
    </aside>
  );
};
