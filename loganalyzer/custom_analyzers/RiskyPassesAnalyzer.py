# pylint: disable = C0103, C0114, C0115, C0116, C0301, R0903, R0902, R0912, R0914, R0915, R1702

import math


class RiskyPassesAnalyzer:
    def __init__(self, game):
        self.game = game
        self.play_on_cycles = game.get_play_on_cycles()
        self.pass_status = 0  # 0 --> no kick,  1 --> one kicker detected
        self.pass_last_kicker = -1
        self.pass_last_kick_cycle = -1
        self.i = 0
        self.ball_positions = []

        # Right TEAM
        self.risky_right = []
        self.agent_right_states = []

        # Left TEAM
        self.risky_left = []
        self.agent_left_states = []

    def csv_headers(self):
        return [
            'receiver_x',
            'receiver_y',
            'opponent_1_x',
            'opponent_1_y',
            'opponent_2_x',
            'opponent_2_y',
            'opponent_3_x',
            'opponent_3_y',
            'opponent_4_x',
            'opponent_4_y',
            'ball_x',
            'ball_y',
            'pass_angle',
            'good_pass'
        ]

    def to_csv_line(self):
        line = []

        for j in range(len(self.agent_left_states)):
            aux = [self.agent_left_states[j]] + \
                self.agent_right_states[j] + [self.ball_positions[j]] + [[self.risky_left[j]]]
            line.append([item for sublist in aux for item in sublist])

        return line

    def to_dictionary(self):
        dictionaries = []

        for j in range(len(self.agent_left_states)):
            dictionaries.append({
                "receiver_x": self.agent_left_states[j][0],
                "receiver_y": self.agent_left_states[j][1],
                "opponent_1_x": self.agent_right_states[j][0][0],
                "opponent_1_y": self.agent_right_states[j][0][1],
                "opponent_2_x": self.agent_right_states[j][1][0],
                "opponent_2_y": self.agent_right_states[j][1][1],
                "opponent_3_x": self.agent_right_states[j][2][0],
                "opponent_3_y": self.agent_right_states[j][2][1],
                "opponent_4_x": self.agent_right_states[j][3][0],
                "opponent_4_x": self.agent_right_states[j][3][1],
                "ball_x": self.ball_positions[j][0],
                "ball_y": self.ball_positions[j][1],
                "pass_angle": self.ball_positions[j][2],
                "good_pass" : self.risky_left[j] 
            })

        return dictionaries

    def draw_heatmap(self):
        raise NotImplementedError(
            "Risky passes analyzer has no heatmap implementation.")

    def check_pass(self, key):
        if len(self.game.get_last_kickers(key)) > 0:
            if key not in self.play_on_cycles:
                self.pass_status = 0

            elif self.pass_status == 0:
                self.pass_last_kicker = self.game.get_last_kickers(key)[0]
                self.pass_last_kick_cycle = key
                self.pass_status = 1

            elif self.pass_status == 1:

                if self.pass_last_kicker == self.game.get_last_kickers(key)[0] and self.game.get_last_kickers(key)[0].data[key]['is_kicked']:
                    self.pass_status = 1
                    self.pass_last_kick_cycle = key

                elif self.pass_last_kicker != self.game.get_last_kickers(key)[0] and self.pass_last_kicker.team == self.game.get_last_kickers(key)[0].team:
                    self.i = self.i + 1
                    ball1 = (self.game.ball_pos[self.pass_last_kick_cycle]['x'],
                             self.game.ball_pos[self.pass_last_kick_cycle]['y'])
                    ball2 = (self.game.ball_pos[key]['x'],
                             self.game.ball_pos[key]['y'])

                    if self.pass_last_kicker.team.name == self.game.right_team.name:
                        self.check_risky_pass(key, ball1, ball2, True, False)
                    else:
                        self.check_risky_pass(key, ball1, ball2, False, False)

                    self.pass_status = 1
                    self.pass_last_kicker = self.game.get_last_kickers(key)[0]
                    self.pass_last_kick_cycle = key

                elif self.pass_last_kicker.team != self.game.get_last_kickers(key)[0].team:
                    ball1 = (self.game.ball_pos[self.pass_last_kick_cycle]['x'],
                             self.game.ball_pos[self.pass_last_kick_cycle]['y'])

                    ball2 = (self.game.ball_pos[key]['x'],
                             self.game.ball_pos[key]['y'])

                    if self.game.get_last_kickers(key)[0].team.name == self.game.right_team.name:
                        self.check_risky_pass(key, ball1, ball2, False, True)
                    else:
                        self.check_risky_pass(key, ball1, ball2, True, True)

                    self.pass_status = 1
                    self.pass_last_kicker = self.game.get_last_kickers(key)[0]
                    self.pass_last_kick_cycle = key

    def check_risky_pass(self, key, ball1, ball2, team, intercept):
        if math.sqrt((ball2[0] - ball1[0])**2 + (ball2[1] - ball1[1])**2) < 5.0:
            return

        if team:
            offside_left = 0

            for agent in self.game.left_team.agents:
                if agent.number != 1 and offside_left > agent.data[self.pass_last_kick_cycle]['x']:
                    offside_left = agent.data[self.pass_last_kick_cycle]['x']

            if offside_left > ball2[0]:
                if intercept or key != 2999 and key != 5999 and self.game.get_last_kickers(key+1)[0].data[self.pass_last_kick_cycle]['x'] < offside_left:
                    self.risky_right.append(0)
                else:
                    self.risky_right.append(1)
        else:
            offside_right = 0

            for agent in self.game.right_team.agents:
                if agent.number != 1 and offside_right < agent.data[self.pass_last_kick_cycle]['x']:
                    offside_right = agent.data[self.pass_last_kick_cycle]['x']

            if offside_right < ball2[0]:
                if self.check_risky_players(key):
                    if intercept or key != 2999 and key != 5999 and self.game.get_last_kickers(key+1)[0].data[self.pass_last_kick_cycle]['x'] > offside_right:
                        self.risky_left.append(0)
                    else:
                        self.risky_left.append(1)

    def check_risky_players(self, key):
        # Aliados -> Esquerda

        # print(self.pass_last_kick_cycle)

        ball_x = self.game.ball_pos[self.pass_last_kick_cycle]['x']
        ball_y = self.game.ball_pos[self.pass_last_kick_cycle]['y']

        receive_x = self.game.ball_pos[key]['x']
        receive_y = self.game.ball_pos[key]['y']

        pass_angle = math.atan2(receive_y - ball_y, receive_x - ball_x)

        left_pass_states = []
        right_pass_states = []

        pass_player = self.pass_last_kicker.data[self.pass_last_kick_cycle]
        angle_candidates = []

        for agent in self.game.left_team.agents:
            player_data = agent.data[self.pass_last_kick_cycle]

            if math.sqrt((pass_player['x'] - player_data['x'])**2 + (pass_player['y'] - player_data['y'])**2) > 40.0:
                continue

            player_angle = math.atan2(
                player_data['y'] - ball_y, player_data['x'] - ball_x)

            left_pass_states.append((player_data['x'], player_data['y']))
            angle_candidates.append(abs(player_angle - pass_angle))

        if len(angle_candidates) == 0:
            return False

        self.agent_left_states.append(sorted(
            left_pass_states, key=lambda x: angle_candidates[left_pass_states.index(x)])[0])

        angle_candidates = []
        for agent in self.game.right_team.agents:
            player_data = agent.data[self.pass_last_kick_cycle]

            if math.sqrt((pass_player['x'] - player_data['x'])**2 + (pass_player['y'] - player_data['y'])**2) > 40.0:
                continue

            player_angle = math.atan2(
                player_data['y'] - ball_y, player_data['x'] - ball_x)

            right_pass_states.append((player_data['x'], player_data['y']))
            angle_candidates.append(abs(player_angle - pass_angle))

        if len(angle_candidates) < 4:
            return False

        self.agent_right_states.append((sorted(
            right_pass_states, key=lambda x: angle_candidates[right_pass_states.index(x)]))[:4])
        self.ball_positions.append((ball_x, ball_y, pass_angle))

        return True

    def analyze(self):
        '''pass, shoot, pass intercept, shot intercept, possesion'''

        for key in range(1, self.play_on_cycles[-1] + 1):
            self.check_pass(key)
