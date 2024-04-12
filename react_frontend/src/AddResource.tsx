import React, { useState } from 'react';
import { TextField, Button, Grid, Paper, Snackbar, MenuItem, Select, InputLabel, FormControl } from '@mui/material';

const AddResource = () => {
  const [name, setName] = useState('');
  const [type, setType] = useState('');
  const [description, setDescription] = useState('');
  const [image, setImage] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [url, setUrl] = useState('');
  const [streetAddress, setStreetAddress] = useState('');
  const [addressLocality, setAddressLocality] = useState('');
  const [addressRegion, setAddressRegion] = useState('');
  const [postalCode, setPostalCode] = useState('');
  const [addressCountry, setAddressCountry] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
  
    if (!name || !type || !description || !email || !phone || !url || !streetAddress || !addressLocality || !addressRegion || !postalCode || !addressCountry) {
      alert('Please fill in all fields.');
      return;
    }
  
    const resource = {
      name,
      description,
      image,
      email,
      phone,
      url,
      address: {
        streetAddress,
        addressLocality,
        addressRegion,
        postalCode,
        addressCountry,
      },
    };
  
    console.log('Sending data:', { type, resource });
  
    const token = localStorage.getItem('access_token');
  
    fetch('http://localhost:5000/api/resources', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`, // Include the JWT token in the Authorization header
      },
      body: JSON.stringify({ type, resource }),
    })
      .then(response => {
        console.log('Received response:', response);
        if (!response.ok) {
          throw new Error('Network response was not ok. Status:', response.status);
        }
        return response.json(); // Convert the response to JSON
      })
      .then(data => {
        console.log('Success:', data);
        setOpenSnackbar(true);
        setName('');
        setType('');
        setDescription('');
        setImage('');
        setEmail('');
        setPhone('');
        setUrl('');
        setStreetAddress('');
        setAddressLocality('');
        setAddressRegion('');
        setPostalCode('');
        setAddressCountry('');
      })
      .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
      });
  };


  const handleCloseSnackbar = () => {
    setOpenSnackbar(false);
  };

  return (
    <Paper sx={{ p: 2 }}>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth sx={{ my: 1 }}>
              <InputLabel id="type-label">Type</InputLabel>
              <Select
                labelId="type-label"
                id="type-select"
                value={type}
                label="Type" // This is necessary for the label to float
                onChange={(e) => setType(e.target.value)}
              >
                <MenuItem value="Food bank">Food Bank</MenuItem>
                <MenuItem value="Animal">Animal</MenuItem>
                <MenuItem value="Substance abuse">Substance Abuse</MenuItem>
                <MenuItem value="Veteran">Veteran</MenuItem>
              </Select>
            </FormControl>
            <TextField fullWidth label="Name" variant="outlined" value={name} onChange={(e) => setName(e.target.value)} sx={{ my: 1 }} />

            <TextField fullWidth label="Description" variant="outlined" value={description} onChange={(e) => setDescription(e.target.value)} sx={{ my: 1 }} />
            <TextField fullWidth label="Email" variant="outlined" value={email} onChange={(e) => setEmail(e.target.value)} sx={{ my: 1 }} />
            <TextField fullWidth label="Phone" variant="outlined" value={phone} onChange={(e) => setPhone(e.target.value)} sx={{ my: 1 }} />
            <TextField fullWidth label="Image URL" variant="outlined" value={image} onChange={(e) => setImage(e.target.value)} sx={{ my: 1 }} />

          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField fullWidth label="Website URL" variant="outlined" value={url} onChange={(e) => setUrl(e.target.value)} sx={{ my: 1 }} />
            <TextField fullWidth label="Street Address" variant="outlined" value={streetAddress} onChange={(e) => setStreetAddress(e.target.value)} sx={{ my: 1 }} />
            <TextField fullWidth label="City/Locality" variant="outlined" value={addressLocality} onChange={(e) => setAddressLocality(e.target.value)} sx={{ my: 1 }} />
            <TextField fullWidth label="State/Region" variant="outlined" value={addressRegion} onChange={(e) => setAddressRegion(e.target.value)} sx={{ my: 1 }} />
            <TextField fullWidth label="Postal Code" variant="outlined" value={postalCode} onChange={(e) => setPostalCode(e.target.value)} sx={{ my: 1 }} />
            <TextField fullWidth label="Country" variant="outlined" value={addressCountry} onChange={(e) => setAddressCountry(e.target.value)} sx={{ my: 1 }} />
          </Grid>
          <Grid item xs={12}>
            <Button type="submit" variant="contained" color="primary" fullWidth>
              Add Resource
            </Button>
          </Grid>
        </Grid>
      </form>
      <Snackbar
        open={openSnackbar}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        message="Resource added successfully!"
      />
    </Paper>
  );
};

export default AddResource;
