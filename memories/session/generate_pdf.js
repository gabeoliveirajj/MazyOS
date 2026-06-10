const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

(async () => {
  try {
    const htmlPath = path.resolve(__dirname, 'apresentacao-nutri-chedid.html');
    const pdfPath = path.resolve(__dirname, 'apresentacao-nutri-chedid.pdf');
    const html = fs.readFileSync(htmlPath, 'utf8');

    // Prefer explicit env path (set in CI) then fallback to common locations
    let executablePath = process.env.PUPPETEER_EXECUTABLE_PATH || null;
    if (!executablePath) {
      const chromeCandidates = [
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
    await page.setContent(html, { waitUntil: 'networkidle0' });
    await page.pdf({ path: pdfPath, format: 'A4', printBackground: true });
    await browser.close();

    console.log('PDF criado em:', pdfPath);
  } catch (error) {
    console.error('Erro ao gerar PDF:', error);
    process.exit(1);
  }
})();
