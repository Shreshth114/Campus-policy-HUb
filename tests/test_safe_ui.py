from pathlib import Path
import subprocess

def test_safe_minimal_markdown_and_citations():
    path=Path(__file__).resolve().parents[1]/'web/ui.js'
    code="""const assert=require('node:assert/strict');const ui=require(process.argv[1]);
const rendered=ui.render('**Answer:** *condition*\\n- Item [C1]\\n<img src=x onerror=bad()> <script>bad()</script>',{maxCitation:1});
assert(rendered.includes('<strong>Answer:</strong>'));assert(rendered.includes('<em>condition</em>'));assert(rendered.includes('<ul><li>'));
assert(rendered.includes('href=\"#evidence-C1\"'));assert(!rendered.includes('<img'));assert(!rendered.includes('<script>'));
assert(!ui.render('[C2]',{maxCitation:1}).includes('<a'));assert(ui.footer(true).includes('not been verified'));"""
    result=subprocess.run(['node','-e',code,str(path)],capture_output=True,text=True)
    assert result.returncode==0,result.stderr
