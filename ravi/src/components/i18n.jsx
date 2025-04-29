// src/i18n.js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
    en: {
        translation: {
            welcome: "Welcome",
            howItWorks: "How It Works?",
            getStarted: "Get Started",
            uploadImage: "Upload Image",
        }
    },
    ur: {
        translation: {
            welcome: "خوش آمدید",
            howItWorks: "یہ کیسے کام کرتا ہے؟",
            getStarted: "شروع کریں",
            uploadImage: "تصویر اپ لوڈ کریں",
        }
    }
};

i18n
    .use(initReactI18next)
    .init({
        resources,
        lng: 'en', // Default language
        fallbackLng: 'en',
        interpolation: {
            escapeValue: false // React already handles escaping
        }
    });

export default i18n;
