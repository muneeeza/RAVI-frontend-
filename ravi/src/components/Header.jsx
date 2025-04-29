import React, { useState } from 'react';
import { AppBar, Toolbar, Button, Menu, MenuItem } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { useNavigate } from 'react-router-dom';
import logo from '../assets/ravi_white.png';
import LanguageSwitcher from './LanguageSwitcher';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';

const Header = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const handleHowItWorksClick = () => {
    if (window.location.pathname === '/') {
      // Already on home page - scroll to section
      const section = document.getElementById('how-it-works');
      section?.scrollIntoView({ behavior: 'smooth' });
    } else {
      // Navigate to home with scroll state
      navigate('/', { state: { scrollToHowItWorks: true } });
    }
  };

  return (
    <AppBar position="fixed" sx={{ backgroundColor: '#3C3C3B', boxShadow: '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)' }}>
      <Toolbar sx={{ display: 'flex', justifyContent: 'space-between', padding: '0 16px' }}>
        {/* Left Section: Navigation Items */}
        <div className="flex items-center space-x-4 ">
          <LanguageSwitcher />

          <Button
            onClick={handleHowItWorksClick}
            sx={{
              textTransform: 'none',
              color: 'white',
              fontWeight: 'bold',
              fontSize: '1.1rem',
            }}
          >
            {t('header.howItWorks')}
          </Button>
        </div>

        {/* Right Section: Logo */}
        <div className="flex items-center">
          <img
            src={logo}
            alt="Logo"
            style={{ height: '60px', transform: 'scale(1.5)', transformOrigin: 'center' }}
          />
        </div>
      </Toolbar>
    </AppBar>
  );
};

export default Header;