import React, { useState, useEffect } from 'react';
import { Bot, Play, Square, Activity, Cpu } from 'lucide-react';

interface Agent {
    name: string;
    role: string;
    status: string;
    memory_size: number;
}

interface EvolutionStatus {
    generation: number;
    best_scenario: string;
    fitness: number;
    status?: string;
}

const AgentsOrchestrator: React.FC = () => {
    const [agents, setAgents] = useState<Agent[]>([]);
    const [evolution, setEvolution] = useState<EvolutionStatus | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const agentsRes = await fetch('/api/cognitive/agents');
                if (agentsRes.ok) {
                    const agentsData = await agentsRes.json();
                    setAgents(agentsData);
                }

                const evoRes = await fetch('/api/cognitive/evolution');
                if (evoRes.ok) {
                    const evoData = await evoRes.json();
                    setEvolution(evoData);
                }
            } catch (error) {
                console.error("Failed to fetch cognitive data", error);
            }
        };

        fetchData();
        const interval = setInterval(fetchData, 3000); // Poll every 3 seconds
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-white mb-2">Cognitive Agents Orchestrator</h1>
                <p className="text-gray-400">Manage autonomous cognitive agents and evolutionary simulations.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <div className="bg-gray-900 border border-gray-800 p-4 rounded-xl">
                    <div className="text-gray-500 text-xs uppercase font-bold tracking-wider mb-1">Active Agents</div>
                    <div className="text-2xl font-bold text-white flex items-center">
                        {agents.filter(a => a.status === 'Running').length} <span className="text-sm text-gray-500 font-normal ml-2">/ {agents.length}</span>
                    </div>
                </div>
                 <div className="bg-gray-900 border border-gray-800 p-4 rounded-xl">
                    <div className="text-gray-500 text-xs uppercase font-bold tracking-wider mb-1">Evolution Generation</div>
                    <div className="text-2xl font-bold text-purple-400">
                        {evolution?.generation || 0}
                    </div>
                </div>
            </div>

            {/* Evolution Insight */}
            {evolution && evolution.best_scenario && (
                 <div className="bg-gray-900 border border-purple-900/50 p-6 rounded-xl relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-4 opacity-10">
                        <Cpu size={100} className="text-purple-500" />
                    </div>
                    <h3 className="text-lg font-bold text-white mb-2 flex items-center">
                        <Cpu className="mr-2 text-purple-500" size={20} />
                        Evolutionary Insight (Fitness: {evolution.fitness.toFixed(1)})
                    </h3>
                    <p className="text-gray-300 font-mono text-sm border-l-2 border-purple-500 pl-4 py-2 bg-black/30 rounded">
                        {evolution.best_scenario}
                    </p>
                 </div>
            )}

            <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
                <table className="w-full text-left text-sm text-gray-400">
                    <thead className="bg-gray-950 text-gray-200 uppercase font-medium">
                        <tr>
                            <th className="px-6 py-4">Agent Name</th>
                            <th className="px-6 py-4">Role</th>
                            <th className="px-6 py-4">Status</th>
                            <th className="px-6 py-4">Memory Items</th>
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
                                <td className="px-6 py-4 font-mono">{agent.memory_size}</td>
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
