import React, { useState } from 'react';
import { Container, Typography, Card, CardContent, CardActions, Button, TextField } from '@mui/material';

const ResourceList = () => {
  const [resources, setResources] = useState([]);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  const fetchResources = (zip) => {
    console.log(`Searching for zip code: ${zip}`);
    const url = 'http://localhost:5000/api/search';
    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ zip: zip }), // Send the zip code under the 'zip' key
    };

    fetch(url, options)
      .then(response => response.json())
      .then(data => {
        console.log("Search results:", data);
        if (Array.isArray(data)) {
          setResources(data);
        } else {
          // Handle unexpected data format gracefully
          setResources([]); // Clear previous results or set to a default state
          setError('Unexpected data format');
        }
      })
      .catch(error => {
        setError(`Error fetching resources: ${error}`);
        console.error('Error:', error);
      });
  };

  const handleSearch = () => {
    setError(null); // Clear previous errors
    if (!searchQuery) {
      setError('Please enter a search query');
      return;
    }
    console.log("Search query submitted:", searchQuery);
    fetchResources(searchQuery);
  };

  if (error) {
    return (
      <Container maxWidth="sm">
        <Typography variant="h4" component="h2" gutterBottom>
          Error: {error}
        </Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" component="h2" gutterBottom>
        Search Community Resources by Zip Code
      </Typography>
      <TextField
        fullWidth
        label="Enter Zip Code"
        variant="outlined"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        margin="normal"
        onKeyPress={(e) => {
          if (e.key === 'Enter') handleSearch();
        }}
      />
      <Button variant="contained" onClick={handleSearch} sx={{ mb: 2 }}>
        Search
      </Button>

      {resources.map((resource, index) => (
        <Card key={index} sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="h5" component="div">
              {resource.name}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {resource.description}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Address: {resource.address.streetAddress}, {resource.address.addressLocality}, {resource.address.addressRegion} {resource.address.postalCode}, {resource.address.addressCountry}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Phone: {resource.phone}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Email: {resource.email}
            </Typography>
          </CardContent>
          <CardActions>
            <Button size="small" href={resource.url} target="_blank">
              Learn More
            </Button>
          </CardActions>
        </Card>
      ))}
    </Container>
  );
};

export default ResourceList;
