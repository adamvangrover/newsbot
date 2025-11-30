import React, { useState, useEffect } from 'react';
import { Folder, FileText, ChevronRight, ChevronDown, Code, AlertCircle, Copy, Check } from 'lucide-react';

interface FileNode {
  name: string;
  path: string;
  type: 'folder' | 'file';
  size?: number;
  file_type?: string;
  content?: string;
  children?: FileNode[];
}

const RepoExplorer: React.FC = () => {
  const [fileTree, setFileTree] = useState<FileNode | null>(null);
  const [selectedFile, setSelectedFile] = useState<FileNode | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}repo_map.json`)
      .then(res => {
        if (!res.ok) throw new Error("Failed to load repo map");
        return res.json();
      })
      .then(data => {
        setFileTree(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const handleCopy = () => {
    if (selectedFile?.content) {
      navigator.clipboard.writeText(selectedFile.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const FileTreeItem: React.FC<{ node: FileNode; depth?: number }> = ({ node, depth = 0 }) => {
    const [isOpen, setIsOpen] = useState(false);

    // Auto-open root and first level
    useEffect(() => {
      if (depth < 1) setIsOpen(true);
    }, [depth]);

    const handleClick = (e: React.MouseEvent) => {
      e.stopPropagation();
      if (node.type === 'folder') {
        setIsOpen(!isOpen);
      } else {
        setSelectedFile(node);
      }
    };

    return (
      <div className="select-none">
        <div
          className={`flex items-center py-1 px-2 hover:bg-gray-800 cursor-pointer ${selectedFile?.path === node.path ? 'bg-green-900/30 text-green-400' : 'text-gray-300'}`}
          style={{ paddingLeft: `${depth * 16 + 8}px` }}
          onClick={handleClick}
        >
          {node.type === 'folder' && (
            <span className="mr-1 text-gray-500">
              {isOpen ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
            </span>
          )}
          {node.type === 'folder' ? (
            <Folder size={16} className="mr-2 text-yellow-500" />
          ) : (
            <FileText size={16} className="mr-2 text-blue-400" />
          )}
          <span className="text-sm truncate">{node.name}</span>
        </div>
        {isOpen && node.children && (
          <div>
            {node.children.map((child) => (
              <FileTreeItem key={child.path} node={child} depth={depth + 1} />
            ))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="flex h-[calc(100vh-6rem)] border border-gray-800 rounded bg-gray-900 overflow-hidden">
      {/* Sidebar */}
      <div className="w-1/3 min-w-[250px] max-w-sm border-r border-gray-800 flex flex-col">
        <div className="p-3 bg-gray-950 border-b border-gray-800 font-bold text-gray-200 flex items-center">
            <Code size={18} className="mr-2 text-green-500" />
            Repository Explorer
        </div>
        <div className="flex-1 overflow-y-auto p-2 bg-gray-950">
          {loading && <div className="text-gray-500 text-center mt-4">Loading repository map...</div>}
          {error && (
            <div className="text-red-400 p-4 text-sm flex items-center">
               <AlertCircle size={16} className="mr-2" />
               Failed to load repo map. Ensure `scripts/generate_repo_map.py` has been run.
            </div>
          )}
          {fileTree && <FileTreeItem node={fileTree} />}
        </div>
      </div>

      {/* Main Content (Code View) */}
      <div className="flex-1 bg-[#1e1e1e] overflow-hidden flex flex-col">
        {selectedFile ? (
          <>
            <div className="bg-gray-800 border-b border-gray-700 px-4 py-2 flex justify-between items-center">
                <div className="flex items-center space-x-2">
                    <span className="font-mono text-sm text-gray-300">{selectedFile.path}</span>
                    <span className="text-xs text-gray-500">({selectedFile.size} bytes)</span>
                </div>
                <button
                    onClick={handleCopy}
                    className="flex items-center space-x-1 text-xs bg-gray-700 hover:bg-gray-600 px-2 py-1 rounded transition-colors text-gray-300"
                    title="Copy to clipboard"
                >
                    {copied ? <Check size={14} className="text-green-400" /> : <Copy size={14} />}
                    <span>{copied ? 'Copied' : 'Copy'}</span>
                </button>
            </div>
            <div className="flex-1 overflow-auto p-4 relative group">
              {selectedFile.content ? (
                <pre className="text-sm font-mono text-gray-300 whitespace-pre-wrap leading-relaxed">
                  {selectedFile.content}
                </pre>
              ) : (
                <div className="flex flex-col items-center justify-center h-full text-gray-500">
                  <FileText size={48} className="mb-4 opacity-50" />
                  <p>Binary file or content not available for preview.</p>
                </div>
              )}
            </div>
          </>
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-gray-500">
            <Code size={64} className="mb-6 opacity-20" />
            <p className="text-lg">Select a file to view its content</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default RepoExplorer;
