/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,ts}"],
  theme: {
    extend: {
      backgroundColor: {
        primary: "#0f0e17",
        secondary: "#ff8906",
        hover: "#d36f04",
      },
      colors: {
        primary: "#fffffe",
        secondary: "#a7a9be",
        button: "#fffffe",
        hover: "#ff8906",
      },
      borderColor: {
        primary: "#ff8906",
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
        Changa: ["Changa", "sans"],
      },
      boxShadow: {
        button: "0 0 10px 1px rgba(0, 0, 0, 0.3)",
      },
      screens: {
        1600: "1600px",
      },
    },
  },
  plugins: [],
};
