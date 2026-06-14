import React from 'react';
import { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import { AppDispatch } from '../redux/store';
import { loginWithGitHub } from '../redux/slices/authSlice';
import { useNavigate } from 'react-router-dom';
import { Container, CircularProgress, Box, Typography } from '@mui/material';

const AuthCallback: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const code = params.get('code');
    const state = params.get('state');

    console.log('OAuth Callback - Code:', code, 'State:', state);

    if (code) {
      // Exchange code for tokens with the backend
      dispatch(loginWithGitHub(code))
        .unwrap()
        .then((result) => {
          console.log('Login successful:', result);
          // Wait a moment then navigate to dashboard
          setTimeout(() => navigate('/'), 500);
        })
        .catch((error) => {
          console.error('Login error:', error);
          setError(`Authentication failed: ${error}`);
          // Redirect to login after 2 seconds
          setTimeout(() => navigate('/login'), 2000);
        });
    } else {
      const errorCode = params.get('error');
      const errorDescription = params.get('error_description');
      console.error('OAuth error:', errorCode, errorDescription);
      setError(`Authentication error: ${errorCode || 'Unknown error'}`);
      setTimeout(() => navigate('/login'), 2000);
    }
  }, [dispatch, navigate]);

  return (
    <Container maxWidth="sm">
      <Box
        display="flex"
        flexDirection="column"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
        gap={2}
      >
        {error ? (
          <>
            <Typography variant="h5" color="error">
              ❌ {error}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Redirecting to login...
            </Typography>
          </>
        ) : (
          <>
            <CircularProgress size={50} />
            <Typography variant="h6">Authenticating with GitHub...</Typography>
            <Typography variant="body2" color="textSecondary">
              Please wait, this should only take a moment
            </Typography>
          </>
        )}
      </Box>
    </Container>
  );
};

export default AuthCallback;
