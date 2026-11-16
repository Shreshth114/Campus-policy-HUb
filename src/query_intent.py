"""Conservative event cues; no policy answers or institution-specific rules."""
import re


def understand(question):
    q=question.casefold()
    classes=bool(re.search(r'\b(?:miss\w*|absen\w*)\b.{0,45}\b(?:classes|lectures|labs)\b',q))
    exams=bool(re.search(r'\bmiss(?:ed|ing)?\s+(?:(?:my|the|an|a|end[- ]term|final)\s+){0,3}(?:exam|examination|finals)\b',q))
    sick=bool(re.search(r'\b(?:sick|ill|illness|medical)\b',q))
    ambiguous=sick and not re.search(r'\b(?:personally|approved|today|tomorrow|morning|status)\b',q) and not classes and not exams and not re.search(r'attendance|condonation|certificate|deadline|threshold',q)
    event='missed_classes' if classes and not exams else 'missed_exam' if exams and not classes else None
    return {'event':event,'clarification':('Did you miss classes, an examination, or both?' if ambiguous else None)}


def search_question(question):
    event=understand(question)['event']
    cue={'missed_classes':'Event: absence from classes; attendance shortage. No missed examination has been stated.',
         'missed_exam':'Event: absence from an examination; make-up examination.'}.get(event)
    return question+ ('\n'+cue if cue else '')


def provision_terms(question):
    """Generic event vocabulary for selection; never numbers or policy rules."""
    terms=set(re.findall(r'\b\w{4,}\b',question.casefold()))
    event=understand(question)['event']
    if event=='missed_classes':
        terms.update(('attendance','absence','shortage'))
    elif event=='missed_exam':
        terms.update(('examination','make','miss'))
    if re.search(r'\b(?:sick|ill|illness|medical)\b',question,re.I):
        terms.update(('medical','illness'))
    return terms
