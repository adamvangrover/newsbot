import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { DataProviderProvider } from './api/DataProviderContext';
import { Layout } from './components/Layout';
import { Box, Typography } from '@mui/material';
import { PerformanceDashboard } from './pages/PerformanceDashboard';
import { FederatedLearningVisualizer } from './components/FederatedLearningVisualizer';
import { KnowledgeGraph } from './components/KnowledgeGraph';
import { DashboardHome } from './pages/DashboardHome';

function App() {
  return (
    <DataProviderProvider>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<DashboardHome />} />
            <Route path="/performance" element={<PerformanceDashboard />} />
            <Route path="/federated" element={<FederatedLearningVisualizer />} />
            <Route path="/knowledge-graph" element={<KnowledgeGraph />} />
          </Routes>
        </Layout>
      </Router>
    </DataProviderProvider>
  );
}

export default App;
