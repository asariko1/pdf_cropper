// BUILD-ONLY FILE — do not upload to the web host.
// Together with in.css this regenerates tailwind.css. Rebuild with:
//   npx tailwindcss@3 -c tailwind.config.js -i in.css -o tailwind.css --minify
//
// Run the command from inside the project folder. `./*.html` matches every HTML
// file there, so renaming copy_deck_finder_styled.html -> index.html needs NO
// change here. Tailwind scans these files for class names; if the pattern matched
// nothing the build would still "succeed" but emit an almost-empty stylesheet and
// the page would lose all styling.
module.exports = {
  content: ['./*.html'],
  // These are added by script.js at runtime, so the scanner can never see them.
  safelist: [
    'bg-white/85',
    'backdrop-blur',
    'border-b',
    'border-slate-100',
    'shadow-sm',
    'py-4',
    'py-6',
    'hidden',
    'flex',
    'opacity-0',
    'opacity-100',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        slate: {
          850: '#1f2937',
        },
      },
    },
  },
  plugins: [],
};
