import React, { useState, useEffect } from 'react';
import { Puzzle, CheckCircle, XCircle, Power } from 'lucide-react';

interface Plugin {
    name: string;
    description: string;
    enabled: boolean;
}

const Plugins: React.FC = () => {
    const [plugins, setPlugins] = useState<Plugin[]>([]);

    useEffect(() => {
        fetch('/api/plugins')
            .then(res => res.json())
            .then(data => setPlugins(data))
            .catch(() => {
                 // Mock fallback
                 setPlugins([
                     { name: 'market_volatility_monitor', description: 'Monitors market events for volatility spikes.', enabled: true },
                     { name: 'sentiment_analyzer_pro', description: 'Advanced sentiment analysis using GPT-4.', enabled: false },
                 ]);
            });
    }, []);

    const togglePlugin = async (name: string, enabled: boolean) => {
        try {
            const res = await fetch('/api/plugins/toggle', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, enabled })
            });
            const data = await res.json();
            if (data.success) {
                setPlugins(data.plugins);
            }
        } catch (e) {
            console.error(e);
        }
    };

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-white mb-2">Plugin Manager</h1>
                <p className="text-gray-400">Extend functionality with dynamic modules.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {plugins.map((plugin) => (
                    <div key={plugin.name} className={`bg-gray-900 border ${plugin.enabled ? 'border-green-500/50' : 'border-gray-800'} p-6 rounded-xl transition-all`}>
                        <div className="flex justify-between items-start mb-4">
                            <div className="p-3 bg-gray-800 rounded-lg text-gray-400">
                                <Puzzle size={24} />
                            </div>
                            <button
                                onClick={() => togglePlugin(plugin.name, !plugin.enabled)}
                                className={`p-2 rounded-full transition-colors ${plugin.enabled ? 'bg-green-500/20 text-green-500 hover:bg-green-500/30' : 'bg-gray-800 text-gray-500 hover:text-white'}`}
                            >
                                <Power size={20} />
                            </button>
                        </div>
                        <h3 className="text-xl font-bold text-white mb-2 truncate" title={plugin.name}>{plugin.name}</h3>
                        <p className="text-sm text-gray-400 mb-4 h-10 overflow-hidden">{plugin.description}</p>

                        <div className="flex items-center space-x-2 text-sm">
                            {plugin.enabled ? (
                                <span className="flex items-center text-green-400"><CheckCircle size={14} className="mr-1"/> Active</span>
                            ) : (
                                <span className="flex items-center text-gray-500"><XCircle size={14} className="mr-1"/> Disabled</span>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Plugins;
