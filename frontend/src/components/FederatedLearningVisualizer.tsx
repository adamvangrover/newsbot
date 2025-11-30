import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const Node = ({ name, color, isActive }: { name: string, color: string, isActive: boolean }) => (
  <div
    className={`w-24 h-24 flex flex-col justify-center items-center rounded-full border-4 bg-gray-900 z-10 transition-colors duration-500`}
    style={{ borderColor: isActive ? color : '#374151' }}
  >
    <span className="text-xs font-bold text-gray-200">{name}</span>
  </div>
);

const FederatedLearningVisualizer: React.FC = () => {
    const [cycle, setCycle] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setCycle(c => (c + 1) % 4); // 0: Idle, 1: Train, 2: Upload, 3: Aggregation
        }, 2000);
        return () => clearInterval(interval);
    }, []);

    const clients = [
        { id: 1, name: 'Client A', color: '#f97316' }, // Orange
        { id: 2, name: 'Client B', color: '#3b82f6' }, // Blue
        { id: 3, name: 'Client C', color: '#22c55e' }, // Green
    ];

    return (
        <div className="p-8 h-full flex flex-col items-center bg-gray-950">
            <h2 className="text-2xl font-bold text-white mb-2">Federated Learning Simulation</h2>
            <p className="text-gray-400 mb-8">
                Status: <span className="text-green-400">{['Idle', 'Training Local Models', 'Sending Updates', 'Global Aggregation'][cycle]}</span>
            </p>

            <div className="relative w-full max-w-2xl h-[500px] flex justify-center">

                {/* Connecting Lines (Static SVG) */}
                <svg className="absolute inset-0 w-full h-full z-0 pointer-events-none">
                    <line x1="50%" y1="120" x2="20%" y2="400" stroke="#374151" strokeWidth="2" />
                    <line x1="50%" y1="120" x2="50%" y2="400" stroke="#374151" strokeWidth="2" />
                    <line x1="50%" y1="120" x2="80%" y2="400" stroke="#374151" strokeWidth="2" />
                </svg>

                {/* Global Model */}
                <div className="absolute top-10">
                    <Node name="Global Model" color="#ffffff" isActive={cycle === 3} />
                </div>

                {/* Clients */}
                <div className="absolute bottom-10 w-full flex justify-between px-10 md:px-20">
                    {clients.map((client, index) => (
                        <div key={client.id} className="relative">
                            <Node name={client.name} color={client.color} isActive={cycle === 1} />

                            {/* Packet Animation (Upload) */}
                            {cycle === 2 && (
                                <motion.div
                                    initial={{ opacity: 1, y: 0 }}
                                    animate={{
                                        y: -280, // Distance to global model
                                        x: index === 0 ? 100 : index === 2 ? -100 : 0, // Convergence towards center
                                        opacity: 0
                                    }}
                                    transition={{ duration: 1.5 }}
                                    className="absolute top-0 left-1/2 w-3 h-3 rounded-full transform -translate-x-1/2"
                                    style={{ backgroundColor: client.color }}
                                />
                            )}

                            {/* Download Animation (Aggregation) */}
                            {cycle === 3 && (
                                <motion.div
                                    initial={{
                                        opacity: 0,
                                        y: -280,
                                        x: index === 0 ? 100 : index === 2 ? -100 : 0,
                                    }}
                                    animate={{ y: 0, x: 0, opacity: 1 }}
                                    transition={{ duration: 1.5 }}
                                    className="absolute top-0 left-1/2 w-3 h-3 bg-white rounded-full transform -translate-x-1/2"
                                />
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default FederatedLearningVisualizer;
