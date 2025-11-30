import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Activity,
  Database,
  Network,
  Info,
  Cpu,
  Menu,
  X,
  Server,
  Layers
} from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'System Status', href: '/status', icon: Activity },
    { name: 'Performance', href: '/performance', icon: Layers },
    { name: 'Synthetic Data', href: '/showcase', icon: Database },
    { name: 'Impact Analysis', href: '/impact', icon: Network },
    { name: 'Federated Learning', href: '/federated', icon: Server },
    { name: 'Architecture', href: '/architecture', icon: Cpu },
    { name: 'About', href: '/about', icon: Info },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <div className="min-h-screen bg-black text-gray-200 font-sans flex">
      {/* Sidebar for Desktop */}
      <div className="hidden md:flex flex-col w-64 bg-gray-900 border-r border-gray-800 fixed h-full z-10">
        <div className="p-6 border-b border-gray-800">
           <Link to="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-green-500 rounded-sm flex items-center justify-center">
                  <span className="text-black font-bold text-xl">N</span>
              </div>
              <span className="text-xl font-bold text-white tracking-tight">NewsBot Nexus</span>
           </Link>
        </div>

        <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
          {navigation.map((item) => (
            <Link
              key={item.name}
              to={item.href}
              className={`flex items-center px-4 py-3 text-sm font-medium rounded-md transition-colors ${
                isActive(item.href)
                  ? 'bg-green-900/20 text-green-400 border border-green-900/50'
                  : 'text-gray-400 hover:bg-gray-800 hover:text-white'
              }`}
            >
              <item.icon className="mr-3 h-5 w-5" />
              {item.name}
            </Link>
          ))}
        </nav>

        <div className="p-4 border-t border-gray-800">
            <div className="bg-gray-800/50 p-3 rounded text-xs text-gray-500">
                <p>Status: <span className="text-green-500">● Online</span></p>
                <p>Version: 2.0.1</p>
            </div>
        </div>
      </div>

      {/* Mobile Header */}
      <div className="md:hidden fixed top-0 w-full bg-gray-900 border-b border-gray-800 z-20 px-4 py-3 flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-green-500 rounded-sm flex items-center justify-center">
                  <span className="text-black font-bold text-xl">N</span>
              </div>
              <span className="text-lg font-bold text-white">NewsBot Nexus</span>
           </Link>
           <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="text-gray-400 hover:text-white">
               {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
           </button>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
          <div className="md:hidden fixed inset-0 z-10 bg-black pt-16">
              <nav className="p-4 space-y-2">
                  {navigation.map((item) => (
                    <Link
                      key={item.name}
                      to={item.href}
                      onClick={() => setIsMobileMenuOpen(false)}
                      className={`flex items-center px-4 py-3 text-base font-medium rounded-md ${
                        isActive(item.href)
                          ? 'bg-green-900/20 text-green-400 border border-green-900/50'
                          : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                      }`}
                    >
                      <item.icon className="mr-4 h-6 w-6" />
                      {item.name}
                    </Link>
                  ))}
              </nav>
          </div>
      )}

      {/* Main Content */}
      <div className="flex-1 md:ml-64 p-4 md:p-8 pt-20 md:pt-8 w-full overflow-hidden">
        {children}
      </div>
    </div>
  );
};

export default Layout;
