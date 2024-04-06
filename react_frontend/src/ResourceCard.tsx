import React from 'react';
import { Card, CardContent, CardActions, Button, Typography, Grid, Divider } from '@mui/material';
import { LocationOn, Phone, Email } from '@mui/icons-material';

const ResourceCard = ({ resource }) => {


const formatDescription = (description) => {
    if (description.startsWith('"') && description.endsWith('"')) {
        return description;
    }
    return `"${description}"`;
    };
    
  return (
    <Card sx={{ mb: 2, p: 2 }}>
      <CardContent>
        <Typography variant="h6" component="div" gutterBottom>
          {resource.name}
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" gutterBottom>
          {formatDescription(resource.description)}
        </Typography>
        <Divider sx={{ my: 2 }} />
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
          <Typography variant="body2" color="text.secondary" sx={{ display: 'flex', alignItems: 'flex-start' }}>
            <LocationOn sx={{ mr: 1, mt: '2px' }} />
            <span>
              {resource.address.streetAddress}, {resource.address.addressLocality},{' '}
              {resource.address.addressRegion} {resource.address.postalCode},{' '}
              {resource.address.addressCountry}
            </span>
          </Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2" color="text.secondary">
              <Phone sx={{ verticalAlign: 'middle', mr: 1 }} />
              {resource.phone}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              <Email sx={{ verticalAlign: 'middle', mr: 1 }} />
              {resource.email}
            </Typography>
          </Grid>
        </Grid>
      </CardContent>
      <CardActions>
        <Button size="small" href={resource.url} target="_blank">
          Learn More
        </Button>
      </CardActions>
    </Card>
  );
};
export default ResourceCard;