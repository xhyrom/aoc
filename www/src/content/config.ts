import { defineCollection } from "astro:content";
import { readdir } from "node:fs/promises";

const __dirname = new URL(".", import.meta.url).pathname;

const years = await readdir(__dirname);
years.shift();

export const yearsMap = Object.fromEntries(
  years.map((year) => [year, defineCollection({ type: "data" })])
);

export const collections = {
  ...yearsMap,
};
