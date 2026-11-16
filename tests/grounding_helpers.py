"""Explicit model-double responses for the structured evidence contract."""
import json
from src.llm import LLMResponse

def selection(quote,source='C1'):
    return json.dumps({'status':'answer','claims':[{'quote':quote,'source':source}]})

def accepted_review(question='q',refs=None):
    from src.question_coverage import question_requirements
    return json.dumps({'coverage':[{'requirement_id':r['id'],'status':'covered','evidence':refs or ['C1/P1'],'reason':''} for r in question_requirements(question)],'relevant':True,'complete':True,'qualifications_preserved':True,'supported':True,'reasons':[]})

def fixture_reply(messages,quote):
    if messages[0]['content'].startswith('Review a proposed evidence selection'):
        import re,html
        from src.evidence import normalize
        data=json.loads(messages[1]['content']);refs=[]
        for claim in data['proposed_selection']['claims']:
            if 'provision' in claim:refs.append(claim['source']+'/'+claim['provision']);continue
            source=re.search(r'<excerpt id="'+claim['source']+r'"[^>]*>(.*?)</excerpt>',data['evidence'],re.S)[1]
            refs += [claim['source']+'/'+pid for pid,text in re.findall(r'<provision id="(P\d+)">(.*?)</provision>',source,re.S)
                     if normalize(html.unescape(text))==normalize(claim['quote'])]
        text=accepted_review(data['question'],refs)
    else:
        text=selection(quote)
    return LLMResponse(text,'fixture','fixture-model',2,3,4)
