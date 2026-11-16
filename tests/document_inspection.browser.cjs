// Read-only local browser verification. Target JSON stays outside the repo and contains a capability.
// Usage: NODE_PATH=/path/to/node_modules node tests/document_inspection.browser.cjs
const {chromium}=require('playwright'),fs=require('node:fs'),assert=require('node:assert/strict');
(async()=>{
 const target=JSON.parse(fs.readFileSync(process.env.INSPECTION_TARGETS || '/private/tmp/inspection-targets.json'))[0];
 const expected=JSON.parse(fs.readFileSync(process.env.INSPECTION_CHUNKS || '/private/tmp/inspection-chunks.json'));
 const browser=await chromium.launch({headless:true});const page=await browser.newPage({viewport:{width:1440,height:1000}});const errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.route('**/*',route=>{
  const u=new URL(route.request().url());
  if(u.protocol==='blob:')return route.continue();
  if(u.hostname!=='127.0.0.1')return route.abort();
  if(route.request().method()!=='GET')return route.abort();
  if(u.pathname.startsWith('/institutions'))return route.fulfill({json:{institutions:[]}});
  if(u.pathname.startsWith('/admin'))return route.abort();
  return route.continue();
 });
 await page.addInitScript(wid=>localStorage.setItem('campus-personal-workspace',wid),target.workspace);
 await page.goto('http://127.0.0.1:8000');
 await page.locator('#primary-tabs [data-view="documents"]').click();
 await page.locator(`[data-p-detail="${target.doc_id}"]`).click();
 await page.locator('#personal-preview').waitFor();
 await page.locator('#personal-inspection-body details').first().locator('summary').click();
 await page.locator('#personal-preview').click();await page.locator('#personal-original iframe').waitFor();
 await page.locator('#personal-close-preview').click();assert(await page.locator('#personal-original').isHidden());
 assert(await page.locator('#personal-inspection-body details').first().getAttribute('open')!==null);
 assert(await page.locator('#personal-preview').evaluate(e=>e===document.activeElement));
 await page.locator('#personal-preview').click();await page.locator('#personal-original iframe').waitFor();await page.keyboard.press('Escape');assert(await page.locator('#personal-original').isHidden());
 await page.locator('#personal-document-back').click();
 await page.locator(`[data-p-chunks="${target.doc_id}"]`).click();await page.locator('#personal-chunk-select').waitFor();
 assert.equal(await page.locator('#personal-chunk-select option').count(),77);
 for(let i=0;i<77;i++){
  await page.locator('#personal-chunk-select').selectOption(String(i));
  assert.equal(await page.locator('.stored-chunk-text').textContent(),expected.chunks[i].text);
  const text=await page.locator('#personal-chunk-content').textContent();
  assert(text.includes(expected.chunks[i].chunk_id));assert(text.includes('Source page: '+expected.chunks[i].page));
 }
 assert(await page.locator('#personal-chunk-next').isDisabled());await page.locator('#personal-chunk-prev').click();assert.equal(await page.locator('#personal-chunk-select').inputValue(),'75');await page.locator('#personal-chunk-next').click();
 await page.locator('#personal-chunk-select').selectOption('0');assert(await page.locator('#personal-chunk-prev').isDisabled());
 fs.mkdirSync('docs/screenshots/document-inspection',{recursive:true});
 for(const width of [1440,390])for(const theme of ['light','dark']){
  await page.setViewportSize({width,height:900});await page.evaluate(t=>document.documentElement.dataset.theme=t,theme);await page.evaluate(()=>Promise.all(document.getAnimations().map(a=>a.finished.catch(()=>{}))));
  await page.locator('#personal-document-back').scrollIntoViewIfNeeded();
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  await page.screenshot({path:`docs/screenshots/document-inspection/chunks-${width}-${theme}.png`,fullPage:true});
 }
 await page.locator('#personal-document-back').click();assert(await page.locator(`[data-p-chunks="${target.doc_id}"]`).isVisible());
 // Empty/missing metadata and error states use explicit browser fixtures, never mutate data.
 const chunksUrl='**/personal/documents/*/chunks';
 await page.route(chunksUrl,r=>r.fulfill({json:{filename:'SYNTHETIC empty fixture',chunks:[],total:0}}));
 await page.locator(`[data-p-chunks="${target.doc_id}"]`).click();await page.getByText('No stored chunks are available', {exact:false}).waitFor();await page.locator('#personal-document-back').click();
 await page.unroute(chunksUrl);
 await page.route(chunksUrl,r=>r.fulfill({json:{filename:'SYNTHETIC metadata fixture',chunks:[{text:'Exact\n  whitespace <script>unsafe</script>'}],total:1}}));
 await page.locator(`[data-p-chunks="${target.doc_id}"]`).click();await page.locator('.stored-chunk-text').waitFor();assert.equal(await page.locator('.stored-chunk-text').textContent(),'Exact\n  whitespace <script>unsafe</script>');assert((await page.locator('#personal-chunk-content').textContent()).includes('Source page: Unavailable'));assert.equal(await page.locator('#personal-chunk-content script').count(),0);await page.locator('#personal-document-back').click();await page.unroute(chunksUrl);
 await page.route(chunksUrl,r=>r.fulfill({status:503,json:{detail:'Fixture storage unavailable'}}));await page.locator(`[data-p-chunks="${target.doc_id}"]`).click();await page.getByText('Chunks unavailable. Fixture storage unavailable').waitFor();await page.locator('#personal-document-back').click();await page.unroute(chunksUrl);
 await page.locator(`[data-p-detail="${target.doc_id}"]`).click();await page.locator('#personal-preview').click();await page.locator('#personal-original iframe').waitFor();
 for(const width of [1440,390])for(const theme of ['light','dark']){
  await page.setViewportSize({width,height:900});await page.evaluate(t=>document.documentElement.dataset.theme=t,theme);await page.evaluate(()=>Promise.all(document.getAnimations().map(a=>a.finished.catch(()=>{}))));await page.locator('#personal-close-preview').scrollIntoViewIfNeeded();assert(await page.locator('#personal-close-preview').isVisible());assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);await page.screenshot({path:`docs/screenshots/document-inspection/preview-${width}-${theme}.png`,fullPage:true});
 }
 await page.locator('#personal-close-preview').click();assert.deepEqual(errors,[]);
 console.log('PASS: close/focus/Escape/state; all 77 exact stored chunks and pages; prev/next/jump/back; empty/missing/error/escaping; desktop/mobile light/dark; no browser errors.');
 await browser.close();
})().catch(e=>{console.error(e.message);process.exit(1)});
