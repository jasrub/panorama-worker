from database_connection import db
from scipy.interpolate import interp1d

days_m = interp1d([0, 7],[1, 0.2])
seconds_m = interp1d([0,86400], [1, 0.7])
score_m = interp1d([0, 1], [-1, 1])

def score(text, publish_date):
    score = -1
    trends = db.get_all_trends(5)
    for t in trends:
        part_text = 0
        in_text = is_in_text(t['id'], text.lower())
        if not in_text:
            part_text = part_in_text(t['id'], text.lower())
        if in_text or part_text>0:
            mul  = 1 if in_text else part_text
            time_difference = t['updated_at']-publish_date
            curr_score =  calculate_score(time_difference, mul)
            score = max(score, curr_score)
    return float(score)

def is_in_text(term, text):
    words = term.split(' ')
    all_words = True
    for w in words:
        if w not in text:
            all_words = False
    return all_words or term in text

def part_in_text(term, text):
    words = term.split(' ')
    count = 0
    for w in words:
        if w in text:
            count+=1
    return count*1.0/len(words)

def calculate_score(time_difference, mul):
    if time_difference.days <= 0:
        score = seconds_m(abs(time_difference.seconds))*mul
    else:
        score = days_m(time_difference.days)*mul
    return score_m(score)
