import axios from 'axios';
import { AnyEntity, Company, Driver, CompanyDriverInfo, KGStats } from '@/types/api_types'; // Using path alias @

// Base URL for the API.
// If using Vite's proxy (e.g., /api mapped to http://localhost:8000),
// then this would be '/api'.
// If calling FastAPI directly (e.g. it's on port 8000 and handles CORS):
const API_BASE_URL = 'http://localhost:8000'; // Adjust if your FastAPI is elsewhere or if using proxy

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- Entity Endpoints ---
export const getEntityById = async (entityId: string): Promise<AnyEntity | null> => {
  try {
    const response = await apiClient.get<AnyEntity>(`/entities/${entityId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching entity ${entityId}:`, error);
    // Consider how to handle errors: throw, return null, or return an error object
    return null;
  }
};

// --- Driver Endpoints ---
export const getDriverById = async (driverId: string): Promise<Driver | null> => {
    try {
      const response = await apiClient.get<Driver>(`/drivers/${driverId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching driver ${driverId}:`, error);
      return null;
    }
  };

// --- Company Endpoints ---
export const getCompanyDetails = async (companyId: string): Promise<Company | null> => {
  try {
    const response = await apiClient.get<Company>(`/companies/${companyId}/details`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching company details for ${companyId}:`, error);
    return null;
  }
};

export const getCompanyDirectDrivers = async (companyId: string): Promise<CompanyDriverInfo[]> => {
  try {
    const response = await apiClient.get<CompanyDriverInfo[]>(`/companies/${companyId}/direct_drivers`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching direct drivers for company ${companyId}:`, error);
    return []; // Return empty array on error
  }
};

export const getCompanyNarrative = async (companyId: string): Promise<string | null> => {
  try {
    // The response for narrative is expected to be a plain string, not JSON directly for the data part.
    // Axios might still parse it if content-type is application/json, but FastAPI returns text/plain for string responses by default.
    // Let's assume FastAPI might wrap it in JSON like {"narrative": "..."} or we adjust FastAPI to return JSON.
    // For now, let's assume the backend returns a string directly.
    const response = await apiClient.get<string>(`/companies/${companyId}/narrative`);
    return response.data; // FastAPI returns plain text string for string responses
  } catch (error) {
    console.error(`Error fetching narrative for company ${companyId}:`, error);
    return null;
  }
};


// --- Knowledge Graph Stats ---
export const getKGStats = async (): Promise<KGStats | null> => {
    try {
        const response = await apiClient.get<KGStats>('/knowledge_graph/stats');
        return response.data;
    } catch (error) {
        console.error('Error fetching KG stats:', error);
        return null;
    }
};


// Example of a more generic fetch function if needed later
// export const fetchData = async <T>(endpoint: string): Promise<T | null> => {
//   try {
//     const response = await apiClient.get<T>(endpoint);
//     return response.data;
//   } catch (error) {
//     console.error(`Error fetching data from ${endpoint}:`, error);
//     return null;
//   }
// };
