import { Sparkles } from "lucide-react";
import ReactMarkdown from "react-markdown";

interface ReportSummaryProps {
  takeaways: string[];
}

export const ReportSummary = ({ takeaways }: ReportSummaryProps) => {
  return (
    <div className="bg-[#f8fafc] border border-[#e2e8f0] rounded-xl p-6 shadow-sm my-8 relative overflow-hidden">
      {/* Decorative accent line */}
      <div className="absolute top-0 left-0 w-1 h-full bg-[#1e3a8a]"></div>

      <div className="flex items-center mb-4">
        <Sparkles size={20} className="text-[#1e3a8a] mr-2" />
        <h2 className="text-xl font-semibold text-[#1e3a8a]">
          Tóm tắt Nội dung
        </h2>
      </div>

      <ul className="space-y-3">
        {takeaways.map((point, index) => (
          <li key={index} className="flex items-start">
            <span className="flex-shrink-0 w-1.5 h-1.5 rounded-full bg-[#3b82f6] mt-2.5 mr-3"></span>
            <div className="text-gray-700 leading-relaxed text-[15px]">
              <ReactMarkdown>{point}</ReactMarkdown>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};
