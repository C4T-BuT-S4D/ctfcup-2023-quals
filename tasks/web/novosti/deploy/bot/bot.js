import { createClient } from "redis";
import puppeteer from "puppeteer";
import fs from "fs";

const REDIS_URL = process.env["REDIS_URL"];
const TASK_URL = process.env["TASK_URL"];
const ADMIN_TOKEN = fs
  .readFileSync(process.env["ADMIN_TOKEN_FILE"], "utf-8")
  .trim();

let browser = null;

async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function visit(storyID) {
  console.log(`Visiting news story ${storyID}`);

  let context = null;
  try {
    if (!browser) {
      const args = [
        "--js-flags=--jitless,--no-expose-wasm",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--no-sandbox",
        "--block-new-web-contents",
      ];

      browser = await puppeteer.launch({
        headless: "new",
        args,
      });
    }

    context = await browser.createIncognitoBrowserContext();

    const page = await context.newPage();
    await page.setCookie({ name: "NOVOSTI_ADMIN_TOKEN", value: ADMIN_TOKEN });
    await page.goto(`${TASK_URL}/news/${storyID}`);
    await sleep(5000);
    await page.close();
  } catch (e) {
    console.log(`Unexpected error: ${e}`);
  } finally {
    if (context) await context.close();
  }
}

async function main() {
  const client = await createClient({
    url: REDIS_URL,
  })
    .on("error", (err) => console.log(`Failed to connect to redis: ${err}`))
    .connect();

  console.log("Connected to redis, waiting on news channel");

  await client.subscribe("news", visit);
}

process.on("SIGTERM", process.exit);
process.on("SIGINT", process.exit);

main();
