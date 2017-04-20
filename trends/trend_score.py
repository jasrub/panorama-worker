from database_connection import db
from scipy.interpolate import interp1d

# -1 is trending, 1 is ongoing

num_days = 15

days_m = interp1d([0, num_days],[1, 0.3]) #map to 0-1 score of trendiness. higher score = more trending
seconds_m = interp1d([0,86400], [1, 0.6]) # map to 0-1 score of trendiness. higher score = more trending (1 - very trending, 0 - not trending)
score_m = interp1d([1, 0], [-1, 1]) # map a score of 0-1 to a score of -1 - 1


def score(text, publish_date):
    score = 1
    trends = db.get_all_trends(num_days)
    for t in trends:
        part_text = 0
        in_text = is_in_text(t['id'], text.lower())
        if not in_text:
            part_text = part_in_text(t['id'], text.lower())
        if in_text or part_text>0:
            mul  = 1 if in_text else part_text
            time_difference = t['updated_at']-publish_date
            curr_score =  calculate_score(time_difference, mul)
            score = min(score, curr_score)
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
