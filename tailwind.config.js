/** @type {import('tailwindcss').Config} */
module.exports = {
  purge: [
    './templates/*.html',
    './**/*.js',
    './randomizer/**/**/*.html',
    './accounts/**/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}