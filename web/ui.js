'use strict';
(function(root){
 const escape=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 function render(text,options={}){
  const inline=value=>value.replace(/\*\*([^*\n]+)\*\*/g,'<strong>$1</strong>').replace(/(?<!\*)\*([^*\n]+)\*(?!\*)/g,'<em>$1</em>').replace(/\[C(\d+)\]/g,(all,n)=>Number(n)>0&&Number(n)<=(options.maxCitation??1000)?`<a class="citation" data-citation="${Number(n)-1}" href="#evidence-C${Number(n)}">[C${Number(n)}]</a>`:all);
  let html='',list=false;
  for(const line of escape(text).split(/\r?\n/)){
   const bullet=line.match(/^\s*[-*•]\s+(.+)$/);
   if(bullet){if(!list){html+='<ul>';list=true;}html+='<li>'+inline(bullet[1])+'</li>';}
   else{if(list){html+='</ul>';list=false;}html+=inline(line)+'<br>';}
  }
  return html+(list?'</ul>':'');
 }
 function footer(personal=true){return personal?'Answers are based on documents you uploaded. They have not been verified by your institution.':'Answers cite reviewed source passages. Insufficient evidence leads to abstention.';}
 function init(){
  const trigger=document.getElementById('advanced-trigger'),menu=document.getElementById('advanced-menu'),toggle=document.getElementById('nav-toggle'),tabs=document.getElementById('primary-tabs');
  const close=()=>{menu.hidden=true;trigger.setAttribute('aria-expanded','false');};
  trigger.addEventListener('click',()=>{const open=menu.hidden;menu.hidden=!open;trigger.setAttribute('aria-expanded',String(open));if(open)menu.querySelector('[role="menuitem"]')?.focus();});
  menu.addEventListener('keydown',event=>{const items=[...menu.querySelectorAll('[role="menuitem"]')],index=items.indexOf(document.activeElement);if(['ArrowDown','ArrowUp','Home','End'].includes(event.key)){event.preventDefault();items[event.key==='Home'?0:event.key==='End'?items.length-1:(index+(event.key==='ArrowUp'?-1:1)+items.length)%items.length]?.focus();}});
  menu.addEventListener('click',event=>{if(event.target.closest('[data-view]'))close();});
  document.addEventListener('click',event=>{if(!document.getElementById('advanced-control').contains(event.target))close();});
  document.addEventListener('keydown',event=>{if(event.key==='Escape'){close();trigger.focus();tabs.classList.remove('mobile-open');toggle.setAttribute('aria-expanded','false');}});
  toggle.addEventListener('click',()=>{const open=tabs.classList.toggle('mobile-open');toggle.setAttribute('aria-expanded',String(open));});
  tabs.addEventListener('click',event=>{if(event.target.closest('[data-view]')){tabs.classList.remove('mobile-open');toggle.setAttribute('aria-expanded','false');}});
 }
 const api={escape,render,footer};if(typeof module!=='undefined')module.exports=api;root.SafeUI=api;
 if(typeof document!=='undefined')document.addEventListener('DOMContentLoaded',init);
})(typeof globalThis!=='undefined'?globalThis:this);
 (function(root){
 const rows=[];
 function record(data,latency){rows.push({latency,cache:!!data.cache_hit,abstained:(data.decision==='abstained'||data.verdict==='insufficient evidence')&&data.decision!=='provider_unavailable',provider_unavailable:data.decision==='provider_unavailable',provider:data.provider||data.explanation_provider||data.hyde?.provider||null,failovers:Number(data.failovers||0)});}
 function summary(){const sorted=rows.map(r=>r.latency).sort((a,b)=>a-b),n=sorted.length;return {requests:n,cache_hit_rate:n?rows.filter(r=>r.cache).length/n:null,p50_ms:n?sorted[Math.ceil(n*.5)-1]:null,p95_ms:n?sorted[Math.ceil(n*.95)-1]:null,abstain_rate:n?rows.filter(r=>r.abstained).length/n:null,provider_unavailable_count:rows.filter(r=>r.provider_unavailable).length,provider_unavailable_rate:n?rows.filter(r=>r.provider_unavailable).length/n:null,providers:[...new Set(rows.map(r=>r.provider).filter(Boolean))],failovers:rows.reduce((acc,r)=>acc+(r.failovers||0),0)};}
 const api={record,summary};root.SessionMetrics=api;if(typeof module!=='undefined')module.exports.SessionMetrics=api;
})(typeof globalThis!=='undefined'?globalThis:this);


// Presentation preference only. Workspace state and requests are untouched.
(function () {
  if (typeof document === 'undefined') return;
  document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('theme-toggle');
    if (!button) return;
    const preference = matchMedia('(prefers-color-scheme: dark)');
    function display(theme) {
      document.documentElement.dataset.theme = theme;
      button.textContent = theme === 'dark' ? 'Light mode' : 'Dark mode';
      button.setAttribute('aria-label', 'Switch to ' + (theme === 'dark' ? 'light' : 'dark') + ' mode');
    }
    display(document.documentElement.dataset.theme || (preference.matches ? 'dark' : 'light'));
    button.addEventListener('click', function () {
      const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      display(theme);
      try { localStorage.setItem('campus-ui-theme', theme); } catch (_) {}
    });
    preference.addEventListener('change', function (event) {
      let saved;
      try { saved = localStorage.getItem('campus-ui-theme'); } catch (_) {}
      if (!['light', 'dark'].includes(saved)) display(event.matches ? 'dark' : 'light');
    });
    window.addEventListener('storage', function (event) {
      if (event.key === 'campus-ui-theme') display(['light', 'dark'].includes(event.newValue)
        ? event.newValue : (preference.matches ? 'dark' : 'light'));
    });
  });
})();

// Product navigation and local help. No policy inference or provider requests.
(function(){
 if(typeof document==='undefined')return;
 document.addEventListener('DOMContentLoaded',()=>{
  const esc=SafeUI.escape;
  const views={home:['Overview','Your workspace, ready for discovery.'],documents:['My Documents','Inspect the sources behind every answer.'],rulebook:['Rule Book','Requirements with their supporting evidence.'],analysis:['Ask & Analyse','Bring a question. Start with the evidence.'],conflicts:['Policy Conflicts','Understand where your sources differ.'],changes:['Document Changes','Compare source-backed requirements.'],compare:['Compare Retrieval','Explore Raw, HyDE and Fusion side by side.'],bench:['Benchmark','Review measured retrieval results.'],evidence:['Evidence','Read the passages in your workspace.'],labels:['Label Queries','Build a reviewed evaluation set.'],metrics:['Session Metrics','Observations from this browser session.'],how:['How it works','Follow the path from PDF to cited answer.'],sources:['Institution Admin','Manage institution sources and review.']};
  const paths={home:'M3 10l9-7 9 7v11H3z M9 21v-8h6v8',documents:'M6 3h8l4 4v14H6z M14 3v5h4 M9 12h6 M9 16h6',rulebook:'M4 4h7v16H4z M11 4h9v16h-9',analysis:'M4 4h16v12H9l-5 4z M8 8h8 M8 12h5',conflicts:'M8 3L2 15h12z M17 9l5 12H12z',changes:'M5 4v16 M5 4l-3 3 M5 4l3 3 M19 20V4 M19 20l-3-3 M19 20l3-3'};
  document.querySelectorAll('#primary-tabs button[data-view]').forEach(b=>{const path=paths[b.dataset.view];if(path)b.insertAdjacentHTML('afterbegin','<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="'+path+'"/></svg>');});
  const main=document.getElementById('main-content');
  main.insertAdjacentHTML('afterbegin','<div class="page-chrome"><div class="page-location"><span>Workspace</span><span aria-hidden="true">/</span><strong id="page-location">Overview</strong></div><div class="chrome-actions"><button class="chrome-search" id="quick-nav-open" aria-haspopup="dialog">Jump to… <kbd>⌘ K</kbd></button><button id="header-help">Help & support</button></div></div>');
  const home=document.getElementById('view-home');
  const quick=document.createElement('div');quick.className='quick-start';quick.setAttribute('aria-label','Workspace shortcuts');
  quick.innerHTML=[['01','documents','Build your evidence library','Inspect originals, extracted pages and stored chunks.'],['02','analysis','Ask a policy question','Follow the answer back to the cited passage.'],['03','rulebook','Understand the requirements','Review extracted rules before analysing your facts.']].map(([n,v,t,d])=>'<button type="button" data-quick-view="'+v+'"><span class="quick-number">'+n+'</span><strong>'+t+'</strong><small>'+d+'</small></button>').join('');
  const hero=home.querySelector('.hero');if(hero)hero.after(quick);else home.prepend(quick);
  document.body.insertAdjacentHTML('beforeend','<button class="help-launcher" id="help-launcher" aria-expanded="false" aria-controls="help-panel"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M4 4h16v12H9l-5 4z M8 8h8 M8 12h5"/></svg> Help</button><section class="help-panel" id="help-panel" role="dialog" aria-modal="false" aria-labelledby="help-title" hidden><header class="help-header"><div><h2 id="help-title">How can we help?</h2><p>Campus workspace · Product guide</p></div><button class="help-close" id="help-close" aria-label="Close help">×</button></header><div class="help-messages" id="help-messages" role="log" aria-live="polite" aria-relevant="additions"></div><div class="help-topics" id="help-topics"><button data-help-topic="upload">Upload PDFs</button><button data-help-topic="sources">Check an answer</button><button data-help-topic="modes">Retrieval modes</button><button data-help-topic="trouble">Troubleshooting</button></div><form class="help-form" id="help-form"><label for="help-input" class="sr">Ask about using this app</label><input id="help-input" maxlength="300" autocomplete="off" placeholder="Ask about using the workspace…"><button type="submit" class="primary">Send</button></form><div class="help-disclaimer">Local help guide. No AI calls. For policy answers, use Ask & Analyse.</div></section><dialog class="nav-dialog" id="quick-nav" aria-label="Find a page"><div class="nav-dialog-header"><input id="quick-nav-input" aria-label="Search pages" placeholder="Where would you like to go?" autocomplete="off"><button id="quick-nav-close" class="help-close" aria-label="Close quick navigation">×</button></div><div class="nav-results" id="quick-nav-results"></div><div class="nav-dialog-footer"><kbd>↑</kbd> <kbd>↓</kbd> to move · <kbd>Enter</kbd> to open · <kbd>Esc</kbd> to close</div></dialog><button id="back-top" class="back-top" aria-label="Back to top" hidden>↑</button><div id="ui-toast" class="ui-toast" role="status" hidden></div>');
  const topics={
   upload:['Upload PDFs','On Overview, choose Browse PDFs or drop your files in the upload area. Upload & index adds them to your personal workspace. In My Documents you can inspect original pages, extracted text and stored chunks. Personal uploads remain unverified.','documents'],
   sources:['Check an answer','Open Sources & cited evidence below an answer. Follow its document and page, inspect the full cited passage, and use My Documents to compare it with the original PDF. Source-backed guidance is not an official eligibility decision.','documents'],
   modes:['Retrieval modes','Raw searches your question directly. HyDE generates formal search wording. Fusion combines their rankings. HyDE text is a search aid, never policy evidence. Compare Retrieval shows actual returned passages; no method is guaranteed to win.','compare'],
   trouble:['Troubleshooting','If no answer is returned, inspect How this answer was produced. Missing evidence, failed grounding checks and provider availability are different issues. Confirm your document is indexed in My Documents. For provider errors, wait and retry; repeated clicks can worsen rate limiting.','documents'],
   rules:['Analyse facts','First extract requirements in Rule Book. On Ask & Analyse, enter or parse your facts, edit them, and confirm both the values and rule applicability. The comparison covers only the extracted conditions. The what-if simulator appears after a confirmed analysis.','rulebook'],
   privacy:['Workspace & privacy','Personal workspaces are saved in this browser using a private access capability. Avoid sharing browser storage or access credentials. This help conversation stays in page memory and is cleared on refresh; it is not sent to a provider.','how'],
   compare:['Document comparison','Document Changes requires two uploaded documents or retained versions and extracted rules for both. It compares validated rule tables, not every paragraph. Different wording or a later date does not establish which policy applies.','changes'],
   benchmark:['Evaluation','Benchmark requires reviewed relevance labels and available source chunks before it reports scores. Use Label Queries to review candidates. Pending suggestions are not verified results.','labels']
  };
  const log=document.getElementById('help-messages');
  function message(text,user=false,view=null){const row=document.createElement('div');row.className='help-message'+(user?' user':'');row.textContent=text;if(view){const b=document.createElement('button');b.className='copy-result';b.textContent='Open '+views[view][0];b.dataset.quickView=view;row.appendChild(document.createElement('br'));row.appendChild(b);}log.appendChild(row);log.scrollTop=log.scrollHeight;}
  message('Hi. I can help you upload documents, inspect evidence and use the workspace. Choose a topic or type a question about the app.');
  let returnFocus=null;
  function setHelp(open){const p=document.getElementById('help-panel');if(open)returnFocus=document.activeElement;p.hidden=!open;document.getElementById('help-launcher').setAttribute('aria-expanded',String(open));if(open)document.getElementById('help-input').focus();else returnFocus?.focus();}
  const helpReply=q=>{
   const t=q.toLowerCase();let key=Object.keys(topics).find(k=>t===k);
   if(!key){if(/upload|pdf|add.*document/.test(t))key='upload';else if(/citation|source|evidence|chunk/.test(t))key='sources';else if(/hyde|fusion|raw|retriev/.test(t))key='modes';else if(/error|fail|unavail|retry|problem|not work/.test(t))key='trouble';else if(/rule|fact|what.if|eligib|simulat/.test(t))key='rules';else if(/privacy|workspace|save|data/.test(t))key='privacy';else if(/compar|version|change/.test(t))key='compare';else if(/benchmark|label|evaluat/.test(t))key='benchmark';}
   if(key){message(topics[key][1],false,topics[key][2]);}else message('I can guide you around the app: uploads, sources, retrieval modes, rules, document comparisons and evaluation. For a university-policy question, open Ask & Analyse so the answer can use your documents.',false,'analysis');
  };
  document.getElementById('help-launcher').onclick=()=>setHelp(document.getElementById('help-panel').hidden);
  document.getElementById('header-help').onclick=()=>setHelp(true);document.getElementById('help-close').onclick=()=>setHelp(false);
  document.getElementById('help-topics').onclick=e=>{const b=e.target.closest('[data-help-topic]');if(b){message(b.textContent,true);helpReply(b.dataset.helpTopic);}};
  document.getElementById('help-form').onsubmit=e=>{e.preventDefault();const input=document.getElementById('help-input'),q=input.value.trim();if(!q)return;message(q,true);input.value='';helpReply(q);};
  function navigate(view){if(!views[view])return;setHelp(false);const dialog=document.getElementById('quick-nav');if(dialog.open)dialog.close();const existing=document.querySelector('button[data-view="'+view+'"]');if(existing)existing.click();else showView(view);document.getElementById('page-location').textContent=views[view][0];main.focus({preventScroll:true});window.scrollTo({top:0,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});}
  document.addEventListener('click',e=>{const q=e.target.closest('[data-quick-view]');if(q)navigate(q.dataset.quickView);});
  const dialog=document.getElementById('quick-nav'),search=document.getElementById('quick-nav-input'),results=document.getElementById('quick-nav-results');
  function renderNav(){const q=search.value.trim().toLowerCase();const options=Object.entries(views).filter(([id,[title,desc]])=>(title+' '+desc).toLowerCase().includes(q));results.innerHTML=options.length?options.map(([v,[title]])=>'<button data-quick-view="'+v+'">'+esc(title)+'<span aria-hidden="true">↗</span></button>').join(''):'<p class="muted" style="padding:12px">No matching page. Try “documents” or “rules”.</p>';}
  function openNav(){if(!dialog.open){search.value='';renderNav();dialog.showModal();search.focus();}}
  document.getElementById('quick-nav-open').onclick=openNav;document.getElementById('quick-nav-close').onclick=()=>dialog.close();search.oninput=renderNav;
  dialog.addEventListener('keydown',e=>{const buttons=[...results.querySelectorAll('button')];const i=buttons.indexOf(document.activeElement);if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();buttons[i<0?(e.key==='ArrowDown'?0:buttons.length-1):(i+(e.key==='ArrowDown'?1:-1)+buttons.length)%buttons.length]?.focus();}if(e.key==='Enter'&&document.activeElement===search){e.preventDefault();buttons[0]?.click();}});
  document.addEventListener('keydown',e=>{if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();openNav();}if(e.key==='Escape'&&!document.getElementById('help-panel').hidden){e.preventDefault();e.stopImmediatePropagation();setHelp(false);}},true);
  const updateLocation=()=>{const active=[...document.querySelectorAll('main>.view')].find(el=>!el.hidden);if(active&&views[active.id.replace('view-','')])document.getElementById('page-location').textContent=views[active.id.replace('view-','')][0];};
  document.querySelectorAll('main>.view').forEach(el=>new MutationObserver(updateLocation).observe(el,{attributes:true,attributeFilter:['hidden']}));
  const top=document.getElementById('back-top');window.addEventListener('scroll',()=>top.hidden=window.scrollY<500,{passive:true});top.onclick=()=>window.scrollTo({top:0,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
  let toastTimer;function toast(text){const t=document.getElementById('ui-toast');t.textContent=text;t.hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.hidden=true,2800);}
  const answerArea=document.getElementById('personal-result');new MutationObserver(()=>{const card=answerArea.querySelector('.result-card');if(!card||card.querySelector('.copy-result'))return;const b=document.createElement('button');b.className='copy-result';b.type='button';b.textContent='Copy guidance';b.onclick=async()=>{try{const body=card.querySelector('.answer-body,.answer-conclusion');if(!body){toast('No answer text to copy yet.');return;}await navigator.clipboard.writeText([...card.querySelectorAll('.answer-body,.answer-conclusion')].map(el=>el.innerText).join('\n\n'));toast('Guidance copied.');}catch{toast('Copy unavailable. Select the answer text to copy it.');}};card.appendChild(b);}).observe(answerArea,{childList:true,subtree:true});
 });
})();

(function(root){
 let pending=null;
 root.CampusUI={confirm(options){
  if(pending)return Promise.resolve(false);
  return new Promise(resolve=>{
   const dialog=document.createElement('dialog');dialog.className='confirm-dialog';dialog.setAttribute('aria-labelledby','confirm-title');dialog.setAttribute('aria-describedby','confirm-description');
   dialog.innerHTML='<div class="confirm-body"><div class="confirm-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 6h18M9 6V3h6v3M5 6l1 15h12l1-15M10 10v7M14 10v7"/></svg></div><h2 id="confirm-title"></h2><p id="confirm-description"></p></div><div class="confirm-actions"><button type="button" data-confirm-cancel autofocus>Cancel</button><button type="button" class="confirm-danger" data-confirm-accept></button></div>';
   dialog.querySelector('h2').textContent=options.title;dialog.querySelector('p').textContent=options.description;dialog.querySelector('[data-confirm-accept]').textContent=options.action;
   const previous=document.activeElement;pending=dialog;
   const finish=value=>{if(pending!==dialog)return;pending=null;dialog.close();dialog.remove();previous?.focus({preventScroll:true});resolve(value);};
   dialog.querySelector('[data-confirm-cancel]').onclick=()=>finish(false);dialog.querySelector('[data-confirm-accept]').onclick=()=>finish(true);
   dialog.addEventListener('cancel',e=>{e.preventDefault();finish(false);});
   document.body.appendChild(dialog);dialog.showModal();dialog.querySelector('[data-confirm-cancel]').focus();
  });
 }};
 if(typeof document!=='undefined')document.addEventListener('DOMContentLoaded',()=>{
  const select=document.getElementById('personal-mode'),radios=[...document.querySelectorAll('[name="retrieval-mode-ui"]')];
  radios.forEach(input=>input.addEventListener('change',()=>{if(input.checked){select.value=input.value;select.dispatchEvent(new Event('change',{bubbles:true}));}}));
  select.addEventListener('change',()=>radios.forEach(input=>input.checked=input.value===select.value));
 });
})(typeof globalThis!=='undefined'?globalThis:this);
