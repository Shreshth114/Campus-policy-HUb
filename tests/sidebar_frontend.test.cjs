const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
(async()=>{
const ctx={module:{exports:{}},console,URL,FormData};vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(__dirname,'../web/personal.js'),'utf8'),ctx);
const elements=new Map();ctx.window={};ctx.document={getElementById:id=>{if(!elements.has(id))elements.set(id,{textContent:'old workspace content',checked:true});return elements.get(id);}};
ctx.module.exports.pSetWorkspace('another-workspace');
for(const id of ['personal-documents','personal-changes','evidence-content','label-content'])assert.equal(ctx.document.getElementById(id).textContent,'');
const demo={window:{personalWorkspaceId:'A',personalEpoch:1},console};vm.createContext(demo);vm.runInContext(fs.readFileSync(path.join(__dirname,'../web/demo.js'),'utf8'),demo);
const label={textContent:'new workspace',innerHTML:'new workspace'};demo.document={getElementById:()=>label};
let finish;demo.pApi=()=>new Promise(resolve=>{finish=resolve});
const pending=demo.loadEvidence();demo.window.personalEpoch=2;label.textContent='new workspace';finish({chunks:[{text:'old workspace passage'}]});await pending;assert.equal(label.textContent,'new workspace');assert.equal(label.innerHTML,'new workspace');
let reject;demo.pApi=()=>new Promise((_,fail)=>{reject=fail});demo.window.personalEpoch=3;const failed=demo.loadEvidence();demo.window.personalEpoch=4;label.textContent='current workspace';reject(Error('old request error'));await failed;assert.equal(label.textContent,'current workspace');
console.log('Sidebar workspace clearing and stale-response checks passed');
})().catch(error=>{console.error(error);process.exitCode=1;});
