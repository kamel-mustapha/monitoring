/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: ["./src/**/*.{html,ts}"],
  theme: {
    extend: {
      backgroundColor: {
        "dark-primary": "#18191A",
        "dark-secondary": "#3E4042",
        "light-primary": "#ffedd5", //orange-100
        "light-primary-dark": "#fed7aa", //orange-200
        "light-secondary": "#FFF8EE",
        primary: "#0f0e17",
        secondary: "#ff8906",
        hover: "#d36f04",
      },
      colors: {
        "dark-primary": "#fff",
        "dark-secondary": "#9ca3af", //gray-400
        "light-primary": "#030712", //gray-950
        "light-secondary": "#374151", //gray-700
        primary: "#fffffe",
        secondary: "#ff8906",
        button: "#fffffe",
        hover: "#ff8906",
      },
      borderColor: {
        primary: "#e5e7eb", //gray-100
        secondary: "#1f2937", //gray-800
      },
      width: {
        content: "fit-content",
      },
      height: {
        85: "85vh",
        95: "95vh",
        most: "90%",
        content: "fit-content",
      },
      maxWidth: {
        1900: "1920px",
        300: "500px",
        100: "100px",
      },
      minHeight: {
        "85vh": "90vh",
        800: "800px",
      },
      lineHeight: {
        large: "100px",
        medium: "60px",
      },
      gridRowEnd: {
        11: "11",
      },
      fontFamily: {
        changa: ["Changa", "sans"],
        work: ["Work Sans", "arial", "sans"],
        inter: ["Inter", "arial", "sans"],
        poppins: ["Poppins", "arial", "sans"],
        lexend: ["Lexend", "arial", "sans"],
      },
      boxShadow: {
        button: "0 0 10px 1px rgba(0, 0, 0, 0.3)",
        "navbar-light": "3px 3px 0 #ff8906",
      },
      screens: {
        1600: "1600px",
      },
      spacing: {
        "1px": "1px",
      },
    },
  },
  plugins: [],
};
