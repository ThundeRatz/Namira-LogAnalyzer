class RegularPassesAnalyzer:
    def __init__(self, game):
        self.game = game
        self.play_on_cycles = game.get_play_on_cycles()
        self.pass_status = 0  # 0 --> no kick,  1 --> one kicker detected
        self.pass_last_kicker = -1
        self.pass_last_kick_cycle = -1
        self.kick_states = []
        self.missed_pass = False
        self.missed_pass_count = 0
        self.pass_count = 0

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
                    self.pass_status = 1
                    self.pass_last_kicker = self.game.get_last_kickers(cycle)[0]
                    self.pass_last_kick_cycle = cycle

                elif self.pass_last_kicker.team != self.game.get_last_kickers(cycle)[0].team:
                    self.pass_status = 1
                    self.pass_last_kicker = self.game.get_last_kickers(cycle)[0]
                    self.pass_last_kick_cycle = cycle
                    self.missed_pass = True
                    self.missed_pass_count += 1
                # Cycle is not exact. Most of the times it is the receiving cycle 
                if len(self.kick_states) == 0: # prevent off-by-one error
                    self.kick_states.append([cycle, self.pass_last_kicker.number, 0])
                    self.pass_count += 1
                # Actual pass
                elif self.pass_last_kicker.number != self.kick_states[len(self.kick_states) - 1][1] and self.pass_last_kicker.team.name == self.game.left_team.name:
                    if not self.missed_pass:
                        self.kick_states[len(self.kick_states) - 1][2] = self.pass_last_kicker.number
                    self.kick_states.append([cycle, self.pass_last_kicker.number, 0])
                    self.missed_pass = False
                    self.pass_count += 1
                elif self.missed_pass: # Ball lost to enemy
                    self.kick_states[len(self.kick_states) - 1][2] = -1


    def draw_heatmap(self):
        raise NotImplementedError(
            "Regular passes analyzer has no heatmap implementation.")
    
    def analyze(self):
        '''pass, shoot, pass intercept, shot intercept, possesion'''

        for cycle in range(1, self.play_on_cycles[-1] + 1):
            self.check_pass(cycle)
        
        print(f"Total passes: {self.missed_pass_count + self.pass_count}")
        print(f"Missed passes: {self.missed_pass_count}")
        print(f"Actual passes: {self.pass_count}")
        print(f"Total pass accuracy: {((100*self.pass_count)/(self.missed_pass_count + self.pass_count)):.2f}%")