import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { I18nextProvider } from 'react-i18next'; // Add this import
import Header from './components/Header';
import HeroSection from './components/HeroSection';
import HowItWorks from './components/AboutSection';
import ImageUpload from './components/ImageUpload';
import Footer from './components/Footer';
import i18n from './i18n'; // Import the i18n instance created


const App = () => {
  return (
    <I18nextProvider i18n={i18n}> {/* Wrap entire app with this provider */}
      <Router>
        <Header />
        <Routes>
          <Route
            path="/"
            element={
              <>
                <HeroSection />
                <HowItWorks />
                <Footer />
              </>
            }
          />
          <Route path="/get-started" element={<ImageUpload />} />

        </Routes>
      </Router>
    </I18nextProvider>
  );
};

export default App;