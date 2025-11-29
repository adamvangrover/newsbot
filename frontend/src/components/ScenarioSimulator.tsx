import React, { useState } from 'react';

const ScenarioSimulator: React.FC = () => {
    const [scenario, setScenario] = useState("Global Chip Shortage");
    const [results, setResults] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);

    const runSimulation = async () => {
        setLoading(true);
        // Simulate API call delay
        setTimeout(() => {
            const mockResults = [
                { ticker: "NVDA", impact: "+5.2%", reason: "Increased demand for available chips." },
                { ticker: "TSLA", impact: "-3.1%", reason: "Supply chain delays for ECU." },
                { ticker: "AAPL", impact: "-1.5%", reason: "Potential iPhone shipment delays." },
                { ticker: "INTC", impact: "+2.0%", reason: "Domestic production focus." },
            ];
            setResults(mockResults);
            setLoading(false);
        }, 1500);
    };

    return (
        <div className="bg-gray-800 text-white p-4 rounded border border-gray-600">
            <h2 className="text-xl font-bold mb-4">Scenario Simulator</h2>
            <div className="flex gap-4 mb-4">
                <select
                    value={scenario}
                    onChange={(e) => setScenario(e.target.value)}
                    className="bg-gray-700 p-2 rounded text-white flex-1"
                >
                    <option>Global Chip Shortage</option>
                    <option>Oil Price Spike ($100)</option>
                    <option>Housing Market Crash</option>
                    <option>Tech Sector Regulation</option>
                </select>
                <button
                    onClick={runSimulation}
                    disabled={loading}
                    className="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded font-bold"
                >
                    {loading ? "Simulating..." : "Run Simulation"}
                </button>
            </div>

            {results.length > 0 && (
                <div className="space-y-2">
                    <h3 className="font-semibold text-gray-400">Projected Market Impact:</h3>
                    {results.map((res, idx) => (
                        <div key={idx} className="flex justify-between bg-gray-700 p-2 rounded">
                            <span className="font-bold w-16">{res.ticker}</span>
                            <span className={res.impact.startsWith('+') ? "text-green-400 w-16" : "text-red-400 w-16"}>
                                {res.impact}
                            </span>
                            <span className="text-gray-300 text-sm flex-1">{res.reason}</span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default ScenarioSimulator;
