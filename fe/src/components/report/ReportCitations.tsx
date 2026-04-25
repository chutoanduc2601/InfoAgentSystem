import { ExternalLink, BookOpen } from 'lucide-react';

export type Citation = {
  id: string;
  title: string;
  url: string;
};

interface ReportCitationsProps {
  citations: Citation[];
}

export const ReportCitations = ({ citations }: ReportCitationsProps) => {
  if (!citations || citations.length === 0) return null;

  return (
    <div className="mt-12 pt-8 border-t border-gray-200">
      <div className="flex items-center mb-6">
        <BookOpen size={20} className="text-gray-500 mr-2" />
        <h3 className="text-lg font-semibold text-gray-800">Trích dẫn & Tài liệu tham khảo</h3>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {citations.map((citation, index) => (
          <a
            key={citation.id}
            href={citation.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-start p-4 bg-gray-50 border border-gray-100 rounded-lg hover:bg-gray-100 hover:border-gray-200 transition-colors group"
          >
            <span className="text-sm font-medium text-gray-400 mr-3 mt-0.5">
              [{index + 1}]
            </span>
            <div className="flex-1">
              <h4 className="text-sm font-medium text-gray-800 group-hover:text-[#1e3a8a] transition-colors line-clamp-2">
                {citation.title}
              </h4>
              <p className="text-xs text-gray-500 mt-1 truncate">
                {new URL(citation.url).hostname}
              </p>
            </div>
            <ExternalLink size={16} className="text-gray-400 group-hover:text-[#1e3a8a] ml-2 shrink-0 mt-0.5 transition-colors" />
          </a>
        ))}
      </div>
    </div>
  );
};
