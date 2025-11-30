import React from 'react';
import MatrixView from '../components/MatrixView';
import ImpactGraph from '../components/ImpactGraph';
import ScenarioSimulator from '../components/ScenarioSimulator';

const Dashboard: React.FC = () => {
  return (
    <div className="space-y-6">
      <header className="mb-6 border-b border-gray-800 pb-4">
        <h1 className="text-3xl font-bold text-green-500 tracking-tighter">
          OPERATIONAL DASHBOARD <span className="text-xs text-gray-500 font-normal">[Live Feed]</span>
        </h1>
      </header>

      <main className="grid grid-cols-1 lg:grid-cols-2 gap-6">

        {/* Left Column: Intelligence Feed */}
        <section className="space-y-6">
          <MatrixView />
          <ScenarioSimulator />
        </section>

        {/* Right Column: Visualization */}
        <section className="space-y-6">
           <ImpactGraph />

           <div className="bg-gray-900 border border-gray-700 p-4 rounded h-64 overflow-auto font-mono text-sm text-green-300">
               <h3 className="text-white font-bold mb-2 border-b border-gray-700 pb-1">Agent Monologue</h3>
               <p>[SYSTEM] Initializing Cognitive Core...</p>
               <p>[SYSTEM] Connected to Synthetic Data Stream.</p>
               <p>[AGENT] Analyzing correlation between Oil Prices and Transport Sector...</p>
               <p>[AGENT] &gt; Detected anomaly in ticker TSLA.</p>
               <p>[AGENT] &gt; Cross-referencing with news source ID 42.</p>
               <p>[AGENT] &gt; Confidence Score: 0.87. Flagging as Signal.</p>
           </div>
        </section>

      </main>
    </div>
  );
};

export default Dashboard;
