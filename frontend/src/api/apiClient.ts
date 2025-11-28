import { useDataProvider } from './DataProviderContext';

// Hook to access the current data provider
export const useApiClient = () => {
    const { provider } = useDataProvider();
    return provider;
};
