// The footer says what time it is where I am, and how awake I probably am.
const FOOTER = {
  timeZone: "Asia/Kolkata",
  sleepHours: { start: 21, end: 5 },
  intervals: { sleep: 2000, awake: 800 },
  kaomojis: {
    sleeping: [
      "[(－－)]..zzzZ",
      "(－_－) zzZZ",
      "(∪｡∪)｡｡｡ZZzz",
      "(－ω－) ...zzz",
      "(￣o￣) ZZZzzz",
      "(( _ _ ))..zZzZ",
      "(￣ρ￣)..zzZZZ",
      "(－.－)...ZzZz",
      "(＿ ＿*) z Z z Z",
      "(x . x) ~~zZzZ",
    ],
    awake: [
      "(*^ω^)",
      "(´ ∀ `*)",
      "ヽ(・∀・)ﾉ",
      "(☆▽☆)",
      "(✧ω✧)",
      "٩(◕‿◕｡)۶",
      "(っ≧ω≦)っ",
    ],
  },
};

const footer = document.getElementById("footer");
let index = 0;
let timer = null;
let wasAsleep = null;

function localTime() {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: FOOTER.timeZone,
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  }).formatToParts(new Date());
  const hour24 = Number(
    new Intl.DateTimeFormat("en-US", {
      timeZone: FOOTER.timeZone,
      hour: "numeric",
      hour12: false,
    }).format(new Date())
  );
  return {
    hour: hour24 % 24,
    label: parts.map((part) => part.value).join(""),
  };
}

function tick() {
  const { hour, label } = localTime();
  const asleep = hour >= FOOTER.sleepHours.start || hour < FOOTER.sleepHours.end;

  if (wasAsleep !== asleep) {
    wasAsleep = asleep;
    index = 0;
    clearInterval(timer);
    timer = setInterval(
      tick,
      asleep ? FOOTER.intervals.sleep : FOOTER.intervals.awake
    );
  }

  const kaomojis = asleep ? FOOTER.kaomojis.sleeping : FOOTER.kaomojis.awake;
  footer.innerHTML = `it's ${label} here.... <span class="nowrap">${
    kaomojis[index]
  }</span>`;
  index = (index + 1) % kaomojis.length;
}

if (footer) tick();
