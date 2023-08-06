from locdataMAC.logger import logger
from locdataMAC.cutom_exception import InvalidpathException
from ensure import ensure_annotations
import os
import json
import numpy as np
import pandas as pd
import plotly.express as px

@ensure_annotations
def json_data(path:str):
    if not os.path.exists(path):
        raise InvalidpathException(f"json file not found.")
    try:
        f = open(path)
        data = json.load(f)
        # Closing file
        f.close()
        json_object = json.dumps(data['activities'], indent=4)
        logger.info(f"json file saved at: {path}")
        with open("data.json", "w") as outfile:
            outfile.write(json_object)
        return open("data.json", mode='r')
    except Exception:
        raise InvalidpathException

def hour_convvertor(x):
    json_data=x[0]
    hour=round(json_data['hours']+(json_data['minutes']/60)+(json_data['seconds']/(60*60)),5)
    return hour

@ensure_annotations
def mydata_analysis(path:str):
    df= pd.read_json(path)
    df['time_spent'] = df.time_entries.apply(hour_convvertor)
    df.drop(['time_entries'],axis='columns',inplace=True)
    fig = px.bar(df, x='name', y='time_spent')
    df_sorted = df.sort_values('time_spent',ascending=False)
    fig1 = px.bar(df_sorted.head(3), x='name', y='time_spent')
    return fig.show(),fig1.show()
    
