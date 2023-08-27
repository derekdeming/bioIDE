import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  searchTerm: '',
  filters: [],
  results: []
};

const searchSlice = createSlice({
  name: 'search',
  initialState,
  reducers: {
    setSearchTerm: (state, action) => {
      state.searchTerm = action.payload;
    },
    setFilters: (state, action) => {
      state.filters = action.payload;
    },
    setResults: (state, action) => {
      state.results = action.payload;
    }
  }
});

export const { setSearchTerm, setFilters, setResults } = searchSlice.actions;
export default searchSlice.reducer;
