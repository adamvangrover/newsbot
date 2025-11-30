import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Activity, Database, Brain } from 'lucide-react';

const Home: React.FC = () => {
  return (
    <div className="max-w-6xl mx-auto space-y-12">
      {/* Hero Section */}
      <section className="text-center space-y-6 py-16">
        <div className="inline-block px-4 py-1.5 rounded-full bg-green-900/30 border border-green-800 text-green-400 text-sm font-medium mb-4">
          NewsBot Nexus v2.0 Now Available
        </div>
        <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white">
          Synthetic Reality <span className="text-green-500">Engine</span>
        </h1>
        <p className="text-xl text-gray-400 max-w-2xl mx-auto">
          An advanced platform for generating synthetic financial market data, simulating complex geopolitical events, and training federated learning models.
        </p>
        <div className="flex justify-center gap-4 pt-4">
          <Link to="/dashboard" className="px-8 py-3 bg-green-600 hover:bg-green-700 text-black font-bold rounded-lg flex items-center transition-colors">
            Launch Dashboard <ArrowRight className="ml-2 h-5 w-5" />
          </Link>
          <Link to="/about" className="px-8 py-3 bg-gray-800 hover:bg-gray-700 text-white font-medium rounded-lg border border-gray-700 transition-colors">
            Learn More
          </Link>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="grid md:grid-cols-3 gap-8">
        <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl hover:border-green-900/50 transition-colors">
          <div className="w-12 h-12 bg-blue-900/30 rounded-lg flex items-center justify-center mb-4 text-blue-400">
            <Activity className="h-6 w-6" />
          </div>
          <h3 className="text-xl font-bold text-white mb-2">Market Simulation</h3>
          <p className="text-gray-400">
            Real-time simulation of stock prices, corporate actions, and market anomalies driven by synthetic news events.
          </p>
        </div>

        <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl hover:border-green-900/50 transition-colors">
          <div className="w-12 h-12 bg-purple-900/30 rounded-lg flex items-center justify-center mb-4 text-purple-400">
            <Brain className="h-6 w-6" />
          </div>
          <h3 className="text-xl font-bold text-white mb-2">Federated Learning</h3>
          <p className="text-gray-400">
            Train Small Language Models (SLMs) on decentralized synthetic data nodes without compromising privacy.
          </p>
        </div>

        <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl hover:border-green-900/50 transition-colors">
          <div className="w-12 h-12 bg-green-900/30 rounded-lg flex items-center justify-center mb-4 text-green-400">
            <Database className="h-6 w-6" />
          </div>
          <h3 className="text-xl font-bold text-white mb-2">Synthetic Data</h3>
          <p className="text-gray-400">
            Generate massive datasets of financial news, SEC filings, and geopolitical events for model training.
          </p>
        </div>
      </section>

      {/* Code Snippet Showcase */}
      <section className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
         <div className="bg-gray-950 px-4 py-2 border-b border-gray-800 flex items-center">
            <div className="flex space-x-2 mr-4">
                <div className="w-3 h-3 rounded-full bg-red-500"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
            </div>
            <span className="text-xs text-gray-500 font-mono">synthetic_generator.py</span>
         </div>
         <div className="p-6 overflow-x-auto">
             <pre className="font-mono text-sm text-gray-300">
{`class SyntheticDataEngine:
    def generate_event_chain(self, root_event: PoliticalEvent):
        """Simulate complex causal chains in market data."""
        impact_score = self.impact_analyzer.assess(root_event)

        if impact_score > 0.8:
            affected_sectors = self.knowledge_graph.query(
                root_event.affected_sectors
            )
            return self.propagate_shock(affected_sectors)

        return None`}
             </pre>
         </div>
      </section>
    </div>
  );
};

export default Home;
