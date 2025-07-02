import React, { useState, useEffect } from 'react';
import { getEntityById, getDriverById }_from '@/services/api'; // Using path alias
import { AnyEntity, Driver } from '@/types/api_types';

interface EntityViewerProps {
  entityIdToView: string;
  entityType: 'Entity' | 'Driver'; // To call the correct API
}

const EntityViewer: React.FC<EntityViewerProps> = ({ entityIdToView, entityType }) => {
  const [data, setData] = useState<AnyEntity | Driver | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      let result = null;
      try {
        if (entityType === 'Entity') {
          result = await getEntityById(entityIdToView);
        } else if (entityType === 'Driver') {
          result = await getDriverById(entityIdToView);
        }

        if (result) {
          setData(result);
        } else {
          setError(`Failed to fetch ${entityType.toLowerCase()} ${entityIdToView} or it was not found.`);
        }
      } catch (err) {
        setError(`Error fetching ${entityType.toLowerCase()} ${entityIdToView}: ${err instanceof Error ? err.message : String(err)}`);
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (entityIdToView) {
      fetchData();
    } else {
      setData(null);
      setLoading(false);
      setError(null);
    }
  }, [entityIdToVew, entityType]);

  if (loading) return <p className="loading">Loading {entityType.toLowerCase()} data for "{entityIdToView}"...</p>;
  if (error) return <p className="error">Error: {error}</p>;
  if (!data) return <p>No {entityType.toLowerCase()} data to display for "{entityIdToView}".</p>;

  return (
    <div className="component-section">
      <h2>{entityType} Viewer: {data.name} ({data.id})</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
};

export default EntityViewer;
