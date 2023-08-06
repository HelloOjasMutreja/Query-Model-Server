/** @type {import('tailwindcss').Config} */
module.exports = {
  purge: [
    './templates/*.html',
    './**/*.js',
    './randomizer/templates/randomizer/*.html',
    './accounts/templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}