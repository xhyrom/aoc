import config from "@xhyrom/configs/tailwind.config";

/** @type {import('tailwindcss').Config} */
export default {
  ...config({
    content: ["./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}"],
    theme: {
      backgroundImage: {
        primaryDottedFooter: "radial-gradient(#D5D5B8 1px, #ECECE2 1px)",
      },
      backgroundSize: {
        primaryDottedSize: "15px 15px",
      },
    },
  }),
};
