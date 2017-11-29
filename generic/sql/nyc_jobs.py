from sqlalchemy import Column, Integer, Float, Date, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv
import re
from datetime import datetime

# define DB schema
Base = declarative_base()
class DBTable(Base):
    __tablename__ = 'NYC_Jobs'
    # __table_args__ = {'convert_unicode': True}
    # columns
    job_id = Column(String, primary_key=True)
    agency = Column(String)
    posting_type = Column(String)
    nr_positions = Column(String)
    title = Column(String)
    level = Column(String)
    job_category = Column(String)
    # full_time = Column(String)
    salary = Column(String)
    # work_location = Column(String)
    # division = Column(String)
    # job_description = Column(String)
    # hours_shift = Column(String)
    residency_requirement = Column(String)
    posting_date = Column(String)
    # post_until = Column(String)


# create engine
engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)

# create the session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

"""
NYC jobs CSV structure:
(https://data.cityofnewyork.us/City-Government/NYC-Jobs/kpav-sd4t)
col description 
0   Job ID
1	Agency
2	Posting Type
3	# Of Positions
4	Business Title
5	Civil Service Title
6	Title Code No
7	Level
8	Job Category
9	Full-Time/Part-Time indicator
10	Salary Range From
11	Salary Range To
12	Salary Frequency
13	Work Location
14	Division/Work Unit
15	Job Description
16	Minimum Qual Requirements
17	Preferred Skills
18	Additional Information
19	To Apply
20	Hours/Shift
21	Work Location 1
22	Recruitment Contact
23	Residency Requirement
24	Posting Date
25	Post Until
26	Posting Updated
27	Process Date
"""

# field specific functions
def format_agency(s):
    # "MANHATTAN COMMUNITY BOARD #6" -> "MANHATTAN COMMUNITY BOARD"
    s = re.sub(r'\s+#\d+$', '', s)
    return u"AGENCY_[{}]".format(s)

def format_posting_type(s):
    return u"POSTING_TYPE_" + s

def format_nr_positions(s):
    try:
        n = int(s)
    except:
        n = 0
    if n <= 0:
        return u""
    elif n == 1:
        return u"SINGLE_POSITION"
    else:
        return u"MULTIPLE_POSITIONS"

def format_title(s):
    l = re.sub(r'\(.*$', '', s).split()
    if not l:
        return u""
    else:
        return u"TITLE_" + l[-1]

def format_level(s):
    s = re.sub(r'\D', '', s)
    try:
        n = int(s)
    except:
        return u""
    if n > 10:
        return u"LEVEL_OTHER"
    return u"LEVEL_" + s

def format_job_category(s):
    if not re.match(r'^\S*$', s): return u""
    return u"JOB_CATEGORY_[{}]".format(s)

def format_full_time(s):
    if s == "F":
        return u"FULL_TIME"
    else:
        return u"PART_TIME"

def format_salary(salary_from, salary_to, salary_freq):
    if not re.match(r'^\d+$', salary_from) or not re.match(r'^\d+$', salary_to):
        return u""
    n = (int(salary_from) + int(salary_to)) / 2
    if salary_freq == "Hourly":
        n = n * 8 * 20 * 12
    elif salary_freq == "Daily":
        n = n * 20 * 12
    # n is the annual salary
    if n <= 50000:
        return u"SALARY_0-50K_YEAR"
    elif n <= 70000:
        return u"SALARY_50K-70K_YEAR"
    elif n <= 90000:
        return u"SALARY_70K-90K_YEAR"
    else:
        return u"SALARY_90+K_YEAR"

def format_work_location(s):
    if not s: s = u""
    return u"WORK_LOCATION_[{}]".format(s)

def format_residency_requirement(s):
    s = s.lower()
    if re.match(r'.*residency (is |)required.*', s):
        return "RESIDENCY_REQUIREMENT_YES"
    elif re.match(r'.*residency is generally required.*however.*', s):
        return "RESIDENCY_REQUIREMENT_YES"
        # return "RESIDENCY_REQUIREMENT_PENDING"
    else:
        return "RESIDENCY_REQUIREMENT_NO"

def format_posting_date(s):
    try:
        dt = datetime.strptime(s, '%d-%b-%y')
        return u"POSTED_IN_" + dt.strftime('%Y')
    except:
        return u""

def format_post_until(date_from, date_until):
    if not date_until:
        return u"POST_UNTIL_FILLED"
    try:
        dtf = datetime.strptime(date_from, '%d-%b-%y')
        dtt = datetime.strptime(date_until, '%d-%b-%y')
        # return u"POST_UNTIL_" + dt.strftime('%B_%Y')
        months = (dtt - dtf).days / 30
        if months <= 6:
            return u"POST_FOR_LESS_THAN_6_MONTHS"
        else:
            return u"POST_FOR_MORE_THAN_6_MONTHS"
    except:
        return u""


fname = "NYC_Jobs.csv"
f = open(fname, 'r')

# CSV reader
reader = csv.reader(f, delimiter=',', quotechar='\"')
titles = reader.next()
job_id_seen = set() # to remove duplicate records in CSV
try:
    for line in reader:
        line = [item.decode('utf-8') for item in line]
        jid = line[0]
        if jid in job_id_seen: 
            # print "Skipping duplicate Job ID {}".format(jid)
            continue
        job_id_seen.add(jid)
        record = DBTable(**{
            'job_id': line[0],
            'agency': format_agency(line[1]),
            'posting_type': format_posting_type(line[2]),
            'nr_positions': format_nr_positions(line[3]),
            'title': format_title(line[5]),
            'level': format_level(line[7]),
            'job_category': format_job_category(line[8]),
            # 'full_time': format_full_time(line[9]),
            'salary': format_salary(line[10], line[11], line[12]),
            # 'work_location': format_work_location(line[13]),
            # 'job_description': line[15],
            # 'hours_shift': line[20],
            'residency_requirement': format_residency_requirement(line[23]),
            'posting_date': format_posting_date(line[24]),
            # 'post_until': format_post_until(line[24], line[25])
            })
        session.add(record)
    session.commit()
    print "\nCommitted"
except Exception as e:
    session.rollback()
    print "\nFailed: {}".format(e)
finally:
    session.close()

f.close()
# print session.query(DBTable).count()

# dump to csv
outname = "NYC_Jobs_reformat.csv"
with open(outname, 'wb') as outfile:
    outcsv = csv.writer(outfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
    records = session.query(DBTable).all()
    outcsv.writerow(DBTable.__table__.columns.keys())
    for rec in records:
        outcsv.writerow([getattr(rec, column.name) for column in DBTable.__mapper__.columns])





