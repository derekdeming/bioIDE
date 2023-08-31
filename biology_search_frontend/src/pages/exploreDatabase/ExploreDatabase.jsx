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
        // Mock database call, will replace this with actual data from the API later
        const fetchData = async () => {
            const response = [
                {id: 1, name: 'Sample 1', description: 'Description 1', fileType: 'PDF', author: 'Author 1', study: 'Study 1'},
                {id: 2, name: 'Sample 2', description: 'Description 2', fileType: 'DOC', author: 'Author 2', study: 'Study 2'},
                // ... more data
            ];
            setData(response);
        };
        fetchData();
    }, []);

    const handleSearch = async () => {
        try {
            const response = await axios.get(`/getPubMedData/${query}`);
            if (response.data.error) {
                console.error('Error fetching data:', response.data.error);
                return;
            }
            setData(response.data.Data);  // Update the data state
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
