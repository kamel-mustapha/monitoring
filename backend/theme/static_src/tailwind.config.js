/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
  content: ["../../templates/**/*.html"],
  theme: {
    extend: {
      backgroundColor: {
        primary: "#0f0e17",
        secondary: "#ff8906",
        hover: "#d36f04",
      },
      colors: {
        primary: "#fffffe",
        secondary: "#ff8906",
        button: "#fffffe",
        hover: "#ff8906",
      },
      borderColor: {
        primary: "#ff8906",
      },
      width: {
        content: "fit-content",
        400: "400px",
        550: "550px",
      },
      height: {
        85: "85vh",
        content: "fit-content",
      },
      maxWidth: {
        1900: "1920px",
        300: "500px",
        1400: "1250px",
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
        work: ["Work Sans", "arial", "sans"],
        poppins: ["Poppins", "arial", "sans"],
        inter: ["Inter", "arial", "sans"],
        lexend: ["Lexend", "arial", "sans"],
      },
      boxShadow: {
        button: "0 0 10px 1px rgba(0, 0, 0, 0.3)",
      },
    },
  },
  plugins: [
    /**
     * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
     * for forms. If you don't like it or have own styling for forms,
     * comment the line below to disable '@tailwindcss/forms'.
     */
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/line-clamp"),
    require("@tailwindcss/aspect-ratio"),
  ],
};
