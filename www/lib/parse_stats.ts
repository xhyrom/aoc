import { JSDOM } from "jsdom";
import { writeFile, mkdir } from "node:fs/promises";

const date = new Date();
const year = process.argv[2] || date.getFullYear();

const res = await (
  await fetch(`https://adventofcode.com/${year}/stats`, {
    headers: {
      "User-Agent":
        "source at github.com/xHyroM/aoc/blob/main/www/lib/parse_stats.ts",
    },
  })
).text();

const parser = new JSDOM(res);
let entries = Array.from(parser.window.document.querySelectorAll("a"));

entries = entries.slice(0, 100);

// get leaderboard-entry div with leaderboard-position span and leaderboard-time span
const parsed = entries
  .map((entry) => {
    const day = entry.textContent?.trim()?.split(" ");
    if (!day || day.length === 0 || !day?.[0]) return null;

    const statsBoth = entry.querySelector(".stats-both")?.textContent?.trim();
    const statsFirstOnly = entry
      .querySelector(".stats-firstonly")
      ?.textContent?.trim();
    if (!statsBoth || !statsFirstOnly) return null;

    return {
      day: parseInt(day[0]),
      both: parseInt(statsBoth),
      first: parseInt(statsFirstOnly),
    };
  })
  .filter((e) => e);

try {
  await mkdir(`${import.meta.dirname}/../src/content/stats`);
} catch (e) {}

await writeFile(
  `${import.meta.dirname}/../src/content/stats/${year}.json`,
  JSON.stringify(parsed, null, 2),
);

export default {};
