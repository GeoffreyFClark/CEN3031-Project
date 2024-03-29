import React, { useState }  from 'react';
import { AppBar, Toolbar, Typography, Button, IconButton, Box } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { Link, useNavigate } from 'react-router-dom';

function Navigation() {
  const navigate = useNavigate();
  const [showLogout, setShowLogout] = useState(false);
  const username = localStorage.getItem('username');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/login')
  }

  return (
    <AppBar position="static">
      <Toolbar>

        <IconButton edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }}>
          <MenuIcon />
        </IconButton>

        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          CommuniCare
        </Typography>
        <Button color="inherit" component={Link} to="/">Home</Button>
        <Button color="inherit" component={Link} to="/add-resource">Add Resource</Button>

        {username ? (
          <Box
            sx={{ position: 'relative', display: 'inline-block' }}
            onMouseEnter={() => setShowLogout(true)}
            onMouseLeave={() => setShowLogout(false)}
          >
          
          <Typography variant="h6" component="div" marginLeft={2} sx={{ flexGrow: 0 }}>
            {username}
          </Typography>

          {showLogout && (
            <Button
            color='inherit'
            onClick={handleLogout}
            sx={{
              position: 'absolute',
              top: '100%',
              right: 0,
            }}
            >Logout</Button>
          )}
          </Box>
        ) : (
          <>
            <Button color="inherit" component={Link} to="/login">Login</Button>
            <Button color="inherit" component={Link} to="/register">Register</Button>
          </>
        )}

      </Toolbar>
    </AppBar>
  );
}

export default Navigation;
