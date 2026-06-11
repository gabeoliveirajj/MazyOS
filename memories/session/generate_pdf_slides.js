const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

(async () => {
  try {
    const htmlPath = path.resolve(__dirname, 'apresentacao-slides-nutri-chedid.html');
    const pdfPath = path.resolve(__dirname, 'apresentacao-nutri-chedid-SLIDES.pdf');
    const html = fs.readFileSync(htmlPath, 'utf8');

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
    await page.setViewport({ width: 1920, height: 1080 });
    await page.setContent(html, { waitUntil: 'networkidle0' });
    
    // Gerar PDF com tamanho customizado (16:9)
    await page.pdf({ 
      path: pdfPath, 
      width: '1920px',
      height: '1080px',
      margin: { top: 0, right: 0, bottom: 0, left: 0 },
      printBackground: true,
      scale: 1
    });
    await browser.close();

    console.log('PDF de slides criado em:', pdfPath);
  } catch (error) {
    console.error('Erro ao gerar PDF:', error);
    process.exit(1);
  }
})();
