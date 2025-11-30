import React from 'react';
import { Database, FileText, Table } from 'lucide-react';

const Showcase: React.FC = () => {
    // Mock data based on the memory of what the synthetic engine produces
    const datasets = [
        {
            name: "Synthetic Corporate News",
            description: "Generated news articles covering earnings, mergers, and scandals.",
            format: "JSONL",
            records: "50,000+",
            size: "120 MB",
            icon: FileText
        },
        {
            name: "Market Tick Data",
            description: "Simulated price movements for 500+ tickers with anomaly injection.",
            format: "Parquet",
            records: "10M+",
            size: "4.5 GB",
            icon: Table
        },
        {
            name: "SEC Filings (10-K/10-Q)",
            description: "Synthetic financial reports with realistic textual structure.",
            format: "JSON",
            records: "5,000",
            size: "800 MB",
            icon: Database
        }
    ];

    const sampleNews = [
        { id: 1, time: "09:30:01", source: "Reuters (Synth)", headline: "TechSector Inc. reports Q3 earnings miss; stock plummets 5%." },
        { id: 2, time: "09:31:15", source: "Bloomberg (Synth)", headline: "Oil supply shock: Tanker collision in Strait of Hormuz." },
        { id: 3, time: "09:45:00", source: "WSJ (Synth)", headline: "Federal Reserve hints at rate hike in leaked memo." },
        { id: 4, time: "10:15:22", source: "CNBC (Synth)", headline: "MegaCorp announces acquisition of TinyStartup for $2B." },
    ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Synthetic Data Showcase</h1>
        <p className="text-gray-400">Explore the generated datasets used for training and simulation.</p>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
          {datasets.map((dataset) => (
              <div key={dataset.name} className="bg-gray-900 border border-gray-800 p-6 rounded-xl hover:border-green-500/50 transition-colors">
                  <div className="flex items-center space-x-3 mb-4">
                      <div className="p-2 bg-gray-800 rounded text-green-400">
                          <dataset.icon size={24} />
                      </div>
                      <h3 className="font-bold text-white">{dataset.name}</h3>
                  </div>
                  <p className="text-sm text-gray-400 mb-4">{dataset.description}</p>
                  <div className="flex items-center justify-between text-xs text-gray-500 font-mono">
                      <span>{dataset.format}</span>
                      <span>{dataset.records} records</span>
                  </div>
              </div>
          ))}
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-800 flex justify-between items-center">
              <h3 className="text-lg font-semibold text-white">Live Data Stream (Preview)</h3>
              <span className="text-xs text-green-500 animate-pulse">● LIVE</span>
          </div>
          <div className="divide-y divide-gray-800">
              {sampleNews.map((news) => (
                  <div key={news.id} className="p-4 hover:bg-gray-800/50 transition-colors flex flex-col md:flex-row md:items-center space-y-2 md:space-y-0">
                      <span className="text-xs font-mono text-gray-500 w-24">{news.time}</span>
                      <span className="text-xs font-bold text-blue-400 w-32">{news.source}</span>
                      <span className="text-gray-300 text-sm flex-1">{news.headline}</span>
                  </div>
              ))}
          </div>
      </div>
    </div>
  );
};

export default Showcase;
