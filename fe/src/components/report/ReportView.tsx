import { useState } from "react";
import { motion } from "framer-motion";
import { ReportHeader } from "./ReportHeader";
import { ReportSummary } from "./ReportSummary";
import { ReportCitations } from "./ReportCitations";
import { ChatSidebar } from "./ChatSidebar";
import {
  MessageSquarePlus,
  Loader2,
  AlertTriangle,
  ArrowLeft,
} from "lucide-react";
import { useQueryContext } from "../../context/QueryContext";
import { Link } from "react-router-dom";
import ReactMarkdown from "react-markdown";

export const ReportView = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const { report, isLoading, error, query } = useQueryContext();

  if (isLoading) {
    return (
      <div className="flex h-full w-full items-center justify-center bg-white p-20">
        <div className="text-center">
          <Loader2
            size={48}
            className="animate-spin text-blue-500 mx-auto mb-6"
          />
          <h2 className="text-xl font-semibold text-gray-800">
            Đang phân tích...
          </h2>
          <p className="text-gray-500 mt-2 italic">"{query}"</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex h-full w-full items-center justify-center bg-white">
        <div className="text-center max-w-md">
          <AlertTriangle size={48} className="text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-800">Đã xảy ra lỗi</h2>
          <p className="text-gray-500 mb-6">{error}</p>
          <Link to="/" className="px-6 py-3 bg-blue-600 text-white rounded-xl">
            Thử lại
          </Link>
        </div>
      </div>
    );
  }

  if (!report) return <Navigate to="/" />;

  return (
    <div className="flex h-full w-full overflow-hidden bg-white">
      <div className="flex-1 overflow-y-auto px-8 py-10">
        <ReportHeader
          title={report.query}
          status={report.confidence_label}
          timestamp={new Date().toLocaleString()}
        />
        <ReportSummary takeaways={report.quick_summary} />

        <div className="mt-8">
          <h3 className="text-lg font-semibold mb-4">Phân tích Chi tiết</h3>
          <div className="prose max-w-none bg-gray-50 rounded-xl p-6 border border-gray-100">
            {/* {report.detailed_report} */}
            <ReactMarkdown>{report.detailed_report}</ReactMarkdown>
          </div>
        </div>

        {report.recommendations.length > 0 && (
          <div className="mt-8">
            <h3 className="text-lg font-semibold mb-4">Gợi ý</h3>
            <div className="flex flex-wrap gap-2">
              {report.recommendations.map((r: string, i: number) => (
                <span
                  key={i}
                  className="px-3 py-1 bg-blue-50 text-blue-700 rounded-lg text-sm"
                >
                  {r}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
      <ChatSidebar isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
    </div>
  );
};
import { Navigate } from "react-router-dom";
