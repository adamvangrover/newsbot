import React from 'react';
import { Puzzle, Zap, Globe, Lock, Cpu, GitMerge } from 'lucide-react';

const Plugins: React.FC = () => {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Plugins & Extensions</h1>
        <p className="text-gray-400">Expand the capabilities of NewsBot Nexus with community and first-party modules.</p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Plugin Card 1 */}
          <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl group hover:border-purple-500/50 transition-all">
              <div className="mb-4 flex items-center justify-between">
                  <div className="w-12 h-12 bg-purple-900/30 rounded-lg flex items-center justify-center text-purple-400 group-hover:bg-purple-900/50 transition-colors">
                      <Globe size={24} />
                  </div>
                  <span className="text-xs font-mono text-gray-500 border border-gray-700 px-2 py-1 rounded">v1.2</span>
              </div>
              <h3 className="text-lg font-bold text-white mb-2">GeoSpatial Visualizer</h3>
              <p className="text-gray-400 text-sm mb-4">
                  Renders news events on an interactive 3D globe using WebGL. Highlights conflict zones and trade routes.
              </p>
              <div className="flex flex-wrap gap-2 mb-4">
                  <span className="text-xs text-gray-500 bg-gray-800 px-2 py-0.5 rounded">Visualization</span>
                  <span className="text-xs text-gray-500 bg-gray-800 px-2 py-0.5 rounded">React</span>
              </div>
              <button className="w-full py-2 border border-gray-700 hover:bg-gray-800 text-gray-300 rounded text-sm transition-colors">
                  Install
              </button>
          </div>

          {/* Plugin Card 2 */}
          <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl group hover:border-purple-500/50 transition-all">
              <div className="mb-4 flex items-center justify-between">
                  <div className="w-12 h-12 bg-blue-900/30 rounded-lg flex items-center justify-center text-blue-400 group-hover:bg-blue-900/50 transition-colors">
                      <Lock size={24} />
                  </div>
                   <span className="text-xs font-mono text-gray-500 border border-gray-700 px-2 py-1 rounded">v0.8</span>
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Homomorphic Encryption</h3>
              <p className="text-gray-400 text-sm mb-4">
                  Enable secure multi-party computation for training models on encrypted financial data.
              </p>
               <div className="flex flex-wrap gap-2 mb-4">
                  <span className="text-xs text-gray-500 bg-gray-800 px-2 py-0.5 rounded">Security</span>
                  <span className="text-xs text-gray-500 bg-gray-800 px-2 py-0.5 rounded">Core</span>
              </div>
               <button className="w-full py-2 border border-gray-700 hover:bg-gray-800 text-gray-300 rounded text-sm transition-colors">
                  Install
              </button>
          </div>

          {/* Plugin Card 3 */}
          <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl group hover:border-purple-500/50 transition-all">
              <div className="mb-4 flex items-center justify-between">
                  <div className="w-12 h-12 bg-yellow-900/30 rounded-lg flex items-center justify-center text-yellow-400 group-hover:bg-yellow-900/50 transition-colors">
                      <Zap size={24} />
                  </div>
                   <span className="text-xs font-mono text-gray-500 border border-gray-700 px-2 py-1 rounded">v2.0</span>
              </div>
              <h3 className="text-lg font-bold text-white mb-2">High-Frequency Mock</h3>
              <p className="text-gray-400 text-sm mb-4">
                  Generates nanosecond-level mock tick data for stress testing HFT algorithms.
              </p>
               <div className="flex flex-wrap gap-2 mb-4">
                  <span className="text-xs text-gray-500 bg-gray-800 px-2 py-0.5 rounded">Simulation</span>
              </div>
               <button className="w-full py-2 border border-gray-700 hover:bg-gray-800 text-gray-300 rounded text-sm transition-colors">
                  Install
              </button>
          </div>

          {/* Plugin Card 4 */}
          <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl group hover:border-purple-500/50 transition-all">
              <div className="mb-4 flex items-center justify-between">
                  <div className="w-12 h-12 bg-green-900/30 rounded-lg flex items-center justify-center text-green-400 group-hover:bg-green-900/50 transition-colors">
                      <Cpu size={24} />
                  </div>
                   <span className="text-xs font-mono text-gray-500 border border-gray-700 px-2 py-1 rounded">v1.0</span>
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Edge Learning Agent</h3>
              <p className="text-gray-400 text-sm mb-4">
                  Deploy lightweight inference models to edge devices (Raspberry Pi/Jetson) for local news filtering.
              </p>
               <div className="flex flex-wrap gap-2 mb-4">
                  <span className="text-xs text-gray-500 bg-gray-800 px-2 py-0.5 rounded">IoT</span>
                  <span className="text-xs text-gray-500 bg-gray-800 px-2 py-0.5 rounded">Inference</span>
              </div>
               <button className="w-full py-2 border border-gray-700 hover:bg-gray-800 text-gray-300 rounded text-sm transition-colors">
                  Install
              </button>
          </div>

           {/* Plugin Card 5 */}
          <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl group hover:border-purple-500/50 transition-all">
              <div className="mb-4 flex items-center justify-between">
                  <div className="w-12 h-12 bg-red-900/30 rounded-lg flex items-center justify-center text-red-400 group-hover:bg-red-900/50 transition-colors">
                      <GitMerge size={24} />
                  </div>
                   <span className="text-xs font-mono text-gray-500 border border-gray-700 px-2 py-1 rounded">v1.5</span>
              </div>
              <h3 className="text-lg font-bold text-white mb-2">CrowdCluster</h3>
              <p className="text-gray-400 text-sm mb-4">
                  Consensus mechanism for validating synthetic news events via crowdsourced voting.
              </p>
               <div className="flex flex-wrap gap-2 mb-4">
                  <span className="text-xs text-gray-500 bg-gray-800 px-2 py-0.5 rounded">Consensus</span>
              </div>
               <button className="w-full py-2 border border-gray-700 hover:bg-gray-800 text-gray-300 rounded text-sm transition-colors">
                  Install
              </button>
          </div>

           {/* Add New Plugin */}
           <div className="border border-gray-800 border-dashed p-6 rounded-xl flex flex-col items-center justify-center text-gray-500 hover:text-gray-300 hover:border-gray-600 transition-colors cursor-pointer">
              <Puzzle size={48} className="mb-4 opacity-50" />
              <h3 className="font-bold text-lg">Submit a Plugin</h3>
              <p className="text-xs text-center mt-2 max-w-[200px]">Have a module to share? Contribute to the Nexus ecosystem.</p>
           </div>
      </div>
    </div>
  );
};

export default Plugins;
