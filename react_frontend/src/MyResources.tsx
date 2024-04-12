import React, { useState, useEffect } from 'react';
import { Container, Typography, Grid, CircularProgress, Button } from '@mui/material';
import { Delete } from '@mui/icons-material';
import ResourceCard from './ResourceCard';

const MyResources = () => {
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMyResources();
  }, []);

  const handleDelete = (resourceId) => {
    const url = `http://localhost:5000/api/resources/${resourceId}`;
    const options = {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
    };

    fetch(url, options)
      .then(response => {
        if (response.ok) {
          // Remove the deleted resource from the local state
          setResources(resources.filter(resource => resource.id !== resourceId));
        } else {
          throw new Error('Failed to delete resource');
        }
      })
      .catch(error => {
        console.error('Error deleting resource:', error);
      });
  };

  const fetchMyResources = () => {
    const url = 'http://localhost:5000/api/my-resources';
    const options = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
    };

    fetch(url, options)
      .then(response => response.json())
      .then(data => {
        console.log("My resources:", data);
        if (Array.isArray(data)) {
          setResources(data);
        } else {
          setResources([]);
          setError('Unexpected data format');
        }
        setLoading(false);
      })
      .catch(error => {
        setError(`Error fetching my resources: ${error}`);
        console.error('Error:', error);
        setLoading(false);
      });
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
        My Resources
      </Typography>
      {loading ? (
        <Grid container justifyContent="center">
          <CircularProgress />
        </Grid>
      ) : resources.length === 0 ? (
        <Typography variant="body1" align="center">
          No resources found.
        </Typography>
      ) : (
        <Grid container spacing={2}>
          {resources.map((resource, index) => (
            <Grid item xs={12} key={index}>
              <Grid container spacing={2} alignItems="center">
                <Grid item xs={10}>
                  <ResourceCard resource={resource} />
                </Grid>
                <Grid item xs={2}>
                  <Button
                    variant="outlined"
                    color="error"
                    startIcon={<Delete />}
                    onClick={() => handleDelete(resource.id)}
                  >
                    Delete
                  </Button>
                </Grid>
              </Grid>
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
};

export default MyResources;