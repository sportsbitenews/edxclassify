"""
Summarize affect distributions at varying course granularities.
"""

from classify.feature_spec import FEATURE_COLUMNS
from classify.data_cleaners.dc_util import compress_likert
import cPickle
import glob
import os
import sys

def post_fractions(values):
    post_counts = sorted(values)
    total_count = sum(post_counts)
    post_fractions = [100 * float(c) / total_count for c in post_counts[-10:]]
    return post_fractions

print sys.argv[1]
file_paths = [f for f in glob.glob(sys.argv[1]) if os.path.isfile(f)]
uid_pos = FEATURE_COLUMNS['forum_uid']
sent_pos = FEATURE_COLUMNS['sentiment']
conf_pos = FEATURE_COLUMNS['confusion']
urg_pos = FEATURE_COLUMNS['urgency']
op_pos = FEATURE_COLUMNS['opinion']
ans_pos = FEATURE_COLUMNS['answer']
q_pos = FEATURE_COLUMNS['question']
for path in file_paths:
    with open(path, 'rb') as f:
        dataset = cPickle.load(f)
        # dictionaries of persons --> affect
        posts = {}
        sentiment = [{}, {}, {}]
        confusion = [{}, {}, {}]
        urgency = [{}, {}, {}]
        opinion = [{}, {}]
        answer = [{}, {}]
        question = [{}, {}]
        for record in dataset:
            if len(record) > uid_pos and record[uid_pos] != '':
                forum_uid = record[uid_pos]
                posts[forum_uid] = posts.get(forum_uid, 0) + 1

                s = compress_likert(record[sent_pos])
                sentiment[s][forum_uid] = sentiment[s].get(forum_uid, 0) + 1

                c = compress_likert(record[conf_pos])
                confusion[c][forum_uid] = confusion[c].get(forum_uid, 0) + 1

                u = compress_likert(record[urg_pos])
                urgency[u][forum_uid] = urgency[u].get(forum_uid, 0) + 1

                o = int(record[op_pos])
                opinion[o][forum_uid] = opinion[o].get(forum_uid, 0) + 1

                a = int(record[ans_pos])
                answer[a][forum_uid] = answer[a].get(forum_uid, 0) + 1

                q = int(record[q_pos])
                question[q][forum_uid] = question[q].get(forum_uid, 0) + 1

        # number of persons in dictionary
        # percentage of posts accounted for by top 10 posters
        # percentage of affect posts accounted for by top 10 posters
        print '------- Course: %s --------' % os.path.basename(path)
        print '\tTotal posts: %d' % sum(posts.values())
        print '\tDistinct posters: %d' % len(posts)
        print '\t  ' + str(post_fractions(posts.values()))
        print '\tSentiment'
        print '\t  Negative: %d' % sum(sentiment[0].values())
        print '\t  ' + str(post_fractions(sentiment[0].values()))
        print '\t  Neutral: %d' % sum(sentiment[1].values())
        print '\t  ' + str(post_fractions(sentiment[1].values()))
        print '\t  Positive: %d' % sum(sentiment[2].values())
        print '\t  ' + str(post_fractions(sentiment[2].values()))
        print '\tConfusion'
        print '\t  Knowledgeable: %d' % sum(confusion[0].values())
        print '\t  ' + str(post_fractions(confusion[0].values()))
        print '\t  Neutral: %d' % sum(confusion[1].values())
        print '\t  ' + str(post_fractions(confusion[1].values()))
        print '\t  Confused: %d' % sum(confusion[2].values())
        print '\t  ' + str(post_fractions(confusion[2].values()))
        print '\tUrgency'
        print '\t  Non-urgent: %d' % sum(urgency[0].values())
        print '\t  ' + str(post_fractions(urgency[0].values()))
        print '\t  Semi-urgent: %d' % sum(urgency[1].values())
        print '\t  ' + str(post_fractions(urgency[1].values()))
        print '\t  Urgent: %d' % sum(urgency[2].values())
        print '\t  ' + str(post_fractions(urgency[2].values()))
        print '\tOpinion'
        print '\t  Fact: %d' % sum(opinion[0].values())
        print '\t  ' + str(post_fractions(opinion[0].values()))
        print '\t  Opinion: %d' % sum(opinion[1].values())
        print '\t  ' + str(post_fractions(opinion[1].values()))
        print '\tAnswer'
        print '\t  Not Answer: %d' % sum(answer[0].values())
        print '\t  ' + str(post_fractions(answer[0].values()))
        print '\t  Answer: %d' % sum(answer[1].values())
        print '\t  ' + str(post_fractions(answer[1].values()))
        print '\tQuestion'
        print '\t  Not Question: %d' % sum(question[0].values())
        print '\t  ' + str(post_fractions(question[0].values()))
        print '\t  Question: %d' % sum(question[1].values())
        print '\t  ' + str(post_fractions(question[1].values()))