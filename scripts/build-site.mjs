import { mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const dist = join(root, "dist");
const serverDir = join(dist, "server");

rmSync(dist, { recursive: true, force: true });
mkdirSync(serverDir, { recursive: true });
mkdirSync(join(dist, ".openai"), { recursive: true });

const assets = [
  ["/index.html", "demo/index.html", "text/html; charset=utf-8"],
  ["/styles.css", "demo/styles.css", "text/css; charset=utf-8"],
  ["/app.js", "demo/app.js", "application/javascript; charset=utf-8"],
  ["/demo_data.js", "demo/demo_data.js", "application/javascript; charset=utf-8"],
];

const assetEntries = assets.map(([route, source, contentType]) => {
  const body = readFileSync(join(root, source), "utf8");
  return [route, { body, contentType }];
});

const serverSource = `const assets = new Map(${JSON.stringify(assetEntries, null, 2)});

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const route = url.pathname === "/" ? "/index.html" : url.pathname;
    const asset = assets.get(route);

    if (!asset) {
      return new Response("Not found", {
        status: 404,
        headers: { "content-type": "text/plain; charset=utf-8" },
      });
    }

    return new Response(asset.body, {
      headers: {
        "content-type": asset.contentType,
        "cache-control": "public, max-age=300",
      },
    });
  },
};
`;

writeFileSync(join(serverDir, "index.js"), serverSource, "utf8");
writeFileSync(
  join(dist, ".openai", "hosting.json"),
  readFileSync(join(root, ".openai", "hosting.json"), "utf8"),
  "utf8"
);

console.log("Built Sites bundle at dist/server/index.js");
