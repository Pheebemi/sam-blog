/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
    ],
    theme: {
        extend: {
            colors: {
                'primary': '#0f182b',
                'dark': {
                    '100': '#1a2435',
                    '200': '#141c2b',
                },
                'light': {
                    '100': '#ffffff',
                    '300': '#94a3b8',
                },
                'secondary': '#3b82f6',
            },
            fontFamily: {
                'poppins': ['Poppins', 'sans-serif'],
            },
            keyframes: {
                slideUp: {
                    '0%': { transform: 'translateY(20px)', opacity: '0' },
                    '100%': { transform: 'translateY(0)', opacity: '1' },
                },
            },
            animation: {
                'slide-up': 'slideUp 0.6s ease forwards',
            },
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('flowbite/plugin')
    ],
}