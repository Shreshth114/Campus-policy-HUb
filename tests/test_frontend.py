"""Run the dashboard's JavaScript behavior checks as part of the full suite."""
from pathlib import Path
import shutil
import subprocess
import pytest


def test_frontend_behavior():
    node=shutil.which('node')
    if not node:
        pytest.fail('Node.js is required for dashboard behavior verification')
    script=Path(__file__).with_name('frontend.test.cjs')
    result=subprocess.run([node,str(script)],capture_output=True,text=True,timeout=20)
    assert result.returncode==0,result.stdout+result.stderr
    assert '19 dashboard checks passed' in result.stdout


def test_personal_frontend_behavior():
    node=shutil.which('node')
    assert node,'Node.js required'
    result=subprocess.run([node,str(Path(__file__).with_name('personal_frontend.test.cjs'))],capture_output=True,text=True,timeout=20)
    assert result.returncode==0,result.stdout+result.stderr


def test_document_changes_frontend_behavior():
    node=shutil.which('node')
    assert node,'Node.js required'
    result=subprocess.run([node,str(Path(__file__).with_name('document_changes_frontend.test.cjs'))],capture_output=True,text=True,timeout=20)
    assert result.returncode==0,result.stdout+result.stderr
