import React from 'react';

const Performance: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="bg-yellow-900/20 border border-yellow-800 p-4 rounded-lg text-yellow-200">
        <p><strong>Note:</strong> Performance metrics are currently simulated. Connect a live data source to see real-time analytics.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-900 p-6 rounded-lg border border-gray-800">
            <h3 className="text-xl font-bold mb-4">Model Accuracy</h3>
            <div className="h-64 flex items-center justify-center bg-gray-800/50 rounded text-gray-500">
                [Chart Placeholder: Accuracy over Epochs]
            </div>
        </div>
        <div className="bg-gray-900 p-6 rounded-lg border border-gray-800">
            <h3 className="text-xl font-bold mb-4">Latency Distribution</h3>
             <div className="h-64 flex items-center justify-center bg-gray-800/50 rounded text-gray-500">
                [Chart Placeholder: Request Latency Histogram]
            </div>
        </div>
      </div>
    </div>
  );
};

export default Performance;
