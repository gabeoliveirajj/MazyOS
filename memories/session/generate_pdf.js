const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

(async () => {
  try {
    const htmlPath = path.resolve(__dirname, 'apresentacao-nutri-chedid.html');
    const pdfPath = path.resolve(__dirname, 'apresentacao-nutri-chedid.pdf');
    const html = fs.readFileSync(htmlPath, 'utf8');

    const browser = await puppeteer.launch({ args: ['--no-sandbox', '--disable-setuid-sandbox'] });
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
