// GMY_Soru_Atlasi.html dosyasından A4 PDF üretir. Kullanım: node pdf.js <html> <pdf>
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [src, out] = process.argv.slice(2);
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const b = await chromium.launch({ proxy });
  const p = await b.newPage({ ignoreHTTPSErrors: true, colorScheme: 'light' });
  await p.goto('file://' + path.resolve(src), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForSelector('#mm svg', { timeout: 15000 }).catch(() => console.log('uyarı: konu ağacı çizilemedi'));
  await p.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true, scale: 0.72 });
  await b.close();
})();
