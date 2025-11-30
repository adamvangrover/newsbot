import React from 'react';
import { KnowledgeGraph } from '../components/KnowledgeGraph';

const ImpactAnalysis: React.FC = () => {
    return (
        <div className="space-y-6">
             <div>
                <h1 className="text-3xl font-bold text-white mb-2">Impact Analysis</h1>
                <p className="text-gray-400">
                    Visualizing the causal chains of events through the Semantic Knowledge Graph.
                    This graph illustrates how a single event (e.g., Supply Chain Issue) propagates through connected entities.
                </p>
            </div>

             <div className="h-[600px] bg-gray-900 border border-gray-800 rounded-xl overflow-hidden relative">
                 <div className="absolute top-4 left-4 z-10 bg-black/50 p-2 rounded text-xs text-gray-400">
                    Drag nodes to explore connections. Scroll to zoom.
                 </div>
                <KnowledgeGraph />
            </div>
        </div>
    )
}

export default ImpactAnalysis;
