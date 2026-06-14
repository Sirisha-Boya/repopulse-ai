import React, { useEffect, useState } from 'react';
import { Container, Box, Paper, TextField, Button, CircularProgress } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../redux/store';
import { fetchRepositories, syncRepositories } from '../redux/slices/repositoriesSlice';
import { DataGrid, GridColDef } from '@mui/x-data-grid';

const RepositoriesPage: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { repositories, total, page, pageSize, loading, syncing } = useSelector(
    (state: RootState) => state.repositories
  );
  const [localPage, setLocalPage] = useState(0);

  useEffect(() => {
    dispatch(fetchRepositories({ page: localPage + 1, pageSize }));
  }, [dispatch, localPage, pageSize]);

  const handleSync = () => {
    dispatch(syncRepositories());
  };

  const columns: GridColDef[] = [
    { field: 'name', headerName: 'Repository', width: 150 },
    { field: 'description', headerName: 'Description', width: 300 },
    { field: 'default_branch', headerName: 'Branch', width: 100 },
    { field: 'language', headerName: 'Language', width: 100 },
    { field: 'stars', headerName: 'Stars', width: 80 },
  ];

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 3, display: 'flex', gap: 2 }}>
        <TextField placeholder="Search repositories..." size="small" sx={{ flex: 1 }} />
        <Button variant="contained" onClick={handleSync} disabled={syncing}>
          {syncing ? <CircularProgress size={24} /> : 'Sync from GitHub'}
        </Button>
      </Box>

      <Paper sx={{ height: 600 }}>
        <DataGrid
          rows={repositories}
          columns={columns}
          paginationModel={{ pageSize, page: localPage }}
          onPaginationModelChange={(newModel) => setLocalPage(newModel.page)}
          rowCount={total}
          pageSizeOptions={[20]}
          paginationMode="server"
          loading={loading}
          sx={{ border: 0 }}
        />
      </Paper>
    </Container>
  );
};

export default RepositoriesPage;
