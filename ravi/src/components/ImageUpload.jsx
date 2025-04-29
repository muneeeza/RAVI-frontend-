import { motion } from 'framer-motion';
import waveBackground from '../assets/bg3.png';
import {
  Button,
  IconButton,
  Menu,
  MenuItem,
  Paper,
  Typography,
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  Refresh as RestartIcon,
  VolumeUp as VolumeIcon,
  AccountCircle as UserIcon,
  Close as CloseIcon,
  Check as CheckIcon,
} from '@mui/icons-material';
import UploadIcon from '@mui/icons-material/CloudUpload';
import React, { useState, useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';

// Dummy audio URL placeholder
const DEMO_AUDIO_URL = 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3';

const ImageUpload = () => {
  const { t } = useTranslation();

  const [files, setFiles] = useState([]);
  const [ocrText, setOcrText] = useState('');
  const [ocrLoading, setOcrLoading] = useState(false);
  const [audioUrl, setAudioUrl] = useState('');
  const [ttsLoading, setTtsLoading] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  const [showOverlay, setShowOverlay] = useState(true);

  const audioRef = useRef(null);

  // Placeholder OCR function
  const handleOcr = (file) => {
    setOcrLoading(true);
    setTimeout(() => {
      setOcrText('یہ اردو میں ڈیمنسٹریشن کے لیے مثال کا متن ہے'); // <-- DUMMY TEXT
      setOcrLoading(false);
    }, 1500);
  };

  // Placeholder TTS function
  const handleReadAloud = () => {
    if (!ocrText) return;
    setTtsLoading(true);
    setTimeout(() => {
      setAudioUrl(DEMO_AUDIO_URL); // <-- DUMMY AUDIO
      setTtsLoading(false);
      audioRef.current?.play();
    }, 1000);
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setFiles([file]);
    setOcrText('');
    setAudioUrl('');
    setUploadError(null);
    handleOcr(file); // <-- DUMMY OCR call
  };

  const handleClear = () => {
    setFiles([]);
    setOcrText('');
    setAudioUrl('');
    setUploadError(null);
  };

  useEffect(() => {
    return () => {
      files.forEach(f => URL.revokeObjectURL(f.preview));
    };
  }, [files]);

  return (
    <motion.section
      className="relative w-full min-h-screen flex flex-col items-center pt-24 text-center bg-bg_color font-sans"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Background */}
      <div
        className="absolute inset-0 w-full h-full bg-cover bg-center filter blur"
        style={{ backgroundImage: `url(${waveBackground})` }}
      />

      {/* Help Overlay */}
      {showOverlay && (
        <div className="absolute inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60">
          <div className="bg-white rounded-lg shadow-lg p-6 max-w-md text-center">
            <Typography variant="h6" className="mb-2">
              {t('uploadSection.popUpHeading')}
            </Typography>
            <Typography className="mb-4">
              {t('uploadSection.helperText')}
            </Typography>
            <Button
              variant="contained"
              onClick={() => setShowOverlay(false)}
              sx={{ backgroundColor: '#B86544', color: '#fff', borderRadius: '20px', textTransform: 'none' }}
            >
              OK
            </Button>
          </div>
        </div>
      )}

      {/* Upload Section */}
      <div className="w-full max-w-3xl px-4 mb-8 z-20">
        {/* Format Heading */}
        <Typography
          variant="h4"
          className="mb-6 font-bold text-gray-800 font-josefin font-semibold"
          sx={{ fontSize: '1.75rem', letterSpacing: '0.5px' }}
        >
          {t('uploadSection.title')}
        </Typography>

        {/* Upload Area */}
        <div className="relative">
          <Paper
            elevation={3}
            className="border-dashed border-2 border-gray-300 rounded-lg w-full h-[400px] bg-white shadow-lg flex items-center justify-center"
            sx={{ backgroundColor: '#f8f8f8' }}
          >
            {files.length > 0 ? (
              <img
                src={URL.createObjectURL(files[0])}
                alt={files[0].name}
                className="object-contain max-w-full max-h-full rounded-md p-4"
              />
            ) : (
              <label htmlFor="file-upload" className="cursor-pointer flex flex-col items-center space-y-4">
                <input
                  accept="image/*,application/pdf"
                  id="file-upload"
                  type="file"
                  className="hidden"
                  onChange={handleFileUpload}
                />
                <UploadIcon sx={{ fontSize: 60, color: '#B86544' }} />
                <Button
                  variant="contained"
                  component="span"
                  sx={{
                    backgroundColor: '#B86544',
                    color: '#fff',
                    borderRadius: '8px',
                    padding: '12px 32px',
                    fontSize: '1.1rem',
                    textTransform: 'none',
                    '&:hover': { backgroundColor: '#9a5340' }
                  }}
                >
                  Choose File
                </Button>
                <Typography variant="body2" className="text-gray-500 mt-2">
                  Max file size: 5MB
                </Typography>
              </label>
            )}
          </Paper>

          {/* Delete Button */}
          {files.length > 0 && (
            <IconButton
              onClick={handleClear}
              aria-label="clear files"
              className="absolute top-1 left-1 bg-white shadow-md hover:bg-gray-50"
              sx={{
                border: '1px solid #e0e0e0',
                '&:hover': { backgroundColor: '#f5f5f5' }
              }}
            >
              <CloseIcon fontSize="medium" sx={{ color: '#6b6b6b' }} />
            </IconButton>
          )}
        </div>
      </div>

      {/* OCR & TTS Section */}
      <div className="w-full max-w-3xl px-4 mb-12 z-20 space-y-6">
        {ocrLoading && (
          <Typography className="text-gray-600 text-lg">
            {t('uploadSection.loading')}
          </Typography>
        )}

        {ocrText && (
          <Paper className="p-6 rounded-lg shadow-md">
            <div className="space-y-6">
              <Typography variant="h5" className="font-semibold text-gray-800">
                {t('uploadSection.heading')}
              </Typography>

              <div className="bg-gray-50 rounded-md p-4 border border-gray-200">
                <Typography
                  component="pre"
                  className="whitespace-pre-wrap text-gray-800 text-lg leading-relaxed max-h-96 overflow-y-auto"
                >
                  {ocrText}
                </Typography>
              </div>

              <div className="flex items-center gap-4 mt-6">
                <Button
                  onClick={handleReadAloud}
                  disabled={ttsLoading}
                  variant="contained"
                  sx={{
                    backgroundColor: '#B86544',
                    color: '#fff',
                    borderRadius: '25px',
                    padding: '12px 32px',
                    fontSize: '1.1rem',
                    textTransform: 'none',
                    '&:disabled': { opacity: 0.7 }
                  }}
                >
                  {ttsLoading ? 'Generating Audio...' : 'Read Aloud'}
                </Button>

                {audioUrl && (
                  <audio
                    ref={audioRef}
                    controls
                    src={audioUrl}
                    className="flex-1"
                    style={{ minWidth: '200px' }}
                  />
                )}
              </div>
            </div>
          </Paper>
        )}

        {uploadError && (
          <Typography
            color="error"
            className="mt-4 text-lg font-medium text-center"
          >
            {uploadError}
          </Typography>
        )}
      </div>
    </motion.section>
  );
};

export default ImageUpload;