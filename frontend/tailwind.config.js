/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: 'var(--bg)',
        card: 'var(--card)',
        text: 'var(--text)',
        muted: 'var(--muted)',
        primary: 'var(--primary)',
        accent: 'var(--accent)',
        border: 'var(--border)',
        error: 'var(--error)',
        success: 'var(--success)',
        warning: 'var(--warning)',
      },
    },
  },
  plugins: [],
};