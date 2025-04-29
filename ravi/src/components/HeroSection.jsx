import React from 'react';
import { motion } from 'framer-motion'; // Import Framer Motion for animations
import Button from '@mui/material/Button';
import { Link } from 'react-router-dom';
import bg_ver2 from '../assets/bg3.png';
import { useTranslation } from 'react-i18next';

const HeroSection = () => {
  const { t, i18n } = useTranslation();
  return (
    <motion.section
      className="relative w-full h-screen flex items-center justify-center text-center bg-grey bg-contain overflow-hidden"
      initial={{ opacity: 5, y: 10 }} // Start with opacity 0 and slight downward movement
      animate={{ opacity: 5, y: 0 }} // Animate to full opacity and back to position
      exit={{ opacity: 0, y: -5 }} // Animate upward fade out when exiting
      transition={{ duration: 0.4, ease: 'easeOut' }} // Smooth animation transition 
    >
      {/* Background with Gradient Overlay */}
      <div
        className="absolute inset-0 w-full h-full bg-cover bg-no-repeat"
        style={{ backgroundImage: `url(${bg_ver2})` }}>

        {/* Gradient Overlay */}
        {/* <div className="absolute inset-0 bg-gradient-to-t from-gray-300/50 to-transparent z-10"></div> */}

      </div>

      {/* Content on Top of Image */}
      <div className="relative z-10 p-5 max-w-2xl mx-auto">
        {/* Title */}
        <motion.h1
          className="text-6xl md:text-9xl font-josefin font-semibold mb-6 md:mb-8 rtl:mb-10 rtl:md:mb-16 text-title_color text-center rtl:font-urdu ltr:font-josefin"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.6, ease: 'easeOut' }}
        >
          {t('RAVI')}
        </motion.h1>

        <motion.h2
          className="text-4xl font-josefin mb-4 md:mb-5 rtl:mb-6 rtl:md:mb-8 font-semibold text-center rtl:font-urdu ltr:font-quicksand"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.6, ease: 'easeOut' }}
        >
          {t('heroTitle')}
        </motion.h2>

        {/* Description */}
        <motion.p
          className="max-w-lg mx-auto text-lg md:text-xl mb-8 font-quicksand  rtl:font-urdu ltr:font-quicksand"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.6, ease: 'easeOut' }}
          style={{ color: 'color3' }}
        >
          {t('heroText')}
        </motion.p>

        {/* Get Started Button */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.8, duration: 0.5, ease: 'easeOut' }}
        >
          <Link to="/get-started">
            <Button
              className="rtl:font-urdu ltr:font-quicksand"
              variant="contained"
              style={{
                backgroundColor: '#F4B400',
                color: 'black',
                borderRadius: '25px',
                padding: '14px 35px',
                fontWeight: 'bold',
                fontSize: '1.2rem',
                transition: 'transform 0.2s ease-in-out',
              }}
              size="large"
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'scale(1.05)';
                e.currentTarget.style.backgroundColor = '#D99A00';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'scale(1)';
                e.currentTarget.style.backgroundColor = '#F4B400';
              }}
            >
              {t('btnText')}

            </Button>
          </Link>
        </motion.div>
      </div>
    </motion.section>
  );
};

export default HeroSection;
