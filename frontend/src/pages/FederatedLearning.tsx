import React from 'react';
import FederatedLearningVisualizer from '../components/FederatedLearningVisualizer';

const FederatedLearning: React.FC = () => {
    return (
        <div className="space-y-6">
            <h1 className="text-3xl font-bold text-white mb-4">Federated Learning Network</h1>
             <div className="h-[600px] bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
                <FederatedLearningVisualizer />
            </div>
        </div>
    )
}

export default FederatedLearning;
