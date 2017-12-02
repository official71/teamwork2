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
    __tablename__ = 'NYC_Restaurants'
    # columns
    rid = Column(String, primary_key=True)
    dba = Column(String)
    boro = Column(String)
    street = Column(String)
    # zipcode = Column(String)
    cuisine = Column(String)
    inspect_time = Column(String)
    action = Column(String)
    # violation = Column(String)
    critical_flag = Column(String)
    grade = Column(String)
    inspect_type = Column(String)


# create engine
engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)

# create the session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# field specific functions
def fun_dba(v):
    if not v: v = "N/A"
    return u"DBA_({})".format(v)

def fun_boro(v):
    if not v: v = "Missing"
    return u"BORO_({})".format(v)

def fun_street(v):
    if not v: v = "N/A"
    v = " ".join(v.split())
    return u"STREET_({})".format(v)

def fun_zipcode(v):
    if not v: v = "N/A"
    return u"ZIPCODE_({})".format(v)

def fun_cuisine(v):
    if not v: v = "N/A"
    return u"CUISINE_({})".format(v)

def fun_inspect_time(v):
    try:
        dt = datetime.strptime(v, '%m/%d/%Y')
        r = "Q{}".format(1 + (dt.month-1) / 3)
    except:
        r = "N/A"
    return u"INSPEC_TIME_{}".format(r)

def fun_action(v):
    if "Closed by DOHMH" in v:
        r = "CLOSED"
    elif "Violations were cited" in v:
        r = "CITED"
    elif "No violations" in v:
        r = "NO_VIOLATION"
    elif "re-opened" in v:
        r = "RE-OPEN"
    elif "re-closed" in v:
        r = "RE-CLOSED"
    else:
        r = "N/A"
    return u"ACTION_{}".format(r)

def fun_violation(v):
    if len(v) != 3:
        return u"VIOLATION_NONE"
    return u"VIOLATION_{}".format(v[:2])

def fun_critical_flag(v):
    if v == "Critical":
        return u"CRITICAL_VIOLATION"
    else:
        return u"NON_CRITICAL_VIOLATION"

def fun_grade(grade, score):
    # reference: http://www1.nyc.gov/assets/doh/downloads/pdf/rii/how-we-score-grade.pdf
    if grade in ['Z', 'P', 'Not Yet Graded']:
        r = "PEND"
    elif not grade:
        if not score or score <= 13:
            r = "A"
        elif score <= 27:
            r = "B"
        else:
            r = "C"
    else:
        r = grade
    return u"GRADE_{}".format(r)

def fun_inspect_type(v):
    try:
        r = v.split(' / ')[-1]
        if r == "Initial Inspection":
            return u"INITIAL_INSPECTION"
        elif r == "Re-inspection":
            return u"RE-INSPECTION"
    except:
        pass
    return u"OTHER_INSPECTION_TYPE"


"""
DOHMH New York City Restaurant Inspection Results:
(https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j)
col#    description 
0       CAMIS
1       DBA
2       BORO
3       BUILDING
4       STREET
5       ZIPCODE
6       PHONE
7       CUISINE DESCRIPTION
8       INSPECTION DATE
9       ACTION
10      VIOLATION CODE
11      VIOLATION DESCRIPTION
12      CRITICAL FLAG
13      SCORE
14      GRADE
15      GRADE DATE
16      RECORD DATE
17      INSPECTION TYPE
"""
fname = "DOHMH_New_York_City_Restaurant_Inspection_Results.csv"
f = open(fname, 'r')

# CSV reader
reader = csv.reader(f, delimiter=',', quotechar='\"')
titles = reader.next()
rid = 0
try:
    for line in reader:
        line = [item.decode('utf-8') for item in line]
        rid += 1
        record = DBTable(**{
            "rid": str(rid),
            "dba": fun_dba(line[1]),
            "boro": fun_boro(line[2]),
            "street": fun_street(line[4]),
            # "zipcode": fun_zipcode(line[5]),
            "cuisine": fun_cuisine(line[7]),
            "inspect_time": fun_inspect_time(line[8]),
            "action": fun_action(line[9]),
            # "violation": fun_violation(line[10]),
            "critical_flag": fun_critical_flag(line[12]),
            "grade": fun_grade(line[14], line[13]),
            "inspect_type": fun_inspect_type(line[17])
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
outname = "DOHMH_New_York_City_Restaurant_Inspection_Results.reformat.csv"
with open(outname, 'wb') as outfile:
    outcsv = csv.writer(outfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
    records = session.query(DBTable).all()
    outcsv.writerow(DBTable.__table__.columns.keys())
    for rec in records:
        l = [getattr(rec, column.name).encode('utf-8') for column in DBTable.__mapper__.columns]
        outcsv.writerow(l)





