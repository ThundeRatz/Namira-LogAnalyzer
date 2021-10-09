# -*- coding: utf-8 -*-

from Parser import *
from Game import *
from Analyzer import *
import numpy as np
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

files = os.listdir(__location__ + "/Data")
logs = [file.split('.')[0] for file in files if file.endswith(".rcg")]
logs = list(set(logs))

data = []
results = []

for i, log in enumerate(logs):
    print(f"Starting: {i} - {log}")

    parser = Parser(__location__+ "/Data/" + log)
    game = Game(parser)
    analyzer = Analyzer(game)
    analyzer.analyze()

    for j in range(len(analyzer.agent_left_states)):
        try:
            aux = [analyzer.agent_left_states[j]] + analyzer.agent_right_states[j] + [analyzer.ball_positions[j]]
            data.append([item for sublist in aux for item in sublist])
            results.append(analyzer.risky_left[j])
        except:
            continue

    print(f"Finishing: {i} - {log}")

data = np.transpose(data)

np.savetxt("data.txt", data, fmt='%.4f')
np.savetxt("results.txt", [results], fmt='%d')

#L.x,L.y,L.stm,R.1.x,R.1.y,R.1.stm,R.2.x,R.2.y,R.2.stm,R.3.x,R.3.y,R.3.stm,R.4.x,R.4.y,R.4.stm,Ball.x,Ball.y,Pass.Angle
