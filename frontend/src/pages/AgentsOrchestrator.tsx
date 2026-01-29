import React from 'react';
import { Bot, Play, Square, Activity } from 'lucide-react';

const AgentsOrchestrator: React.FC = () => {
    const agents = [
        { name: 'SentimentAgent', role: 'Sentiment Analysis', status: 'Running', tasks: 124, load: 45 },
        { name: 'RiskAgent', role: 'Risk Assessment', status: 'Idle', tasks: 45, load: 0 },
        { name: 'EvolutionaryAgent', role: 'Scenario Generation', status: 'Running', tasks: 12, load: 78 },
        { name: 'NewsIngester', role: 'Data Ingestion', status: 'Running', tasks: 8902, load: 32 },
    ];

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-white mb-2">Agent Orchestrator</h1>
                <p className="text-gray-400">Manage and monitor autonomous async agents.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <div className="bg-gray-900 border border-gray-800 p-4 rounded-xl">
                    <div className="text-gray-500 text-xs uppercase font-bold tracking-wider mb-1">Active Agents</div>
                    <div className="text-2xl font-bold text-white flex items-center">
                        3 <span className="text-sm text-gray-500 font-normal ml-2">/ 4</span>
                    </div>
                </div>
                <div className="bg-gray-900 border border-gray-800 p-4 rounded-xl">
                     <div className="text-gray-500 text-xs uppercase font-bold tracking-wider mb-1">Total Tasks</div>
                    <div className="text-2xl font-bold text-white">9,083</div>
                </div>
            </div>

            <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
                <table className="w-full text-left text-sm text-gray-400">
                    <thead className="bg-gray-950 text-gray-200 uppercase font-medium">
                        <tr>
                            <th className="px-6 py-4">Agent Name</th>
                            <th className="px-6 py-4">Role</th>
                            <th className="px-6 py-4">Status</th>
                            <th className="px-6 py-4">Load</th>
                            <th className="px-6 py-4">Tasks</th>
                            <th className="px-6 py-4 text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-800">
                        {agents.map((agent) => (
                            <tr key={agent.name} className="hover:bg-gray-800/50">
                                <td className="px-6 py-4 flex items-center space-x-3 text-white font-medium">
                                    <div className="bg-blue-900/30 p-2 rounded text-blue-400">
                                        <Bot size={18} />
                                    </div>
                                    <span>{agent.name}</span>
                                </td>
                                <td className="px-6 py-4">{agent.role}</td>
                                <td className="px-6 py-4">
                                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${
                                        agent.status === 'Running' ? 'bg-green-900/20 text-green-400 border-green-900' : 'bg-gray-800 text-gray-400 border-gray-700'
                                    }`}>
                                        <Activity className="w-3 h-3 mr-1" />
                                        {agent.status}
                                    </span>
                                </td>
                                <td className="px-6 py-4 w-32">
                                    <div className="flex items-center space-x-2">
                                        <div className="w-full bg-gray-700 rounded-full h-1.5">
                                            <div className="bg-blue-500 h-1.5 rounded-full" style={{ width: `${agent.load}%`}}></div>
                                        </div>
                                        <span className="text-xs">{agent.load}%</span>
                                    </div>
                                </td>
                                <td className="px-6 py-4 font-mono">{agent.tasks}</td>
                                <td className="px-6 py-4 flex justify-end space-x-2">
                                    <button className="p-2 hover:bg-green-900/30 text-green-400 rounded transition-colors" title="Start Agent"><Play size={16} /></button>
                                    <button className="p-2 hover:bg-red-900/30 text-red-400 rounded transition-colors" title="Stop Agent"><Square size={16} /></button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default AgentsOrchestrator;
