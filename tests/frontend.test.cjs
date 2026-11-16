// Dashboard behavior in a small DOM harness; this is not a visual browser test.
const assert = require('node:assert/strict');
class Element {
  constructor(id='') { this.id=id; this.value=''; this.innerHTML=''; this.textContent=''; this.disabled=false; this.listeners={}; this.dataset={}; this.className=''; this.hidden=false; this.classList={toggle(){}}; }
  addEventListener(name,handler) { this.listeners[name]=handler; }
  appendChild(child) { (this.children??=[]).push(child); }
  scrollIntoView() { this.scrolled=true; }
  focus() { this.focused=true; }
  setAttribute() {}
}
const elements = new Map();
const element = id => { if(!elements.has(id)) elements.set(id,new Element(id)); return elements.get(id); };
const tabs = ['chat','compare','bench','sources'].map(name => {const e=new Element();e.dataset.view=name;return e;});
const views = ['chat','compare','bench','sources'].map(name=>element('view-'+name));
global.document = {getElementById:element, createElement:()=>new Element(),querySelectorAll:selector=>selector==='[data-view]'?tabs:selector==='.view'?views:[]};
global.fetch = async path => ({ok:true,status:200,json:async()=>({chunks:0,production_ready:false})});
const app=require('../web/app.js');
let checks=0;
function test(name,fn) { fn();checks++;console.log('PASS '+name); }
async function main() {
  await new Promise(setImmediate);
  test('untrusted content is escaped',()=>{
    assert.equal(app.escapeHtml('<img src=x onerror="bad()">'), '&lt;img src=x onerror=&quot;bad()&quot;&gt;');
    const html=app.chunkCard({doc_title:'<script>bad()</script>',text_preview:'<img>',score:5,page:1},0);
    assert(!html.includes('<script>'));assert(html.includes('width:100%'));
  });
  test('zero and null metrics stay distinct',()=>{
    assert.equal(app.format(0),'0.000'); assert.equal(app.format(null),'—');
    app.renderBenchmark({metadata:{status:'awaiting_verified_labels',labels_verified:false},retrieval_metrics:{}});
    assert(element('bench-content').innerHTML.includes('No measurements yet'));
    assert(!element('bench-content').innerHTML.includes('width:0%'));
  });
  test('all benchmark views render measured observations safely',()=>{
    app.renderBenchmark({metadata:{status:'completed',labels_verified:true,evaluation_scope:'production'},
      retrieval_metrics:{raw:{recall_at_1:0,recall_at_5:.5,mrr:.25,threshold_sweep:[{threshold:.35,retrieval_acceptance_rate:.5,accepted_without_gold_rate:0}],observations:[{id:'<script>',best_similarity:.1,gold_hit:false}]}},
      safety_metrics:{raw:{citation_validity_rate:0}},decoy_isolation:{raw:[]}});
    const html=element('bench-content').innerHTML;
    assert(html.includes('0.000'));assert(html.includes('width:50%'));assert(html.includes('threshold sweep'));assert(!html.includes('<script>'));
  });
  test('trace separates raw cosine and RRF and shows fallback',()=>{
    app.renderInternals({mode:'fusion',decision:'abstained',abstain_reason:'low_confidence',hyde_failed:true,
      hyde_text:'<fake>',retrieved:[{doc_title:'Fixture',section:'1',page:0,score:.1,rrf_score:.033,approved:true,text_preview:'<data>'}],timings_ms:{total:12}});
    const html=element('internals').innerHTML;
    assert(html.includes('RRF rank score'));assert(html.includes('Cosine similarity'));assert(html.includes('raw retrieval was used'));assert(!html.includes('<fake>'));
  });
  test('compare handles empty results and partial failures',()=>{
    app.renderCompare({raw:{chunks:[],timings_ms:{}},hyde:{chunks:[],error:'<script>error</script>',hyde_failed:true}});
    const html=element('compare-results').innerHTML;
    assert(html.includes('No approved matching'));assert(html.includes('&lt;script&gt;'));assert(!html.includes('<script>'));
  });
  test('all four tabs toggle accessible state',()=>{
    tabs[1].listeners.click();
    assert.equal(element('view-chat').hidden,true);assert.equal(element('view-compare').hidden,false);
    tabs[0].listeners.click();assert.equal(element('view-chat').hidden,false);
  });
  app.switchInstitution('institution-a');
  let resolve,posts=0;
  global.fetch=async()=>{posts++;return await new Promise(r=>resolve=r);};
  element('question').value='<img src=x onerror=bad()>';
  element('mode').value='fusion';
  const first=app.sendQuestion({preventDefault(){}});
  element('question').value='Second request';
  await app.sendQuestion();
  assert.equal(posts,1);assert(element('send-btn').disabled);
  const trace={question:'fixture',mode:'fusion',decision:'answered',answer:'Fixture [C1]',citations:['c1'],retrieved:[{chunk_id:'c1',doc_title:'Fixture',score:.9,approved:true,text_preview:'Fixture'}],timings_ms:{}};
  resolve({ok:true,json:async()=>trace});await first;
  test('duplicate submissions are blocked and citations focus source',()=>{
    assert.equal(posts,1);assert(!element('send-btn').disabled);
    const messages=element('messages').children;
    assert(!messages[0].innerHTML.includes('<img'));
    const last=messages.at(-1);assert(last.innerHTML.includes('data-citation="0"'));
    last.listeners.click({target:{closest:()=>({dataset:{citation:'0'}})}});
    assert(element('chunk-current-0').focused);
  });
  global.fetch=async()=>({ok:false,status:429,json:async()=>({error:'<rate-limit>'})});
  element('question').value='Fixture';await app.sendQuestion();
  test('HTTP errors are escaped and buttons recover',()=>{
    assert(element('messages').children.at(-1).innerHTML.includes('&lt;rate-limit&gt;'));
    assert(!element('send-btn').disabled);
  });
  global.fetch=async path=>({ok:true,json:async()=>path==='/admin/institutions'?{institutions:[]}:{sources:[],chunks:0}});
  element('admin-token').value='fixture-token';
  await element('admin-login').listeners.submit({preventDefault(){}});
  app.switchInstitution('institution-a');
  await app.loadSources();
  test('source and cache dashboards have honest empty state',()=>{
    assert(element('source-list').innerHTML.includes('No source documents'));
    assert(element('admin-summary').innerHTML.includes('uploaded'));
  });
  global.fetch=async()=>{throw new Error('Offline fixture');};
  element('compare-q').value='Fixture';await app.runCompare();
  test('compare network failure recovers controls',()=>{
    assert(element('compare-results').innerHTML.includes('Offline fixture'));
    assert(!element('compare-btn').disabled);
  });
  let late;
  global.fetch=async()=>await new Promise(resolve=>late=resolve);
  element('question').value='Old institution question';
  const pending=app.sendQuestion();
  app.switchInstitution('institution-b');
  // The harness models clearing inner content explicitly.
  element('messages').children=[];
  late({ok:true,json:async()=>trace});await pending;
  test('institution switching clears trace and rejects late answers',()=>{
    assert.equal(element('internals').textContent,'');
    assert.equal(element('compare-results').textContent,'');
    assert.equal(element('messages').children.length,0);
  });

  global.fetch=async path=>({ok:true,json:async()=>path==='/institutions'?{institutions:[]}:{institutions:[{institution_id:'private-a',name:'Private Test University',published:false}]}});
  await app.loadInstitutions();
  test('no published institutions gives an actionable landing state',()=>{
    assert(element('institution-status').textContent.includes('No institutions are published'));
    assert(element('student-entry').disabled);
  });
  element('admin-token').value='fixture-token';await app.unlockAdmin({preventDefault(){}});
  test('admin sign-in exposes a dedicated unpublished workspace selector',()=>{
    assert(!element('admin-controls').hidden);assert(element('admin-institution').innerHTML.includes('Private Test University'));
    assert(element('admin-institution').innerHTML.includes('Unpublished'));
    assert(element('institution').innerHTML.includes('No published institutions'));
  });
  global.fetch=async path=>({ok:true,json:async()=>({institution:{name:'Private Test University',published:false,status:'active'},sources:[],chunks:0})});
  await app.selectAdmin('private-a');
  test('choosing an admin workspace exposes document management',()=>{
    assert(!element('workspace-management').hidden);
    assert(element('admin-publication-status').textContent.includes('Unpublished'));
    assert(element('source-list').innerHTML.includes('Drop PDFs'));
    assert(element('publish-btn').disabled);
  });
  let createdBody;
  global.fetch=async(path,options)=>({ok:true,json:async()=>{
    if(path==='/admin/institutions'&&options.method==='POST'){createdBody=JSON.parse(options.body);return {institution_id:'created-a'};}
    if(path==='/admin/institutions')return {institutions:[{institution_id:'created-a',name:'Created University',published:false}]};
    return {institution:{name:'Created University',published:false,status:'active'},sources:[],chunks:0};
  }});
  element('institution-name').value='Created University';await app.createWorkspace({preventDefault(){}});
  test('name-only creation selects its newly created workspace',()=>{
    assert.deepEqual(createdBody,{name:'Created University'});assert.equal(element('admin-institution').value,'created-a');
    assert(!element('workspace-management').hidden);
  });
  const requests=[];
  global.XMLHttpRequest=class{
    constructor(){this.upload={};}
    open(method,path){this.path=path;requests.push(path);}
    setRequestHeader(key,value){assert.equal(key,'Authorization');assert(value.startsWith('Bearer '));}
    send(body){assert.equal(body.getAll('files').length,1);this.upload.onprogress({lengthComputable:true,loaded:5,total:10});this.status=200;this.responseText=JSON.stringify({documents:[{source:{doc_id:'fixture-doc',original_filename:'fixture.pdf'}}]});queueMicrotask(()=>this.onload());}
  };
  global.fetch=async(path,options)=>{requests.push(path);return {ok:true,json:async()=>path.endsWith('/reindex-current')?{status:'ok',errors:[]}:{institution:{name:'Created University',published:false},sources:[],chunks:1}};};
  const file=new Blob(['%PDF-1.4 fixture'],{type:'application/pdf'});file.name='fixture.pdf';
  app.chooseFiles([file]);element('replacement-id').value='';
  await app.uploadDocuments({preventDefault(){}});
  test('upload progress leads to scoped indexing and explicit pending review',()=>{
    assert.equal(element('upload-progress').value,100);
    assert(requests.includes('/admin/institutions/created-a/documents'));
    assert(requests.includes('/admin/institutions/created-a/sources/fixture-doc/reindex-current'));
    assert(!requests.some(path=>path.includes('/approve')));
    assert(element('upload-status').textContent.includes('Documents remain pending'));
  });
  app.chooseFiles([{name:'bad.txt',size:1}]);
  test('invalid drop selections cannot submit',()=>{assert(element('upload-submit').disabled);});
  global.fetch=async path=>({ok:true,json:async()=>path==='/institutions'?{institutions:[{institution_id:'student-a',name:'Published University',published:true}]}:{production_ready:true}});
  await app.loadInstitutions();element('institution').value='student-a';await app.enterStudent();await new Promise(setImmediate);
  test('student entry preserves selection and names the institution',()=>{
    assert.equal(element('institution').value,'student-a');assert.equal(element('selected-institution-name').textContent,'Published University');
    assert(!element('student-chat').hidden);assert(element('student-empty').hidden);
  });
  global.fetch=async()=>({ok:true,json:async()=>({production_ready:false})});await app.checkStudentReadiness();
  test('no approved evidence shows the exact helpful empty state',()=>{
    assert(element('student-chat').hidden);assert(!element('student-empty').hidden);
    assert(element('student-empty').innerHTML.includes('No verified institutional policies are currently available for this institution. Please contact your institution administrator.'));
    assert(element('send-btn').disabled);
  });
  console.log(`${checks} dashboard checks passed (DOM harness; no visual QA)`);
}
main().catch(error=>{console.error(error);process.exitCode=1;});
