import csv
from nltk import word_tokenize, pos_tag
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict

"""
NYC jobs CSV structure:
(https://data.cityofnewyork.us/City-Government/NYC-Jobs/kpav-sd4t)
col     description 
0       Job ID
...
15      Job Description
16      Minimum Qual Requirements
17      Preferred Skills
...
"""

class JobInfo(object):
    stemmer = SnowballStemmer("english")
    stem_lookup = {}

    def __init__(self, job_id, jd, mqr, ps):
        self.job_id = job_id
        self.job_description = jd
        self.minimum_qual_req = mqr
        self.preferred_skills = ps
        self.keywords = set()

    def __str__(self):
        return u",".join(sorted(list(self.keywords)))

    def __stem__(self, word):
        if not word: return word
        key = self.stemmer.stem(word)
        res = self.stem_lookup.get(key, None)
        if res is None:
            res = self.stem_lookup[key] = word
        return res

    def __gen_keyword_from(self, source, df_counter):
        text = word_tokenize(source)
        phrase = []
        tags = pos_tag(text)
        for i, (word, pos) in enumerate(tags):
            if 'NNP' in pos:
                word = self.__stem__(word.encode('ascii', 'ignore'))
                if word: 
                    phrase.append(word)
            if phrase and (i == len(tags) - 1 or not 'NNP' in pos):
                p = "KW[{}]".format(" ".join(phrase))
                phrase = []
                self.keywords.add(p)
                df_counter[p] += 1

    def gen_keywords(self, df_counter):
        for source in [self.job_description, self.preferred_skills]:
            self.__gen_keyword_from(source, df_counter)




fname = "NYC_Jobs.csv"

job_info_list = []
job_id_seen = set() # to remove duplicate records in CSV
nr_docs = 0
with open(fname, 'r') as f:
    reader = csv.reader(f, delimiter=',', quotechar='\"')
    titles = reader.next()
    for line in reader:
        nr_docs += 1
        job_id = line[0].decode('utf-8')
        if job_id in job_id_seen: continue
        job_id_seen.add(job_id)
        jd = line[15].decode('utf-8')
        mqr = line[16].decode('utf-8')
        ps = line[17].decode('utf-8')
        job_info_list.append(JobInfo(job_id, jd, mqr, ps))

df_counter = defaultdict(int)
for job_info in job_info_list:
    job_info.gen_keywords(df_counter)

df_threshold = int(float(nr_docs) * 0.01)
print "Minimum df required: {}".format(df_threshold)
df_filter = set()
for word, df in df_counter.items():
    if df >= df_threshold: df_filter.add(word)
print df_filter

outfname = "NYC_Jobs_keywords.txt"
with open(outfname, 'wb') as outfile:
    for job_info in job_info_list:
        words = job_info.keywords & df_filter
        s = u",".join(sorted(list(words)))
        # print s
        outfile.write(s + '\n')




