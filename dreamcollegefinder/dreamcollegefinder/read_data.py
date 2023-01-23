import pandas as pd
from .models import Rankings, SchoolInfo
import os

def getData(request):
    filename="Rankings.csv"
    df = pd.read_csv(filename)

    for i in range(1, df.shape[0]):
        rank = Rankings(
            name=df['Name'][i], 
            academics=df['Academics'][i],
            athletics=df['Athletics'][i],
            diversity=df['Diversity'][i],
            professors=df['Professors'][i],
            safety=df['Safety'][i],
            rank=df['Value'][i],
            collegeLife=df['Student_Life'][i])
        rank.save()
    
    filename="SchoolInfo.csv"
    df = pd.read_csv(filename)

    for i in range(1, df.shape[0]):
        info = SchoolInfo(
            name = df['Name'][i],
            location = df['Location'][i],
            acceptanceRate = df['Acceptance_Rate'][i],
            netPrice = df['Net_Price'][i],
            rangeSAT = df['SAT_Range'][i])
        info.save()

