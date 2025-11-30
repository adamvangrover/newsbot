import React, { useState, useEffect } from 'react';
import { Activity, Cpu, Server, AlertCircle, CheckCircle } from 'lucide-react';

const SystemStatus: React.FC = () => {
    const [stats, setStats] = useState({
        articlesProcessed: 12450,
        agentsActive: 5,
        marketUptime: '99.9%'
    });

    useEffect(() => {
        const interval = setInterval(() => {
            setStats(prev => ({
                ...prev,
                articlesProcessed: prev.articlesProcessed + Math.floor(Math.random() * 5)
            }));
        }, 1000);
        return () => clearInterval(interval);
    }, []);

    const agents = [
        { name: 'MarketDataAgent', status: 'Active', load: 85, type: 'Ingestion' },
        { name: 'SentimentAnalyzer', status: 'Active', load: 60, type: 'Processing' },
        { name: 'EarningsParser', status: 'Idle', load: 10, type: 'Ingestion' },
        { name: 'RiskAssessor', status: 'Active', load: 45, type: 'Analysis' },
        { name: 'ClusterEngine', status: 'Processing', load: 92, type: 'Core' },
    ];

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-white mb-2">System Status</h1>
                <p className="text-gray-400">Real-time monitoring of NewsBot Nexus infrastructure.</p>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl flex items-center space-x-4">
                    <div className="p-3 bg-blue-900/20 rounded-lg text-blue-500">
                        <Server size={24} />
                    </div>
                    <div>
                        <p className="text-sm text-gray-500">Articles Processed</p>
                        <p className="text-2xl font-bold text-white">{stats.articlesProcessed.toLocaleString()}</p>
                    </div>
                </div>

                <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl flex items-center space-x-4">
                    <div className="p-3 bg-orange-900/20 rounded-lg text-orange-500">
                        <Cpu size={24} />
                    </div>
                    <div>
                        <p className="text-sm text-gray-500">Active Agents</p>
                        <p className="text-2xl font-bold text-white">{stats.agentsActive}</p>
                    </div>
                </div>

                <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl flex items-center space-x-4">
                    <div className="p-3 bg-green-900/20 rounded-lg text-green-500">
                        <Activity size={24} />
                    </div>
                    <div>
                        <p className="text-sm text-gray-500">System Uptime</p>
                        <p className="text-2xl font-bold text-white">{stats.marketUptime}</p>
                    </div>
                </div>
            </div>

            {/* Agent Table */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
                <div className="px-6 py-4 border-b border-gray-800">
                    <h3 className="text-lg font-semibold text-white">Active Agents</h3>
                </div>
                <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm text-gray-400">
                        <thead className="bg-gray-950 text-gray-200 uppercase font-medium">
                            <tr>
                                <th className="px-6 py-3">Agent Name</th>
                                <th className="px-6 py-3">Type</th>
                                <th className="px-6 py-3">Status</th>
                                <th className="px-6 py-3">Load</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-800">
                            {agents.map((agent) => (
                                <tr key={agent.name} className="hover:bg-gray-800/50">
                                    <td className="px-6 py-4 font-medium text-white">{agent.name}</td>
                                    <td className="px-6 py-4">{agent.type}</td>
                                    <td className="px-6 py-4">
                                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${
                                            agent.status === 'Active' ? 'bg-green-900/20 text-green-400 border-green-900' :
                                            agent.status === 'Processing' ? 'bg-blue-900/20 text-blue-400 border-blue-900' :
                                            'bg-gray-800 text-gray-400 border-gray-700'
                                        }`}>
                                            {agent.status === 'Active' && <CheckCircle className="w-3 h-3 mr-1" />}
                                            {agent.status === 'Processing' && <Activity className="w-3 h-3 mr-1" />}
                                            {agent.status === 'Idle' && <AlertCircle className="w-3 h-3 mr-1" />}
                                            {agent.status}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="flex items-center space-x-2">
                                            <div className="w-full bg-gray-700 rounded-full h-2 max-w-[100px]">
                                                <div
                                                    className={`h-2 rounded-full ${agent.load > 90 ? 'bg-red-500' : agent.load > 60 ? 'bg-yellow-500' : 'bg-green-500'}`}
                                                    style={{ width: `${agent.load}%` }}
                                                ></div>
                                            </div>
                                            <span className="text-xs">{agent.load}%</span>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default SystemStatus;
