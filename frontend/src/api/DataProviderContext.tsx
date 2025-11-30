import React, { createContext, useContext, useState, useMemo } from 'react';
import type { IDataProvider } from './types';
import { StaticProvider } from './StaticProvider';
import { LiveProvider } from './LiveProvider';

interface DataProviderContextType {
  provider: IDataProvider;
  mode: 'demo' | 'live';
  setMode: (mode: 'demo' | 'live') => void;
  configureLive: (url: string, apiKey: string) => void;
}

const DataProviderContext = createContext<DataProviderContextType | null>(null);

export const DataProviderProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [mode, setMode] = useState<'demo' | 'live'>('demo');
  const [liveConfig, setLiveConfig] = useState({ url: 'http://localhost:8000', apiKey: '' });

  const provider = useMemo(() => {
    if (mode === 'live') {
      return new LiveProvider(liveConfig.url, liveConfig.apiKey);
    }
    return new StaticProvider();
  }, [mode, liveConfig]);

  const configureLive = (url: string, apiKey: string) => {
    setLiveConfig({ url, apiKey });
  };

  return (
    <DataProviderContext.Provider value={{ provider, mode, setMode, configureLive }}>
      {children}
    </DataProviderContext.Provider>
  );
};

export const useDataProvider = () => {
  const context = useContext(DataProviderContext);
  if (!context) {
    throw new Error('useDataProvider must be used within a DataProviderProvider');
  }
  return context;
};
