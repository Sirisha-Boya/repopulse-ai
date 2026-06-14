import React from 'react';
import { Container, Button, Box, Paper, Typography } from '@mui/material';
import GitHubIcon from '@mui/icons-material/GitHub';
import { apiClient } from '../services/apiClient';

const LoginPage: React.FC = () => {
  const handleGitHubLogin = async () => {
    try {
      const response = await apiClient.get('/api/auth/github/login');
      const { oauth_url } = response.data;
      window.location.href = oauth_url;
    } catch (error) {
      console.error('Failed to get OAuth URL:', error);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box
        display="flex"
        flexDirection="column"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
      >
        <Paper elevation={3} sx={{ p: 4, textAlign: 'center', width: '100%' }}>
          <Typography variant="h3" component="h1" gutterBottom sx={{ mb: 3 }}>
            🚀 Deployment Platform
          </Typography>
          <Typography variant="body1" color="textSecondary" sx={{ mb: 4 }}>
            AI-powered deployment orchestration for your GitHub repositories
          </Typography>
          <Button
            variant="contained"
            size="large"
            startIcon={<GitHubIcon />}
            onClick={handleGitHubLogin}
            sx={{ width: '100%', py: 1.5 }}
          >
            Sign in with GitHub
          </Button>
          <Typography variant="caption" display="block" sx={{ mt: 3, color: 'textSecondary' }}>
            We only access your public repositories and GitHub Actions workflows
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
};

export default LoginPage;
