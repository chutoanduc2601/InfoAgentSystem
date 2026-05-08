import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bot, Shield, Zap, Workflow } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { LoginForm } from '../components/auth/LoginForm';
import { RegisterForm } from '../components/auth/RegisterForm';
import { ForgotPasswordForm } from '../components/auth/ForgotPasswordForm';

interface AuthPageProps {
  onAuthSuccess: () => void;
}

export const AuthPage: React.FC<AuthPageProps> = ({ onAuthSuccess }) => {
  const [mode, setMode] = useState<'login' | 'register' | 'forgot'>('login');
  const navigate = useNavigate();

  const toggleMode = () => {
    setMode(prev => prev === 'login' ? 'register' : 'login');
  };

  return (
    <div className="min-h-screen flex w-full bg-white">
      {/* Left Panel: Value Proposition (Hidden on very small screens, visible on md and up) */}
      <div className="hidden md:flex md:w-1/2 bg-[#1e3a8a] text-white flex-col justify-between p-12 relative overflow-hidden">
        {/* Background decorative elements */}
        <div className="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 rounded-full bg-white opacity-5 blur-3xl"></div>
        <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-80 h-80 rounded-full bg-blue-400 opacity-10 blur-3xl"></div>

        <div className="relative z-10">
          <div className="flex items-center space-x-3 mb-16">
            <Bot size={40} className="text-blue-300" />
            <span className="text-3xl font-bold tracking-tight">InfoAgent</span>
          </div>

          <h1 className="text-4xl lg:text-5xl font-bold leading-tight mb-6">
            Xử lý Thông tin Thông minh Đa tác nhân
          </h1>
          <p className="text-blue-100 text-lg max-w-md mb-12">
            Tận dụng sức mạnh của các AI agent phi tập trung để điều phối, tìm kiếm và xác thực dữ liệu phức tạp với độ chính xác chưa từng có.
          </p>

          <div className="space-y-6">
            <div className="flex items-center space-x-4">
              <div className="bg-blue-800/50 p-3 rounded-xl">
                <Workflow className="text-blue-300" size={24} />
              </div>
              <div>
                <h3 className="font-semibold text-lg">Điều phối Tự động</h3>
                <p className="text-blue-200 text-sm">Các agent phối hợp các tác vụ một cách mượt mà.</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="bg-blue-800/50 p-3 rounded-xl">
                <Zap className="text-blue-300" size={24} />
              </div>
              <div>
                <h3 className="font-semibold text-lg">Xử lý Thời gian thực</h3>
                <p className="text-blue-200 text-sm">Tổng hợp dữ liệu nhanh như chớp.</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="bg-blue-800/50 p-3 rounded-xl">
                <Shield className="text-blue-300" size={24} />
              </div>
              <div>
                <h3 className="font-semibold text-lg">Trí tuệ được Xác thực</h3>
                <p className="text-blue-200 text-sm">Các luồng xác thực nhiều bước.</p>
              </div>
            </div>
          </div>
        </div>

        <div className="relative z-10 text-blue-200 text-sm">
          &copy; {new Date().getFullYear()} InfoAgent System. Đã đăng ký bản quyền.
        </div>
      </div>

      {/* Right Panel: Authentication Form */}
      <div className="w-full md:w-1/2 flex items-center justify-center p-6 sm:p-12 bg-gray-50 relative">
        {/* Mobile Logo Header */}
        <div className="md:hidden absolute top-8 left-8 flex items-center space-x-2">
          <Bot size={28} className="text-[#1e3a8a]" />
          <span className="text-xl font-bold text-[#1e3a8a] tracking-tight">InfoAgent</span>
        </div>

        <div className="w-full max-w-md relative">
          <AnimatePresence mode="wait">
            {mode === 'login' && (
              <motion.div
                key="login"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ duration: 0.3 }}
              >
                <LoginForm
                  onToggleMode={toggleMode}
                  onLoginSuccess={onAuthSuccess}
                  onForgotPassword={() => setMode('forgot')}
                />
              </motion.div>
            )}
            {mode === 'register' && (
              <motion.div
                key="register"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
              >
                <RegisterForm onToggleMode={toggleMode} onRegisterSuccess={onAuthSuccess} />
              </motion.div>
            )}
            {mode === 'forgot' && (
              <motion.div
                key="forgot"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
              >
                <ForgotPasswordForm onBack={() => setMode('login')} />
              </motion.div>
            )}
          </AnimatePresence>

          {/* Nút Tiếp tục với tư cách Khách */}
          {mode !== 'forgot' && (
            <div className="mt-6 text-center">
              <div className="relative mb-4">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300" />
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-gray-50 text-gray-500">Hoặc</span>
                </div>
              </div>
              <button
                onClick={() => navigate('/')}
                className="w-full py-2.5 px-4 border-2 border-dashed border-gray-300 rounded-lg text-sm font-medium text-gray-600 hover:border-[#1e3a8a] hover:text-[#1e3a8a] transition-colors"
              >
                Tiếp tục với tư cách Khách
              </button>
              <p className="mt-2 text-xs text-gray-400">Giới hạn 5 lần tra cứu • Không lưu lịch sử</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
