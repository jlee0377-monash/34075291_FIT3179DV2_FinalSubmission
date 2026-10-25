"""Build data-derived summary CSVs for the Farmers' Markets data story.
Run from this folder: python build_data.py
Only geographic reference coordinates are specified in code; counts are calculated from source CSVs.
"""
import csv, re
from collections import defaultdict

STATE_RE = re.compile(r'\b(NSW|VIC|QLD|SA|WA|TAS|ACT|NT)\s*\d{4}\b', re.I)
STATE_NAMES = {'NSW':'New South Wales','VIC':'Victoria','SA':'South Australia','WA':'Western Australia','QLD':'Queensland','TAS':'Tasmania','ACT':'Australian Capital Territory','NT':'Northern Territory'}
# Approximate state-capital reference anchors, used only to place state-level aggregates.
COORDS = {'NSW':(147.0,-32.0),'VIC':(145.0,-37.0),'SA':(133.0,-30.0),'WA':(122.0,-25.0),'QLD':(144.0,-22.0),'TAS':(147.0,-42.0),'ACT':(149.13,-35.28),'NT':(133.0,-19.0)}
counts = defaultdict(int); weekend = defaultdict(int); schedules = defaultdict(set)
with open('AFMA_markets.csv', newline='', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        address = row.get('Address_Details','') or ''
        match = STATE_RE.search(address)
        code = match.group(1).upper() if match else 'Other'
        if code not in COORDS: continue
        counts[code] += 1
        days = (row.get('Market_Days','') or '').strip()
        if re.search(r'saturday|sunday', days, re.I): weekend[code] += 1
        if days: schedules[code].add(days)
with open('state_market_metrics.csv','w',newline='',encoding='utf-8') as f:
    fields=['State','Code','TotalMarkets','WeekendMentionCount','WeekendMentionShare','DistinctScheduleDescriptions','longitude','latitude']
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
    for code in ['NSW','VIC','QLD','SA','WA','TAS','ACT','NT']:
        total=counts[code]; c,lat=COORDS[code]
        w.writerow({'State':STATE_NAMES[code],'Code':code,'TotalMarkets':total,'WeekendMentionCount':weekend[code], 'WeekendMentionShare':round(weekend[code]/total,4) if total else 0, 'DistinctScheduleDescriptions':len(schedules[code]),'longitude':c,'latitude':lat})
# Summary data for the donut chart: derive categories directly from actual event-type values.
from collections import Counter
counter=Counter()
with open('brisbane-markets.csv',newline='',encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        category=(row.get('Event type(Id:21893)','') or '').strip() or 'Unspecified'
        counter[category]+=1
with open('brisbane_event_type_summary.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['MarketType','Mentions']); w.writeheader()
    for category,count in counter.most_common(): w.writerow({'MarketType':category,'Mentions':count})
print('Rebuilt state_market_metrics.csv and brisbane_event_type_summary.csv from source CSV files.')
