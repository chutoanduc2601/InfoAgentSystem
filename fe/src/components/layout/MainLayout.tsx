import { useState } from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

interface MainLayoutProps {
  children: React.ReactNode;
}

export const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);

  return (
    <div className="flex h-screen w-full bg-[#f3f4f6] overflow-hidden font-sans text-gray-900">
      {/* Sidebar */}
      <Sidebar isCollapsed={isSidebarCollapsed} setIsCollapsed={setIsSidebarCollapsed} />

      {/* Main Content Area */}
      <div className="flex flex-col flex-1 min-w-0 h-screen transition-all duration-300">
        <Header />
        
        {/* Main Content Body */}
        <main className="flex-1 overflow-y-auto p-6 md:p-8 relative">
          <div className="max-w-6xl mx-auto h-full flex flex-col">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};
