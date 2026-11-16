'use strict';
const pEl=id=>document.getElementById(id);
const pEsc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const PERSONAL_NOTICE='Based on documents you uploaded. Not verified by your institution.';
let pId='',pEpoch=0,pFiles=[],pDocs=[],pRules=[],pFacts=[],pBusy=false,pReplace='',pBlob=null;
function pSetWorkspace(id){pClosePreview(false);pInspectionEpoch++;pEl('personal-documents').hidden=false;window.CampusWhatIf?.clear();pId=id;pEpoch++;window.personalWorkspaceId=id;window.personalEpoch=pEpoch;for(const key of ['personal-result','personal-rules','personal-conflicts','personal-document-detail','personal-facts','compare-results','bench-content','personal-documents','personal-changes','evidence-content','label-content','personal-document-status'])pEl(key).textContent='';pFacts=[];pRules=[];pDocs=[];if(pBlob){URL.revokeObjectURL(pBlob);pBlob=null;}pEl('personal-facts-confirmed').checked=false;pEl('personal-applicability').checked=false;}
async function pApi(path,body,method){
 const requestStarted=Date.now();
 const response=await fetch('/personal'+path,{method:method||(body===undefined?'GET':'POST'),headers:{...(pId?{'X-Workspace-ID':pId}:{}),...(body===undefined||body instanceof FormData?{}:{'Content-Type':'application/json'})},...(body===undefined?{}:{body:body instanceof FormData?body:JSON.stringify(body)})});
 let data;try{data=await response.json();}catch{throw new Error('Local service unavailable; check the server and retry.');}
 if(['/ask','/analyse','/compare'].includes(path)&&typeof SessionMetrics!=='undefined')SessionMetrics.record(data,Date.now()-requestStarted);
 if(!response.ok)throw new Error(typeof data.detail==='string'?data.detail:Array.isArray(data.detail)?data.detail.map(d=>d.msg).join('; '):'Request failed ('+response.status+')');return data;
}
async function pEnsure(){
 if(pId)return pId;const created=await pApi('/workspaces',{college:pEl('personal-college').value});pSetWorkspace(created.workspace_id);localStorage.setItem('campus-personal-workspace',pId);await pRefresh();return pId;
}
async function pRefresh(){
 if(!pId){pEl('personal-count').textContent='No documents yet';return;}
 const ticket=pEpoch;
 const data=await pApi('/workspace');if(ticket!==pEpoch)return;
 pEl('personal-workspace-name').textContent=data.workspace.college||'My personal workspace';pEl('personal-count').textContent=data.documents+' documents · '+data.chunks+' chunks';pEl('workspace-chip-count').textContent='Personal · '+data.documents+' documents';pEl('personal-resume-status').textContent='Saved in this browser';pEl('synthetic-banner').hidden=!data.workspace.synthetic_demo;
 pEl('personal-start').textContent='Workspace ready';pEl('personal-start').disabled=true;pEl('personal-limits').textContent=`PDF only · ${data.limits.bytes/1024/1024} MB/file · ${data.limits.pages} pages/file · ${data.limits.documents} documents/workspace`;
}
function pGo(view){pEl('advanced-scope').value='personal';showView(view);if(view==='documents')pLoadDocs();if(view==='rulebook')pLoadRules();if(view==='conflicts')pLoadConflicts();if(view==='changes')pLoadChanges();}
function pSelectFiles(files){pFiles=Array.from(files);const invalid=!pFiles.length||pFiles.length>5||pFiles.some(f=>!f.name.toLowerCase().endsWith('.pdf'));pEl('personal-selection').textContent=invalid?'Choose one to five PDF files.':pFiles.map(f=>f.name).join(' · ');pEl('personal-upload').disabled=invalid;}
function pUploadRequest(body,ticket){return new Promise((resolve,reject)=>{const xhr=new XMLHttpRequest();xhr.open('POST','/personal/documents');xhr.setRequestHeader('X-Workspace-ID',pId);xhr.timeout=600000;xhr.upload.onprogress=e=>{if(e.lengthComputable&&ticket===pEpoch)pEl('personal-upload-progress').value=100*e.loaded/e.total;};xhr.onload=()=>{try{const data=JSON.parse(xhr.responseText);if(xhr.status>=300)throw new Error(data.detail||'Upload failed');resolve(data);}catch(error){reject(error);}};xhr.onerror=()=>reject(new Error('Upload interrupted. Refresh My Documents before retrying.'));xhr.ontimeout=()=>reject(new Error('Upload timed out. Refresh My Documents before retrying.'));xhr.send(body);});}
async function pUpload(files,replacement=''){
 const status=pEl('view-documents').hidden?'personal-status':'personal-document-status';
 if(pBusy)return;pBusy=true;pEl('personal-upload').disabled=true;let timer;
 try{
  await pEnsure();const ticket=pEpoch;const body=new FormData();for(const f of files)body.append('files',f);if(replacement)body.append('document_id',replacement);
  pEl('personal-upload-progress').hidden=false;pEl('personal-upload-progress').value=0;pEl(status).textContent='Uploading your PDF originals…';
  timer=setInterval(async()=>{try{const a=await pApi('/activity');if(ticket===pEpoch&&a.status==='running')pEl(status).textContent=(a.file||'')+' · '+a.stage+' · '+a.completed+'/'+a.total+' documents';}catch{}},1500);
  const uploaded=await pUploadRequest(body,ticket);if(ticket!==pEpoch)return;pEl('personal-upload-progress').value=100;const errors=[];
  for(const row of uploaded.documents){if(row.error){errors.push(row.error);continue;}pEl(status).textContent='Extracting, chunking and embedding '+row.source.original_filename+'…';const report=await pApi('/documents/'+encodeURIComponent(row.source.doc_id)+'/index',{});if(ticket!==pEpoch)return;if(report.errors?.length)errors.push(row.source.original_filename+': no completed index. See extraction errors in My Documents.');}
  pEl(status).textContent=errors.length?errors.join(' '):'Documents indexed. Ask a question now, or extract conditions in Rule Book. '+PERSONAL_NOTICE;
  pFiles=[];pEl('personal-files').value='';pEl('personal-selection').textContent='No files selected.';await pRefresh();await pLoadDocs();
 }catch(error){pEl(status).textContent=error.message;}finally{clearInterval(timer);pBusy=false;pEl('personal-upload').disabled=!pFiles.length;}
}
async function pLoadDocs(){
 const ticket=pEpoch;if(!pId){pEl('personal-documents').innerHTML='<div class="empty-state">Start your personal workspace and upload PDFs on Home.</div>';return;}
 try{const data=await pApi('/documents');if(ticket!==pEpoch)return;pDocs=data.documents;
 pEl('personal-documents').innerHTML=pDocs.length?pDocs.map(d=>`<article class="rule-card"><h3>${pEsc(d.original_filename)}</h3><span class="badge">Unverified upload</span><span class="badge">${pEsc(d.extraction_status)}</span><p>${pEsc(d.page_count)} pages · ${pEsc(d.chunk_count)} chunks</p>${d.indexing_elapsed_s!=null?'<p class="ok">Indexed in '+pEsc(d.indexing_elapsed_s.toFixed(2))+' s</p>':''}${d.cache_invalidated?'<p class="notice">'+pEsc(d.cache_invalidated)+' cached answer(s) invalidated by this update.</p>':''}${d.extraction_error?'<p class="error">'+pEsc(d.extraction_error)+' No extractable text may indicate a scanned PDF; OCR is not available.</p>':''}<div class="form"><button data-p-detail="${pEsc(d.doc_id)}">Inspect original & extracted text</button><button data-p-chunks="${pEsc(d.doc_id)}">View Chunks</button><button data-p-index="${pEsc(d.doc_id)}">Re-index this document</button><button data-p-replace="${pEsc(d.doc_id)}">Replace PDF</button><button data-p-remove="${pEsc(d.doc_id)}">Remove</button></div></article>`).join(''):'<div class="empty-state">No documents yet. Upload your college PDFs on Home.</div>';
 }catch(error){if(ticket===pEpoch)pEl('personal-documents').textContent=error.message;}
}
let pInspectionEpoch=0,pPreviewEpoch=0,pPreviewReturn=null,pDocumentReturn=null;
function pClosePreview(restore=true){
 pPreviewEpoch++;
 const panel=pEl('personal-original');if(panel){panel.replaceChildren?.();panel.hidden=true;}
 if(pBlob){URL.revokeObjectURL(pBlob);pBlob=null;}
 if(restore&&pPreviewReturn){pEl('personal-preview')?.focus({preventScroll:true});window.scrollTo(pPreviewReturn.x,pPreviewReturn.y);}
 pPreviewReturn=null;
}
function pDocumentBack(){
 pClosePreview(false);pInspectionEpoch++;pEl('personal-document-detail').replaceChildren();pEl('personal-documents').hidden=false;
 if(pDocumentReturn){pDocumentReturn.button?.focus({preventScroll:true});window.scrollTo(pDocumentReturn.x,pDocumentReturn.y);}
}
function pBeginInspection(){
 pClosePreview(false);pDocumentReturn={button:document.activeElement,x:window.scrollX,y:window.scrollY};
 pEl('personal-documents').hidden=true;
 pEl('personal-document-detail').innerHTML='<article class="rule-card document-inspector"><button id="personal-document-back">Back to My Documents</button><div id="personal-inspection-body" role="status">Loading document…</div></article>';
 pEl('personal-document-back').onclick=pDocumentBack;pEl('personal-document-back').focus();
 return ++pInspectionEpoch;
}
async function pInspect(did){
 const ticket=pEpoch,inspection=pBeginInspection();try{const data=await pApi('/documents/'+encodeURIComponent(did));if(ticket!==pEpoch||inspection!==pInspectionEpoch)return;
 pEl('personal-inspection-body').innerHTML='<h3>'+pEsc(data.source.original_filename)+'</h3><p>Version / SHA-256: '+pEsc(data.source.version_id)+'</p><button id="personal-preview">Preview original PDF</button><section id="personal-original" hidden aria-label="Original PDF preview"></section><details><summary>Extracted pages</summary>'+data.pages.map(p=>'<h3>Page '+pEsc(p.page)+'</h3><blockquote>'+pEsc(p.text||'No extracted text')+'</blockquote>').join('')+'</details><details><summary>Indexed chunks</summary>'+data.chunks.map(c=>'<p>Page '+pEsc(c.page)+' · '+pEsc(c.section)+'</p><blockquote>'+pEsc(c.text)+'</blockquote>').join('')+'</details>';
 pEl('personal-preview').onclick=async()=>{
 pClosePreview(false);const preview=++pPreviewEpoch;pPreviewReturn={x:window.scrollX,y:window.scrollY};
 const panel=pEl('personal-original');panel.hidden=false;panel.innerHTML='<div class="inspection-toolbar"><h4>Original PDF preview</h4><button id="personal-close-preview" class="primary">Close Preview</button></div><div id="personal-preview-body" role="status">Loading original PDF…</div>';
 pEl('personal-close-preview').onclick=()=>pClosePreview();pEl('personal-close-preview').focus({preventScroll:true});
 try{const response=await fetch('/personal/documents/'+encodeURIComponent(did)+'/original',{headers:{'X-Workspace-ID':pId}});if(!response.ok)throw new Error('Original unavailable. Close the preview and retry.');const blob=await response.blob();if(ticket!==pEpoch||inspection!==pInspectionEpoch||preview!==pPreviewEpoch)return;pBlob=URL.createObjectURL(blob);pEl('personal-preview-body').innerHTML='<iframe title="Your uploaded PDF" src="'+pEsc(pBlob)+'"></iframe>';
 }catch(error){if(ticket===pEpoch&&inspection===pInspectionEpoch&&preview===pPreviewEpoch)pEl('personal-preview-body').textContent=error.message;}};
 }catch(error){if(ticket===pEpoch&&inspection===pInspectionEpoch)pEl('personal-inspection-body').textContent=error.message;}
}
async function pInspectChunks(did){
 const ticket=pEpoch,inspection=pBeginInspection();
 try{const data=await pApi('/documents/'+encodeURIComponent(did)+'/chunks');if(ticket!==pEpoch||inspection!==pInspectionEpoch)return;
 const chunks=data.chunks||[];
 pEl('personal-inspection-body').innerHTML='<h3>'+pEsc(data.filename)+'</h3><p>'+chunks.length+' stored chunks · Current document version</p>'+(chunks.length?'<div class="inspection-toolbar"><button id="personal-chunk-prev">Previous chunk</button><label>Go to chunk <select id="personal-chunk-select" aria-label="Go to chunk">'+chunks.map((c,i)=>'<option value="'+i+'">'+(i+1)+' of '+chunks.length+'</option>').join('')+'</select></label><button id="personal-chunk-next">Next chunk</button></div><div id="personal-chunk-content" aria-live="polite"></div>':'<div class="empty-state">No stored chunks are available for this document version. Check its extraction status in My Documents.</div>');
 if(!chunks.length)return;
 let index=0;const render=()=>{const c=chunks[index];const pages=c.pages||c.page;const page=Array.isArray(pages)?pages.join(', '):pages;
 pEl('personal-chunk-content').innerHTML='<h4>Chunk '+(index+1)+' of '+chunks.length+'</h4><p>Stored index: '+pEsc(c.chunk_index??'Unavailable')+' · Source page: '+pEsc(page||'Unavailable')+'</p><p class="chunk-identifier">ID: '+pEsc(c.chunk_id||'Unavailable')+'</p><p>'+pEsc(c.section||'Section unavailable')+' · '+pEsc(c.character_count??'Unknown')+' characters</p><pre class="stored-chunk-text"></pre>';
 pEl('personal-chunk-content').querySelector('pre').textContent=c.text??'Chunk text unavailable.';
 pEl('personal-chunk-select').value=String(index);pEl('personal-chunk-prev').disabled=index===0;pEl('personal-chunk-next').disabled=index===chunks.length-1;};
 pEl('personal-chunk-prev').onclick=()=>{if(index>0){index--;render();}};pEl('personal-chunk-next').onclick=()=>{if(index<chunks.length-1){index++;render();}};pEl('personal-chunk-select').onchange=e=>{index=Number(e.target.value);render();};render();
 }catch(error){if(ticket===pEpoch&&inspection===pInspectionEpoch)pEl('personal-inspection-body').textContent='Chunks unavailable. '+error.message;}
}
function pRuleCard(r,conflict=false){return `<article class="rule-card"><h3>${pEsc(r.subject)} <span class="badge">${pEsc(r.operator)} ${pEsc(r.value)} ${pEsc(r.unit)}</span>${conflict?'<span class="badge">Possible conflict</span>':''}</h3><blockquote>${pEsc(r.verbatim_quote)}</blockquote><p class="source-label">${pEsc(r.document)} · page ${pEsc(r.page)}</p><p>Applies to: ${pEsc(r.applies_to||'Not specified in extracted quote')} · Exceptions: ${pEsc(r.exceptions?.join('; ')||'None extracted; verify the original')}</p><p>Deadline: ${pEsc(r.deadline||'Not extracted')} · Penalty: ${pEsc(r.penalty||'Not extracted')}</p><p>Effective date: ${pEsc(r.effective_date||'Not provided')} · Issuer: ${pEsc(r.issuing_authority||'Not provided')}</p></article>`;}
async function pLoadRules(){
 if(!pId){pEl('personal-rules').textContent='Upload documents on Home, then extract rules.';return;}
 const ticket=pEpoch;try{const [data,conflicts]=await Promise.all([pApi('/rules'),pApi('/conflicts')]);if(ticket!==pEpoch)return;pRules=data.rules;window.personalConflicts=conflicts.conflicts;
 const docs=[...new Map(pRules.map(r=>[r.document_id,r.document])).entries()];pEl('personal-rule-document').innerHTML='<option value="">All documents</option>'+docs.map(([id,name])=>'<option value="'+pEsc(id)+'">'+pEsc(name)+'</option>').join('');pEl('personal-rule-subject').innerHTML='<option value="">All subjects</option>'+[...new Set(pRules.map(r=>r.subject))].map(s=>'<option>'+pEsc(s)+'</option>').join('');pRenderRules();
 }catch(error){if(ticket===pEpoch)pEl('personal-rules').textContent=error.message;}
}
function pRenderRules(){const doc=pEl('personal-rule-document').value,sub=pEl('personal-rule-subject').value;const flagged=new Set((window.personalConflicts||[]).map(c=>c.subject));const rules=pRules.filter(r=>(!doc||r.document_id===doc)&&(!sub||r.subject===sub));pEl('personal-rules').innerHTML=rules.length?rules.map(r=>pRuleCard(r,flagged.has(r.subject))).join(''):'<div class="empty-state">No validated numeric rules yet. Extract rules from indexed documents; unsupported or fabricated rules are discarded.</div>';}
function pRenderFacts(){pEl('personal-facts-confirmed').checked=false;pEl('personal-facts').innerHTML=pFacts.map((f,i)=>`<div class="facts-row" data-fact="${i}"><input aria-label="Subject" data-field="subject" value="${pEsc(f.subject)}" placeholder="Rule subject"><input aria-label="Your value" data-field="value" value="${pEsc(f.value)}" placeholder="Value"><input aria-label="Unit" data-field="unit" value="${pEsc(f.unit)}" placeholder="Unit"><button data-p-fact-remove="${i}">Remove</button></div>`).join('')||'<p class="muted">No stated facts parsed yet. Parse your situation above, or add a fact using a Rule Book subject.</p>';}
function pReadFacts(){return Array.from(pEl('personal-facts').querySelectorAll('[data-fact]')).map(row=>Object.fromEntries(Array.from(row.querySelectorAll('[data-field]')).map(input=>[input.dataset.field,input.value.trim()])));}
function pTrace(trace){
  const modeDisplay = (trace.mode || 'fusion').toUpperCase();
  return '<details><summary>How this answer was produced</summary>'
    + '<p>Retrieval mode: <strong>' + pEsc(modeDisplay) + '</strong> · Cache: ' + (trace.cache_hit?'hit (live sources revalidated)':'miss') + ' · confidence gate: ' + (trace.confidence_passed?'passed':'not passed') + ' · provider: ' + pEsc(trace.provider||'none / cached') + '</p>'
    + '<p>HyDE: search key only, never shown to the answer model.</p>'
    + '<pre>' + pEsc(trace.hyde_text||'No HyDE passage used') + '</pre>'
    + '<p>Citations verified: ' + pEsc(trace.citations_verified?'yes':'no answered claim') + ' · Quotes verified: ' + pEsc(trace.verified_quotes?.length||0) + '</p>'
    + '<p>Tokens: before=' + (trace.tokens_estimated_before??'n/a') + ' · after=' + (trace.tokens_estimated_after??'n/a') + '</p>'
    + '<p>' + pEsc(trace.abstain_reason||trace.decision) + '</p>'
    + (trace.validation_failures?.length?'<h3>Validation findings</h3><pre>'+pEsc(JSON.stringify(trace.validation_failures,null,2))+'</pre>':'')
    + '<h3>Stage timings (ms)</h3>'
    + '<pre>' + pEsc(JSON.stringify(trace.timings_ms,null,2)) + '</pre>'
    + trace.retrieved.map(c=>'<article class="chunk"><strong>' + pEsc(c.doc_title) + ' · page ' + pEsc(c.page) + ' · ' + pEsc(c.section) + '</strong><p>Cosine ' + pEsc(c.score) + ' · RRF ' + pEsc(c.rrf_score??'not used') + '</p><blockquote>' + pEsc(c.matched_sentence||c.text_preview) + '</blockquote></article>').join('')
    + '</details>';
}

function pRenderAnswer(trace){
  const isProvUnavail = trace.decision === 'provider_unavailable';
  let verdictText = 'Abstained · insufficient evidence';
  if (trace.decision === 'clarification_required') verdictText = 'Clarification needed';
  else if (trace.decision === 'answered') verdictText = 'Source-backed guidance';
  else if (isProvUnavail) verdictText = 'AI Provider Rate-Limited';

  const modeLabels = {
    'raw': 'Raw retrieval',
    'hyde': 'HyDE retrieval',
    'fusion': 'Fusion retrieval'
  };
  const modeKey = (trace.mode || 'fusion').toLowerCase();
  const modeBadge = modeLabels[modeKey] || ((trace.mode || 'Fusion') + ' retrieval');

  let retryHtml = '';
  if (isProvUnavail) {
    const sec = Math.ceil(trace.retry_after_s || 15);
    retryHtml = '<div class="provider-unavailable-banner" style="margin:12px 0;padding:14px;background:rgba(229,195,122,0.12);border:1px solid #E5C37A;border-radius:8px;">'
      + '<strong>The AI provider is rate-limited. Retrying in ' + sec + ' seconds</strong>'
      + '<p>' + pEsc(trace.answer || 'The AI provider is rate-limited. Retrying in ' + sec + ' seconds') + '</p>'
      + '<button type="button" class="primary" style="margin-top:8px" onclick="document.getElementById(\'personal-ask\').click()">Retry Question</button>'
      + '</div>';
  }

  const rawAnswer = trace.answer || trace.error || '';
  const parts = rawAnswer.split(/\n\n(?=\*\*)/);
  let answerHtml = '';
  if (parts.length > 1) {
    const conclusion = parts[0];
    const body = parts.slice(1).join('\n\n');
    answerHtml =
      '<div class="answer-conclusion" style="font-size:15.5px;font-weight:600;line-height:1.65;color:var(--text-primary);padding:14px 18px;margin:12px 0 16px 0;background:rgba(138,216,181,0.06);border-left:3px solid var(--accent);border-radius:0 8px 8px 0;">'
      + (typeof SafeUI !== 'undefined' ? SafeUI.render(conclusion, {maxCitation: trace.retrieved.length}) : pEsc(conclusion))
      + '</div>'
      + '<div class="answer-body" style="font-size:13.5px;line-height:1.7;color:var(--text-secondary);">'
      + (typeof SafeUI !== 'undefined' ? SafeUI.render(body, {maxCitation: trace.retrieved.length}) : pEsc(body))
      + '</div>';
  } else {
    answerHtml =
      '<div class="answer-body" style="font-size:14px;line-height:1.65;color:var(--text-primary);margin-top:10px;">'
      + (typeof SafeUI !== 'undefined' ? SafeUI.render(rawAnswer, {maxCitation: trace.retrieved.length}) : pEsc(rawAnswer))
      + '</div>';
  }

  const citationsHtml = trace.citations.map((cid, index) => {
    const sourceIndex = trace.retrieved.findIndex(c => c.chunk_id === cid);
    const c = trace.retrieved[sourceIndex];
    return c ? '<blockquote class="evidence-card" id="evidence-C' + (sourceIndex + 1) + '"><mark>' + pEsc(c.matched_sentence || c.text_preview) + '</mark><p class="source-label">' + pEsc(c.doc_title) + ' · page ' + pEsc((c.pages || [c.page]).join(', ')) + ' · ' + pEsc(c.section) + '</p><button data-p-citation="' + pEsc(cid) + '" data-full-text="' + pEsc(c.text || '') + '">Full cited passage</button><div data-citation-content></div></blockquote>' : '';
  }).join('');

  return '<article class="result-card">'
    + '<div style="display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;margin-bottom:12px;">'
    + '<span class="verdict">' + verdictText + '</span>'
    + '<span class="badge" style="font-size:12px;font-weight:600;background:rgba(138,216,181,0.1);color:var(--accent);border:1px solid rgba(138,216,181,0.25);">' + pEsc(modeBadge) + '</span>'
    + '</div>'
    + (retryHtml || answerHtml)
    + '<h3>Sources &amp; cited evidence</h3>'
    + '<p class="trust-note" style="margin:4px 0 14px 0;font-size:12px;color:var(--text-muted);display:flex;align-items:center;gap:6px;"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="opacity:0.6;flex-shrink:0;"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>'+pEsc(PERSONAL_NOTICE)+'</p>'
    + citationsHtml
    + (trace.verified_quotes?.length ? '<span class="badge ok">' + trace.verified_quotes.length + ' verified quote' + (trace.verified_quotes.length === 1 ? '' : 's') + '</span>' : '')
    + (trace.warnings || []).map(w => '<p class="notice">' + pEsc(w) + '</p>').join('')
    + pTrace(trace)
    + '</article>';
}
function pRenderAnalysis(data){return '<article class="result-card"><span class="verdict">'+pEsc(data.verdict)+'</span><span class="trust-badge">'+PERSONAL_NOTICE+'</span><p>'+pEsc(data.scope)+'</p>'+(data.abstained?'<p>No matching extracted rule was found. Extract rules or ask about supported evidence.</p>':'')+'<div class="table-wrap"><table><thead><tr><th>Rule</th><th>Your value</th><th>Required</th><th>Status</th><th>Source</th></tr></thead><tbody>'+data.conditions.map(c=>'<tr><td>'+pEsc(c.rule.subject)+'</td><td>'+pEsc(c.your_value??'Missing')+'</td><td>'+pEsc(c.rule.operator+' '+c.rule.value+' '+c.rule.unit)+'</td><td>'+pEsc(c.status)+'</td><td>'+pEsc(c.rule.document)+' · page '+pEsc(c.rule.page)+'</td></tr>').join('')+'</tbody></table></div>'+data.conditions.map(c=>'<h3>'+pEsc(c.rule.subject)+'</h3><p>'+pEsc(c.reason)+'</p><blockquote>'+pEsc(c.rule.verbatim_quote)+'<p class="source-label">'+pEsc(c.rule.document)+' · page '+pEsc(c.rule.page)+'</p></blockquote>').join('')+(data.missing_facts.length?'<p>Missing facts: '+pEsc(data.missing_facts.join(', '))+'</p>':'')+'<details><summary>AI explanation of computed comparisons</summary>'+data.explanations.map(e=>'<p>'+pEsc(e.text)+' ['+pEsc(e.document)+', page '+pEsc(e.page)+']</p>').join('')+'<p>'+pEsc(data.explanation_warning||'The verdict above is computed by code, not the model.')+'</p></details></article>';}
async function pLoadConflicts(){if(!pId){pEl('personal-conflicts').textContent='Upload and extract rules from documents first.';return;}const ticket=pEpoch;try{const data=await pApi('/conflicts');if(ticket!==pEpoch)return;pEl('personal-conflicts').innerHTML=data.conflicts.length?data.conflicts.map(c=>'<article class="result-card"><span class="verdict">Possible conflict · '+pEsc(c.subject)+'</span><p>'+pEsc(c.reason)+'</p><div class="columns">'+c.evidence.map(r=>pRuleCard(r,true)).join('')+'</div></article>').join(''):'<div class="empty-state">No possible conflicts among the currently extracted rules. This does not prove that documents are complete or consistent.</div>';}catch(error){if(ticket===pEpoch)pEl('personal-conflicts').textContent=error.message;}}
async function pLoadChanges(){
 if(!pId){pEl('personal-changes').textContent='Upload document versions first.';return;}
 const ticket=pEpoch;try{const data=await pApi('/versions');if(ticket!==pEpoch)return;
 if(data.versions.length<2){pEl('personal-changes').textContent='Upload another document or replace a PDF to retain an earlier version for comparison.';return;}
 const options=data.versions.map((v,i)=>'<option value="'+i+'">'+pEsc(v.document)+' · '+pEsc(v.version_id.slice(0,10))+(v.current?' · current':' · earlier')+'</option>').join('');
 pEl('personal-changes').innerHTML='<div class="form"><label for="personal-old-version">Earlier / reference</label><select id="personal-old-version">'+options+'</select><label for="personal-new-version">New / comparison</label><select id="personal-new-version">'+options+'</select><button id="personal-compare-versions">Extract & compare selected versions</button></div><div id="personal-change-results"></div>';
 pEl('personal-new-version').value='1';
 pEl('personal-compare-versions').onclick=()=>pRun('personal-change-results',async epoch=>{
 const old=data.versions[Number(pEl('personal-old-version').value)],next=data.versions[Number(pEl('personal-new-version').value)];
 if(old.document_id===next.document_id&&old.version_id===next.version_id)throw new Error('Choose two different document versions.');
 for(const v of [old,next]){const extracted=await pApi('/rules/extract',{document_id:v.document_id,version_id:v.version_id});if(extracted.errors.length)throw new Error('Rule extraction incomplete: '+JSON.stringify(extracted.errors));}
 const result=await pApi('/changes',{old_document_id:old.document_id,old_version_id:old.version_id,new_document_id:next.document_id,new_version_id:next.version_id});if(epoch!==pEpoch)return;
 pEl('personal-change-results').innerHTML='<p>'+pEsc(result.notice||result.message)+'</p>'+(result.changes.length?result.changes.map(c=>'<article class="result-card"><h3>'+pEsc(c.kind)+' · '+pEsc(c.subject)+'</h3><div class="columns"><div><h3>Reference</h3>'+c.old.map(r=>pRuleCard(r)).join('')+'</div><div><h3>Comparison</h3>'+c.new.map(r=>pRuleCard(r)).join('')+'</div></div></article>').join(''):'<p>No validated rule-table differences found, or extraction is incomplete. This is not a whole-document diff.</p>');
 });
 }catch(error){if(ticket===pEpoch)pEl('personal-changes').textContent=error.message;}
}
async function pRun(target,work){const ticket=pEpoch;pEl(target).textContent='Working…';pEl(target).classList?.toggle('loading',true);try{await work(ticket);}catch(error){if(ticket===pEpoch)pEl(target).textContent=error.message;}finally{pEl(target).classList?.toggle('loading',false);}}
function pInit(){
 try{pSetWorkspace(localStorage.getItem('campus-personal-workspace')||'');}catch{pSetWorkspace('');}
 if(pId)pRefresh().catch(()=>{pEl('personal-resume-status').textContent='Saved workspace unavailable. Start a new workspace if it was deleted.';localStorage.removeItem('campus-personal-workspace');pSetWorkspace('');});
 pEl('personal-demo').onclick=()=>pRun('personal-status',async()=>{if(pBusy)throw new Error('Wait for the current upload.');const data=await pApi('/demo',{});pSetWorkspace(data.workspace.workspace_id);localStorage.setItem('campus-personal-workspace',pId);await pRefresh();await pLoadDocs();pEl('personal-status').textContent='SYNTHETIC TEST FIXTURE workspace loaded. '+(data.index_report.errors.length?'Some files failed; inspect My Documents.':'Documents indexed; extract the Rule Book to inspect fictional conditions.');});
 pEl('personal-start').onclick=()=>pRun('personal-status',async()=>{await pEnsure();pEl('personal-status').textContent='Workspace ready. Upload your PDFs below.';});
 pEl('personal-browse').onclick=()=>pEl('personal-files').click();pEl('personal-files').onchange=e=>pSelectFiles(e.target.files);pEl('personal-upload').onclick=()=>pUpload(pFiles);
 const zone=pEl('personal-dropzone');for(const name of ['dragenter','dragover'])zone.addEventListener(name,e=>{e.preventDefault();zone.classList.toggle('dragging',true);});for(const name of ['dragleave','drop'])zone.addEventListener(name,e=>{e.preventDefault();zone.classList.toggle('dragging',false);});zone.addEventListener('drop',e=>pSelectFiles(e.dataTransfer.files));
 document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>{if(['documents','rulebook','analysis','conflicts','changes'].includes(b.dataset.view))pGo(b.dataset.view);}));
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!pEl('personal-original')?.hidden&&pEl('personal-original')&&!pEl('view-documents').hidden){e.preventDefault();pClosePreview();}});
 document.addEventListener('click',async e=>{
  const button=e.target.closest('button');if(!button)return;const d=button.dataset;
  if(d.personalGo)pGo(d.personalGo);if(d.personalQuestion)pEl('personal-question').value=d.personalQuestion;
  if(d.pDetail)pInspect(d.pDetail);if(d.pChunks)pInspectChunks(d.pChunks);
  if(d.pReplace){pReplace=d.pReplace;pEl('personal-replace').click();}
  const removeEpoch=pEpoch;
  if(d.pRemove&&await CampusUI.confirm({title:'Remove this document?',description:'The PDF, retained versions and derived evidence will be permanently removed. Other documents are unaffected.',action:'Remove document'})&&removeEpoch===pEpoch)pRun('personal-document-status',async()=>{await pApi('/documents/'+encodeURIComponent(d.pRemove),undefined,'DELETE');await pLoadDocs();await pRefresh();pEl('personal-document-status').textContent='Document removed.';});
  if(d.pIndex)pRun('personal-document-status',async()=>{const report=await pApi('/documents/'+encodeURIComponent(d.pIndex)+'/index',{});await pLoadDocs();await pRefresh();pEl('personal-document-status').textContent=report.errors?.length?'Indexing failed. Inspect the document extraction error below.':'Document re-indexed.';});
  if(d.pFactRemove!==undefined){pFacts=pReadFacts();pFacts.splice(Number(d.pFactRemove),1);pRenderFacts();}
  if(d.pCitation){if(d.fullText){button.nextElementSibling.textContent=d.fullText;return;}const ticket=pEpoch;try{const data=await pApi('/citations/'+encodeURIComponent(d.pCitation));if(ticket===pEpoch)button.nextElementSibling.textContent=data.text;}catch(error){button.nextElementSibling.textContent=error.message;}}
 });
 pEl('personal-replace').onchange=e=>{if(e.target.files.length)pUpload([e.target.files[0]],pReplace);e.target.value='';};
 pEl('personal-delete').onclick=async()=>{const workspace=pId,epoch=pEpoch;if(!workspace||!await CampusUI.confirm({title:'Delete your workspace?',description:'All uploaded PDFs, extracted content and derived evidence in this personal workspace will be permanently removed. This cannot be undone.',action:'Delete workspace'})||epoch!==pEpoch||workspace!==pId)return;await pRun('personal-status',async()=>{await pApi('/workspace',undefined,'DELETE');localStorage.removeItem('campus-personal-workspace');pSetWorkspace('');pEl('personal-start').disabled=false;pEl('personal-start').textContent='Start personal workspace';pEl('personal-count').textContent='No documents yet';pEl('personal-status').textContent='Personal workspace deleted. Institutional data is unchanged.';});};
 pEl('personal-extract-rules').onclick=()=>pRun('personal-rule-status',async ticket=>{if(!pId)throw new Error('Upload documents first.');pEl('personal-extract-rules').disabled=true;const progress=setInterval(async()=>{try{const a=await pApi('/rules/activity');if(ticket===pEpoch&&a.status==='running'){pEl('personal-rule-status').textContent=a.message||(a.document+' · '+a.processed_chunks+'/'+a.total_chunks+' candidate chunks processed');if(a.extracted_rules!=null&&a.extracted_rules>0)pLoadRules();}}catch{}},1500);try{const data=await pApi('/rules/extract',{});if(ticket!==pEpoch)return;pEl('personal-rule-status').textContent=data.rules+' validated rules; '+data.discarded+' unverifiable proposals discarded. '+(data.errors.length?JSON.stringify(data.errors):'');await pLoadRules();}finally{clearInterval(progress);pEl('personal-extract-rules').disabled=false;}});
 for(const id of ['personal-rule-document','personal-rule-subject'])pEl(id).onchange=pRenderRules;
 pEl('personal-ask-form').onsubmit=e=>{e.preventDefault();pRun('personal-answer-status',async ticket=>{if(!pId)throw new Error('Upload documents first.');pEl('personal-ask').disabled=true;pEl('personal-ask').setAttribute('aria-busy','true');pEl('personal-result').innerHTML='<article class="result-card loading-state" style="display:flex;align-items:center;gap:16px;padding:22px;border:1px solid var(--border,#34483E);background:var(--bg-surface,#1C2B25);border-radius:var(--radius-md,9px);animation:reveal 180ms ease-out;"><div style="width:24px;height:24px;border:2.5px solid var(--border,#34483E);border-top-color:var(--accent,#8AD8B5);border-radius:50%;animation:spin .8s linear infinite;flex-shrink:0;"></div><div><h3 style="margin:0 0 4px 0;font-size:15px;font-weight:600;color:var(--text-primary,#E5ECE8);">Analyzing your question...</h3><p style="margin:0;font-size:13px;color:var(--text-muted,#7E9488);">Checking relevant policy provisions and preparing supporting evidence.</p></div></article>';try{const [trace]=await Promise.all([pApi('/ask',{question:pEl('personal-question').value,mode:pEl('personal-mode').value}),new Promise(r=>setTimeout(r,900))]);if(ticket!==pEpoch)return;pEl('personal-result').innerHTML=pRenderAnswer(trace);pEl('personal-answer-status').textContent='';}finally{pEl('personal-ask').disabled=false;pEl('personal-ask').removeAttribute('aria-busy');}});};
 pEl('personal-parse-facts').onclick=()=>pRun('personal-answer-status',async ticket=>{if(!pId)throw new Error('Upload and extract rules first.');const data=await pApi('/facts/parse',{text:pEl('personal-question').value});if(ticket!==pEpoch)return;pFacts=data.facts;pRenderFacts();pEl('personal-answer-status').textContent=data.message;});
 pEl('personal-add-fact').onclick=()=>{pFacts=pReadFacts();pFacts.push({subject:pRules[0]?.subject||'',value:'',unit:pRules[0]?.unit||''});pRenderFacts();};
 pEl('personal-analyse').onclick=()=>pRun('personal-answer-status',async ticket=>{if(!pId)throw new Error('Upload and extract rules first.');const request={question:pEl('personal-question').value,facts:pReadFacts(),confirmed:pEl('personal-facts-confirmed').checked,applicability_confirmed:pEl('personal-applicability').checked};const data=await pApi('/analyse',request);if(ticket!==pEpoch)return;pEl('personal-result').innerHTML=pRenderAnalysis(data);if(request.confirmed&&request.applicability_confirmed&&pEl('personal-facts-confirmed').checked&&pEl('personal-applicability').checked&&JSON.stringify(pReadFacts())===JSON.stringify(request.facts))window.CampusWhatIf.mount(data,request.facts);pEl('personal-answer-status').textContent='';});
 pEl('personal-run-benchmark').onclick=()=>pRun('bench-content',async ticket=>{if(!pId)throw new Error('Start a personal workspace first.');const data=await pApi('/bench/run',{});if(ticket===pEpoch)renderBenchmark(data);});
 pEl('personal-refresh-conflicts').onclick=pLoadConflicts;
}
if(typeof document!=='undefined')pInit();
if(typeof module!=='undefined')module.exports={pEsc,pRuleCard,pRenderAnswer,pRenderAnalysis,pTrace,pSetWorkspace,pApi,pSelectFiles,pEnsure,pRefresh};


// Scenario values live only in this closure, never in confirmed facts or storage.
if (typeof document !== 'undefined') window.CampusWhatIf = (function () {
 let baseline=null, timer=null, controller=null, generation=0;
 const esc=pEsc;
 function display(value){const text=String(value??'Missing');return /^-?\d+\.\d{7,}$/.test(text)?'≈'+text.slice(0,text.indexOf('.')+7):text;}
 function clear(){baseline=null;generation++;clearTimeout(timer);controller?.abort();const entry=document.getElementById('whatif-entry');if(entry)entry.hidden=false;}
 function differs(facts){return facts.some((fact,i)=>Number(fact.value)!==Number(baseline.facts[i].value)||fact.unit!==baseline.facts[i].unit);}
 function render(result){
  const verdict=result.conflicted?'Conflicting rules require more evidence. No combined verdict or path is available.':(result.conditions.length?result.verdict:'No numeric rules found.');
  let html='<p><strong>'+esc(verdict)+'</strong></p><p>'+esc(result.scope)+'</p>';
  html+=result.conditions.map(c=>{
   const rule=c.rule;let path='',countsHtml='';
   if(c.gap){const g=c.gap;path=g.direction==='equal'?'Must equal '+g.boundary:g.direction==='different'?'Must differ from '+g.boundary:(g.direction==='increase'?'Increase':'Decrease')+' by '+display(g.amount)+' '+rule.unit+(g.strict?' to the boundary, then '+(g.direction==='increase'?'exceed it.':'go below it.'):' to meet the threshold.');}
   if(c.counts){const a=c.counts;countsHtml+='<p>Current count percentage: '+esc(display(a.current_percent))+'%. Additional consecutive fully completed items: '+esc(a.additional_completed??a.reason)+'.</p>';
    if(a.reachable!==undefined)countsHtml+='<p>With the remaining items: '+(a.reachable?'reachable; maximum that can be missed: '+esc(a.max_remaining_missed):'unreachable')+'. If all are completed: '+esc(display(a.all_completed_percent))+'%.</p>';
   }
   const caveats=[...(rule.exceptions||[]),rule.applies_to].filter(Boolean);
   return '<article class="chunk"><h4>'+esc(rule.subject)+'</h4><blockquote>'+esc(rule.verbatim_quote)+'<p>'+esc(rule.document)+' · page '+esc(rule.page)+'</p></blockquote><table class="whatif-table"><thead><tr><th>Required</th><th>Scenario value</th><th>Status</th></tr></thead><tbody><tr><td>'+esc(rule.operator+' '+rule.value+' '+rule.unit)+'</td><td>'+esc(display(c.your_value))+'</td><td>○ '+esc(c.status)+'</td></tr></tbody></table><div>'+ (c.gap?esc(path):'')+countsHtml+'</div>'+(c.status==='insufficient evidence'?'<p>'+esc(c.reason)+'</p>':'')+caveats.map(v=>'<blockquote>'+esc(v)+'<p>'+esc(rule.document)+' · page '+esc(rule.page)+'</p></blockquote>').join('')+(caveats.length?'<p>These may change what applies to you. Check with your institution.</p>':'')+'</article>';
  }).join('');
  return html+'<p>Values marked ≈ are shortened for display. Calculations use full precision.</p><p>'+esc(result.arithmetic_notice)+'</p>';
 }
 function values(){return baseline.facts.map((fact,i)=>({...fact,value:document.getElementById('whatif-value-'+i).value,unit:document.getElementById('whatif-unit-'+i).value}));}
 function schedule(){clearTimeout(timer);controller?.abort();generation++;const facts=values();document.getElementById('whatif-banner').hidden=!differs(facts);document.getElementById('whatif-results').textContent='Updating scenario…';timer=setTimeout(update,220);}
 async function update(){
  if(!baseline)return;const ticket=++generation,workspace=window.personalWorkspaceId;const facts=values(),counts={};
  const target=document.getElementById('whatif-results');
  try{
   baseline.facts.forEach((fact,i)=>{const check=document.getElementById('whatif-counts-'+i);if(check?.checked){const done=document.getElementById('whatif-done-'+i).value,total=document.getElementById('whatif-total-'+i).value,remaining=document.getElementById('whatif-remaining-'+i).value;if(done===''||total==='')throw Error('Enter done and total counts, or turn off compute from counts.');counts[fact.subject]={done:Number(done),total:Number(total),...(remaining===''?{}:{remaining:Number(remaining)})};}});
   controller=new AbortController();
   const response=await fetch('/api/personal/'+encodeURIComponent(workspace)+'/whatif',{method:'POST',headers:{'Content-Type':'application/json','X-Workspace-ID':workspace},signal:controller.signal,body:JSON.stringify({facts,counts,rule_ids:baseline.ruleIds,confirmed:true,applicability_confirmed:true})});
   const data=await response.json();if(ticket!==generation||workspace!==window.personalWorkspaceId)return;
   if(!response.ok)throw Error(typeof data.detail==='string'?data.detail:'Check the numeric values and counts.');
   target.innerHTML=render(data);
   const changed=differs(facts)||data.conditions.some(c=>{const f=baseline.facts.find(f=>f.subject===c.rule.subject);return f&&c.your_value!=null&&Number(c.your_value)!==Number(f.value);});document.getElementById('whatif-banner').hidden=!changed;
  }catch(error){if(ticket===generation&&error.name!=='AbortError')target.textContent=error.message;}
 }
 function mount(analysis,facts){
  clear();baseline={facts:facts.map(f=>({...f})),ruleIds:analysis.conditions.map(c=>c.rule.rule_id)};
  const panel=document.createElement('section');panel.id='whatif-panel';panel.className='result-card';
  panel.innerHTML='<h3>What if I change this?</h3><p>'+PERSONAL_NOTICE+'</p><p>Rules extracted by AI, verify against the source quote. The verdict covers only rules found in your uploaded documents.</p><p id="whatif-banner" class="notice" hidden>Scenario only. These are not your real values.</p>'+facts.map((f,i)=>'<div class="whatif-control"><label for="whatif-value-'+i+'">'+esc(f.subject)+' scenario value</label><input id="whatif-value-'+i+'" type="number" min="0" max="'+(f.unit==='%'?'100':'1000000000000')+'" step="any" value="'+esc(f.value)+'"><label for="whatif-unit-'+i+'">Unit</label><input id="whatif-unit-'+i+'" value="'+esc(f.unit)+'">'+(f.unit==='%'?'<input id="whatif-slider-'+i+'" type="range" min="0" max="100" step="any" value="'+esc(f.value)+'" aria-label="'+esc(f.subject)+' scenario percentage"><label><input id="whatif-counts-'+i+'" type="checkbox"> Compute from counts</label><div id="whatif-count-fields-'+i+'" hidden><p>The counts determine this scenario value.</p>'+['done','total','remaining'].map(name=>'<label for="whatif-'+name+'-'+i+'">'+esc(name)+(name==='remaining'?' (optional)':'')+'</label><input id="whatif-'+name+'-'+i+'" type="number" step="1" min="'+(name==='total'?'1':'0')+'" max="1000000000">').join('')+'</div>':'')+'</div>').join('')+'<button id="whatif-reset" type="button">Reset to my real facts</button><div id="whatif-results" aria-live="polite" role="status">'+(facts.length?'Updating scenario…':'Missing confirmed numeric facts. Insufficient evidence.')+'</div>';
  document.getElementById('personal-result').appendChild(panel);const entry=document.getElementById('whatif-entry');if(entry)entry.hidden=true;
  panel.addEventListener('input',event=>{const match=event.target.id.match(/^whatif-(value|slider)-(\d+)$/);if(match){const other=document.getElementById('whatif-'+(match[1]==='slider'?'value':'slider')+'-'+match[2]);if(other)other.value=event.target.value;}schedule();});
  panel.addEventListener('change',event=>{const match=event.target.id.match(/^whatif-counts-(\d+)$/);if(match){document.getElementById('whatif-count-fields-'+match[1]).hidden=!event.target.checked;for(const name of ['value','unit','slider'])document.getElementById('whatif-'+name+'-'+match[1]).disabled=event.target.checked;schedule();}});
  document.getElementById('whatif-reset').onclick=()=>{baseline.facts.forEach((f,i)=>{document.getElementById('whatif-value-'+i).value=f.value;document.getElementById('whatif-unit-'+i).value=f.unit;const slider=document.getElementById('whatif-slider-'+i);if(slider)slider.value=f.value;const check=document.getElementById('whatif-counts-'+i);if(check){check.checked=false;document.getElementById('whatif-count-fields-'+i).hidden=true;for(const name of ['value','unit','slider'])document.getElementById('whatif-'+name+'-'+i).disabled=false;}});schedule();};
  update();
 }
 function invalidate(){if(!baseline)return;clear();document.getElementById('whatif-panel')?.remove();}
 document.addEventListener?.('input',event=>{if(event.target.closest('#personal-facts'))invalidate();});
 document.addEventListener?.('change',event=>{if(['personal-facts-confirmed','personal-applicability'].includes(event.target.id))invalidate();});
 document.addEventListener?.('click',event=>{if(event.target.closest('#personal-add-fact,[data-p-fact-remove]'))invalidate();});
 return {mount,clear,render};
})();
