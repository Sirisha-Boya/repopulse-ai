import React, { useEffect } from 'react';
import { Container, Box, Paper, Typography, Grid, Button, CircularProgress, Alert } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../redux/store';
import { fetchRepositories, syncRepositories } from '../redux/slices/repositoriesSlice';
import RefreshIcon from '@mui/icons-material/Refresh';

const Dashboard: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { repositories, syncing, loading, error } = useSelector((state: RootState) => state.repositories);
  const { user } = useSelector((state: RootState) => state.auth);
  const [autoSyncDone, setAutoSyncDone] = React.useState(false);

  useEffect(() => {
    // Auto-sync repositories on first load
    if (!autoSyncDone) {
      console.log('Dashboard: Auto-syncing repositories...');
      dispatch(syncRepositories())
        .then(() => {
          setAutoSyncDone(true);
          // Fetch after sync
          dispatch(fetchRepositories({ page: 1, pageSize: 5 }));
        })
        .catch((err) => {
          console.error('Auto-sync failed:', err);
          setAutoSyncDone(true);
          // Still try to fetch local repos
          dispatch(fetchRepositories({ page: 1, pageSize: 5 }));
        });
    }
  }, [dispatch, autoSyncDone]);

  const handleManualSync = () => {
    console.log('Dashboard: Manual sync triggered');
    dispatch(syncRepositories())
      .then(() => {
        dispatch(fetchRepositories({ page: 1, pageSize: 5 }));
      });
  };

  const stats = [
    { label: 'Total Repositories', value: repositories.length, color: '#1976d2' },
    { label: 'Total Deployments', value: 0, color: '#2196f3' },
    { label: 'Successful', value: 0, color: '#4caf50' },
    { label: 'Failed', value: 0, color: '#f44336' },
  ];

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Welcome, {user?.github_username}! 👋
        </Typography>
        <Typography variant="body1" color="textSecondary">
          Manage and deploy your applications with AI-powered assistance
        </Typography>
      </Box>

      {error && (
        <Alert severity="warning" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3} sx={{ mb: 4 }}>
        {stats.map((stat) => (
          <Grid item xs={12} sm={6} md={3} key={stat.label}>
            <Paper sx={{ p: 3, textAlign: 'center', backgroundColor: `${stat.color}15` }}>
              <Typography variant="h5" sx={{ color: stat.color, fontWeight: 'bold' }}>
                {stat.value}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {stat.label}
              </Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>

      <Paper sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6">Recent Repositories</Typography>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Button
              variant="outlined"
              size="small"
              startIcon={<RefreshIcon />}
              onClick={handleManualSync}
              disabled={syncing}
            >
              {syncing ? <CircularProgress size={20} sx={{ mr: 1 }} /> : 'Sync Again'}
            </Button>
            <Button variant="contained" href="/repositories" size="small">
              View All ({repositories.length})
            </Button>
          </Box>
        </Box>

        {loading && !repositories.length ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
            <CircularProgress />
          </Box>
        ) : repositories.length === 0 ? (
          <Typography color="textSecondary" sx={{ py: 3 }}>
            📭 No repositories found. Try clicking "Sync Again" to fetch from GitHub.
          </Typography>
        ) : (
          <Box>
            {repositories.slice(0, 5).map((repo) => (
              <Box
                key={repo.id}
                sx={{
                  py: 2,
                  px: 2,
                  borderBottom: '1px solid #eee',
                  cursor: 'pointer',
                  transition: 'background-color 0.2s',
                  '&:hover': { backgroundColor: '#f5f5f5' },
                }}
                onClick={() => (window.location.href = `/repositories/${repo.id}`)}
              >
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                      {repo.name}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      {repo.description || 'No description'}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', gap: 1, ml: 2 }}>
                    {repo.language && (
                      <Typography variant="caption" sx={{ bg: '#f0f0f0', px: 1, borderRadius: 1 }}>
                        {repo.language}
                      </Typography>
                    )}
                    <Typography variant="caption" sx={{ bg: '#f0f0f0', px: 1, borderRadius: 1 }}>
                      ⭐ {repo.stars}
                    </Typography>
                  </Box>
                </Box>
              </Box>
            ))}
          </Box>
        )}
      </Paper>
    </Container>
  );
};

export default Dashboard;
