module.exports = {
  content: ["./src/**/*.{html,ts}"],
  theme: {
    extend: {
      width: {
        600: "600px",
      },
      maxWidth: {
        1000: "1200px",
      },
      gridTemplateColumns: {
        screen: "repeat(90, 1fr)",
        medium: "repeat(60, 1fr)",
        mobile: "repeat(30, 1fr)",
      },
      fontFamily: {
        changa: ["Changa", "sans"],
        work: ["Work Sans", "arial", "sans"],
        inter: ["Inter", "arial", "sans"],
        poppins: ["Poppins", "arial", "sans"],
        lexend: ["Lexend", "arial", "sans"],
      },
    },
  },
  plugins: [],
};
