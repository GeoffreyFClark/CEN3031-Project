import React, { useState } from 'react';
import { Container, Typography, Card, CardContent, CardActions, Button, TextField, Select, MenuItem, Grid, FormHelperText } from '@mui/material';
import ResourceCard from './ResourceCard';


const ResourceList = () => {
  const [resources, setResources] = useState([]);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [category, setCategory] = useState('All');
  const [radius, setRadius] = useState(0);

  const fetchResources = (zip) => {
    console.log(`Searching for zip code: ${zip}, category: ${category}, and radius: ${radius}`);
    const url = 'http://localhost:5000/api/search';
    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        zip: zip, 
        category: category === 'All' ? 'none' : category,
        radius: radius
      }),
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
    console.log("Search query submitted:", searchQuery, "Category:", category, "Radius:", radius);
    fetchResources(searchQuery, category, radius);
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
      <Typography variant="h4" component="h2" align="center" gutterBottom>
        Search Community Resources
      </Typography>
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={4}>
          <FormHelperText>Type</FormHelperText>
          <Select
            fullWidth
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            displayEmpty
            inputProps={{ 'aria-label': 'Without label' }}
            variant="outlined"
            sx={{ mt: 1, mb: 1 }}
          >
            <MenuItem value="All">All</MenuItem>
            <MenuItem value="Food Bank">Food Bank</MenuItem>
            <MenuItem value="Animal">Animal</MenuItem>
            <MenuItem value="Substance Abuse">Substance Abuse</MenuItem>
            <MenuItem value="Veteran">Veteran</MenuItem>
          </Select>
        </Grid>
        <Grid item xs={4}>
        <FormHelperText> </FormHelperText>
          <TextField
            fullWidth
            label="Enter Zip Code"
            variant="outlined"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            sx={{ mt: 1, mb: 1 }}
          />
        </Grid>
        <Grid item xs={4}>
          <FormHelperText>In Radius</FormHelperText>
          <Select
            fullWidth
            value={radius}
            onChange={(e) => setRadius(e.target.value)}
            displayEmpty
            inputProps={{ 'aria-label': 'Without label' }}
            variant="outlined"
            sx={{ mt: 1, mb: 1 }}
          >
            <MenuItem value={0}>0 miles</MenuItem>
            <MenuItem value={10}>10 miles</MenuItem>
            <MenuItem value={25}>25 miles</MenuItem>
            <MenuItem value={50}>50 miles</MenuItem>
            <MenuItem value={100}>100 miles</MenuItem>
          </Select>
        </Grid>
        <Grid item xs={12}>
          <Button
            variant="contained"
            onClick={handleSearch}
            fullWidth
            sx={{ mt: 2, mb: 2 }}
          >
            Search
          </Button>
        </Grid>
      </Grid>
      {error && (
        <Typography color="error" gutterBottom>
          {error}
        </Typography>
      )}

      {resources.map((resource, index) => (
        <ResourceCard key={index} resource={resource} />
      ))}
    </Container>
  );
};

export default ResourceList;