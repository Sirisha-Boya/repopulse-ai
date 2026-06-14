import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { apiClient } from '../../services/apiClient';

interface Repository {
  id: number;
  name: string;
  full_name: string;
  description: string | null;
  url: string;
  default_branch: string;
  language: string | null;
  is_private: boolean;
  stars: number;
  last_pushed_at: string | null;
  created_at: string;
  updated_at: string;
}

interface RepositoriesState {
  repositories: Repository[];
  currentRepository: Repository | null;
  total: number;
  page: number;
  pageSize: number;
  loading: boolean;
  error: string | null;
  syncing: boolean;
}

const initialState: RepositoriesState = {
  repositories: [],
  currentRepository: null,
  total: 0,
  page: 1,
  pageSize: 20,
  loading: false,
  error: null,
  syncing: false,
};

export const syncRepositories = createAsyncThunk(
  'repositories/sync',
  async (_, { rejectWithValue }) => {
    try {
      const response = await apiClient.post('/repositories/sync');
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchRepositories = createAsyncThunk(
  'repositories/fetchRepositories',
  async ({ page = 1, pageSize = 20 }, { rejectWithValue }) => {
    try {
      const response = await apiClient.get('/repositories', {
        params: { page, page_size: pageSize },
      });
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

export const searchRepositories = createAsyncThunk(
  'repositories/search',
  async ({ query, page = 1, pageSize = 20 }, { rejectWithValue }: any) => {
    try {
      const response = await apiClient.get('/repositories/search', {
        params: { q: query, page, page_size: pageSize },
      });
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchRepository = createAsyncThunk(
  'repositories/fetchRepository',
  async (repoId: number, { rejectWithValue }) => {
    try {
      const response = await apiClient.get(`/repositories/${repoId}`);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

const repositoriesSlice = createSlice({
  name: 'repositories',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearCurrentRepository: (state) => {
      state.currentRepository = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(syncRepositories.pending, (state) => {
        state.syncing = true;
        state.error = null;
      })
      .addCase(syncRepositories.fulfilled, (state) => {
        state.syncing = false;
      })
      .addCase(syncRepositories.rejected, (state, action) => {
        state.syncing = false;
        state.error = action.payload as string;
      })
      .addCase(fetchRepositories.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchRepositories.fulfilled, (state, action) => {
        state.loading = false;
        state.repositories = action.payload.repositories;
        state.total = action.payload.total;
        state.page = action.payload.page;
        state.pageSize = action.payload.page_size;
      })
      .addCase(fetchRepositories.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(searchRepositories.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(searchRepositories.fulfilled, (state, action) => {
        state.loading = false;
        state.repositories = action.payload.repositories;
        state.total = action.payload.total;
        state.page = action.payload.page;
      })
      .addCase(searchRepositories.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(fetchRepository.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchRepository.fulfilled, (state, action) => {
        state.loading = false;
        state.currentRepository = action.payload;
      })
      .addCase(fetchRepository.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearError, clearCurrentRepository } = repositoriesSlice.actions;
export default repositoriesSlice.reducer;
