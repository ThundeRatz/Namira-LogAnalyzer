
import math
import numpy as np

class DangerAnalyzer:

    def __init__(self, game):

        self.game = game
        self.play_on_cycles = game.get_play_on_cycles()


        # Temp parameters

        self.temp_opponent_pos = np.zeros((11,2))
        self.temp_opponent_dis = []
        self.temp_teammate_pos = np.zeros((11,2))
        self.temp_teammate_dis = []
        self.temp_opponent_angle = []


        # Danger parameters

        self.danger_ball_pos = []
        self.danger_opponent_dis = []
        self.danger_opponent_pos = []
        self.danger_opponent_angle = []
        self.danger_teammate_dis = []
        self.danger_teammate_pos = []

    def csv_headers(self):
        
        return [
            'ball position x',
            'ball position y',
            'opponent 1 distance',
            'opponent 2 distance',
            'opponent 3 distance',
            'opponent 1 position x',
            'opponent 1 position y',
            'opponent 2 position x',
            'opponent 2 position y',
            'opponent 3 position x',
            'opponent 3 position y',
            'opponent 1 angle',
            'opponent 2 angle',
            'opponent 3 angle',
            'teammate 1 distance',
            'teammate 2 distance',
            'teammate 3 distance',
            'teammate 4 distance',
            'teammate 1 position x',
            'teammate 1 position y',
            'teammate 2 position x',
            'teammate 2 position y',
            'teammate 3 position x',
            'teammate 3 position y',
            'teammate 4 position x',
            'teammate 4 position y'
        ]

    def to_csv_line(self):
        line = []

        for j in range(len(self.danger_opponent_dis)):
            aux = [self.danger_ball_pos[j]] + [self.danger_opponent_dis[j]] +\
            [self.danger_opponent_pos[j][0]] + [self.danger_opponent_pos[j][1]] +\
            [self.danger_opponent_pos[j][2]] + [self.danger_opponent_angle[j]] +\
            [self.danger_teammate_dis[j]] + [self.danger_teammate_pos[j][0]] +\
            [self.danger_teammate_pos[j][1]] + [self.danger_teammate_pos[j][2]] +\
            [self.danger_teammate_pos[j][3]]

            line.append([item for sublist in aux for item in sublist])

        return line

    def draw_heatmap(self):
        raise NotImplementedError("Danger analyzer has no heatmap implementation.")

    def to_dictionary(self):
        raise NotImplementedError("Danger analyzer has no dictionary parsing implementation.")
    
    def check_cycle(self, cycle):
        min_cycle1 = 6
        max_cycle1 = 3000

        min_cycle2 = min_cycle1 + 3000
        max_cycle2 = max_cycle1 + 3000

        if ((min_cycle1 < cycle and cycle < max_cycle1) or 
            (cycle > min_cycle2 and cycle < max_cycle2)):
            return True

        return False

    def check_lost_ball(self, cycle):
        lost_ball = False
        if (self.game.get_last_kickers(cycle)[0].team.name == self.game.right_team.name and
            self.game.get_last_kickers(cycle-1)[0].team.name == self.game.left_team.name):
            lost_ball = True
        return lost_ball, cycle-1

    def ball_data(self, cycle, i):
        x_ball = self.game.ball_pos[cycle-i]['x']
        y_ball = self.game.ball_pos[cycle-i]['y']
        self.danger_ball_pos.append([x_ball, y_ball])

    def opponent_data(self, cycle, i):
        for agent in self.game.right_team.agents:
            dx = agent.data[cycle-i]['x'] - self.game.ball_pos[cycle-i]['x']
            dy = agent.data[cycle-i]['y'] - self.game.ball_pos[cycle-i]['y']
            distance = math.sqrt(dx**2 + dy**2)
            self.temp_opponent_dis.append(distance)
            self.temp_opponent_pos[len(self.temp_opponent_dis) - 1][0] = agent.data[cycle-i]['x']
            self.temp_opponent_pos[len(self.temp_opponent_dis) - 1][1] = agent.data[cycle-i]['y']
            self.temp_opponent_angle.append(np.arctan(dy/dx))

    def closest_opponent_data(self):
        for k in range(3):
            for j in range(len(self.temp_opponent_dis) - 1, k, -1):
                if self.temp_opponent_dis[j] < self.temp_opponent_dis[j-1]:
                    temp_dis = self.temp_opponent_dis[j-1]
                    self.temp_opponent_dis[j-1] = self.temp_opponent_dis[j]
                    self.temp_opponent_dis[j] = temp_dis
                    
                    temp_angle = self.temp_opponent_angle[j-1]
                    self.temp_opponent_angle[j-1] = self.temp_opponent_angle[j]
                    self.temp_opponent_angle[j] = temp_angle

                    temp_x = self.temp_opponent_pos[j-1][0]
                    temp_y = self.temp_opponent_pos[j-1][1]
                    self.temp_opponent_pos[j-1][0] = self.temp_opponent_pos[j][0]
                    self.temp_opponent_pos[j][0] = temp_x
                    self.temp_opponent_pos[j-1][1] = self.temp_opponent_pos[j][1]
                    self.temp_opponent_pos[j][1] = temp_y
        
        self.danger_opponent_dis.append(self.temp_opponent_dis[0:3])
        self.danger_opponent_pos.append(self.temp_opponent_pos[0:3])
        self.danger_opponent_angle.append(self.temp_opponent_angle[0:3])

    def teammate_data(self, cycle, i):
        for agent in self.game.left_team.agents:
            dx = agent.data[cycle-i]['x'] - self.game.ball_pos[cycle-i]['x']
            dy = agent.data[cycle-i]['y'] - self.game.ball_pos[cycle-i]['y']
            distance = math.sqrt(dx**2 + dy**2)
            self.temp_teammate_dis.append(distance)
            self.temp_teammate_pos[len(self.temp_teammate_dis) - 1][0] = agent.data[cycle-i]['x']
            self.temp_teammate_pos[len(self.temp_teammate_dis) - 1][1] = agent.data[cycle-i]['y']

    def closest_teammate_data(self):
        for k in range(4):
            for j in range(len(self.temp_teammate_dis) - 1, k, -1):
                if self.temp_teammate_dis[j] < self.temp_teammate_dis[j-1]:
                    temp_dis = self.temp_teammate_dis[j-1]
                    self.temp_teammate_dis[j-1] = self.temp_teammate_dis[j]
                    self.temp_teammate_dis[j] = temp_dis

                    temp_x = self.temp_teammate_pos[j-1][0]
                    temp_y = self.temp_teammate_pos[j-1][1]
                    self.temp_teammate_pos[j-1][0] = self.temp_teammate_pos[j][0]
                    self.temp_teammate_pos[j][0] = temp_x
                    self.temp_teammate_pos[j-1][1] = self.temp_teammate_pos[j][1]
                    self.temp_teammate_pos[j][1] = temp_y
        
        self.danger_teammate_dis.append(self.temp_teammate_dis[0:4])
        self.danger_teammate_pos.append(self.temp_opponent_pos[0:4])

    def check_danger_param(self, cycle):
        if (self.check_cycle(cycle)):
            if self.check_lost_ball(cycle)[0]:
                for i in range(5):
                    self.temp_opponent_pos = np.zeros((11,2))
                    self.temp_opponent_dis = []
                    self.temp_teammate_pos = np.zeros((11,2))
                    self.temp_teammate_dis = []
                    self.temp_opponent_angle = []

                    self.ball_data(cycle, i)
                    self.opponent_data(cycle, i)
                    self.closest_opponent_data()
                    self.teammate_data(cycle, i)   
                    self.closest_teammate_data()

    def analyze(self):
        """Analyze game"""

        for cycle in range(1,self.play_on_cycles[-1]+1):
            self.check_danger_param(cycle)
