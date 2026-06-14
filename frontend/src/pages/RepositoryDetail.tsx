import React from 'react';
import { Container, Typography, Box } from '@mui/material';

const RepositoryDetailPage: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box>
        <Typography variant="h4">Repository Detail</Typography>
        <Typography variant="body1" sx={{ mt: 2 }}>
          Coming soon: Repository analysis, deployment configuration, and health reports.
        </Typography>
      </Box>
    </Container>
  );
};

export default RepositoryDetailPage;
