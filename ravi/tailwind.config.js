/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: { 
        teal2: '#67C2C6',
        color3: 'black',
        title_color: '#5C2A4D',
        button_color: '#F4B400',
        bg_color: '#F9FAFB',
        body_text: 'black',
        main_text: '#111827',
        p_1: 'black',
        p_2:'#F3C75B',
        footer: '#3C3C3B',
        btn_2: '#401F71',
        highlight_color: '#F3C75B',

      },
      
      fontFamily: {
        sans: ['DM Sans', 'sans-serif'], 
        josefin: ['"Josefin Sans"', 'sans-serif'],
        quicksand: ['"Quicksand"', 'sans-serif'],// Adds DM Sans as a font option
        montserrat: ['"Montserrat"', 'sans-serif'],
        poppins: ['"Poppins"', 'sans-serif'],
        playfair: ['"Playfair Display"', 'serif'],
        urdu: ['Noto Nastaliq Urdu', 'serif'],
      },
    },
  },
  plugins: [
    require('tailwindcss-rtl'),
  ],
}


