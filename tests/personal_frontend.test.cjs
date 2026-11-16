const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const context={module:{exports:{}},console,URL,FormData,XMLHttpRequest:class{}};
vm.createContext(context);vm.runInContext(fs.readFileSync(require('node:path').join(__dirname,'../web/personal.js'),'utf8'),context);
const app=context.module.exports;
assert.equal(app.pEsc('<img onerror="bad()">'),'&lt;img onerror=&quot;bad()&quot;&gt;');
const rule={subject:'attendance',operator:'>=',value:'75',unit:'%',verbatim_quote:'SYNTHETIC TEST FIXTURE <script>bad</script>',document:'Fixture',page:2,exceptions:[]};
assert(!app.pRuleCard(rule).includes('<script>'));assert(app.pRuleCard(rule).includes('page 2'));
const trace={decision:'answered',answer:'Source statement [C1]',citations:['c'],retrieved:[{chunk_id:'c',doc_title:'Fixture',page:2,text_preview:'Source quote',score:.9}],timings_ms:{retrieve:5}};
const answer=app.pRenderAnswer(trace);assert(answer.includes('Based on documents you uploaded. Not verified by your institution.'));assert(!answer.includes('class="message'));assert(answer.includes('Full cited passage'));
const analysis=app.pRenderAnalysis({verdict:'insufficient evidence',scope:'These conditions only',abstained:false,conditions:[{rule,your_value:null,status:'insufficient evidence',reason:'Missing fact'}],missing_facts:['attendance'],explanations:[]});
assert(analysis.includes('<table>'));assert(analysis.includes('Missing facts'));assert(analysis.includes('page 2'));
const secondSource=app.pRenderAnswer({...trace,citations:['second'],retrieved:[{chunk_id:'first',doc_title:'Uncited source',page:1,text_preview:'WRONG PASSAGE',score:.9},{chunk_id:'second',doc_title:'Actual source',page:8,text_preview:'RIGHT PASSAGE',score:.8}]});
assert(secondSource.includes('id="evidence-C2"'));assert(secondSource.includes('<mark>RIGHT PASSAGE</mark>'));assert(!secondSource.includes('<mark>WRONG PASSAGE</mark>'));
assert(!fs.readFileSync(require('node:path').join(__dirname,'../web/index.html'),'utf8').includes('btn-prepared-compare'));
const elements=new Map();context.document={getElementById:id=>{if(!elements.has(id))elements.set(id,{textContent:'',value:'',checked:false,disabled:false});return elements.get(id);}};context.window={};const saved=new Map();context.localStorage={setItem:(k,v)=>saved.set(k,v)};
context.fetch=async(path,options)=>{
 if(path==='/personal/workspaces'){assert(!options.headers.Authorization);return {ok:true,json:async()=>({workspace_id:'temporary-personal-capability'})};}
 assert.equal(options.headers['X-Workspace-ID'],'temporary-personal-capability');return {ok:true,json:async()=>({workspace:{college:'Fixture college'},documents:2,chunks:3,limits:{bytes:1024*1024,pages:20,documents:5}})};
};
(async()=>{
 context.document.getElementById('personal-college').value='Fixture college';await app.pEnsure();assert.equal(saved.get('campus-personal-workspace'),'temporary-personal-capability');assert.equal(context.window.personalWorkspaceId,'temporary-personal-capability');
 assert(context.document.getElementById('personal-count').textContent.includes('2 documents'));
 context.document.getElementById('personal-result').textContent='Old answer';app.pSetWorkspace('other-personal-capability');assert.equal(context.document.getElementById('personal-result').textContent,'');
 assert(!context.document.getElementById('personal-facts-confirmed').checked);
 app.pSelectFiles([{name:'bad.txt'}]);assert(context.document.getElementById('personal-upload').disabled);
 console.log('Personal UI: structured cards, trust labels, quotes, persistence, capability headers, scope clearing and file selection passed');
})().catch(error=>{console.error(error);process.exitCode=1;});
