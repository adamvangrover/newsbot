import React, { useState } from 'react';
import { GitBranch, Calendar, TrendingUp, AlertTriangle, ArrowRight } from 'lucide-react';

const FutureProjections: React.FC = () => {
    const [scenarios] = useState([
        { id: 1, date: 'T+1 Month', outcome: 'Market Correction', probability: 0.65, type: 'Negative', drivers: ['Rate Hike', 'Tech Selloff'] },
        { id: 2, date: 'T+3 Months', outcome: 'Tech Sector Recovery', probability: 0.45, type: 'Positive', drivers: ['Earnings Beat', 'AI Adoption'] },
        { id: 3, date: 'T+6 Months', outcome: 'Inflation Stabilization', probability: 0.30, type: 'Neutral', drivers: ['Fed Pivot'] },
    ]);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white mb-2">Evolutionary Projections</h1>
                    <p className="text-gray-400">Probabilistic future scenarios based on current market dynamics.</p>
                </div>
                <button className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center transition-colors">
                    <GitBranch className="mr-2 h-4 w-4" /> Run Simulation
                </button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {scenarios.map((s) => (
                    <div key={s.id} className="bg-gray-900 border border-gray-800 p-6 rounded-xl relative overflow-hidden group hover:border-green-500/50 transition-all cursor-pointer">
                        <div className={`absolute top-0 left-0 w-1 h-full ${s.type === 'Negative' ? 'bg-red-500' : s.type === 'Positive' ? 'bg-green-500' : 'bg-blue-500'}`}></div>
                        <div className="flex justify-between items-start mb-4">
                            <div className="bg-gray-800 p-2 rounded-lg text-gray-400 group-hover:text-white transition-colors">
                                <Calendar size={20} />
                            </div>
                            <span className="text-xs font-mono text-gray-500">{s.date}</span>
                        </div>
                        <h3 className="text-xl font-bold text-white mb-2">{s.outcome}</h3>
                        <div className="flex items-center space-x-2 text-sm text-gray-400 mb-4">
                            {s.type === 'Negative' ? <AlertTriangle size={16} className="text-red-500" /> : <TrendingUp size={16} className="text-green-500" />}
                            <span>Probability: {(s.probability * 100).toFixed(0)}%</span>
                        </div>

                        <div className="mb-4">
                            <p className="text-xs text-gray-500 mb-1">Key Drivers:</p>
                            <div className="flex flex-wrap gap-2">
                                {s.drivers.map(d => (
                                    <span key={d} className="text-xs bg-gray-800 px-2 py-1 rounded text-gray-300">{d}</span>
                                ))}
                            </div>
                        </div>

                        <div className="w-full bg-gray-800 h-1.5 rounded-full overflow-hidden">
                            <div className={`h-full ${s.type === 'Negative' ? 'bg-red-500' : s.type === 'Positive' ? 'bg-green-500' : 'bg-blue-500'}`} style={{ width: `${s.probability * 100}%` }}></div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Timeline View Simulation */}
            <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl">
                <h3 className="text-lg font-semibold text-white mb-4">Timeline Evolution</h3>
                <div className="relative border-l-2 border-gray-800 ml-3 space-y-8 pl-8 py-2">
                    {scenarios.map((s, idx) => (
                        <div key={idx} className="relative">
                            <div className="absolute -left-[41px] bg-gray-900 border-2 border-gray-700 w-6 h-6 rounded-full flex items-center justify-center">
                                <div className={`w-2 h-2 rounded-full ${s.type === 'Negative' ? 'bg-red-500' : s.type === 'Positive' ? 'bg-green-500' : 'bg-blue-500'}`}></div>
                            </div>
                            <h4 className="text-white font-medium">{s.date}</h4>
                            <p className="text-gray-400 text-sm">{s.outcome}</p>
                        </div>
                    ))}
                    <div className="relative">
                         <div className="absolute -left-[41px] bg-gray-800 w-6 h-6 rounded-full flex items-center justify-center text-gray-500">
                             <ArrowRight size={12} />
                         </div>
                         <p className="text-gray-500 italic text-sm">Forecasting horizon limit reached.</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default FutureProjections;
