import React, { useState, useEffect } from 'react';
import { Server, Activity, Users, Play, Square } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const FederatedLearning: React.FC = () => {
  const [status, setStatus] = useState('Checking...');
  const [round, setRound] = useState(0);
  const [accuracy, setAccuracy] = useState(0.50);
  const [participants, setParticipants] = useState(0);
  const [data, setData] = useState<{ time: string; accuracy: number }[]>([]);

  useEffect(() => {
    const fetchStatus = async () => {
        try {
            const response = await fetch('/api/federated/status');
            if (response.ok) {
                const res = await response.json();
                setStatus(res.status);
                setRound(res.round);
                setAccuracy(res.accuracy);
                setParticipants(res.participants);

                if (res.status === 'training') {
                    setData(prev => {
                        const newData = [...prev, { time: `R${res.round}`, accuracy: res.accuracy }];
                        return newData.slice(-20); // Keep last 20 points
                    });
                }
            }
        } catch (e) {
            setStatus('Offline (Mock)');
        }
    };

    const interval = setInterval(fetchStatus, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleStart = async () => {
      await fetch('/api/federated/start', { method: 'POST' });
  };

  const handleStop = async () => {
      await fetch('/api/federated/stop', { method: 'POST' });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
           <h1 className="text-3xl font-bold text-white mb-2">Federated Learning</h1>
           <p className="text-gray-400">Decentralized model training simulation.</p>
        </div>
        <div className="flex space-x-3">
             <button onClick={handleStart} disabled={status === 'training'} className="bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white px-4 py-2 rounded-lg flex items-center transition-colors">
                 <Play className="mr-2 h-4 w-4" /> Start Training
             </button>
             <button onClick={handleStop} disabled={status !== 'training'} className="bg-red-600 hover:bg-red-700 disabled:opacity-50 text-white px-4 py-2 rounded-lg flex items-center transition-colors">
                 <Square className="mr-2 h-4 w-4" /> Stop
             </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl flex items-center space-x-4">
              <div className="p-3 bg-purple-900/20 rounded-lg text-purple-500">
                  <Activity size={24} />
              </div>
              <div>
                  <p className="text-sm text-gray-500">Global Accuracy</p>
                  <p className="text-2xl font-bold text-white">{(accuracy * 100).toFixed(2)}%</p>
              </div>
          </div>

          <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl flex items-center space-x-4">
              <div className="p-3 bg-blue-900/20 rounded-lg text-blue-500">
                  <Server size={24} />
              </div>
              <div>
                  <p className="text-sm text-gray-500">Current Round</p>
                  <p className="text-2xl font-bold text-white">#{round}</p>
              </div>
          </div>

          <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl flex items-center space-x-4">
              <div className="p-3 bg-green-900/20 rounded-lg text-green-500">
                  <Users size={24} />
              </div>
              <div>
                  <p className="text-sm text-gray-500">Active Nodes</p>
                  <p className="text-2xl font-bold text-white">{participants}</p>
              </div>
          </div>
      </div>

      <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl h-96">
          <h3 className="text-lg font-semibold text-white mb-6">Model Convergence</h3>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="time" stroke="#9CA3AF" />
              <YAxis domain={[0.4, 1]} stroke="#9CA3AF" />
              <Tooltip
                contentStyle={{ backgroundColor: '#111827', borderColor: '#374151' }}
                itemStyle={{ color: '#D1D5DB' }}
              />
              <Line type="monotone" dataKey="accuracy" stroke="#10B981" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
      </div>
    </div>
  );
};

export default FederatedLearning;
