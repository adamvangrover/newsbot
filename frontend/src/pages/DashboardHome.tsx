import React, { useState, useEffect } from 'react';
import { Box, Grid, Paper, Typography, LinearProgress } from '@mui/material';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import ArticleIcon from '@mui/icons-material/Article';
import ShowChartIcon from '@mui/icons-material/ShowChart';

const StatCard = ({ title, value, icon, color }: { title: string, value: string | number, icon: React.ReactNode, color: string }) => (
  <Paper sx={{ p: 3, display: 'flex', flexDirection: 'column', height: 140, justifyContent: 'space-between', borderLeft: `6px solid ${color}` }}>
    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
      <Typography variant="subtitle2" color="textSecondary">{title}</Typography>
      <Box sx={{ color: color }}>{icon}</Box>
    </Box>
    <Typography variant="h3" component="div">{value}</Typography>
  </Paper>
);

export const DashboardHome: React.FC = () => {
    const [stats, setStats] = useState({
        articlesProcessed: 0,
        agentsActive: 5,
        marketUptime: '99.9%'
    });

    useEffect(() => {
        // Simulation of increasing article count
        const interval = setInterval(() => {
            setStats(prev => ({ ...prev, articlesProcessed: prev.articlesProcessed + Math.floor(Math.random() * 5) }));
        }, 1000);
        return () => clearInterval(interval);
    }, []);

    const agents = [
        { name: 'MarketDataAgent', status: 'Active', load: 85 },
        { name: 'SentimentAnalyzer', status: 'Active', load: 60 },
        { name: 'EarningsParser', status: 'Idle', load: 10 },
        { name: 'RiskAssessor', status: 'Active', load: 45 },
        { name: 'ClusterEngine', status: 'Processing', load: 92 },
    ];

    return (
        <Box>
            <Typography variant="h4" gutterBottom>System Dashboard</Typography>
            <Grid container spacing={3} sx={{ mb: 4 }}>
                <Grid item xs={12} sm={4}>
                    <StatCard
                        title="Articles Processed"
                        value={stats.articlesProcessed.toLocaleString()}
                        icon={<ArticleIcon fontSize="large" />}
                        color="#2196f3"
                    />
                </Grid>
                <Grid item xs={12} sm={4}>
                    <StatCard
                        title="Active Agents"
                        value={stats.agentsActive}
                        icon={<SmartToyIcon fontSize="large" />}
                        color="#ff9800"
                    />
                </Grid>
                <Grid item xs={12} sm={4}>
                    <StatCard
                        title="System Uptime"
                        value={stats.marketUptime}
                        icon={<ShowChartIcon fontSize="large" />}
                        color="#4caf50"
                    />
                </Grid>
            </Grid>

            <Typography variant="h6" gutterBottom>Active Agents Status</Typography>
            <Grid container spacing={2}>
                {agents.map((agent) => (
                    <Grid item xs={12} md={6} lg={4} key={agent.name}>
                        <Paper sx={{ p: 2 }}>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                <Typography variant="subtitle1">{agent.name}</Typography>
                                <Typography
                                    variant="caption"
                                    sx={{
                                        color: agent.status === 'Active' || agent.status === 'Processing' ? 'success.main' : 'text.secondary',
                                        fontWeight: 'bold',
                                        border: '1px solid',
                                        borderColor: agent.status === 'Active' || agent.status === 'Processing' ? 'success.main' : 'text.secondary',
                                        px: 1,
                                        borderRadius: 1
                                    }}
                                >
                                    {agent.status.toUpperCase()}
                                </Typography>
                            </Box>
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Box sx={{ width: '100%', mr: 1 }}>
                                    <LinearProgress variant="determinate" value={agent.load} color={agent.load > 90 ? 'error' : 'primary'} />
                                </Box>
                                <Box sx={{ minWidth: 35 }}>
                                    <Typography variant="body2" color="text.secondary">{`${Math.round(agent.load)}%`}</Typography>
                                </Box>
                            </Box>
                        </Paper>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
};
