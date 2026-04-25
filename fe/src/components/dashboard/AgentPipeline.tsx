
import { motion } from 'framer-motion';
import { BrainCircuit, Globe, Cpu, CheckCircle2, FileText, Check } from 'lucide-react';

const steps = [
  { id: 'orchestrator', label: 'Điều phối', icon: BrainCircuit },
  { id: 'search', label: 'Tìm kiếm', icon: Globe },
  { id: 'processing', label: 'Xử lý', icon: Cpu },
  { id: 'verification', label: 'Xác thực', icon: CheckCircle2 },
  { id: 'summary', label: 'Tóm tắt', icon: FileText }
];

// Mocking the active step (e.g., currently searching)
const currentStepIndex = 1;

export const AgentPipeline = () => {
  return (
    <div className="w-full max-w-5xl mx-auto my-12 bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
      <h2 className="text-lg font-semibold text-gray-800 mb-8 flex items-center">
        <BrainCircuit className="mr-2 text-blue-600" size={20} />
        Trạng thái Luồng Agent
      </h2>

      <div className="relative flex items-center justify-between w-full">
        {/* Background Line */}
        <div className="absolute left-0 top-1/2 -translate-y-1/2 w-full h-1 bg-gray-100 rounded-full"></div>
        
        {/* Active Line Progress */}
        <motion.div 
          className="absolute left-0 top-1/2 -translate-y-1/2 h-1 bg-blue-500 rounded-full"
          initial={{ width: '0%' }}
          animate={{ width: `${(currentStepIndex / (steps.length - 1)) * 100}%` }}
          transition={{ duration: 1, ease: 'easeInOut' }}
        ></motion.div>

        {/* Steps */}
        {steps.map((step, index) => {
          const isCompleted = index < currentStepIndex;
          const isActive = index === currentStepIndex;
          
          const Icon = step.icon;

          return (
            <div key={step.id} className="relative z-10 flex flex-col items-center">
              {/* Node */}
              <div className="relative flex items-center justify-center">
                <motion.div 
                  className={`w-14 h-14 rounded-full flex items-center justify-center border-4 transition-colors duration-500 ${
                    isCompleted ? 'bg-blue-600 border-blue-200 text-white' : 
                    isActive ? 'bg-blue-500 border-blue-100 text-white shadow-lg shadow-blue-200' : 
                    'bg-white border-gray-200 text-gray-400'
                  }`}
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ delay: index * 0.1, duration: 0.4 }}
                >
                  {isCompleted ? <Check size={24} /> : <Icon size={24} />}
                </motion.div>
              </div>

              {/* Label */}
              <motion.div 
                className={`mt-4 text-sm font-medium ${
                  isCompleted ? 'text-gray-700' : 
                  isActive ? 'text-blue-600 font-bold' : 
                  'text-gray-400'
                }`}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 + (index * 0.1), duration: 0.4 }}
              >
                {step.label}
              </motion.div>
              
              {/* Status text for active step */}
              {isActive && (
                <motion.span 
                  className="absolute -bottom-6 text-xs text-blue-500 font-medium tracking-wide uppercase"
                  animate={{ opacity: [0.5, 1, 0.5] }}
                  transition={{ repeat: Infinity, duration: 2 }}
                >
                  Đang xử lý...
                </motion.span>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
