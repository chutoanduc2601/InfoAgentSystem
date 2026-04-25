
import { Search, BrainCircuit, Globe, Cpu } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="h-20 bg-white border-b border-gray-200 flex items-center justify-between px-6 shrink-0 z-10 shadow-sm">
      {/* Search Bar */}
      <div className="flex-1 max-w-2xl">
        <div className="relative group">
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400 group-focus-within:text-blue-500 transition-colors" />
          </div>
          <input
            type="text"
            className="block w-full pl-11 pr-4 py-2.5 border border-gray-300 rounded-xl leading-5 bg-gray-50 placeholder-gray-400 focus:outline-none focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all sm:text-sm"
            placeholder="Tìm kiếm nhanh..."
          />
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
            <span className="text-gray-400 text-xs border border-gray-300 rounded px-1.5 py-0.5 bg-white">⌘K</span>
          </div>
        </div>
      </div>

      {/* Agent Status Indicators */}
      <div className="ml-6 flex items-center space-x-4">
        <div className="hidden md:flex items-center space-x-3 text-sm">
          <span className="text-gray-500 font-medium">Agents:</span>
          
          <div className="flex items-center space-x-1.5 bg-gray-50 px-3 py-1.5 rounded-full border border-gray-200" title="Agent Điều phối">
            <BrainCircuit size={16} className="text-green-500" />
            <span className="text-gray-700 font-medium">Điều phối</span>
            <span className="relative flex h-2 w-2 ml-1">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
            </span>
          </div>

          <div className="flex items-center space-x-1.5 bg-gray-50 px-3 py-1.5 rounded-full border border-gray-200" title="Agent Tìm kiếm">
            <Globe size={16} className="text-blue-500" />
            <span className="text-gray-700 font-medium">Tìm kiếm</span>
            <span className="relative flex h-2 w-2 ml-1">
              <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
            </span>
          </div>

          <div className="flex items-center space-x-1.5 bg-gray-50 px-3 py-1.5 rounded-full border border-gray-200" title="Agent Xử lý">
            <Cpu size={16} className="text-amber-500" />
            <span className="text-gray-700 font-medium">Xử lý</span>
            <span className="relative flex h-2 w-2 ml-1">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-amber-500"></span>
            </span>
          </div>
        </div>
      </div>
    </header>
  );
};
