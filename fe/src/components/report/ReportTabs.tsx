import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

type Tab = {
  id: string;
  label: string;
  content: React.ReactNode;
};

interface ReportTabsProps {
  tabs: Tab[];
}

export const ReportTabs = ({ tabs }: ReportTabsProps) => {
  const [activeTab, setActiveTab] = useState(tabs[0].id);

  return (
    <div className="w-full mt-8">
      {/* Tab Header */}
      <div className="flex border-b border-gray-200">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`relative px-6 py-4 text-sm font-medium transition-colors ${
                isActive ? 'text-[#1e3a8a]' : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              {tab.label}
              {isActive && (
                <motion.div
                  layoutId="activeTabIndicator"
                  className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#1e3a8a]"
                  transition={{ type: 'tween', duration: 0.3 }}
                />
              )}
            </button>
          );
        })}
      </div>

      {/* Tab Content */}
      <div className="py-6 min-h-[400px]">
        <AnimatePresence mode="wait">
          {tabs.map((tab) => {
            if (tab.id === activeTab) {
              return (
                <motion.div
                  key={tab.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.3, ease: 'easeInOut' }}
                  className="text-gray-700 leading-relaxed text-[15px]"
                >
                  {tab.content}
                </motion.div>
              );
            }
            return null;
          })}
        </AnimatePresence>
      </div>
    </div>
  );
};
