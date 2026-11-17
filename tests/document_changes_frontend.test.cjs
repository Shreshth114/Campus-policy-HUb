const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const nodes=new Map();const el=id=>{if(!nodes.has(id))nodes.set(id,{textContent:'Compare',innerHTML:'',disabled:false,value:id==='personal-old-version'?'0':'1',classList:{toggle(){}}});return nodes.get(id);};
let timerId=0;const timers=new Map();
const ctx={module:{exports:{}},console,URL,FormData,AbortController,
 setTimeout:(fn,ms)=>{timers.set(++timerId,{fn,ms});return timerId;},clearTimeout:id=>timers.delete(id)};
vm.createContext(ctx);vm.runInContext(fs.readFileSync(require('node:path').join(__dirname,'../web/personal.js'),'utf8'),ctx);
ctx.document={getElementById:el};
const app=ctx.module.exports,versions=[{document_id:'a',version_id:'old',document:'Fixture A'},{document_id:'b',version_id:'new',document:'Fixture B'}];
(async()=>{
 let resolve,requests=[];
 ctx.fetch=async(path,options)=>{requests.push(path);if(path.endsWith('/rules/extract'))return await new Promise(r=>resolve=r);if(path.endsWith('/rules/activity'))return {ok:true,json:async()=>({status:'running',document:'Fixture A',message:'Processed 3/9 chunks'})};return {ok:true,json:async()=>({status:'completed',changes:[],notice:'Validated rules only'})};};
 const running=app.pCompareVersions(versions);assert(el('personal-compare-versions').disabled);
 await app.pCompareVersions(versions);assert.equal(requests.length,1);
 assert(el('personal-change-results').textContent.includes('Document 1 of 2'));
 const poll=[...timers.values()].find(t=>t.ms===500);await poll.fn();assert(el('personal-change-results').textContent.includes('Processed 3/9'));
 resolve({ok:true,json:async()=>({status:'partial',errors:[{message:'Provider unavailable; retry to resume'}]})});
 await running;
 assert(!requests.some(p=>p.endsWith('/changes')));assert(el('personal-change-results').textContent.includes('retry to resume'));assert(!el('personal-compare-versions').disabled);
 let calls=0;
 ctx.fetch=async path=>{calls++;return {ok:true,json:async()=>path.endsWith('/rules/extract')?{status:'complete',errors:[]}:{status:'completed',changes:[],notice:'Validated rules only'}};};
 await app.pCompareVersions(versions);assert.equal(calls,3);assert(el('personal-change-results').innerHTML.includes('No differences found'));
 ctx.fetch=async path=>({ok:true,json:async()=>path.endsWith('/rules/extract')?{status:'complete',errors:[]}:{status:'blocked',message:'Extraction incomplete',changes:[]}});
 await app.pCompareVersions(versions);assert.equal(el('personal-change-results').textContent,'Extraction incomplete');
 ctx.fetch=async(path,{signal})=>new Promise((resolve,reject)=>signal.addEventListener('abort',()=>reject(new DOMException('aborted','AbortError'))));
 const timeout=app.pApi('/changes',{},undefined,{timeoutMs:123,timeoutMessage:'Timed out; retry'});
 [...timers.values()].find(t=>t.ms===123).fn();await assert.rejects(timeout,/Timed out; retry/);
 console.log('Document changes UI: progress, duplicate prevention, partial/blocked handling, retry, completion and request timeout passed');
})().catch(e=>{console.error(e);process.exitCode=1;});
