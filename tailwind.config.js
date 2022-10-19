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
        'baskerville': ['"Libre Baskerville"', 'serif']
      },
      colors: {
        "mainColor":"#FF7A00",
        'mainDark': '#0c1023',
        'mainDarkLight': '#191f3a',
        'whiteLight': '#c8c8c8',
      },
      boxShadow: {
        'shadow1': '0 0 15px rgba(0,0,0,0.25)'
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
  },
  plugins: [
    require('flowbite/plugin')
  ]
}
