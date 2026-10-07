// Markdown raporu Gümrük Koçu tasarımıyla A4 PDF'e çevirir.
// Kullanım: node rapor_pdf.mjs RAPOR.md CIKTI.pdf
// Gereksinim: pandoc, Node için playwright (Chromium). Playwright global kuruluysa NODE_PATH ile gösterin.
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';

const { chromium } = createRequire(import.meta.url)('playwright');

const [, , girdi, cikti] = process.argv;
const LACIVERT = '#1B3A5C';
const ALTIN = '#B8860B';

let govde = execFileSync('pandoc', ['-f', 'gfm', '-t', 'html5', girdi], { encoding: 'utf-8' });

// Markdown'daki ilk başlık bloğunu (H1, H2, marka satırı) kapak sayfasına taşı.
const md = readFileSync(girdi, 'utf-8');
const baslik = (md.match(/^# (.+)$/m) || [, ''])[1];
const altBaslik = (md.match(/^## (.+)$/m) || [, ''])[1];
const tarih = (md.match(/·\s*(.+)$/m) || [, ''])[1];
govde = govde.replace(/^[\s\S]*?<hr \/>/, '');

const html = `<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><title>${baslik}</title>
<style>
  @page { size: A4; margin: 22mm 18mm 20mm 18mm;
    @top-left { content: 'Gümrük Koçu - Ufuk Çetintaş'; font-family: 'Liberation Sans', Arial, sans-serif; font-size: 7.5pt; font-weight: bold; color: ${LACIVERT}; }
    @top-right { content: '${baslik}'; font-family: 'Liberation Sans', Arial, sans-serif; font-size: 7.5pt; color: #6b7785; }
    @bottom-right { content: counter(page) ' / ' counter(pages); font-family: 'Liberation Sans', Arial, sans-serif; font-size: 7.5pt; color: #6b7785; }
  }
  @page :first { @top-left { content: none; } @top-right { content: none; } @bottom-right { content: none; } }
  * { box-sizing: border-box; }
  body { font-family: 'Liberation Sans', Arial, sans-serif; font-size: 10pt; line-height: 1.45; color: #1d1d1f; margin: 0; }
  .kapak { height: 247mm; display: flex; flex-direction: column; justify-content: space-between; page-break-after: always; }
  .kapak .bant { background: ${LACIVERT}; color: #fff; padding: 34mm 14mm 16mm; border-bottom: 3mm solid ${ALTIN}; }
  .kapak .ust { color: ${ALTIN}; font-size: 10pt; letter-spacing: .18em; text-transform: uppercase; font-weight: bold; margin-bottom: 8mm; }
  .kapak h1 { font-size: 30pt; line-height: 1.15; margin: 0 0 6mm; border: 0; color: #fff; }
  .kapak .alt { font-size: 14pt; color: #dbe4ee; }
  .kapak .ozet { padding: 0 14mm; font-size: 11pt; color: #333; }
  .kapak .rakamlar { display: flex; gap: 4mm; padding: 0 14mm; }
  .kapak .rakam { flex: 1; border-top: 1mm solid ${ALTIN}; padding-top: 2.5mm; }
  .kapak .rakam b { display: block; font-size: 20pt; color: ${LACIVERT}; line-height: 1.1; }
  .kapak .rakam span { font-size: 8.5pt; color: #555; }
  .kapak .ozet b { color: ${LACIVERT}; }
  .kapak .imza { padding: 0 14mm 6mm; border-top: 1px solid #d9d9d9; padding-top: 5mm; display: flex; justify-content: space-between; font-size: 10pt; }
  .kapak .imza .marka { color: ${LACIVERT}; font-weight: bold; font-size: 12pt; }
  h1, h2, h3, h4 { color: ${LACIVERT}; page-break-after: avoid; break-after: avoid; }
  h2 { font-size: 15pt; margin: 8mm 0 3mm; padding-bottom: 1.5mm; border-bottom: 1.2mm solid ${ALTIN}; }
  h3 { font-size: 12pt; margin: 6mm 0 2mm; }
  h4 { font-size: 10.5pt; margin: 4mm 0 1.5mm; }
  p { margin: 0 0 2.4mm; }
  ul, ol { margin: 0 0 2.4mm; padding-left: 6mm; }
  li { margin: 0 0 1mm; }
  strong { color: #10263d; }
  code { font-family: 'Liberation Mono', monospace; font-size: 8.8pt; background: #f1f3f6; padding: 0 1mm; border-radius: 1mm; }
  blockquote { margin: 3mm 0; padding: 2.5mm 4mm; border-left: 1.2mm solid ${ALTIN}; background: #fbf7ec; color: #333; page-break-inside: avoid; }
  blockquote p:last-child { margin-bottom: 0; }
  hr { border: 0; border-top: 1px solid #d9d9d9; margin: 5mm 0; }
  table { width: 100%; border-collapse: collapse; margin: 2mm 0 4mm; font-size: 8.6pt; line-height: 1.35; page-break-inside: auto; }
  thead { display: table-header-group; }
  tr { page-break-inside: avoid; break-inside: avoid; }
  th { background: ${LACIVERT}; color: #fff; text-align: left; padding: 1.6mm 2mm; font-weight: bold; }
  td { padding: 1.4mm 2mm; border-bottom: 1px solid #dde2e8; vertical-align: top; }
  tbody tr:nth-child(even) td { background: #f5f7fa; }
  td:empty { background: transparent !important; border-bottom-color: transparent; }
</style></head>
<body>
<section class="kapak">
  <div class="bant">
    <div class="ust">GMY Sınavı · Çıkmış Soru Analizi</div>
    <h1>${baslik}</h1>
    <div class="alt">${altBaslik}</div>
  </div>
  <div class="ozet">
    <p><b>Kapsam:</b> 2021–2025 Gümrük Müşavir Yardımcılığı sınavları, 500 soru ve resmî cevapları. 400 gümrük sorusunun her biri tek tek mevzuat metniyle eşlendi.</p>
    <p><b>Soru:</b> Yazar bu soruyu neden sordu, adayı nerede yakalamak istedi, bir sonraki sınavda aynı maddeden neyi sorar?</p>
  </div>
  <div class="rakamlar">
    <div class="rakam"><b>400</b><span>gümrük sorusu, resmî cevaplarıyla</span></div>
    <div class="rakam"><b>%69</b><span>doğru şık madde metninden birebir</span></div>
    <div class="rakam"><b>%41</b><span>çeldirici komşu hükümden taşınmış</span></div>
    <div class="rakam"><b>18</b><span>beş yıl tekrar eden ikiz kavram ekseni</span></div>
  </div>
  <div class="imza"><span class="marka">Gümrük Koçu - Ufuk Çetintaş</span><span>${tarih}</span></div>
</section>
${govde}
</body></html>`;

const tarayici = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const sayfa = await tarayici.newPage();
await sayfa.setContent(html, { waitUntil: 'load' });
await sayfa.pdf({
  path: cikti,
  format: 'A4',
  printBackground: true,
  preferCSSPageSize: true,
});
await tarayici.close();
console.log('PDF yazıldı:', cikti);
