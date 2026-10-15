// Play a pack's replay.json against the Crawler engine, from the town to the far gate.
//
//   node crawler_walk.mjs <crawler root> <pack dir>
//
// <crawler root> is the crawler/ directory of games-osr-fort-on-lake (engine/crawl.js,
// tools/load.mjs). Wandering fights are fought with default orders; a member at death's
// door lets go. Exits 0 when the replay reaches the "end-out" ending, 1 otherwise.
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const [root, packDir] = process.argv.slice(2);
if (!root || !packDir) {
  console.error("usage: node crawler_walk.mjs <crawler root> <pack dir>");
  process.exit(2);
}
const { loadPack } = await import(pathToFileURL(join(resolve(root), "tools", "load.mjs")));
const Crawl = createRequire(import.meta.url)(join(resolve(root), "engine", "crawl.js"));
const pack = loadPack(packDir);
const replay = JSON.parse(readFileSync(join(packDir, "replay.json"), "utf8"));

let s = Crawl.create(pack, { seed: replay.seed });
let fights = 0, refused = 0;

function settle() {
  // A wandering fight or a death can interrupt the walk. Play through it.
  for (let guard = 0; guard < 200; guard++) {
    if (s.mode === "fight") { s = Crawl.step(pack, s, { t: "orders", orders: [] }).state; fights++; }
    else if (s.mode === "deathDoor") s = Crawl.step(pack, s, { t: "letgo" }).state;
    else return;
  }
}

for (const cmd of replay.commands) {
  if (s.mode === "ending") break;
  settle();
  const r = Crawl.step(pack, s, cmd);
  for (const ev of r.events) if (ev.k === "refuse") { refused++; console.log("refused", JSON.stringify(cmd), ev.text); }
  s = r.state;
}
settle();

const log = s.log.slice(-6).join("\n  ");
console.log(`mode ${s.mode}, ending ${s.ending}, turn ${s.turn}, fight rounds ${fights}, refused ${refused}, gold ${s.gold}`);
console.log(`last log lines:\n  ${log}`);
process.exit(s.mode === "ending" && s.ending === "end-out" && refused === 0 ? 0 : 1);
