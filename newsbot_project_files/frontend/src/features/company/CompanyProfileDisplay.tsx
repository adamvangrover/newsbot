import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Avatar from '@mui/material/Avatar';

// Define a type for the company profile data - should match backend schema
interface CompanyProfileData {
    country?: string | null;
    currency?: string | null;
    exchange?: string | null;
    name?: string | null;
    ticker: string;
    ipo?: string | null;
    marketCapitalization?: number | null;
    shareOutstanding?: number | null;
    logo?: string | null; // Assuming HttpUrl becomes string
    phone?: string | null;
    weburl?: string | null; // Assuming HttpUrl becomes string
    finnhubIndustry?: string | null;
}

interface CompanyProfileDisplayProps {
  profile: CompanyProfileData | null | undefined;
}

const CompanyProfileDisplay: React.FC<CompanyProfileDisplayProps> = ({ profile }) => {
  if (!profile) {
    return <Typography>No company profile data available.</Typography>;
  }

  return (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          {profile.logo && (
            <Avatar src={profile.logo} alt={`${profile.name} logo`} sx={{ width: 56, height: 56, mr: 2 }} />
          )}
          <Typography variant="h5" component="div">
            {profile.name} ({profile.ticker})
          </Typography>
        </Box>
        <Typography variant="body2" color="text.secondary">
          <strong>Industry:</strong> {profile.finnhubIndustry || 'N/A'}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          <strong>Exchange:</strong> {profile.exchange || 'N/A'}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          <strong>IPO Date:</strong> {profile.ipo || 'N/A'}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          <strong>Market Cap:</strong> {profile.marketCapitalization ? profile.marketCapitalization.toLocaleString() : 'N/A'} {profile.currency}
        </Typography>
        {profile.weburl && (
          <Typography variant="body2" color="text.secondary">
            <strong>Website:</strong> <a href={profile.weburl} target="_blank" rel="noopener noreferrer">{profile.weburl}</a>
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

export default CompanyProfileDisplay;
