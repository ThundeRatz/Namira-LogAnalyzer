import numpy as np

class MoiseAnalyzer:

    def __init__(self, game):

        self.game = game
        self.play_on_cycles = game.get_play_on_cycles()

        # Temp parameters

        self.temp_opponent_pos = np.zeros((11,2))
        self.temp_teammate_pos = np.zeros((11,2))

        # Moise parameters

        self.ball_pos = []
        self.opponent_pos = []
        self.teammate_pos = []

    def csv_headers(self):
        
        return [
            'ball_x',
            'ball_y',
            'teammate_x_1',
            'teammate_y_1',
            'teammate_x_2',
            'teammate_y_2',
            'teammate_x_3',
            'teammate_y_3',
            'teammate_x_4',
            'teammate_y_4',
            'teammate_x_5',
            'teammate_y_5',
            'teammate_x_6',
            'teammate_y_6',
            'teammate_x_7',
            'teammate_y_7',
            'teammate_x_8',
            'teammate_y_8',
            'teammate_x_9',
            'teammate_y_9',
            'teammate_x_10',
            'teammate_y_10',
            'teammate_x_11',
            'teammate_y_11',
            'opponent_x_1',
            'opponent_y_1',
            'opponent_x_2',
            'opponent_y_2',
            'opponent_x_3',
            'opponent_y_3',
            'opponent_x_4',
            'opponent_y_4',
            'opponent_x_5',
            'opponent_y_5',
            'opponent_x_6',
            'opponent_y_6',
            'opponent_x_7',
            'opponent_y_7',
            'opponent_x_8',
            'opponent_y_8',
            'opponent_x_9',
            'opponent_y_9',
            'opponent_x_10',
            'opponent_y_10',
            'opponent_x_11',
            'opponent_y_11'
        ]

    def to_csv_line(self):
        line = []

        for j in range(len(self.ball_pos)):
            aux = [self.ball_pos[j]] + [item for item in self.teammate_pos[j]] + [item for item in self.opponent_pos[j]]

            line.append([item for sublist in aux for item in sublist])

        return line

    def draw_heatmap(self):
        raise NotImplementedError("Danger analyzer has no heatmap implementation.")

    def to_dictionary(self):
        raise NotImplementedError("Danger analyzer has no dictionary parsing implementation.")

    # TODO: Definir condições para levantar os dados do moise
    def undefined_condition(self, cycle):
        if(cycle % 50 == 10):
            return True

        return False

    def clear_temp_parm(self):
        self.temp_opponent_pos = np.zeros((11,2))
        self.temp_teammate_pos = np.zeros((11,2))
    
    def ball_data(self, cycle):
        x_ball = self.game.ball_pos[cycle]['x']
        y_ball = self.game.ball_pos[cycle]['y']
        self.ball_pos.append([x_ball, y_ball])

    def opponent_data(self, cycle):
        it = 0
        for agent in self.game.right_team.agents:
            self.temp_opponent_pos[it][0] = agent.data[cycle]['x']
            self.temp_opponent_pos[it][1] = agent.data[cycle]['y']
            it += 1
        
        self.opponent_pos.append(self.temp_opponent_pos)
        
    def teammate_data(self, cycle):
        it = 0
        for agent in self.game.left_team.agents:
            self.temp_teammate_pos[it][0] = agent.data[cycle]['x']
            self.temp_teammate_pos[it][1] = agent.data[cycle]['y']
            it += 1
        
        self.teammate_pos.append(self.temp_teammate_pos)

    def check_moise_param(self, cycle):
        if self.undefined_condition(cycle):
            self.clear_temp_parm()
            self.ball_data(cycle)
            self.opponent_data(cycle)
            self.teammate_data(cycle)   

    def analyze(self):
        """Analyze game"""

        for cycle in range(1, self.play_on_cycles[-1]+1):
            self.check_moise_param(cycle)