import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import OperationalDashboard from './pages/OperationalDashboard';
import SystemStatus from './pages/SystemStatus';
import Architecture from './pages/Architecture';
import Showcase from './pages/Showcase';
import About from './pages/About';
import Performance from './pages/Performance';
import ImpactAnalysis from './pages/ImpactAnalysis';
import FederatedLearning from './pages/FederatedLearning';
import SignalIntelligence from './pages/SignalIntelligence';
import Resources from './pages/Resources';
import Plugins from './pages/Plugins';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<OperationalDashboard />} />
          <Route path="/signals" element={<SignalIntelligence />} />
          <Route path="/resources" element={<Resources />} />
          <Route path="/plugins" element={<Plugins />} />
          <Route path="/status" element={<SystemStatus />} />
          <Route path="/architecture" element={<Architecture />} />
          <Route path="/showcase" element={<Showcase />} />
          <Route path="/performance" element={<Performance />} />
          <Route path="/impact" element={<ImpactAnalysis />} />
          <Route path="/federated" element={<FederatedLearning />} />
          <Route path="/about" element={<About />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
