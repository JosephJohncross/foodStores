/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/*.html', 
    './templates/**/*.html',
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {
      backgroundImage: {
        'register': "url(images/register.jpg)"
      },
      fontFamily: {
        'dancing': ['"Dancing Script"', 'cursive'],
        'poppin': ['Poppins', 'sans-serif'],
        'baskerville': ['"Libre Baskerville"', 'serif'],
        'spartan': ['"League Spartan"', 'sans-serif'],
        'monserat': ['"Montserrat"', 'sans-serif']
      },
      colors: {
        "mainColor":"#FF7A00",
        'mainDark': '#0c1023',
        'mainDarkLight': '#191f3a',
        'whiteLight': '#c8c8c8',
      },
      boxShadow: {
        'shadow1': '0 0 15px rgba(0,0,0,0.25)',
        'darkShadow1': '0px 0px 50px 5px #0ff',
        'darkCard1': '0px 0px 50px 5px #eb94ce',
        'darkCard2': '0px 0px 50px 5px #82b0e3',
        'darkCard3': '0px 0px 50px 5px #82b0e3',
        'darkCard4': '0px 0px 50px 5px #a1e5af',
        'darkCard4': '0px 0px 50px 5px #fa8e29',
      },
      keyframes: {
        scale: {
          '0%, 100%': { transform: 'scale(1)' },
          '50%': { transform: 'rotate(1.3)' },
        }
      },
      animation: {
        'scale': 'scale 3s linear infinite',
      }
    },
    data: {
      pressed: "pressed ~= 'aria-pressed' "
    }
  },
  plugins: [
    require('flowbite/plugin')
  ]
}
