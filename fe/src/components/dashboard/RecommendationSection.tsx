import { motion, type Variants } from 'framer-motion';
import { Lightbulb, Database, Activity, Lock, Network } from 'lucide-react';

const recommendations = [
  {
    title: 'Kiến trúc Hệ thống',
    description: 'Khám phá các bản thiết kế mới nhất cho framework đa tác nhân có thể mở rộng.',
    icon: Network,
    color: 'from-blue-500 to-indigo-500',
    bgColor: 'bg-blue-50',
    iconColor: 'text-blue-600'
  },
  {
    title: 'Bảo mật Dữ liệu',
    description: 'Hiểu cách InfoAgent xử lý dữ liệu của bạn một cách an toàn.',
    icon: Lock,
    color: 'from-emerald-500 to-teal-500',
    bgColor: 'bg-emerald-50',
    iconColor: 'text-emerald-600'
  },
  {
    title: 'Hiệu suất Mô hình',
    description: 'Các chỉ số thời gian thực về độ trễ và độ chính xác của mô hình ngôn ngữ.',
    icon: Activity,
    color: 'from-purple-500 to-fuchsia-500',
    bgColor: 'bg-purple-50',
    iconColor: 'text-purple-600'
  },
  {
    title: 'Cơ sở Tri thức',
    description: 'Đi sâu vào cơ sở dữ liệu vector hợp nhất và truy xuất tài liệu.',
    icon: Database,
    color: 'from-amber-500 to-orange-500',
    bgColor: 'bg-amber-50',
    iconColor: 'text-amber-600'
  }
];

const containerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const itemVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { type: 'spring', stiffness: 300, damping: 24 } }
};

export const RecommendationSection = () => {
  return (
    <div className="w-full max-w-5xl mx-auto mt-16 mb-8">
      <div className="flex items-center mb-6">
        <Lightbulb className="text-amber-500 mr-2" size={24} />
        <h3 className="text-xl font-bold text-gray-800 tracking-tight">Chủ đề Đề xuất</h3>
      </div>
      
      <motion.div 
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {recommendations.map((item, index) => {
          const Icon = item.icon;
          return (
            <motion.div 
              key={index}
              variants={itemVariants}
              className="relative group bg-white border border-gray-100 p-6 rounded-2xl shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 cursor-pointer overflow-hidden"
            >
              {/* Top Gradient Bar Effect on Hover */}
              <div className={`absolute top-0 left-0 w-full h-1 bg-gradient-to-r ${item.color} transform origin-left scale-x-0 group-hover:scale-x-100 transition-transform duration-300`}></div>
              
              <div className={`w-12 h-12 ${item.bgColor} rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
                <Icon size={24} className={item.iconColor} />
              </div>
              
              <h4 className="font-semibold text-gray-800 mb-2 group-hover:text-blue-600 transition-colors">
                {item.title}
              </h4>
              <p className="text-sm text-gray-500 leading-relaxed">
                {item.description}
              </p>
            </motion.div>
          );
        })}
      </motion.div>
    </div>
  );
};
