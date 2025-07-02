import React, { useState, useEffect } from 'react';
import { getCompanyDetails, getCompanyDirectDrivers, getCompanyNarrative } from '@/services/api';
import { Company, CompanyDriverInfo } from '@/types/api_types';

interface CompanyExplorerProps {
  companyId: string;
}

const CompanyExplorer: React.FC<CompanyExplorerProps> = ({ companyId }) => {
  const [company, setCompany] = useState<Company | null>(null);
  const [drivers, setDrivers] = useState<CompanyDriverInfo[] | null>(null);
  const [narrative, setNarrative] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!companyId) {
      setCompany(null);
      setDrivers(null);
      setNarrative(null);
      setError(null);
      return;
    }

    const fetchCompanyData = async () => {
      setLoading(true);
      setError(null);
      try {
        // Fetch all data in parallel for a better user experience
        const [details, directDrivers, companyNarrative] = await Promise.all([
          getCompanyDetails(companyId),
          getCompanyDirectDrivers(companyId),
          getCompanyNarrative(companyId)
        ]);

        if (details) {
          setCompany(details);
          setDrivers(directDrivers);
          setNarrative(companyNarrative);
        } else {
          setError(`Company details not found for ID: ${companyId}`);
          setCompany(null);
          setDrivers(null);
          setNarrative(null);
        }

      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : String(err);
        setError(`Error fetching data for company ${companyId}: ${errorMessage}`);
        console.error(err);
        setCompany(null);
        setDrivers(null);
        setNarrative(null);
      } finally {
        setLoading(false);
      }
    };

    fetchCompanyData();
  }, [companyId]);

  if (!companyId) {
    return null;
  }

  if (loading) {
    return <p className="loading">Loading data for company "{companyId}"...</p>;
  }

  if (error) {
    return <p className="error">Error: {error}</p>;
  }

  if (!company) {
    return <p>No company data found for ID "{companyId}". The company may not exist, or there was an issue fetching its details.</p>;
  }

  return (
    <div className="component-section">
      <h2>Company: {company.name} ({company.id})</h2>

      <section>
        <h3>Details:</h3>
        <pre>{JSON.stringify(company, null, 2)}</pre>
      </section>

      <section>
        <h3>Direct Drivers:</h3>
        {drivers && drivers.length > 0 ? (
          <pre>{JSON.stringify(drivers, null, 2)}</pre>
        ) : (
          <p>No direct drivers found or data could not be loaded for this company.</p>
        )}
      </section>

      <section>
        <h3>Simple Narrative:</h3>
        {narrative ? (
          <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>{narrative}</pre>
        ) : (
          <p>No narrative available or data could not be loaded for this company.</p>
        )}
      </section>
    </div>
  );
};

export default CompanyExplorer;
