# -*- coding: utf-8 -*-

from Parser import *
from Game import *
from Analyzer import *
import numpy as np
import pandas as pd
import os

l=os.listdir(os.getcwd())
li=[x.split('.')[0] for x in l if x.endswith(".rcg")]

li = list(set(li))
data = []
results = []

for i in li:
    parser = Parser(i)
    game = Game(parser)
    analyzer = Analyzer(game)
    analyzer.analyze()

    results += analyzer.risky_left

    for i in range(len(analyzer.agent_left_states)):
        aux = [analyzer.agent_left_states[i]] + analyzer.agent_right_states[i] + [analyzer.ball_positions[i]]
        data.append([item for sublist in aux for item in sublist])

data = np.transpose(data)

np.savetxt("data.txt", data, fmt='%.4f')
np.savetxt("results.txt", [results], fmt='%d')

#L.x,L.y,L.stm,R.1.x,R.1.y,R.1.stm,R.2.x,R.2.y,R.2.stm,R.3.x,R.3.y,R.3.stm,R.4.x,R.4.y,R.4.stm,Ball.x,Ball.y,Ball.Vx,Ball.Vy
