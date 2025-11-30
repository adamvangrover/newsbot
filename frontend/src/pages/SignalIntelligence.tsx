import React from 'react';
import { FileCode, BarChart2 } from 'lucide-react';

const SignalIntelligence: React.FC = () => {
  const reports = [
    {
      id: "RPT-2023-892",
      title: "Supply Chain Disruption: Semiconductor Sector",
      severity: "High",
      timestamp: "2023-10-24 08:45:00",
      status: "Active",
      summary: "Detected correlation between Taiwan localized weather events and TSMC production output forecasts. Predicted 12% dip in sector performance.",
      signals: ["Weather API", "Production Forecast NLP", "Shipping Logistics Data"]
    },
    {
      id: "RPT-2023-893",
      title: "Currency Fluctuation: USD/JPY",
      severity: "Medium",
      timestamp: "2023-10-24 09:15:00",
      status: "Monitoring",
      summary: "BOJ policy meeting minutes sentiment analysis indicates potential yield curve control adjustment. Volatility expected.",
      signals: ["Central Bank Minutes Sentiment", "Forex Order Flow"]
    },
    {
      id: "RPT-2023-894",
      title: "Corporate Action: Merger Rumor",
      severity: "Low",
      timestamp: "2023-10-24 10:30:00",
      status: "Investigating",
      summary: "Unusual options activity detected for ticker XYZ preceding unverified social media chatter about acquisition.",
      signals: ["Options Flow Volume", "Social Sentiment (Twitter/X)"]
    }
  ];

  const codeSnippet = `def detect_signal(event_stream):
    """
    Analyzes event stream for arbitrage opportunities based on
    latency differentials between news sources.
    """
    signals = []
    for event in event_stream:
        # Check for high-impact keywords with sentiment polarity > 0.8
        if event.impact_score > 0.8 and event.sentiment.polarity > 0.8:
            # Calculate propagation delay
            delay = time.now() - event.timestamp
            if delay < 50ms:
                 signals.append({
                     "type": "LATENCY_ARB",
                     "target": event.ticker,
                     "confidence": 0.95
                 })
    return signals`;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Signal Intelligence</h1>
        <p className="text-gray-400">Automated market surveillance and algorithmic signal generation reports.</p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
          {/* Recent Reports */}
          <div className="space-y-6">
              <h2 className="text-xl font-bold text-white flex items-center">
                  <FileCode className="mr-2 text-green-500" /> Recent Intelligence Reports
              </h2>
              <div className="space-y-4">
                  {reports.map((report) => (
                      <div key={report.id} className="bg-gray-900 border border-gray-800 p-5 rounded-lg hover:border-green-500/30 transition-colors">
                          <div className="flex justify-between items-start mb-2">
                              <h3 className="font-bold text-white text-lg">{report.title}</h3>
                              <span className={`px-2 py-1 rounded text-xs font-bold ${
                                  report.severity === 'High' ? 'bg-red-900/50 text-red-400' :
                                  report.severity === 'Medium' ? 'bg-yellow-900/50 text-yellow-400' :
                                  'bg-blue-900/50 text-blue-400'
                              }`}>
                                  {report.severity}
                              </span>
                          </div>
                          <div className="text-xs text-gray-500 mb-3 font-mono">
                              ID: {report.id} | {report.timestamp}
                          </div>
                          <p className="text-gray-300 text-sm mb-4">{report.summary}</p>
                          <div className="flex flex-wrap gap-2">
                              {report.signals.map((sig) => (
                                  <span key={sig} className="px-2 py-1 bg-gray-800 rounded text-xs text-gray-400">
                                      {sig}
                                  </span>
                              ))}
                          </div>
                      </div>
                  ))}
              </div>
          </div>

          {/* Logic & Analytics */}
          <div className="space-y-6">
               <h2 className="text-xl font-bold text-white flex items-center">
                  <BarChart2 className="mr-2 text-blue-500" /> Signal Logic
              </h2>

              <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
                 <div className="bg-gray-950 px-4 py-2 border-b border-gray-800 flex items-center justify-between">
                    <span className="text-xs text-gray-500 font-mono">signal_detector.py</span>
                    <div className="flex space-x-1">
                        <div className="w-2 h-2 rounded-full bg-gray-700"></div>
                        <div className="w-2 h-2 rounded-full bg-gray-700"></div>
                    </div>
                 </div>
                 <div className="p-4 overflow-x-auto">
                     <pre className="font-mono text-sm text-blue-300">
                        {codeSnippet}
                     </pre>
                 </div>
              </div>

              <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl">
                  <h3 className="text-lg font-bold text-white mb-4">System Performance</h3>
                  <div className="space-y-4">
                      <div className="flex items-center justify-between">
                          <span className="text-gray-400">Signal Accuracy (24h)</span>
                          <span className="text-green-400 font-mono">94.2%</span>
                      </div>
                      <div className="w-full bg-gray-800 h-2 rounded-full">
                          <div className="bg-green-500 h-2 rounded-full" style={{ width: '94.2%' }}></div>
                      </div>

                      <div className="flex items-center justify-between">
                          <span className="text-gray-400">False Positive Rate</span>
                          <span className="text-yellow-400 font-mono">2.1%</span>
                      </div>
                      <div className="w-full bg-gray-800 h-2 rounded-full">
                          <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '2.1%' }}></div>
                      </div>

                      <div className="flex items-center justify-between">
                          <span className="text-gray-400">Latency (Avg)</span>
                          <span className="text-blue-400 font-mono">45ms</span>
                      </div>
                       <div className="w-full bg-gray-800 h-2 rounded-full">
                          <div className="bg-blue-500 h-2 rounded-full" style={{ width: '15%' }}></div>
                      </div>
                  </div>
              </div>
          </div>
      </div>
    </div>
  );
};

export default SignalIntelligence;
