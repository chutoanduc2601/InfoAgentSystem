import { SmartInput } from './SmartInput';
import { AgentPipeline } from './AgentPipeline';
import { RecommendationSection } from './RecommendationSection';
import { motion } from 'framer-motion';

export const SearchDashboard = () => {
  return (
    <motion.div 
      className="flex flex-col h-full w-full max-w-6xl mx-auto py-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
    >
      <div className="flex-1 flex flex-col items-center">
        {/* Hero Section */}
        <div className="text-center mt-12 mb-8">
          <motion.h1 
            className="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-700 to-blue-400 tracking-tight mb-4"
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.1, duration: 0.5 }}
          >
            Khám phá Thông minh
          </motion.h1>
          <motion.p 
            className="text-gray-500 text-lg md:text-xl max-w-2xl mx-auto"
            initial={{ y: -10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
          >
            Tận dụng sức mạnh của hệ thống Đa tác nhân (Multi-Agent) để truy xuất, xử lý và tóm tắt thông tin phức tạp theo thời gian thực.
          </motion.p>
        </div>

        {/* Smart Input Area */}
        <SmartInput />

        {/* Agent Pipeline Progress */}
        <AgentPipeline />

        {/* Recommendations */}
        <RecommendationSection />
      </div>
    </motion.div>
  );
};
