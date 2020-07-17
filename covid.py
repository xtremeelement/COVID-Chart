import asyncio
import requests
import json
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime


deaths = []
date = []
cases = []
hospital = []
test = []
percentage = []
async def getData():
    url = 'https://covidtracking.com/api/v1/states/fl/daily.json'
    r = requests.get(url)    
    pretty= r.json()

    for increase in pretty:        
        deaths.append(increase['deathIncrease'])
        tempDate = str(increase['date'])
        formattedDate =datetime.strptime(tempDate, '%Y%m%d').strftime('%m/%d/%Y')        
        date.append(formattedDate)
        cases.append(increase['positiveIncrease'])
        hospital.append(increase['hospitalizedIncrease'])
        test.append(increase['totalTestResultsIncrease'])
    
    for a, b in zip(cases,test):
        if(a == 0):
            percentage.append(0)
        else:
            percentage.append((100*(a/b))//1)  
   

asyncio.run(getData())

date.reverse()
deaths.reverse()
cases.reverse()
hospital.reverse()
percentage.reverse()

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("New Cases", "New Deaths", "New Hospitalizations", "Percentage Positive"))

fig.add_trace(go.Scatter(x=date[18:], y=cases[18:], name="New Cases"),
              row=1, col=1)

fig.add_trace(go.Scatter(x=date[18:], y=deaths[18:], name="New Deaths"),
              row=1, col=2)

fig.add_trace(go.Scatter(x=date[18:], y=hospital[18:], name="New Hospitalizations"),
              row=2, col=1)
fig.add_trace(go.Scatter(x=date[18:], y=percentage[18:], name="Percentage Positive"),
              row=2, col=2)

fig.update_layout(height=850, width=1500,
                  title_text="COVID Data")

fig.show()
