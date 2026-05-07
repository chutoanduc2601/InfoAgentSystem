import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { supabase } from '../../lib/supabase';
import { historyService, type HistoryItem } from '../../services/api';
import { useQueryContext } from '../../context/QueryContext';
import {
  Bot,
  Plus,
  MessageSquare,
  Settings,
  ChevronLeft,
  ChevronRight,
  User,
  LogOut,
  Loader2,
  AlertCircle,
  RefreshCw,
  Pencil,
  Trash2,
  Check,
  X,
} from 'lucide-react';

interface SidebarProps {
  isCollapsed: boolean;
  setIsCollapsed: (collapsed: boolean) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ isCollapsed, setIsCollapsed }) => {
  const [history,          setHistory]          = useState<HistoryItem[]>([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [historyError,     setHistoryError]     = useState<string | null>(null);
  const [userName,         setUserName]         = useState<string>('Đang tải...');
  const [userId,           setUserId]           = useState<string | null>(null);
  const [editingId,        setEditingId]        = useState<string | null>(null);
  const [editingTitle,     setEditingTitle]     = useState<string>('');

  const location = useLocation();
  const { loadFromHistory, currentQueryId, sidebarRefreshKey } = useQueryContext();

  const handleRename = async (id: string) => {
    if (!editingTitle.trim()) return;
    const ok = await historyService.renameHistory(id, editingTitle);
    if (ok && userId) {
      setEditingId(null);
      await fetchHistory(userId);
    }
  };

  const handleDelete = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation(); // Không kích hoạt việc load report
    if (window.confirm('Bạn có chắc chắn muốn xóa đoạn chat này?')) {
      const ok = await historyService.deleteHistory(id);
      if (ok && userId) {
        await fetchHistory(userId);
      }
    }
  };

  // ───── Lấy thông tin user lần đầu ─────
  useEffect(() => {
    const init = async () => {
      const { data: { user } } = await supabase.auth.getUser();
      if (user) {
        setUserName(user.user_metadata?.full_name || user.email?.split('@')[0] || 'Người dùng');
        setUserId(user.id);
        await fetchHistory(user.id);
      } else {
        setUserName('Khách');
      }
    };
    init();
  }, []);

  const fetchHistory = async (uid: string) => {
    setIsLoadingHistory(true);
    setHistoryError(null);
    try {
      const data = await historyService.getHistory(uid);
      setHistory(data ?? []);
    } catch {
      setHistoryError('Không thể tải lịch sử');
    } finally {
      setIsLoadingHistory(false);
    }
  };

  // ───── Tự động refresh khi có query mới (sidebarRefreshKey thay đổi) ─────
  useEffect(() => {
    if (userId && sidebarRefreshKey > 0) {
      fetchHistory(userId);
    }
  }, [sidebarRefreshKey]);

  // ───── Refresh khi quay về / ─────
  useEffect(() => {
    if (userId && location.pathname === '/') {
      fetchHistory(userId);
    }
  }, [location.pathname, userId]);

  // ───── Màu badge trạng thái ─────
  const statusColor = (status: string) => {
    if (status === 'done')  return 'bg-green-400';
    if (status === 'error') return 'bg-red-400';
    return 'bg-yellow-400 animate-pulse'; // processing
  };

  return (
    <aside
      className={`relative flex flex-col h-screen bg-[#16275c] text-white transition-all duration-300 ${
        isCollapsed ? 'w-20' : 'w-72'
      }`}
    >
      {/* Collapse Toggle */}
      <button
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="absolute -right-2 top-6 bg-[#1e3a8a] border border-gray-600 rounded-full p-1 z-10 hover:bg-[#2e4a9a] transition-colors"
      >
        {isCollapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
      </button>

      {/* Logo */}
      <Link to="/" className="flex items-center h-20 px-5 border-b border-[#2a4590] hover:bg-[#1e3a8a] transition-colors">
        <Bot className="text-blue-400 shrink-0" size={32} />
        {!isCollapsed && (
          <span className="ml-3 text-xl font-bold tracking-wide">InfoAgent</span>
        )}
      </Link>

      {/* New Question Button */}
      <div className="p-4">
        <Link
          to="/"
          className="flex items-center justify-center w-full bg-blue-600 hover:bg-blue-500 text-white rounded-lg p-3 transition-colors shadow-md"
          title="Câu hỏi mới"
        >
          <Plus size={20} />
          {!isCollapsed && <span className="ml-2 font-medium">Câu hỏi mới</span>}
        </Link>
      </div>

      {/* Search History */}
      <div className="flex-1 overflow-y-auto px-3 py-2 scrollbar-thin scrollbar-thumb-[#2a4590]">
        {!isCollapsed && (
          <div className="flex items-center justify-between mb-3 px-2">
            <h3 className="text-xs font-semibold text-blue-300 uppercase tracking-wider">
              Lịch sử
            </h3>
            {userId && (
              <button
                onClick={() => fetchHistory(userId)}
                title="Làm mới"
                disabled={isLoadingHistory}
                className="text-blue-300 hover:text-white transition-colors disabled:opacity-40"
              >
                <RefreshCw size={13} className={isLoadingHistory ? 'animate-spin' : ''} />
              </button>
            )}
          </div>
        )}

        {/* Loading state */}
        {isLoadingHistory && (
          <div className={`flex ${isCollapsed ? 'justify-center' : 'items-center gap-2 px-2'} text-blue-300 text-xs py-3`}>
            <Loader2 size={14} className="animate-spin shrink-0" />
            {!isCollapsed && <span>Đang tải...</span>}
          </div>
        )}

        {/* Error state */}
        {historyError && !isLoadingHistory && (
          <div className={`flex ${isCollapsed ? 'justify-center' : 'items-center gap-2 px-2'} text-red-300 text-xs py-3`}>
            <AlertCircle size={14} className="shrink-0" />
            {!isCollapsed && <span>{historyError}</span>}
          </div>
        )}

        {/* History list */}
        {!isLoadingHistory && !historyError && (
          <ul className="space-y-1">
            {history.length === 0 && !isCollapsed && (
              <li className="text-xs text-gray-400 px-2 py-4 text-center">
                Chưa có lịch sử tra cứu
              </li>
            )}
            {history.map((item) => {
              const isActive = item.queryId === currentQueryId;
              const isEditing = item.queryId === editingId;
              const canLoad  = item.status === 'done' && item.report != null;

              return (
                <li key={item.queryId} className="group relative">
                  {isEditing ? (
                    <div className="flex items-center gap-1 p-2 bg-[#2a4590] rounded-lg">
                      <input
                        autoFocus
                        className="flex-1 bg-blue-900 text-white text-sm p-1 rounded outline-none border border-blue-400"
                        value={editingTitle}
                        onChange={(e) => setEditingTitle(e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') handleRename(item.queryId);
                          if (e.key === 'Escape') setEditingId(null);
                        }}
                      />
                      <button onClick={() => handleRename(item.queryId)} className="text-green-400 hover:text-white">
                        <Check size={14} />
                      </button>
                      <button onClick={() => setEditingId(null)} className="text-red-400 hover:text-white">
                        <X size={14} />
                      </button>
                    </div>
                  ) : (
                    <div className="relative">
                      <button
                        onClick={() => canLoad && loadFromHistory(item)}
                        disabled={!canLoad}
                        title={item.queryText}
                        className={`flex items-center w-full p-2 rounded-lg transition-colors text-left
                          ${isActive ? 'bg-[#2a4590]' : 'hover:bg-[#1e3a8a]'}
                          ${isCollapsed ? 'justify-center' : ''}
                          ${!canLoad ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer'}
                        `}
                      >
                        {/* Icon + status dot */}
                        <div className="relative shrink-0">
                          <MessageSquare
                            size={18}
                            className={`${isActive ? 'text-blue-400' : 'text-gray-400 group-hover:text-blue-300'} transition-colors`}
                          />
                          <span
                            className={`absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full ${statusColor(item.status)}`}
                          />
                        </div>

                        {/* Text */}
                        {!isCollapsed && (
                          <div className="ml-3 min-w-0 flex-1 pr-8">
                            <p className={`text-sm truncate ${isActive ? 'text-white font-medium' : 'text-gray-200'}`}>
                              {item.queryText}
                            </p>
                            <p className="text-[10px] text-blue-300 mt-0.5">
                              {new Date(item.createdAt).toLocaleString('vi-VN', {
                                day: '2-digit', month: '2-digit',
                                hour: '2-digit', minute: '2-digit',
                              })}
                            </p>
                          </div>
                        )}
                      </button>

                      {/* Action Buttons (Edit/Delete) - Only show on hover and when not collapsed */}
                      {!isCollapsed && (
                        <div className="absolute right-1 top-1/2 -translate-y-1/2 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity bg-inherit">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              setEditingId(item.queryId);
                              setEditingTitle(item.queryText);
                            }}
                            className="p-1 hover:text-blue-400 text-gray-400 transition-colors"
                            title="Đổi tên"
                          >
                            <Pencil size={14} />
                          </button>
                          <button
                            onClick={(e) => handleDelete(e, item.queryId)}
                            className="p-1 hover:text-red-400 text-gray-400 transition-colors"
                            title="Xóa"
                          >
                            <Trash2 size={14} />
                          </button>
                        </div>
                      )}
                    </div>
                  )}
                </li>
              );
            })}
          </ul>
        )}
      </div>

      {/* User Profile */}
      <div className="p-4 border-t border-[#2a4590]">
        <button
          className={`flex items-center w-full p-2 rounded-lg hover:bg-[#2a4590] transition-colors ${
            isCollapsed ? 'justify-center' : ''
          }`}
        >
          <div className="bg-blue-800 rounded-full p-1.5 shrink-0">
            <User size={20} />
          </div>
          {!isCollapsed && (
            <div className="ml-3 text-left">
              <p className="text-sm font-medium">{userName}</p>
              <p className="text-xs text-blue-300">Gói miễn phí</p>
            </div>
          )}
        </button>

        <button
          className={`flex items-center w-full p-2 mt-1 rounded-lg hover:bg-[#2a4590] transition-colors ${
            isCollapsed ? 'justify-center' : ''
          }`}
          title="Cài đặt"
        >
          <Settings size={20} className="text-gray-400 shrink-0" />
          {!isCollapsed && <span className="ml-3 text-sm text-gray-200">Cài đặt</span>}
        </button>

        <button
          onClick={async () => { await supabase.auth.signOut(); }}
          className={`flex items-center w-full p-2 mt-1 rounded-lg hover:bg-red-500/20 text-red-300 transition-colors ${
            isCollapsed ? 'justify-center' : ''
          }`}
          title="Đăng xuất"
        >
          <LogOut size={20} className="shrink-0" />
          {!isCollapsed && <span className="ml-3 text-sm font-medium">Đăng xuất</span>}
        </button>
      </div>
    </aside>
  );
};
