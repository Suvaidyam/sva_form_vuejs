/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
     extend: {
      backgroundColor: {
				'primary': 'var(--color-bg-primary)',
				'secondary': 'var(--color-bg-secondary)',
				'tatary': 'var(--color-bg-tatary)',
				'btn-primary': 'var(--color-bg-btn-primary)',
				'btn-secondary': 'var(--color-bg-btn-secondary)',
			},
      textColor:{
        'primary': 'var(--color-text-primary)',
        'secondary': 'var(--color-text-secondary)',
        'tatary': 'var(--color-text-tatary)',
        'pbase': 'var(--color-text-pbase)',
        'sebase': 'var(--color-text-sebase)',
        'trbase': 'var(--color-text-trbase)',
      },
      fontSize: {
        'h1': 'var(--font-size-h1)',
        'h2': 'var(--font-size-h2)',
        'h3': 'var(--font-size-h3)',
        'h4': 'var(--font-size-h4)',
        'h5': 'var(--font-size-h5)',
        'h6': 'var(--font-size-h6)',
      }
    },
  },
  plugins: [],
}

