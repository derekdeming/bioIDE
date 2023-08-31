import React, { useState, useEffect } from 'react';
import "./ExploreDatabase.scss";
import axios from 'axios';

const ExploreDatabase = () => {
    const [data, setData] = useState([]);
    const [query, setQuery] = useState('');
    const [selectedDatabase, setSelectedDatabase] = useState(null);
    const [selectedGenre, setSelectedGenre] = useState(null);
    const [selectedDate, setSelectedDate] = useState(null);
    const [selectedFileType, setSelectedFileType] = useState(null);
    const [selectedAuthor, setSelectedAuthor] = useState(null);
    const [selectedStudy, setSelectedStudy] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`http://localhost:3001/pubmed/api/getPubMedData/${query}`);
                if (response.data.error) {
                    console.error('Error fetching data:', response.data.error);
                    return;
                }
                setData(response.data.Data);  // Ensure the data structure matches
            } catch (error) {
                console.error('An error occurred:', error);
            }
        };
        fetchData();
    }, [query]);
    

    const handleSearch = async () => {
        try {
            console.log('Query:', query); // Logging the query
            const response = await axios.get(`http://localhost:3001/pubmed/api/getPubMedData/${query}`);
            console.log('API Response:', JSON.stringify(response.data, null, 2)); // Logging the API response
            if (response.data.error) {
                console.error('Error fetching data:', response.data.error);
                return;
            }
            setData(response.data);  // Update this according to the actual data structure
        } catch (error) {
            console.error('An error occurred:', error);
        }
    };
    

    return (
        <div className="exploreDatabase">
            <div className="side-panel">
                <h2>Filters</h2>
                {/* Database Connection Filter */}
                {/* ...same as before */}
                
                {/* File Type Filter */}
                <label>
                    File Type:
                    <select onChange={(e) => setSelectedFileType(e.target.value)}>
                        <option value="pdf">PDF</option>
                        <option value="doc">DOC</option>
                        <option value="FASTA">FASTA</option>

                    </select>
                </label>

                {/* Author Filter */}
                <label>
                    Author:
                    <input type="text" onChange={(e) => setSelectedAuthor(e.target.value)} />
                </label>

                {/* Study Filter */}
                <label>
                    Study:
                    <input type="text" onChange={(e) => setSelectedStudy(e.target.value)} />
                </label>

            </div>
            <div className="main-panel">
                <h1>Database Exploration</h1>
                <div className="search-bar">
                    <input 
                        type="text" 
                        placeholder="Search..." 
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                    />
                    <button onClick={handleSearch}>Search</button>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Description</th>
                            <th>File Type</th>
                            <th>Author</th>
                            <th>Study</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.map(item => (
                            <tr key={item.id}>
                                <td>{item.id}</td>
                                <td>{item.name}</td>
                                <td>{item.description}</td>
                                <td>{item.fileType}</td>
                                <td>{item.author}</td>
                                <td>{item.study}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ExploreDatabase;
