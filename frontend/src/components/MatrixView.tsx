import React, { useState, useEffect } from 'react';

// Mock Data for Matrix View
const initialNews = [
    { id: 1, headline: "Fed Hikes Rates by 50bps", signal: "High Signal", timestamp: "10:00 AM" },
    { id: 2, headline: "Top 10 Stocks to Watch", signal: "Noise", timestamp: "10:05 AM" },
    { id: 3, headline: "Tech Sector Slides on Rate News", signal: "High Signal", timestamp: "10:15 AM" },
    { id: 4, headline: "Rumors of Merger between A and B", signal: "Noise", timestamp: "10:30 AM" },
    { id: 5, headline: "Company X Revenue up 20%", signal: "High Signal", timestamp: "10:45 AM" },
];

const MatrixView: React.FC = () => {
    const [newsFeed, setNewsFeed] = useState(initialNews);

    useEffect(() => {
        // Simulate incoming stream
        const interval = setInterval(() => {
            const newArticle = {
                id: Date.now(),
                headline: `Synthetic Event ${Math.floor(Math.random() * 100)}`,
                signal: Math.random() > 0.5 ? "High Signal" : "Noise",
                timestamp: new Date().toLocaleTimeString()
            };
            setNewsFeed(prev => [newArticle, ...prev].slice(0, 50));
        }, 5000);
        return () => clearInterval(interval);
    }, []);

    const getSignalColor = (signal: string) => {
        if (signal === "High Signal") return "text-green-500 font-bold";
        if (signal === "Noise") return "text-gray-400";
        return "text-blue-500";
    };

    return (
        <div className="bg-black text-green-400 p-4 font-mono h-96 overflow-y-scroll border border-green-800 rounded">
            <h2 className="text-xl mb-4 border-b border-green-800 pb-2">The Matrix View (Live Feed)</h2>
            <div className="space-y-2">
                {newsFeed.map(item => (
                    <div key={item.id} className="flex justify-between items-center border-b border-gray-800 pb-1">
                        <span className="text-xs text-gray-500">{item.timestamp}</span>
                        <span className={`flex-1 mx-4 ${getSignalColor(item.signal)}`}>
                            {item.headline}
                        </span>
                        <span className="text-xs border border-gray-700 px-1 rounded">{item.signal}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default MatrixView;
