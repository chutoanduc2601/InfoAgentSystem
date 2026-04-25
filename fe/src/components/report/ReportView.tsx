import { useState } from 'react';
import { motion } from 'framer-motion';
import { ReportHeader } from './ReportHeader';
import { ReportSummary } from './ReportSummary';
import { ReportTabs } from './ReportTabs';
import { ReportCitations } from './ReportCitations';
import { ChatSidebar } from './ChatSidebar';
import { MessageSquarePlus } from 'lucide-react';

// Mock Data
const MOCK_REPORT_DATA = {
  title: "Comprehensive Analysis: Quantum Computing Innovations 2026",
  status: "Finalized",
  timestamp: "2026-04-25 09:15 AM",
  summaryTakeaways: [
    "Quantum supremacy has reached a new milestone with 1024-qubit stable architectures.",
    "Major investments from tech conglomerates are accelerating the transition from lab to enterprise.",
    "Cryptographic vulnerabilities remain the primary risk factor for legacy systems by 2028."
  ],
  tabs: [
    {
      id: "analysis",
      label: "In-depth Analysis",
      content: (
        <div className="space-y-4">
          <p>The recent breakthroughs in quantum error correction have significantly lowered the barrier to commercial viability. Specifically, the topological qubit approach has yielded a 100x improvement in coherence times.</p>
          <p>Furthermore, cloud-based quantum access models are democratizing the technology, allowing financial and pharmaceutical sectors to run complex simulations previously deemed impossible.</p>
          <h3 className="text-lg font-semibold text-gray-800 mt-6 mb-2">Market Projection</h3>
          <p>The market is expected to grow at a CAGR of 32% over the next five years, driven largely by optimization problems in logistics and material science.</p>
        </div>
      )
    },
    {
      id: "news",
      label: "Recent News",
      content: (
        <div className="space-y-4">
          <div className="p-4 border border-gray-100 rounded-lg bg-white">
            <h4 className="font-semibold text-[#1e3a8a]">Startup Q-Core Secures Series C</h4>
            <p className="text-sm text-gray-500 mt-1">Q-Core announced a $200M funding round to build scalable quantum processors for data centers. (Apr 24, 2026)</p>
          </div>
          <div className="p-4 border border-gray-100 rounded-lg bg-white">
            <h4 className="font-semibold text-[#1e3a8a]">New Encryption Standard Proposed</h4>
            <p className="text-sm text-gray-500 mt-1">The NIST has finalized its recommendations for post-quantum cryptographic algorithms to secure internet traffic. (Apr 20, 2026)</p>
          </div>
        </div>
      )
    },
    {
      id: "risk",
      label: "Risk Assessment",
      content: (
        <div className="space-y-4">
          <p>The primary risk involves the "Store Now, Decrypt Later" strategy employed by malicious actors. Enterprises must adopt post-quantum cryptography (PQC) immediately to protect long-term sensitive data.</p>
          <ul className="list-disc pl-5 space-y-2 text-gray-700">
            <li><strong>High Severity:</strong> Legacy financial records encryption.</li>
            <li><strong>Medium Severity:</strong> Supply chain hardware shortages for specialized cooling systems.</li>
            <li><strong>Low Severity:</strong> Immediate regulatory hurdles.</li>
          </ul>
        </div>
      )
    }
  ],
  citations: [
    { id: "1", title: "State of Quantum Computing 2026", url: "https://example.com/quantum-2026" },
    { id: "2", title: "NIST Post-Quantum Cryptography Standardization", url: "https://example.com/nist-pqc" },
    { id: "3", title: "Global Market Insights: Quantum Tech", url: "https://example.com/market-insights" }
  ]
};

export const ReportView = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);

  return (
    <div className="flex h-full w-full overflow-hidden bg-white">
      {/* Main Content Area */}
      <div className="flex-1 overflow-y-auto relative scrollbar-thin scrollbar-thumb-gray-300">
        <motion.div 
          className="max-w-5xl mx-auto px-8 py-10"
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <ReportHeader 
            title={MOCK_REPORT_DATA.title}
            status={MOCK_REPORT_DATA.status}
            timestamp={MOCK_REPORT_DATA.timestamp}
          />
          
          <ReportSummary takeaways={MOCK_REPORT_DATA.summaryTakeaways} />
          
          <ReportTabs tabs={MOCK_REPORT_DATA.tabs} />
          
          <ReportCitations citations={MOCK_REPORT_DATA.citations} />
        </motion.div>

        {/* Floating Chat Toggle (if closed) */}
        {!isChatOpen && (
          <button
            onClick={() => setIsChatOpen(true)}
            className="fixed bottom-8 right-8 bg-[#1e3a8a] text-white p-4 rounded-full shadow-xl hover:bg-[#2e4a9a] transition-all hover:scale-105 z-50 flex items-center justify-center"
            title="Ask Report Assistant"
          >
            <MessageSquarePlus size={24} />
          </button>
        )}
      </div>

      {/* Chat Sidebar */}
      <ChatSidebar isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
    </div>
  );
};
