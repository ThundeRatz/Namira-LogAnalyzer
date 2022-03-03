
import math

class Region:

    def __init__(self, top_left, bottom_right, name="Unnamed"):

        self.top_left = top_left
        self.bottom_right = bottom_right
        self.name = name
        self.ball_in_region_cycles = 0

        # danger parameters

        self.danger_ball_pos = []
        self.danger_opponent_pos = []
        self.danger_teamMater_pos = []
        self.danger_stamina = []
        self.danger_player = []

    def in_region(self, x, y):
        '''check if a point (x,y) lies in a rectangle
        with upper left corner (x1,y1) and bottom right corner (x2,y2)'''
        if (x > self.top_left[0] and x < self.bottom_right[0] and y > self.top_left[1] and y < self.bottom_right[1]):
            return True
        else:
            return False

class DangerAnalyzer:

    def __init__(self, game):

        self.game = game
        self.play_on_cycles = game.get_play_on_cycles()
        self.pass_status = 0  # 0 --> no kick,  1 --> one kicker detected
        self.shoot_status = 0
        self.pass_last_kicker = -1
        self.pass_last_kick_cycle = -1
        self.i = 0
        self.ball_owner = 0

        # Special Regions
        self.regions = []
        self.regions.append(Region((-52.5, -34), (-17.5, -11), "A"))
        self.regions.append(Region((-52.5, -11), (-17.5, 11), "B"))
        self.regions.append(Region((-52.5, 11), (-17.5, 34), "C"))
        self.regions.append(Region((-17.5, -34), (17.5, -11), "D"))
        self.regions.append(Region((-17.5, -11), (17.5, 11), "E"))
        self.regions.append(Region((-17.5, 11), (17.5, 34), "F"))
        self.regions.append(Region((17.5, -34), (52.5, -11), "G"))
        self.regions.append(Region((17.5, -11), (52.5, 11), "H"))
        self.regions.append(Region((17.5, 11), (52.5, 34), "I"))

        # Right TEAM
        self.status_r = 0  # Winner' 'Loser' 'Draw'
        self.used_stamina_agents_r = []
        self.used_per_distance_r = []
        self.average_stamina_10p_r = 0
        self.average_distance_10p_r = 0
        self.av_st_per_dist_10p_r = 0

        # Left TEAM
        self.status_l = 0  # Winner' 'Loser' 'Draw'
        self.pass_l = 0
        self.intercept_l = 0
        self.pass_in_length_l = 0
        self.pass_in_width_l = 0
        self.pass_accuracy_l = 0
        self.shoot_in_length_l = 0
        self.shoot_in_width_l = 0
        self.on_target_shoot_l = 0
        self.off_target_shoot_l = 0
        self.shoot_accuracy_l = 0
        self.possession_l = 0
        self.used_stamina_agents_l = []
        self.team_moved_distance_l = []
        self.used_per_distance_l = []
        self.average_stamina_10p_l = 0
        self.average_distance_10p_l = 0
        self.av_st_per_dist_10p_l = 0


    def check_lost_ball(self, cycle):
        lost_ball = False
        if (self.game.get_last_kickers(cycle)[0].team.name == self.game.right_team.name and
            self.game.get_last_kickers(cycle-1)[0].team.name == self.game.left_team.name):
            lost_ball = True
        return lost_ball, cycle-1

    def check_danger_param(self, cycle):
        if self.check_lost_ball(cycle)[0]:
            for i in range(1,5):
                pass
            

    def analyze(self):
        """Analyze game."""
        
        for cycle in range(1,self.play_on_cycles[-1]+1):
            self.check_pass(cycle)
            self.check_shoot(cycle)
            self.update_possession(cycle)
            self.update_distance(cycle)
        self.update_parameters()