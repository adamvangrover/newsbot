import React from 'react';
import './App.css'; // Optional: for app-specific styling
import CompanyExplorer from './components/CompanyExplorer'; // We will create this
import EntityViewer from './components/EntityViewer'; // We will create this

function App() {
  const [selectedCompanyId, setSelectedCompanyId] = React.useState<string | null>("comp_alpha"); // Default to comp_alpha for demo

  return (
    <div className="App">
      <header className="App-header">
        <h1>Semantic Narrative Library Explorer</h1>
      </header>
      <main>
        <p>
          This is a basic interface to explore the Semantic Narrative Library.
          The backend API (FastAPI) should be running on port 8000.
        </p>

        <hr />
        <EntityViewer entityIdToView="ind_tech" entityType="Industry" />
        <hr />
        <EntityViewer entityIdToView="drv_cloud_adoption" entityType="Driver" />
        <hr />

        {/* Basic component to select or list companies and then view details */}
        <div>
          <h2>Company Narratives & Drivers</h2>
          <label htmlFor="company-select">Select Company ID (e.g., comp_alpha, comp_beta): </label>
          <input
            type="text"
            id="company-select"
            defaultValue={selectedCompanyId || ""}
            onBlur={(e) => setSelectedCompanyId(e.target.value)}
            placeholder="Enter company ID"
          />
          {selectedCompanyId && <CompanyExplorer companyId={selectedCompanyId} />}
        </div>

      </main>
    </div>
  );
}

export default App;
