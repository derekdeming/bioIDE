import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setSearchTerm, setResults } from '../store/slices/searchSlice';
import Search from '../components/Search';
import Filters from '../components/Filters';
import Results from '../components/Results';

const Home = () => {
  const dispatch = useDispatch();
  const searchTerm = useSelector(state => state.search.searchTerm);
  const results = useSelector(state => state.search.results);

  const handleSearch = async (term) => {
    dispatch(setSearchTerm(term));
    
    // Replace this with the actual endpoint and parameters needed for the PubMed API.
    const apiUrl = `https://pubmedapi.endpoint?query=${term}`;
    try {
      const response = await fetch(apiUrl);
      const data = await response.json();
      
      // Update the Redux store with results
      dispatch(setResults(data.results));  // Assuming 'data.results' contains the results.
      
    } catch (error) {
      console.error("There was an error fetching data from PubMed:", error);
    }
  };

  const handleFilter = (filterName) => {
    console.log(`Selected filter: ${filterName}`);
    // Handle the filter logic here.
  };

  return (
    <div>
      <h1>Welcome to the Biology Search</h1>
      <Search onSearch={handleSearch} />
      <Filters onFilter={handleFilter} />
      <Results data={results} />
    </div>
  );
}

export default Home;
