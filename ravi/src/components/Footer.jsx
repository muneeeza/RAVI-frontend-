import React from 'react';

const Footer = () => (
  <footer className="bg-footer text-white py-4">
    <div className="container mx-auto px-6 md:px-12 flex flex-col md:flex-row items-center justify-between space-y-6 md:space-y-0">
      {/* Left Section */}
      <h2 className="text-2xl font-semibold tracking-wide text-center md:text-left">RAVI</h2>


      {/* Right Section */}
      <div className="text-center md:text-right">
        <div className="text-xl md:text-2xl font-bold font-urdu">راوی</div>
      </div>
    </div>

    {/* Bottom Divider with Message */}
    <div className="border-t border-white-700 mt-8 pt-4 text-center text-xs text-white-500">
      A Final Year Project 2025 (BSAI)
    </div>
  </footer>
);

export default Footer;
