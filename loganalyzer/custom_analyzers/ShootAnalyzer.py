from datetime import datetime


class ShootAnalyzer:
    def __init__(self, game, log_name):
        self.game = game
        self.log_name = log_name
        self.left_goal_count = 0
        self.right_goal_count = 0
        self.cycles_before_goal = 50
        self.shoots_list = []
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ball_positions = self.game.ball_pos
        self.play_on_cycles = game.get_play_on_cycles()
        self.shoot_count = 0

    @staticmethod
    def csv_headers():

        return [
            "timestamp",
            "log_name",
            "team_name",
            "cycle",
            "ball_x",
            "ball_y",
            "is_shoot",
            "is_goal",
            "shoot_id",
        ]

    def to_csv_line(self):
        return self.shoots_list

    def to_dictionary(self):
        dictionaries = []

        for item in self.shoots_list:
            dictionaries.append(
                {
                    "timestamp": item[0],
                    "log_name": item[1],
                    "team_name": item[2],
                    "cycle": item[3],
                    "ball_x": item[4],
                    "ball_y": item[5],
                    "is_shoot": item[6],
                    "is_goal": item[7],
                    "shoot_id": item[8],
                }
            )

        return dictionaries

    def get_shoots(self):
        """
        Filters all shoots that happens in a match.
        """
        # Case 1: Goal situation
        self._get_goal_cycles()

        # Case 2: Goalie catches a shoot
        self._get_goalie_catch_cycles()

        # Case 3: Off target shoots (striker misses the goal area in its shoot)
        self._get_off_target_cycles()

    def _get_kick_cycle(self, initial_cycle, final_cycle):
        """
        Get the cycle of the shoot. It considers that is the last cycle where a
        'kick' action happened, within the [initial_cycle, final_cycle] interval.
        """
        for cycle in range(final_cycle, initial_cycle - 1, -1):
            if cycle in self.game.parser.rcl_kicks.keys():
                return cycle

        return -1

    def _get_goalie_catch_cycles(self):
        """
        Get info about the 50 last cycles before a goalie catch action,
        updating the self.shoots_list.
        """
        ball_near_goal_x = 47

        goalie_catch_cycles = []
        for cycle, playmode_list in self.game.parser.rcl_referee.items():
            for playmode in playmode_list:
                if (
                    "goalie_catch_ball" in playmode
                    and "back_pass" not in playmode
                    and abs(self.ball_positions[cycle]["x"]) > ball_near_goal_x
                ):
                    goalie_catch_cycles.append(cycle)

        # Get last 50 cycles info
        for cycle in goalie_catch_cycles:
            min_cycle = max(0, cycle - 50)  # Avoid cycle < 0
            team_name = (
                self.game.left_team.name
                if self.ball_positions[cycle]["x"] < 0
                else self.game.right_team.name
            )
            kick_cycle = self._get_kick_cycle(min_cycle, cycle)

            for i in range(min_cycle, cycle + 1):
                self.shoots_list.append(
                    [
                        self.timestamp,
                        self.log_name,
                        team_name,
                        i,
                        self.ball_positions[i]["x"],
                        self.ball_positions[i]["y"],
                        i == kick_cycle,
                        False,
                        self.shoot_count,
                    ]
                )

            self.shoot_count += 1

    def _get_off_target_cycles(self):
        """
        Get ball position of the last 50 cycles before a shoot that wasn't in the goal range,
        updatung the self.shoots_list with the filtered data.
        """
        goal_max_y = 7
        for cycle in self.play_on_cycles:
            if (
                abs(self.ball_positions[cycle]["x"]) > 52
                and abs(self.ball_positions[cycle]["y"]) > goal_max_y
            ):
                min_cycle = max(0, cycle - 50)  # Avoid cycle < 0
                team_name = (
                    self.game.left_team.name
                    if self.ball_positions[cycle]["x"] < 0
                    else self.game.right_team.name
                )
                kick_cycle = self._get_kick_cycle(min_cycle, cycle)

                for i in range(min_cycle, cycle + 1):
                    self.shoots_list.append(
                        [
                            self.timestamp,
                            self.log_name,
                            team_name,
                            i,
                            self.ball_positions[i]["x"],
                            self.ball_positions[i]["y"],
                            i == kick_cycle,
                            False,
                            self.shoot_count,
                        ]
                    )

                self.shoot_count += 1

    def _get_goal_cycles(self):
        """
        Get ball position of the last 50 cycles before a goal has happened,
        updating the self.shoots_list.
        """

        for cycle, play_mode in self.game.play_modes.items():
            if play_mode in ["goal_l", "goal_r"]:
                team_name = (
                    self.game.left_team.name
                    if play_mode == "goal_l"
                    else self.game.right_team.name
                )
                min_cycle = max(0, cycle - 50)  # Avoid cycle < 0
                kick_cycle = self._get_kick_cycle(min_cycle, cycle)

                for i in range(min_cycle, cycle + 1):
                    self.shoots_list.append(
                        [
                            self.timestamp,
                            self.log_name,
                            team_name,
                            i,
                            self.ball_positions[i]["x"],
                            self.ball_positions[i]["y"],
                            i == kick_cycle,
                            True,
                            self.shoot_count,
                        ]
                    )

                self.shoot_count += 1

    def analyze(self):
        self.get_shoots()
