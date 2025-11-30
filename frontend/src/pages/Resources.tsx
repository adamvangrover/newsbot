import React from 'react';
import { Database, Server, Cloud, Shield, Share2, Box } from 'lucide-react';

const Resources: React.FC = () => {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Communal Resources</h1>
        <p className="text-gray-400">Shared datasets, APIs, and infrastructure for the NewsBot community.</p>
      </div>

      {/* Hosted Offerings */}
      <section>
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <Cloud className="mr-3 text-blue-500" /> Hosted Offerings
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
              <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl hover:border-blue-500/50 transition-colors">
                  <div className="flex items-center justify-between mb-4">
                      <div className="p-2 bg-blue-900/20 rounded text-blue-400"><Server size={24} /></div>
                      <span className="text-xs bg-green-900/50 text-green-400 px-2 py-1 rounded">Active</span>
                  </div>
                  <h3 className="text-xl font-bold text-white mb-2">Nexus Node (Alpha)</h3>
                  <p className="text-gray-400 text-sm mb-4">
                      Managed node for federated learning participation. Pre-configured with NewsBot SLM v2 weights.
                  </p>
                  <button className="w-full py-2 bg-gray-800 hover:bg-gray-700 text-white rounded text-sm transition-colors">
                      Deploy Instance
                  </button>
              </div>

              <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl hover:border-blue-500/50 transition-colors">
                  <div className="flex items-center justify-between mb-4">
                      <div className="p-2 bg-purple-900/20 rounded text-purple-400"><Database size={24} /></div>
                      <span className="text-xs bg-gray-800 text-gray-400 px-2 py-1 rounded">Beta</span>
                  </div>
                  <h3 className="text-xl font-bold text-white mb-2">Synthetic Lake</h3>
                  <p className="text-gray-400 text-sm mb-4">
                      Petabyte-scale storage of generated financial histories. SQL and Parquet access available.
                  </p>
                  <button className="w-full py-2 bg-gray-800 hover:bg-gray-700 text-white rounded text-sm transition-colors">
                      Request Access
                  </button>
              </div>

              <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl hover:border-blue-500/50 transition-colors">
                  <div className="flex items-center justify-between mb-4">
                      <div className="p-2 bg-orange-900/20 rounded text-orange-400"><Shield size={24} /></div>
                      <span className="text-xs bg-green-900/50 text-green-400 px-2 py-1 rounded">Stable</span>
                  </div>
                  <h3 className="text-xl font-bold text-white mb-2">Privacy Enclave</h3>
                  <p className="text-gray-400 text-sm mb-4">
                      Secure compute environment for model validation against proprietary banking datasets.
                  </p>
                  <button className="w-full py-2 bg-gray-800 hover:bg-gray-700 text-white rounded text-sm transition-colors">
                      View Specs
                  </button>
              </div>
          </div>
      </section>

      {/* Libraries & APIs */}
      <section>
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <Box className="mr-3 text-green-500" /> Libraries & SDKs
          </h2>
          <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
              <div className="overflow-x-auto">
                  <table className="w-full text-left">
                      <thead className="bg-gray-950 text-gray-400 uppercase text-xs font-semibold">
                          <tr>
                              <th className="px-6 py-4">Package Name</th>
                              <th className="px-6 py-4">Language</th>
                              <th className="px-6 py-4">Description</th>
                              <th className="px-6 py-4">Version</th>
                              <th className="px-6 py-4"></th>
                          </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-800">
                          <tr className="hover:bg-gray-800/30 transition-colors">
                              <td className="px-6 py-4 font-mono text-white">newsbot-core</td>
                              <td className="px-6 py-4 text-gray-400">Python</td>
                              <td className="px-6 py-4 text-gray-300">Core logic for event simulation and impact analysis.</td>
                              <td className="px-6 py-4 text-gray-500">2.1.0</td>
                              <td className="px-6 py-4 text-right"><a href="#" className="text-green-500 hover:underline">Docs</a></td>
                          </tr>
                          <tr className="hover:bg-gray-800/30 transition-colors">
                              <td className="px-6 py-4 font-mono text-white">newsbot-client-ts</td>
                              <td className="px-6 py-4 text-gray-400">TypeScript</td>
                              <td className="px-6 py-4 text-gray-300">React hooks and utilities for streaming dashboard data.</td>
                              <td className="px-6 py-4 text-gray-500">1.0.4</td>
                              <td className="px-6 py-4 text-right"><a href="#" className="text-green-500 hover:underline">Docs</a></td>
                          </tr>
                          <tr className="hover:bg-gray-800/30 transition-colors">
                              <td className="px-6 py-4 font-mono text-white">federated-torch</td>
                              <td className="px-6 py-4 text-gray-400">Python</td>
                              <td className="px-6 py-4 text-gray-300">PyTorch extensions for secure aggregation.</td>
                              <td className="px-6 py-4 text-gray-500">0.9.2</td>
                              <td className="px-6 py-4 text-right"><a href="#" className="text-green-500 hover:underline">Docs</a></td>
                          </tr>
                      </tbody>
                  </table>
              </div>
          </div>
      </section>

      {/* Community Feeds */}
      <section>
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <Share2 className="mr-3 text-pink-500" /> Community News Feeds
          </h2>
          <div className="grid md:grid-cols-2 gap-6">
              <div className="p-6 bg-gradient-to-br from-gray-900 to-gray-800 rounded-xl border border-gray-700">
                  <h3 className="font-bold text-white text-lg mb-2">CryptoSentiment Stream</h3>
                  <p className="text-gray-400 text-sm mb-4">
                      Aggregated sentiment scores from 50+ crypto news outlets and influencers. Updated every 500ms.
                  </p>
                  <div className="flex items-center space-x-2 text-xs font-mono text-gray-500">
                      <span>Endpoint:</span>
                      <span className="bg-black/30 px-2 py-1 rounded text-gray-300">wss://api.newsbot.ai/feeds/crypto-sent</span>
                  </div>
              </div>
              <div className="p-6 bg-gradient-to-br from-gray-900 to-gray-800 rounded-xl border border-gray-700">
                   <h3 className="font-bold text-white text-lg mb-2">Global Macro Events</h3>
                  <p className="text-gray-400 text-sm mb-4">
                      Verified geopolitical events with impact scores pre-calculated by the Nexus consensus engine.
                  </p>
                  <div className="flex items-center space-x-2 text-xs font-mono text-gray-500">
                      <span>Endpoint:</span>
                      <span className="bg-black/30 px-2 py-1 rounded text-gray-300">https://api.newsbot.ai/v1/macro/events</span>
                  </div>
              </div>
          </div>
      </section>

    </div>
  );
};

export default Resources;
