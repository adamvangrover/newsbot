import React, { useMemo } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { Box, Typography, Paper } from '@mui/material';

export const KnowledgeGraph: React.FC = () => {
    // Generate static graph data
    const data = useMemo(() => {
        return {
            nodes: [
                { id: 'AAPL', group: 1, val: 20, label: 'Apple Inc.' },
                { id: 'SupplyChain', group: 2, val: 10, label: 'Supply Chain Issue' },
                { id: 'Semiconductor', group: 2, val: 10, label: 'Semiconductor Shortage' },
                { id: 'TSMC', group: 1, val: 15, label: 'TSMC' },
                { id: 'Revenue_Impact', group: 3, val: 5, label: 'Revenue Impact' },
                { id: 'iPhone_Delay', group: 3, val: 5, label: 'iPhone Delay' },
                { id: 'Market_Sentiment', group: 4, val: 8, label: 'Negative Sentiment' },
            ],
            links: [
                { source: 'AAPL', target: 'SupplyChain' },
                { source: 'SupplyChain', target: 'Semiconductor' },
                { source: 'Semiconductor', target: 'TSMC' },
                { source: 'SupplyChain', target: 'iPhone_Delay' },
                { source: 'iPhone_Delay', target: 'Revenue_Impact' },
                { source: 'Revenue_Impact', target: 'AAPL' },
                { source: 'iPhone_Delay', target: 'Market_Sentiment' },
            ]
        };
    }, []);

    return (
        <Paper sx={{ p: 2, height: '80vh', display: 'flex', flexDirection: 'column' }}>
            <Typography variant="h6" color="primary" gutterBottom>
                Semantic Knowledge Graph
            </Typography>
            <Box sx={{ flexGrow: 1, backgroundColor: '#000', borderRadius: 1, overflow: 'hidden' }}>
                 {/* @ts-ignore: ForceGraph2D typings issues are common */}
                <ForceGraph2D
                    graphData={data}
                    nodeLabel="label"
                    nodeColor={node => {
                        const colors = ['#ff9800', '#2196f3', '#f44336', '#4caf50'];
                        return colors[(node as any).group - 1] || '#fff';
                    }}
                    linkColor={() => '#555'}
                    backgroundColor="#000000"
                />
            </Box>
        </Paper>
    );
};
