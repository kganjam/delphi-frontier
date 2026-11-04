import { chromium } from 'playwright-core';
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

// One browser and one page, bounded by the executable's taskpolicy wrapper.
// Read-only: no form submissions, downloads, or scientific job execution.
if (process.env.DELPHI_CAPTURE_ACTIVE) throw new Error('Nested capture refused');
process.env.DELPHI_CAPTURE_ACTIVE = '1';
if (!process.argv[2] || !process.argv[3]) throw new Error('Usage: node capture-sites.mjs TARGETS.json NEW_OUTPUT_DIRECTORY');
const root = path.resolve(process.argv[3]);
try { await fs.access(root); throw new Error('Output directory already exists; use a new directory.'); } catch (error) { if (error.code !== 'ENOENT') throw error; }
await fs.mkdir(root, {recursive: true});
const targets = JSON.parse(await fs.readFile(process.argv[2], 'utf8'));
if (!Array.isArray(targets) || targets.length > 32) throw new Error('Expected at most 32 targets');
const browser = await chromium.launch({
  executablePath: path.join(path.dirname(fileURLToPath(import.meta.url)), 'capped-chromium.sh'),
  headless: true, args: ['--single-process', '--no-zygote', '--disable-gpu', '--renderer-process-limit=1'],
  timeout: 30000
});
const results = [];
try {
  const page = await browser.newPage({viewport: {width:1920,height:1080}, deviceScaleFactor:1});
  for (const target of targets) {
    const url = new URL(target.url);
    if (!['delphibio.org','studio.morphoswarm.ai','morphoswarm.ai'].includes(url.hostname)) throw new Error('Out-of-scope host');
    if (!/^[a-z0-9-]+$/.test(target.id)) throw new Error('Unsafe artifact id');
    try {
      await page.goto(target.url, {waitUntil:'domcontentloaded',timeout:30000});
      await page.waitForFunction(() => document.body && document.body.innerText.length > 500, {timeout:20000});
      await page.waitForLoadState('networkidle', {timeout:8000}).catch(()=>{});
      await page.evaluate(() => document.fonts.ready);
      if (target.text) await page.getByText(target.text, {exact:false}).first().waitFor({state:'visible',timeout:15000});
      const record = await page.evaluate(() => ({
        url:location.href,title:document.title,text:document.body.innerText,
        links:[...document.querySelectorAll('a[href]')].map(a=>({text:a.innerText.trim(),url:a.href})),
        media:[...document.querySelectorAll('video,source,img')].map(a=>({tag:a.tagName,src:a.src,alt:a.alt||'',poster:a.poster||''}))
      }));
      await fs.writeFile(path.join(root,target.id+'.json'),JSON.stringify(record,null,2)+'\n');
      await fs.writeFile(path.join(root,target.id+'.txt'),record.text+'\n');
      const imageFile = path.join(root,target.id+'.png');
      await page.screenshot({path:imageFile,animations:'disabled',fullPage:!!target.full});
      if (target.selector) {
        const componentStyle = target.cleanChrome ? 'header, nav { visibility: hidden !important; }' : '';
        await page.locator(target.selector).first().screenshot({path:path.join(root,target.id+'-detail.png'),animations:'disabled',style:componentStyle});
      }
      const result = {id:target.id,url:record.url,title:record.title,characters:record.text.length,links:record.links.length,
        captured_at:new Date().toISOString(),sha256:crypto.createHash('sha256').update(await fs.readFile(imageFile)).digest('hex'),
        component_capture_style:target.cleanChrome ? 'Navigation/header hidden only for clean component screenshot; scientific content unchanged.' : null};
      results.push(result); console.log(JSON.stringify(result));
    } catch (e) {
      results.push({id:target.id,url:target.url,error:String(e)}); console.log(JSON.stringify(results.at(-1)));
    }
  }
} finally { await browser.close(); }
await fs.writeFile(path.join(root,'capture-manifest-'+Date.now()+'.json'),JSON.stringify(results,null,2)+'\n');
