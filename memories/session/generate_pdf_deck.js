const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

// Uso: node generate_pdf_deck.js <arquivo.html> <arquivo.pdf>
const [, , htmlArg, pdfArg] = process.argv;
if (!htmlArg || !pdfArg) {
  console.error('Uso: node generate_pdf_deck.js <input.html> <output.pdf>');
  process.exit(1);
}

(async () => {
  try {
    const htmlPath = path.resolve(__dirname, htmlArg);
    const pdfPath = path.resolve(__dirname, pdfArg);
    const html = fs.readFileSync(htmlPath, 'utf8');

    let executablePath = process.env.PUPPETEER_EXECUTABLE_PATH || null;
    if (!executablePath) {
      const chromeCandidates = [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '/Applications/Chromium.app/Contents/MacOS/Chromium',
        '/usr/bin/google-chrome-stable',
        '/usr/bin/google-chrome',
        '/usr/bin/chromium-browser',
        '/usr/bin/chromium'
      ];
      for (const p of chromeCandidates) {
        if (fs.existsSync(p)) { executablePath = p; break; }
      }
    }

    const launchOptions = { args: ['--no-sandbox', '--disable-setuid-sandbox'] };
    if (executablePath) launchOptions.executablePath = executablePath;

    const browser = await puppeteer.launch(launchOptions);
    const page = await browser.newPage();
    await page.setViewport({ width: 1600, height: 1000 });
    await page.setContent(html, { waitUntil: 'networkidle0' });

    await page.addStyleTag({ content: `
      @page { size: 1600px 1000px; margin: 0; }
      html, body { width: 1600px; background: var(--bg, #0d0906); }
      body { display: block !important; }
      .deck {
        width: 1600px !important; height: auto !important;
        max-width: none !important; max-height: none !important;
        border-radius: 0 !important; box-shadow: none !important; border: none !important;
        overflow: visible !important;
      }
      .slide {
        position: relative !important; inset: auto !important;
        width: 1600px !important; height: 1000px !important;
        opacity: 1 !important; transform: none !important; pointer-events: auto !important;
        page-break-after: always; break-after: page;
      }
      .slide:last-of-type { page-break-after: auto; break-after: auto; }
      .slide .reveal { opacity: 1 !important; transform: none !important; }
      .progress, .dots, .nav { display: none !important; }
    ` });

    await page.evaluate(() => new Promise(r => setTimeout(r, 400)));

    await page.pdf({
      path: pdfPath,
      width: '1600px',
      height: '1000px',
      margin: { top: 0, right: 0, bottom: 0, left: 0 },
      printBackground: true,
      scale: 1
    });
    await browser.close();

    console.log('PDF criado em:', pdfPath);
  } catch (error) {
    console.error('Erro ao gerar PDF:', error);
    process.exit(1);
  }
})();
