const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('node:assert/strict');
(async()=>{
 const elements=new Map();let pending;
 function element(){return {value:'',hidden:false,events:{},set innerHTML(html){this.html=html;for(const match of html.matchAll(/<[^>]+\bid="([^"]+)"[^>]*>/g)){const item=element();item.value=(match[0].match(/\bvalue="([^"]*)"/)||[])[1]||'';item.hidden=/\bhidden\b/.test(match[0]);item.markup=match[0];elements.set(match[1],item);}},get innerHTML(){return this.html||'';},appendChild(child){elements.set(child.id,child)},addEventListener(name,fn){this.events[name]=fn}};}
 elements.set('personal-result',element());const escape=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const ctx={document:{getElementById:id=>elements.get(id),createElement:element},window:{personalWorkspaceId:'fixture'},pEsc:escape,PERSONAL_NOTICE:'Unverified fixture',AbortController,console,setTimeout:fn=>{pending=fn;return 1},clearTimeout:()=>{},fetch:async()=>({ok:true,json:async()=>({conditions:[],verdict:'insufficient evidence',scope:'fixture',arithmetic_notice:'arithmetic only'})})};vm.createContext(ctx);
 const source=fs.readFileSync(path.join(__dirname,'../web/personal.js'),'utf8');vm.runInContext(source.slice(source.indexOf('// Scenario values')),ctx);
 ctx.window.CampusWhatIf.mount({conditions:[{rule:{rule_id:'r'}}]},[{subject:'credits',value:'70',unit:'units'}]);
 assert.equal(elements.get('whatif-value-0').value,'70');assert(elements.get('whatif-banner').hidden);assert(elements.get('whatif-results').markup.includes('aria-live="polite"'));
 elements.get('whatif-value-0').value='75';elements.get('whatif-panel').events.input({target:{id:'whatif-value-0',value:'75'}});assert(!elements.get('whatif-banner').hidden);await pending();
 elements.get('whatif-reset').onclick();assert.equal(elements.get('whatif-value-0').value,'70');assert(elements.get('whatif-banner').hidden);
 const rendered=ctx.window.CampusWhatIf.render({conflicted:false,conditions:[],scope:'<script>alert(1)</script>',arithmetic_notice:'<img src=x>'});assert(!rendered.includes('<script>'));assert(!rendered.includes('<img'));
 console.log('What-if DOM checks passed: prefill, scenario banner, reset, aria-live and escaping');
})().catch(error=>{console.error(error);process.exitCode=1});
