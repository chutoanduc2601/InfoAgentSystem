import { Download, Share2, CheckCircle2, Clock } from 'lucide-react';

interface ReportHeaderProps {
  title: string;
  status: string;
  timestamp: string;
}

export const ReportHeader = ({ title, status, timestamp }: ReportHeaderProps) => {
  return (
    <div className="flex flex-col md:flex-row md:items-start justify-between gap-6 pb-8 border-b border-gray-200">
      <div className="flex-1">
        <h1 className="text-3xl font-bold text-[#1e3a8a] leading-tight mb-4 tracking-tight">
          {title}
        </h1>
        <div className="flex items-center space-x-6 text-sm text-gray-600">
          <div className="flex items-center space-x-1.5">
            <CheckCircle2 size={16} className="text-emerald-500" />
            <span className="font-medium text-gray-700">Status:</span>
            <span>{status}</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <Clock size={16} className="text-blue-500" />
            <span className="font-medium text-gray-700">Generated:</span>
            <span>{timestamp}</span>
          </div>
        </div>
      </div>
      
      <div className="flex items-center space-x-3 shrink-0">
        <button className="flex items-center space-x-2 px-4 py-2 bg-white border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 hover:border-gray-400 transition-colors shadow-sm font-medium">
          <Share2 size={18} />
          <span>Share</span>
        </button>
        <button className="flex items-center space-x-2 px-4 py-2 bg-[#1e3a8a] text-white rounded-lg hover:bg-[#2e4a9a] transition-colors shadow-sm font-medium">
          <Download size={18} />
          <span>Export PDF</span>
        </button>
      </div>
    </div>
  );
};
