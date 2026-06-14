import React from 'react';
import { Container, Typography, Box, Button } from '@mui/material';
import { Link } from 'react-router-dom';

const NotFoundPage: React.FC = () => {
  return (
    <Container maxWidth="sm">
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', py: 10 }}>
        <Typography variant="h1" sx={{ fontSize: '4rem', fontWeight: 700 }}>
          404
        </Typography>
        <Typography variant="h4" sx={{ mb: 2 }}>
          Page Not Found
        </Typography>
        <Typography variant="body1" color="textSecondary" sx={{ mb: 4, textAlign: 'center' }}>
          The page you're looking for doesn't exist.
        </Typography>
        <Button component={Link} to="/" variant="contained">
          Go Home
        </Button>
      </Box>
    </Container>
  );
};

export default NotFoundPage;
