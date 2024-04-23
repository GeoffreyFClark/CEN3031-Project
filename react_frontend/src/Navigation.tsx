import React, { useState } from 'react';
import { AppBar, Toolbar, Typography, Button, IconButton, Box, Menu, MenuItem, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { Link, useNavigate } from 'react-router-dom';

function Navigation() {
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = useState(null);
  const [navMenuAnchorEl, setNavMenuAnchorEl] = useState(null);
  const [contactDialogOpen, setContactDialogOpen] = useState(false);
  const username = localStorage.getItem('username');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    setAnchorEl(null); 
    setNavMenuAnchorEl(null);
    navigate('/login');
  };

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleNavMenuOpen = (event) => {
    setNavMenuAnchorEl(event.currentTarget);
  };

  const handleNavMenuClose = () => {
    setNavMenuAnchorEl(null);
  };

  const handleContactClick = () => {
    setContactDialogOpen(true);
  };

  const handleContactDialogClose = () => {
    setContactDialogOpen(false);
  };

  const buttonHoverStyle = {
    '&:hover': {
      bgcolor: 'rgba(255, 255, 255, 0.2)'
    }
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <IconButton edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }} onClick={handleNavMenuOpen}>
          <MenuIcon />
        </IconButton>
        <Menu
          id="nav-menu"
          anchorEl={navMenuAnchorEl}
          open={Boolean(navMenuAnchorEl)}
          onClose={handleNavMenuClose}
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'left',
          }}
          transformOrigin={{
            vertical: 'top',
            horizontal: 'left',
          }}
        >
          <MenuItem component={Link} to="/" onClick={handleNavMenuClose}>Home</MenuItem>
          {username && (
            <>
              <MenuItem component={Link} to="/my-resources" onClick={handleNavMenuClose}>My Resources</MenuItem>
              <MenuItem component={Link} to="/add-resource" onClick={handleNavMenuClose}>Add Resource</MenuItem>
            </>
          )}
        </Menu>
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
        <Button color="inherit" onClick={handleContactClick} sx={buttonHoverStyle}>
          Contact Us
        </Button>
        <Dialog open={contactDialogOpen} onClose={handleContactDialogClose}>
          <DialogTitle>Contact Information</DialogTitle>
          <DialogContent>
            <DialogContentText>
              For any questions or feedback, please contact us at:
              <br />
              Email: Support@Communicare.com
              <br />
              Phone: (352) 618-3749
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleContactDialogClose} color="primary">
              Close
            </Button>
          </DialogActions>
        </Dialog>
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