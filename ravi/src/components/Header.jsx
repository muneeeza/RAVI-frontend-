import React, { useState, useEffect } from 'react';
import { AppBar, Toolbar, Button, Menu, MenuItem } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import logo from '../assets/ravi_white.png';
import LanguageSwitcher from './LanguageSwitcher';
import { useTranslation } from 'react-i18next';

const Header = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  
  const handleHowItWorksClick = () => {
    if (window.location.pathname === '/') {
      const section = document.getElementById('how-it-works');
      section?.scrollIntoView({ behavior: 'smooth' });
    } else {
      navigate('/', { state: { scrollToHowItWorks: true } });
    }
  };

  // ======= HEALTH CHECK CODE START =======
  const [ttsOk, setTtsOk] = useState(null);

  useEffect(() => {
    fetch('/health/tts')
      .then((res) => {
        if (!res.ok) throw new Error();
        return res.json();
      })
      .then((data) => setTtsOk(true))
      .catch(() => setTtsOk(false));
  }, []);

  const renderHealthStatus = () => {
    return (
      <div className="flex items-center space-x-2 ml-4">
        <div
          className={`w-3 h-3 rounded-full ${
            ttsOk === null
              ? 'bg-gray-400 animate-pulse'
              : ttsOk
              ? 'bg-green-500'
              : 'bg-red-500'
          }`}
        />
        <span className="text-xs text-white">
          {ttsOk === null
           ? t('header.ttsCheck')
           : ttsOk
           ? t('header.ttsOK')
           : t('header.ttsError')}
        </span>
      </div>
    );
  };
  // ======= HEALTH CHECK CODE END =======

  return (
    <AppBar
      position="fixed"
      sx={{
        backgroundColor: '#3C3C3B',
        boxShadow: '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)',
      }}
    >
      <Toolbar
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          padding: '0 16px',
        }}
      >
        {/* Left Section: Language Switcher and Navigation */}
        <div className="flex items-center space-x-4">
          <LanguageSwitcher />

          <Button
            onClick={handleHowItWorksClick}
            sx={{
              textTransform: 'none',
              color: 'white',
              fontSize: '1rem',
            }}
          >
            {t('header.howItWorks')}
          </Button>
        </div>

        <div>
          {renderHealthStatus()}
        </div>

        {/* Right Section: Logo */}
        <div className="flex items-center">
          <img
            src={logo}
            alt="Logo"
            style={{
              height: '60px',
              transform: 'scale(1.5)',
              transformOrigin: 'center',
            }}
          />
        </div>
      </Toolbar>
    </AppBar>
  );
};

export default Header;