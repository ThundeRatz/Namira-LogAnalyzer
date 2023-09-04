class RegularPassesAnalyzer:
    def __init__(self, game):
        self.game = game
        self.play_on_cycles = game.get_play_on_cycles()
        self.pass_status = 0  # 0 --> no kick,  1 --> one kicker detected
        self.pass_last_kicker = -1
        self.pass_last_kick_cycle = -1
        self.i = 0
        self.ball_positions = []
        self.kick_states = []

        self.agent_right_states = []
        self.agent_left_states = []

    @staticmethod
    def csv_headers():
        return [
            'cycle',
            'kicker',
            'receiver'
        ]
    
    def to_csv_line(self):
        line = []
        for j in range(len(self.kick_states)):
            aux = self.kick_states[j]
            line.append([item for item in aux])
        return line

    def to_dictionary(self):
        dictionaries = []

        for j in range(len(self.kick_states)):
            dictionaries.append({
                "cycle" : self.kick_states[j][0],
                "kicker" : self.kick_states[j][1],
                "receiver": self.kick_states[j][2]
            })

        return dictionaries
    
    # Note this function is different from the check_pass function present on RiskyPassesPanalyzer, since
    # here we are not interested on the risky cases
    def check_pass(self, cycle):
        """Get pass info of a given cycle"""
        
        if len(self.game.get_last_kickers(cycle)) > 0:
            if cycle not in self.play_on_cycles:
                self.pass_status = 0

            elif self.pass_status == 0:
                self.pass_last_kicker = self.game.get_last_kickers(cycle)[0]
                self.pass_last_kick_cycle = cycle
                self.pass_status = 1

            elif self.pass_status == 1:

                if self.pass_last_kicker == self.game.get_last_kickers(cycle)[0] and self.game.get_last_kickers(cycle)[0].data[cycle]['is_kicked']:
                    self.pass_status = 1
                    self.pass_last_kick_cycle = cycle

                elif self.pass_last_kicker != self.game.get_last_kickers(cycle)[0] and self.pass_last_kicker.team == self.game.get_last_kickers(cycle)[0].team:
                    self.i = self.i + 1
                    self.pass_status = 1
                    self.pass_last_kicker = self.game.get_last_kickers(cycle)[0]
                    self.pass_last_kick_cycle = cycle

                elif self.pass_last_kicker.team != self.game.get_last_kickers(cycle)[0].team:
                    self.pass_status = 1
                    self.pass_last_kicker = self.game.get_last_kickers(cycle)[0]
                    self.pass_last_kick_cycle = cycle    

                # TO DO: Pegar o number do receiver. O 'focus_num' abaixo eh apenas para teste 

                self.kick_states.append([cycle, self.pass_last_kicker.number, self.pass_last_kicker.data[self.pass_last_kick_cycle].get('focus_num')])

    def draw_heatmap(self):
        raise NotImplementedError(
            "Risky passes analyzer has no heatmap implementation.")
    
    def analyze(self):
        '''pass, shoot, pass intercept, shot intercept, possesion'''

        for cycle in range(1, self.play_on_cycles[-1] + 1):
            self.check_pass(cycle)