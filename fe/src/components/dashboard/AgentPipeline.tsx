import { motion } from 'framer-motion';
import { BrainCircuit, Globe, Cpu, CheckCircle2, FileText, Check } from 'lucide-react';
import { useQueryContext } from '../../context/QueryContext';

const steps = [
  { id: 'orchestrator', label: 'Điều phối', icon: BrainCircuit },
  { id: 'search', label: 'Tìm kiếm', icon: Globe },
  { id: 'processing', label: 'Xử lý', icon: Cpu },
  { id: 'verification', label: 'Xác thực', icon: CheckCircle2 },
  { id: 'summary', label: 'Tóm tắt', icon: FileText }
];

export const AgentPipeline = () => {
  const { currentStep, isLoading } = useQueryContext();

  if (currentStep < 0 && !isLoading) return null;

  return (
    <div className="w-full max-w-5xl mx-auto my-12 bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
      <h2 className="text-lg font-semibold text-gray-800 mb-8 flex items-center">
        <BrainCircuit className="mr-2 text-blue-600" size={20} />
        Trạng thái Luồng Agent
      </h2>

      <div className="relative flex items-center justify-between w-full">
        <div className="absolute left-0 top-1/2 -translate-y-1/2 w-full h-1 bg-gray-100 rounded-full"></div>
        <motion.div 
          className="absolute left-0 top-1/2 -translate-y-1/2 h-1 bg-blue-500 rounded-full"
          initial={{ width: '0%' }}
          animate={{ width: `${Math.min(((currentStep + 1) / steps.length) * 100, 100)}%` }}
        ></motion.div>

        {steps.map((step, index) => {
          const isCompleted = index < currentStep;
          const isActive = index === currentStep;
          const Icon = step.icon;

          return (
            <div key={step.id} className="relative z-10 flex flex-col items-center">
              <div className={`w-12 h-12 rounded-full flex items-center justify-center border-4 ${
                isCompleted ? 'bg-blue-600 border-blue-100 text-white' : 
                isActive ? 'bg-white border-blue-500 text-blue-500 shadow-lg' : 
                'bg-white border-gray-100 text-gray-300'
              }`}>
                {isCompleted ? <Check size={20} /> : <Icon size={20} />}
              </div>
              <span className={`mt-3 text-xs font-medium ${isActive ? 'text-blue-600' : 'text-gray-400'}`}>
                {step.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
