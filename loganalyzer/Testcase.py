# -*- coding: utf-8 -*-

from Parser import *
from Game import *
from Analyzer import *
import numpy as np
import pandas as pd

parser = Parser('20210909222921-ThunderLeague_0-vs-oto_0')

game = Game(parser)

analyzer = Analyzer(game)
analyzer.analyze()

csv_dump = []

for i in range(len(analyzer.agent_left_states)):
    aux = [analyzer.agent_left_states[i]] + analyzer.agent_right_states[i] + [analyzer.ball_positions[i]]
    csv_dump.append([f"Pass {i+1}"] + [item for sublist in aux for item in sublist])

df = pd.DataFrame(np.array(csv_dump),
                   columns=['Pass Number', 'L.x', 'L.y', 'L.stm',
                            'R.1.x' , 'R.1.y' ,'R.1.stm',
                            'R.2.x' , 'R.2.y' ,'R.2.stm',
                            'R.3.x' , 'R.3.y' ,'R.3.stm',
                            'R.4.x' , 'R.4.y' ,'R.4.stm',
                            'Ball.x', 'Ball.y', 'Ball.Vx', 'Ball.Vy'])

df.to_csv('data.csv', index=False)
