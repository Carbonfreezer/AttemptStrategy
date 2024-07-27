# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 13:56:49 2024

@author: chris
"""
import numpy as np

import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"
import plotly.graph_objects as go
import pandas as pd

def SingleAttempt(work, barrier, maxVal, dimRetInvest):
    if work < barrier : 
        return 0.0 
    else:
        return maxVal * (((work - barrier) / (1.0 - barrier)) ** (1.0 - dimRetInvest))

def MultiAttempt(numOfAttempts, barrier, maxVal, dimRetInvest):
    return 1.0 - (1.0 - SingleAttempt(1.0 / numOfAttempts, barrier, maxVal, dimRetInvest) ) ** numOfAttempts    


delta = 0.01
numEntries = int(1.0 / delta) 
barrierBadge = range(1, numEntries)
attemptSize = 20
attemptArray = range(1,attemptSize)
finalArray = np.zeros((numEntries - 1, numEntries - 1))



def PlotSucessDependency():
    barrier = 0.2
    maxVal = 0.8
    deltaBadge = [delta * x for x in barrierBadge]
    diminishBadge =  [0.0, 0.2, 0.5, 0.6,  0.8 , 0.999]
    
    
    firstColumn = []
    for val in diminishBadge:
        firstColumn.extend([val] * len(deltaBadge))
        
    secondColumn = []
    for _  in diminishBadge:
        secondColumn.extend(deltaBadge)
    
    thirdColumn = [SingleAttempt(secondColumn[idx], barrier, maxVal, firstColumn[idx]) for idx in range(0, len(firstColumn))]
    
    df = pd.DataFrame({'Diminishing return on investment' : firstColumn, 'Effort' : secondColumn, 'Success probability' : thirdColumn})              
    fig = px.line(df, x='Effort', y = 'Success probability', color='Diminishing return on investment', 
                  title="Fig 1: Success for minimum effort " + str(barrier) + " maximum success probability " + str(maxVal))
    fig.show()

def RunBarrierMaxVal(useAttempts):
    exponent = 0.5
    for barrier in barrierBadge:
        for maxVal in barrierBadge:
            testArray = [MultiAttempt(attempt, barrier * delta, maxVal * delta, exponent) for attempt in attemptArray]
            if useAttempts:
                finalArray[barrier - 1, maxVal - 1] = np.argmax(testArray) + 1
            else:
                finalArray[barrier - 1, maxVal - 1] = np.max(testArray)
    
    
    fig = go.Figure(data =
        go.Contour(
            z= np.transpose( finalArray ),
            dx=delta,
            x0=delta,
            dy=delta,
            y0=delta
        )
    )
    
    fig.update_layout(
           {  
            "title" : "Fig 2a: Amount of attempts to use for diminishing return on investment " + str(exponent) if useAttempts else "Fig 2b: Maximum probability for diminishing return on investment " + str(exponent),
            "legend" : {"title" : "Attempts"},
            "showlegend": True,
            "xaxis": {"title": "Minimum effort"}, 
            "yaxis": {"title": "Maximum success probability for single attempt"},
            })
    
    fig.show()
    
    
def RunExponentBarrier(useAttempts):
     maxVal = 0.1
     for barrier in barrierBadge:
         for exponent in barrierBadge:
             testArray = [MultiAttempt(attempt, barrier * delta, maxVal, exponent * delta) for attempt in attemptArray]
             if useAttempts:
                finalArray[barrier - 1, exponent - 1] = np.argmax(testArray) + 1
             else:
                finalArray[barrier - 1, exponent - 1] = np.max(testArray) 
     
     
     fig = go.Figure(data =
         go.Contour(
             z= np.transpose( finalArray ),
             dx=delta,
             x0=delta,
             dy=delta,
             y0=delta
            
         )
     )
     
     fig.update_layout(
            {  
             "title" :  "Fig 3a: Amount of attempts to use for maximum succes probability for single attempt " + str(maxVal) if useAttempts else "Fig 3b: Maximum probability for maximum succes probability for single attempt " + str(maxVal),
             "legend" : {"title" : "Attempts"},
             "showlegend": True,
             "xaxis": {"title": "Minimum effort"}, 
             "yaxis": {"title": "Diminishing return on investment"},
             })
     
     fig.show()   
   


PlotSucessDependency()
for attempts in [True, False]:     
     RunBarrierMaxVal(attempts)   
     RunExponentBarrier(attempts)  
