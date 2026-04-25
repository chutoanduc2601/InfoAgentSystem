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
  title: "Phân tích Toàn diện: Đổi mới Máy tính Lượng tử 2026",
  status: "Đã hoàn thành",
  timestamp: "25/04/2026 09:15 Sáng",
  summaryTakeaways: [
    "Ưu thế lượng tử đã đạt đến một cột mốc mới với kiến trúc ổn định 1024-qubit.",
    "Các khoản đầu tư lớn từ các tập đoàn công nghệ đang đẩy nhanh quá trình chuyển đổi từ phòng thí nghiệm sang doanh nghiệp.",
    "Các lỗ hổng mật mã vẫn là yếu tố rủi ro chính đối với các hệ thống cũ vào năm 2028."
  ],
  tabs: [
    {
      id: "analysis",
      label: "Phân tích Chuyên sâu",
      content: (
        <div className="space-y-4">
          <p>Những đột phá gần đây trong việc sửa lỗi lượng tử đã làm giảm đáng kể rào cản đối với khả năng thương mại hóa. Cụ thể, phương pháp qubit topo đã mang lại sự cải thiện gấp 100 lần về thời gian kết hợp.</p>
          <p>Hơn nữa, các mô hình truy cập lượng tử dựa trên nền tảng đám mây đang dân chủ hóa công nghệ này, cho phép các lĩnh vực tài chính và dược phẩm chạy các mô phỏng phức tạp mà trước đây được coi là không thể.</p>
          <h3 className="text-lg font-semibold text-gray-800 mt-6 mb-2">Dự báo Thị trường</h3>
          <p>Thị trường dự kiến sẽ tăng trưởng với tốc độ CAGR 32% trong 5 năm tới, chủ yếu nhờ vào các bài toán tối ưu hóa trong hậu cần và khoa học vật liệu.</p>
        </div>
      )
    },
    {
      id: "news",
      label: "Tin tức Gần đây",
      content: (
        <div className="space-y-4">
          <div className="p-4 border border-gray-100 rounded-lg bg-white">
            <h4 className="font-semibold text-[#1e3a8a]">Công ty khởi nghiệp Q-Core Gọi vốn Series C thành công</h4>
            <p className="text-sm text-gray-500 mt-1">Q-Core công bố vòng gọi vốn 200 triệu USD để chế tạo bộ xử lý lượng tử có thể mở rộng cho các trung tâm dữ liệu. (24/04/2026)</p>
          </div>
          <div className="p-4 border border-gray-100 rounded-lg bg-white">
            <h4 className="font-semibold text-[#1e3a8a]">Tiêu chuẩn Mã hóa Mới được Đề xuất</h4>
            <p className="text-sm text-gray-500 mt-1">NIST đã hoàn tất các đề xuất về thuật toán mã hóa hậu lượng tử để bảo mật lưu lượng truy cập internet. (20/04/2026)</p>
          </div>
        </div>
      )
    },
    {
      id: "risk",
      label: "Đánh giá Rủi ro",
      content: (
        <div className="space-y-4">
          <p>Rủi ro chính liên quan đến chiến lược "Lưu trữ ngay, Giải mã sau" của các tác nhân độc hại. Các doanh nghiệp phải áp dụng mật mã hậu lượng tử (PQC) ngay lập tức để bảo vệ dữ liệu nhạy cảm trong dài hạn.</p>
          <ul className="list-disc pl-5 space-y-2 text-gray-700">
            <li><strong>Mức độ Nghiêm trọng Cao:</strong> Mã hóa hồ sơ tài chính cũ.</li>
            <li><strong>Mức độ Nghiêm trọng Trung bình:</strong> Thiếu hụt phần cứng chuỗi cung ứng cho các hệ thống làm mát chuyên dụng.</li>
            <li><strong>Mức độ Nghiêm trọng Thấp:</strong> Những trở ngại pháp lý trước mắt.</li>
          </ul>
        </div>
      )
    }
  ],
  citations: [
    { id: "1", title: "Tình trạng Máy tính Lượng tử 2026", url: "https://example.com/quantum-2026" },
    { id: "2", title: "Tiêu chuẩn hóa Mật mã Hậu Lượng tử NIST", url: "https://example.com/nist-pqc" },
    { id: "3", title: "Thông tin chi tiết Thị trường Toàn cầu: Công nghệ Lượng tử", url: "https://example.com/market-insights" }
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
            title="Hỏi Trợ lý Báo cáo"
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
