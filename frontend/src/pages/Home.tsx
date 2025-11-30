import React from 'react';
import { Link } from 'react-router-dom';
import {
  ArrowRight,
  Activity,
  Database,
  Brain,
  Radio,
  Puzzle,
  Layers,
  Server
} from 'lucide-react';

const Home: React.FC = () => {
  return (
    <div className="max-w-6xl mx-auto space-y-16">

      {/* Catalog Header */}
      <section className="text-center space-y-6 pt-12 pb-8">
        <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white">
          NewsBot <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-blue-500">Nexus</span> Catalog
        </h1>
        <p className="text-xl text-gray-400 max-w-3xl mx-auto leading-relaxed">
          A comprehensive suite for <span className="text-white">Synthetic Market Intelligence</span>.
          Explore our ecosystem of signal generators, federated learning nodes, and massive-scale data simulations.
        </p>
        <div className="flex flex-wrap justify-center gap-3 pt-4">
             <span className="px-3 py-1 rounded-full bg-gray-800 border border-gray-700 text-xs text-gray-400">v2.1 Stable</span>
             <span className="px-3 py-1 rounded-full bg-gray-800 border border-gray-700 text-xs text-gray-400">Python 3.10+</span>
             <span className="px-3 py-1 rounded-full bg-gray-800 border border-gray-700 text-xs text-gray-400">PyTorch</span>
             <span className="px-3 py-1 rounded-full bg-gray-800 border border-gray-700 text-xs text-gray-400">React</span>
        </div>
      </section>

      {/* Main Directory Grid */}
      <section className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">

        {/* Module 1: Live Operations */}
        <Link to="/dashboard" className="group relative bg-gray-900 border border-gray-800 rounded-xl overflow-hidden hover:border-green-500/50 transition-all duration-300">
           <div className="absolute top-0 right-0 p-4 opacity-50 group-hover:opacity-100 transition-opacity">
               <ArrowRight className="text-green-500 -rotate-45" />
           </div>
           <div className="p-8 space-y-4">
               <div className="w-12 h-12 bg-green-900/20 rounded-lg flex items-center justify-center text-green-400">
                   <Activity size={24} />
               </div>
               <h2 className="text-2xl font-bold text-white">Live Operations</h2>
               <p className="text-gray-400 text-sm">
                   Real-time dashboard monitoring synthetic market events, system alerts, and impact analysis graphs.
               </p>
               <ul className="text-xs text-gray-500 space-y-1 font-mono pt-2">
                   <li>• Matrix View</li>
                   <li>• Impact Graph</li>
                   <li>• Scenario Simulator</li>
               </ul>
           </div>
        </Link>

        {/* Module 2: Signal Intelligence */}
        <Link to="/signals" className="group relative bg-gray-900 border border-gray-800 rounded-xl overflow-hidden hover:border-blue-500/50 transition-all duration-300">
           <div className="absolute top-0 right-0 p-4 opacity-50 group-hover:opacity-100 transition-opacity">
               <ArrowRight className="text-blue-500 -rotate-45" />
           </div>
           <div className="p-8 space-y-4">
               <div className="w-12 h-12 bg-blue-900/20 rounded-lg flex items-center justify-center text-blue-400">
                   <Radio size={24} />
               </div>
               <h2 className="text-2xl font-bold text-white">Signal Intelligence</h2>
               <p className="text-gray-400 text-sm">
                   Algorithmic detection of market anomalies. View sample reports and the underlying logic for signal generation.
               </p>
                <ul className="text-xs text-gray-500 space-y-1 font-mono pt-2">
                   <li>• Arbitrage Detection</li>
                   <li>• Sentiment Analysis</li>
                   <li>• Automated Reports</li>
               </ul>
           </div>
        </Link>

        {/* Module 3: Synthetic Data */}
        <Link to="/showcase" className="group relative bg-gray-900 border border-gray-800 rounded-xl overflow-hidden hover:border-purple-500/50 transition-all duration-300">
           <div className="absolute top-0 right-0 p-4 opacity-50 group-hover:opacity-100 transition-opacity">
               <ArrowRight className="text-purple-500 -rotate-45" />
           </div>
           <div className="p-8 space-y-4">
               <div className="w-12 h-12 bg-purple-900/20 rounded-lg flex items-center justify-center text-purple-400">
                   <Database size={24} />
               </div>
               <h2 className="text-2xl font-bold text-white">Data Library</h2>
               <p className="text-gray-400 text-sm">
                   Catalog of generated datasets including SEC filings, corporate news, and tick data for model training.
               </p>
                <ul className="text-xs text-gray-500 space-y-1 font-mono pt-2">
                   <li>• JSONL / Parquet</li>
                   <li>• 10M+ Records</li>
                   <li>• Causal Chains</li>
               </ul>
           </div>
        </Link>

        {/* Module 4: Federated Learning */}
        <Link to="/federated" className="group relative bg-gray-900 border border-gray-800 rounded-xl overflow-hidden hover:border-orange-500/50 transition-all duration-300">
           <div className="absolute top-0 right-0 p-4 opacity-50 group-hover:opacity-100 transition-opacity">
               <ArrowRight className="text-orange-500 -rotate-45" />
           </div>
           <div className="p-8 space-y-4">
               <div className="w-12 h-12 bg-orange-900/20 rounded-lg flex items-center justify-center text-orange-400">
                   <Brain size={24} />
               </div>
               <h2 className="text-2xl font-bold text-white">Federated Learning</h2>
               <p className="text-gray-400 text-sm">
                   Decentralized model training architecture. Visualize node aggregation and privacy-preserving updates.
               </p>
                <ul className="text-xs text-gray-500 space-y-1 font-mono pt-2">
                   <li>• SLM Training</li>
                   <li>• Secure Aggregation</li>
                   <li>• Global Model Weights</li>
               </ul>
           </div>
        </Link>

         {/* Module 5: Plugins & Extensions */}
        <Link to="/plugins" className="group relative bg-gray-900 border border-gray-800 rounded-xl overflow-hidden hover:border-pink-500/50 transition-all duration-300">
           <div className="absolute top-0 right-0 p-4 opacity-50 group-hover:opacity-100 transition-opacity">
               <ArrowRight className="text-pink-500 -rotate-45" />
           </div>
           <div className="p-8 space-y-4">
               <div className="w-12 h-12 bg-pink-900/20 rounded-lg flex items-center justify-center text-pink-400">
                   <Puzzle size={24} />
               </div>
               <h2 className="text-2xl font-bold text-white">Plugins & Extras</h2>
               <p className="text-gray-400 text-sm">
                   Community plugins, visualization tools, and extended functionality modules.
               </p>
                <ul className="text-xs text-gray-500 space-y-1 font-mono pt-2">
                   <li>• GeoSpatial Viz</li>
                   <li>• HFT Simulation</li>
                   <li>• Crowd Clustering</li>
               </ul>
           </div>
        </Link>

         {/* Module 6: Resources */}
        <Link to="/resources" className="group relative bg-gray-900 border border-gray-800 rounded-xl overflow-hidden hover:border-teal-500/50 transition-all duration-300">
           <div className="absolute top-0 right-0 p-4 opacity-50 group-hover:opacity-100 transition-opacity">
               <ArrowRight className="text-teal-500 -rotate-45" />
           </div>
           <div className="p-8 space-y-4">
               <div className="w-12 h-12 bg-teal-900/20 rounded-lg flex items-center justify-center text-teal-400">
                   <Server size={24} />
               </div>
               <h2 className="text-2xl font-bold text-white">Resources</h2>
               <p className="text-gray-400 text-sm">
                   Hosted offerings, API documentation, and communal compute resources.
               </p>
                <ul className="text-xs text-gray-500 space-y-1 font-mono pt-2">
                   <li>• Hosted Nodes</li>
                   <li>• Synthetic Lake</li>
                   <li>• Community Feeds</li>
               </ul>
           </div>
        </Link>

      </section>

      {/* Architecture Teaser */}
      <section className="bg-gray-900 border border-gray-800 rounded-xl p-8 flex flex-col md:flex-row items-center justify-between">
          <div className="space-y-4 md:w-2/3">
              <h3 className="text-2xl font-bold text-white flex items-center">
                  <Layers className="mr-3 text-gray-500" /> System Architecture
              </h3>
              <p className="text-gray-400">
                  Understand how the NewsBot Nexus integrates FastApi, React, and PyTorch into a cohesive Hexagonal Architecture.
              </p>
          </div>
          <div className="mt-6 md:mt-0">
              <Link to="/architecture" className="px-6 py-3 bg-gray-800 hover:bg-gray-700 text-white font-medium rounded-lg border border-gray-700 transition-colors">
                  View Diagram
              </Link>
          </div>
      </section>

    </div>
  );
};

export default Home;
