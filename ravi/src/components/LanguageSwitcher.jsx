import React, { useState, useEffect } from 'react'; // Fixed import
import { useTranslation } from 'react-i18next';
import Button from '@mui/material/Button';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const LanguageSwitcher = () => {
    const { i18n } = useTranslation();
    const [anchorEl, setAnchorEl] = useState(null);
    const open = Boolean(anchorEl);

    // 1. Fix the useEffect placement
    useEffect(() => {
        const savedLang = localStorage.getItem('i18nextLng') || 'en';
        document.documentElement.lang = savedLang;
        document.documentElement.dir = savedLang === 'ur' ? 'rtl' : 'ltr';
    }, []); // Empty dependency array = runs once on mount

    const handleMenu = (event) => setAnchorEl(event.currentTarget);
    const handleClose = () => setAnchorEl(null);

    const changeLanguage = (lng) => {
        i18n.changeLanguage(lng);
        document.documentElement.lang = lng;
        document.documentElement.dir = lng === 'ur' ? 'rtl' : 'ltr';
        localStorage.setItem('i18nextLng', lng);
        handleClose();
    };

    return (
        <div>
            <Button
                endIcon={<ExpandMoreIcon />}
                onClick={handleMenu}
                sx={{ textTransform: 'none', color: 'white' }}
            >
                {i18n.language.toUpperCase()}
            </Button>

            <Menu
                anchorEl={anchorEl}
                open={open}
                onClose={handleClose}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                transformOrigin={{ vertical: 'top', horizontal: 'right' }}
            >
                <MenuItem onClick={() => changeLanguage('en')}>ENG</MenuItem>
                <MenuItem onClick={() => changeLanguage('ur')}>اردو</MenuItem>
            </Menu>
        </div>
    );
};

export default LanguageSwitcher;