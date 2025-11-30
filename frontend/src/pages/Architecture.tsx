import React from 'react';
import { Layers, Database, Code, Globe } from 'lucide-react';

const Architecture: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-12">
      <div className="border-b border-gray-800 pb-8">
        <h1 className="text-4xl font-bold text-white mb-4">System Architecture</h1>
        <p className="text-xl text-gray-400">
          NewsBot Nexus is designed as a modular, event-driven platform utilizing Hexagonal Architecture to ensure separation of concerns and scalability.
        </p>
      </div>

      <div className="space-y-8">

        {/* Core Components */}
        <section>
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
            <Layers className="mr-3 text-green-500" /> Core Components
          </h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-gray-900 border border-gray-800 p-6 rounded-lg">
              <h3 className="text-lg font-bold text-white mb-2">FastAPI Backend</h3>
              <p className="text-gray-400 text-sm">
                High-performance Python backend serving REST endpoints. Handles request validation via Pydantic V2 and orchestrates the agentic workflow.
              </p>
            </div>
            <div className="bg-gray-900 border border-gray-800 p-6 rounded-lg">
              <h3 className="text-lg font-bold text-white mb-2">React Frontend</h3>
              <p className="text-gray-400 text-sm">
                Modern SPA built with Vite and Tailwind CSS. Visualizes complex graph data using <code>react-force-graph</code> and real-time metrics with <code>recharts</code>.
              </p>
            </div>
             <div className="bg-gray-900 border border-gray-800 p-6 rounded-lg">
              <h3 className="text-lg font-bold text-white mb-2">Synthetic Engine</h3>
              <p className="text-gray-400 text-sm">
                Generates realistic financial and geopolitical scenarios using causal chains defined in <code>Semantic Narrative Library</code>. Outputs Parquet/JSONL.
              </p>
            </div>
            <div className="bg-gray-900 border border-gray-800 p-6 rounded-lg">
              <h3 className="text-lg font-bold text-white mb-2">Impact Analyzer</h3>
              <p className="text-gray-400 text-sm">
                Reasoning engine that traces the ripple effects of events through the supply chain and competitor graphs.
              </p>
            </div>
          </div>
        </section>

        {/* Data Flow */}
        <section>
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
            <Database className="mr-3 text-blue-500" /> Data Flow
          </h2>
          <div className="bg-gray-900 border border-gray-800 p-8 rounded-lg relative overflow-hidden">
             <div className="absolute top-0 right-0 p-4 opacity-10">
                 <Globe size={120} />
             </div>
             <ul className="space-y-4 relative z-10">
                 <li className="flex items-start">
                     <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-900 text-blue-400 flex items-center justify-center text-xs font-bold mt-0.5">1</span>
                     <div className="ml-4">
                         <h4 className="text-white font-medium">Ingestion / Generation</h4>
                         <p className="text-gray-400 text-sm mt-1">External APIs (Finnhub) or Synthetic Generators create raw event data (News, Prices, Filings).</p>
                     </div>
                 </li>
                 <li className="flex items-start">
                     <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-900 text-blue-400 flex items-center justify-center text-xs font-bold mt-0.5">2</span>
                     <div className="ml-4">
                         <h4 className="text-white font-medium">Processing & Logic</h4>
                         <p className="text-gray-400 text-sm mt-1">Impact Analyzer detects signals using regex heuristics and graph traversal (NetworkX).</p>
                     </div>
                 </li>
                 <li className="flex items-start">
                     <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-900 text-blue-400 flex items-center justify-center text-xs font-bold mt-0.5">3</span>
                     <div className="ml-4">
                         <h4 className="text-white font-medium">Storage & Learning</h4>
                         <p className="text-gray-400 text-sm mt-1">Data is stored in structured formats. Federated Learning nodes update local models based on new insights.</p>
                     </div>
                 </li>
                 <li className="flex items-start">
                     <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-900 text-blue-400 flex items-center justify-center text-xs font-bold mt-0.5">4</span>
                     <div className="ml-4">
                         <h4 className="text-white font-medium">Visualization</h4>
                         <p className="text-gray-400 text-sm mt-1">The Frontend consumes aggregated data to render Impact Graphs and Performance Metrics.</p>
                     </div>
                 </li>
             </ul>
          </div>
        </section>

        {/* Tech Stack */}
         <section>
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
            <Code className="mr-3 text-purple-500" /> Technology Stack
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {['Python 3.10+', 'FastAPI', 'React 19', 'TypeScript', 'Tailwind CSS', 'Pydantic V2', 'Pandas', 'PyTorch'].map((tech) => (
                  <div key={tech} className="bg-gray-800/50 border border-gray-700 p-3 rounded text-center text-gray-300 font-mono text-sm">
                      {tech}
                  </div>
              ))}
          </div>
        </section>

      </div>
    </div>
  );
};

export default Architecture;
