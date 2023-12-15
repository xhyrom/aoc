import config from "@xhyrom/configs/tailwind.config";

/** @type {import('tailwindcss').Config} */
export default {
  ...config({
    content: ["./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}"],
  }),
};
