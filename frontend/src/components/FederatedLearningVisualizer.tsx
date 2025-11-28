import React, { useState, useEffect } from 'react';
import { Box, Typography, Paper, Grid } from '@mui/material';
import { motion } from 'framer-motion';

const Node = ({ name, color, isActive }: { name: string, color: string, isActive: boolean }) => (
  <Paper
    elevation={3}
    sx={{
        width: 100,
        height: 100,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
        borderRadius: '50%',
        border: `3px solid ${isActive ? color : '#555'}`,
        backgroundColor: '#1e1e1e',
        zIndex: 2
    }}
  >
    <Typography variant="body2" sx={{ fontWeight: 'bold' }}>{name}</Typography>
  </Paper>
);

export const FederatedLearningVisualizer: React.FC = () => {
    const [cycle, setCycle] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setCycle(c => (c + 1) % 4); // 0: Idle, 1: Train, 2: Upload, 3: Aggregation
        }, 2000);
        return () => clearInterval(interval);
    }, []);

    const clients = [
        { id: 1, name: 'Client A', color: '#ff9800' },
        { id: 2, name: 'Client B', color: '#2196f3' },
        { id: 3, name: 'Client C', color: '#4caf50' },
    ];

    return (
        <Box sx={{ p: 4, height: '80vh', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <Typography variant="h4" gutterBottom>Federated Learning Simulation</Typography>
            <Typography variant="subtitle1" gutterBottom sx={{color: '#888'}}>
                Status: {['Idle', 'Training Local Models', 'Sending Updates', 'Global Aggregation'][cycle]}
            </Typography>

            <Box sx={{ position: 'relative', width: '100%', height: 500, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>

                {/* Global Model */}
                <Box sx={{ position: 'absolute', top: 50 }}>
                    <Node name="Global Model" color="#fff" isActive={cycle === 3} />
                </Box>

                {/* Clients */}
                <Box sx={{ position: 'absolute', bottom: 50, display: 'flex', gap: 10 }}>
                    {clients.map(client => (
                        <Box key={client.id} sx={{ position: 'relative' }}>
                            <Node name={client.name} color={client.color} isActive={cycle === 1} />

                            {/* Packet Animation */}
                            {cycle === 2 && (
                                <motion.div
                                    initial={{ opacity: 1, y: 0 }}
                                    animate={{ y: -300, opacity: 0 }} // Approximate distance to Global Model
                                    transition={{ duration: 1.5 }}
                                    style={{
                                        position: 'absolute',
                                        top: -20,
                                        left: '50%',
                                        width: 10,
                                        height: 10,
                                        backgroundColor: client.color,
                                        borderRadius: '50%',
                                        transform: 'translateX(-50%)'
                                    }}
                                />
                            )}

                            {/* Download Animation */}
                            {cycle === 3 && (
                                <motion.div
                                    initial={{ opacity: 0, y: -300 }}
                                    animate={{ y: 0, opacity: 1 }}
                                    transition={{ duration: 1.5 }}
                                    style={{
                                        position: 'absolute',
                                        top: -20,
                                        left: '50%',
                                        width: 10,
                                        height: 10,
                                        backgroundColor: '#fff',
                                        borderRadius: '50%',
                                        transform: 'translateX(-50%)'
                                    }}
                                />
                            )}
                        </Box>
                    ))}
                </Box>

                {/* Connecting Lines (Static) */}
                <svg width="100%" height="100%" style={{ position: 'absolute', zIndex: 0, pointerEvents: 'none' }}>
                    <line x1="50%" y1="150" x2="30%" y2="400" stroke="#444" strokeWidth="2" />
                    <line x1="50%" y1="150" x2="50%" y2="400" stroke="#444" strokeWidth="2" />
                    <line x1="50%" y1="150" x2="70%" y2="400" stroke="#444" strokeWidth="2" />
                </svg>
            </Box>
        </Box>
    );
};
