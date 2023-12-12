import { JSDOM } from "jsdom";
import { writeFile, mkdir } from "node:fs/promises";

const date = new Date();
const day = process.argv[2] || date.getDate();
const year = process.argv[3] || date.getFullYear();

const res = await (
  await fetch(`https://adventofcode.com/${year}/leaderboard/day/${day}`)
).text();

const parser = new JSDOM(res);
let entries = Array.from(
  parser.window.document.querySelectorAll(".leaderboard-entry")
);

entries = entries.slice(0, 100);

// get leaderboard-entry div with leaderboard-position span and leaderboard-time span
const parsed = entries.map((entry) => {
  const position = entry
    .querySelector(".leaderboard-position")
    ?.textContent?.trim()!;
  const time = entry.querySelector(".leaderboard-time")?.textContent?.trim()!;
  const [hours, minutes, seconds] = time.split("  ")[1]!.split(":")!;

  return {
    position: parseInt(position!),
    time: {
      hours: parseInt(hours!),
      minutes: parseInt(minutes!),
      seconds: parseInt(seconds!),
    },
  };
});

const pad = (n: number) => (n < 10 ? `0${n}` : n);

try {
  await mkdir(`${import.meta.dir}/../src/content/lb-${year}`);
} catch (e) {}

await writeFile(
  `${import.meta.dir}/../src/content/lb-${year}/${pad(day)}.json`,
  JSON.stringify(parsed, null, 2)
);

export default {};
