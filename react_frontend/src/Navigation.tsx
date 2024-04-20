import React, { useState } from 'react';
import { AppBar, Toolbar, Typography, Button, IconButton, Box, Menu, MenuItem } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { Link, useNavigate } from 'react-router-dom';

function Navigation() {
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = useState(null);
  const username = localStorage.getItem('username');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    setAnchorEl(null); // Reset the anchorEl state
    navigate('/login');
  };

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const buttonHoverStyle = {
    '&:hover': {
      bgcolor: 'rgba(255, 255, 255, 0.2)'
    }
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <IconButton edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }}>
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          CommuniCare
        </Typography>
        <Button color="inherit" component={Link} to="/" sx={buttonHoverStyle}>
          Home
        </Button>
        {username && (
          <>
            <Button color="inherit" component={Link} to="/my-resources" sx={buttonHoverStyle}>
              My Resources
            </Button>
            <Button color="inherit" component={Link} to="/add-resource" sx={buttonHoverStyle}>
              Add Resource
            </Button>
          </>
        )}
        {username ? (
          <Box sx={{ position: 'relative', display: 'inline-block' }}>
            <Button
              color="inherit"
              aria-controls="user-menu"
              aria-haspopup="true"
              onClick={handleMenuOpen}
              sx={buttonHoverStyle}
            >
              {username}
            </Button>
            <Menu
              id="user-menu"
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleMenuClose}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'right',
              }}
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
            >
              <MenuItem onClick={handleLogout}>Logout</MenuItem>
              <MenuItem component={Link} to="/contact" onClick={handleMenuClose}>
                Contact
              </MenuItem>
            </Menu>
          </Box>
        ) : (
          <>
            <Button color="inherit" component={Link} to="/login" sx={buttonHoverStyle}>
              Login
            </Button>
            <Button color="inherit" component={Link} to="/register" sx={buttonHoverStyle}>
              Register
            </Button>
          </>
        )}
      </Toolbar>
    </AppBar>
  );
}

export default Navigation;