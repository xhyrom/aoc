export const secondsToHumanReadable = (value: number): string => {
  const hours = Math.floor(value / 60 / 60);
  const minutes = Math.floor((value - hours * 60 * 60) / 60);
  const seconds = value - hours * 60 * 60 - minutes * 60;
  let label = "";
  if (hours > 0) {
    label += `${hours}h `;
  }

  if (minutes > 0) {
    label += `${minutes}m `;
  }

  if (seconds > 0) {
    label += `${seconds.toFixed(0)}s`;
  }
  return label || "-";
};

export const numberFormatter = (value: number): string => {
  if (value === undefined || Number.isNaN(value) || value == 0) {
    return "??";
  }

  return new Intl.NumberFormat().format(value);
};

export const yearsBetween = (
  first: number,
  second: number = new Date().getFullYear(),
): number[] => {
  const years = [];

  if (new Date().getMonth() < 11) {
    second--;
  }
  for (let i = first; i <= second; i++) {
    years.push(i);
  }
  return years;
};
