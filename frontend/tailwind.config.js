/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // WHY extend? Can add custom colors, fonts, etc. later
      colors: {
        // Git-themed colors
        'git-green': '#28a745',
        'git-red': '#dc3545',
        'git-blue': '#0366d6',
      }
    },
  },
  plugins: [],
}
