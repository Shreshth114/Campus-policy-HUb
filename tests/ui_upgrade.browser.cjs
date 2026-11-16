const {chromium}=require('playwright'),fs=require('fs'),path=require('path'),assert=require('assert/strict');
(async()=>{
 const root=path.resolve(__dirname,'../web'),browser=await chromium.launch({headless:true}),page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));let mutations=0;
 await page.route('**/*',r=>{
  const u=new URL(r.request().url());if(r.request().method()!=='GET'){mutations++;return r.fulfill({status:503,json:{detail:'Read-only UI fixture'}});}
  const file=u.pathname==='/'?'index.html':u.pathname.slice(1);
  if(['index.html','ui.js','app.js','personal.js','demo.js'].includes(file))return r.fulfill({body:fs.readFileSync(path.join(root,file)),contentType:file.endsWith('js')?'text/javascript':'text/html'});
  if(u.pathname==='/health')return r.fulfill({json:{status:'ok',ready:false,providers:{},chunks:0}});
  if(u.pathname==='/institutions')return r.fulfill({json:{institutions:[]}});
  return r.fulfill({status:404,json:{detail:'No fixture data'}});
 });
 await page.goto('http://127.0.0.1:8049');await page.locator('#help-launcher').waitFor();
 await page.locator('#help-launcher').click();await page.locator('[data-help-topic="upload"]').click();assert((await page.locator('#help-messages').textContent()).includes('Upload & index'));
 await page.locator('#help-input').fill('<script>alert(1)</script>');await page.locator('#help-form button').click();assert.equal(await page.locator('#help-messages script').count(),0);
 await page.keyboard.press('Escape');assert(await page.locator('#help-panel').isHidden());assert(await page.locator('#help-launcher').evaluate(e=>e===document.activeElement));
 await page.keyboard.press('Control+k');await page.locator('#quick-nav-input').fill('documents');await page.keyboard.press('Enter');assert(await page.locator('#view-documents').isVisible());assert.equal(await page.locator('#page-location').textContent(),'My Documents');
 await page.locator('#quick-nav-open').click();await page.locator('#quick-nav-input').fill('zzzzz');assert((await page.locator('#quick-nav-results').textContent()).includes('No matching'));await page.keyboard.press('Escape');
 fs.mkdirSync('docs/screenshots/ui-upgrade',{recursive:true});
 for(const width of [1440,390])for(const theme of ['light','dark']){
  await page.setViewportSize({width,height:950});if(await page.locator('html').getAttribute('data-theme')!==theme)await page.locator('#theme-toggle').click();
  for(const view of ['home','documents','analysis','rulebook','conflicts','changes','compare','bench','evidence','metrics','labels','how','sources']){
   await page.evaluate(v=>document.querySelector('button[data-view="'+v+'"]').click(),view);
   await page.evaluate(()=>Promise.all(document.getAnimations().map(a=>a.finished.catch(()=>{}))));
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,view+' overflow '+width+' '+theme);
   if(['home','analysis','documents','compare'].includes(view))await page.screenshot({path:`docs/screenshots/ui-upgrade/${view}-${width}-${theme}.png`,fullPage:true});
  }
  await page.locator('#header-help').click();await page.evaluate(()=>Promise.all(document.getAnimations().map(a=>a.finished.catch(()=>{}))));await page.screenshot({path:`docs/screenshots/ui-upgrade/help-${width}-${theme}.png`,fullPage:true});await page.locator('#help-close').click();
 }

 // The screenshot controls: real mode binding and safe destructive confirmation.
 await page.evaluate(()=>{document.querySelector('button[data-view="analysis"]').click();document.querySelector('#personal-ask-form details').open=true;});
 await page.locator('[name="retrieval-mode-ui"][value="raw"]').check();assert.equal(await page.locator('#personal-mode').inputValue(),'raw');
 await page.locator('[name="retrieval-mode-ui"][value="hyde"]').focus();await page.keyboard.press('Space');assert.equal(await page.locator('#personal-mode').inputValue(),'hyde');
 await page.evaluate(()=>pSetWorkspace('synthetic-ui-only'));
 for(const width of [1440,390])for(const theme of ['light','dark']){
  await page.setViewportSize({width,height:950});if(await page.locator('html').getAttribute('data-theme')!==theme)await page.locator('#theme-toggle').click();
  await page.evaluate(()=>{document.querySelector('button[data-view="analysis"]').click();document.querySelector('#personal-ask-form details').open=true;});
  await page.locator('.mode-picker').scrollIntoViewIfNeeded();await page.screenshot({path:`docs/screenshots/ui-upgrade/mode-picker-${width}-${theme}.png`,fullPage:true});
  await page.evaluate(()=>document.querySelector('button[data-view="home"]').click());await page.locator('#personal-delete').click();
  assert(await page.locator('.confirm-dialog').isVisible());assert(await page.locator('[data-confirm-cancel]').evaluate(e=>e===document.activeElement));
  await page.screenshot({path:`docs/screenshots/ui-upgrade/delete-dialog-${width}-${theme}.png`});
  await page.keyboard.press('Escape');assert.equal(await page.locator('.confirm-dialog').count(),0);assert(await page.locator('#personal-delete').evaluate(e=>e===document.activeElement));
 }
 await page.evaluate(()=>{window.confirmOutcome=null;CampusUI.confirm({title:'Synthetic confirmation',description:'UI-only test; no deletion callback.',action:'Confirm test'}).then(v=>window.confirmOutcome=v);});
 await page.locator('[data-confirm-accept]').click();assert.equal(await page.evaluate(()=>window.confirmOutcome),true);
 await page.emulateMedia({reducedMotion:'reduce'});assert.equal(await page.locator('.view:not([hidden])').evaluate(e=>getComputedStyle(e).animationName),'none');
 assert.deepEqual(errors,[]);assert.equal(mutations,0);console.log('PASS: 13 views, desktop/mobile light/dark, no horizontal overflow, help topics/escaping/Escape/focus, quick navigation/search/keyboard, reduced motion; no browser errors or mutation requests.');await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
