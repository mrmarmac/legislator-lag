// Render outputs/figures/*.svg to PNG at twice the drawn size.
//
//   node legislag/figures_png.js
//
// Needs Playwright with Chromium. Run `python -m legislag.figures` first.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const dir = path.join(__dirname, '..', 'outputs', 'figures');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 900, height: 600 }, deviceScaleFactor: 2 });
  for (const file of fs.readdirSync(dir).filter(f => f.endsWith('.svg')).sort()) {
    const svg = fs.readFileSync(path.join(dir, file), 'utf8');
    await page.setContent(`<body style="margin:0">${svg}</body>`);
    await page.locator('svg').screenshot({ path: path.join(dir, file.replace(/\.svg$/, '.png')) });
    console.log('wrote outputs/figures/' + file.replace(/\.svg$/, '.png'));
  }
  await browser.close();
})();
