
class Parser:
    def __init__(self, path):
        self.path = path
        self.set_data_rcg()
        self.set_data_rcl()
        self.right_team
        self.left_team

    def set_data_rcg(self):
        """
        Get all the data in the .rcg file and stores it in a list of lists.
        """
        try:
            f = open(self.path+'.rcg', 'r')
        except:
            print("RCG file does not exist")
            exit(1)
        data_rcg = []

        def parse(expr):
            def _helper(iter):
                items = []
                for item in iter:
                    if item == '(':
                        result, closeparen = _helper(iter)
                        if not closeparen:
                            return [], False
                        items.append(result)
                    elif item == ')':
                        return items, True
                    else:
                        items.append(item)
                return items, False
            return _helper(iter(expr))[0]

        def cleaner(lis):

            def isfloat(value):
                try:
                    float(value)
                    return True
                except ValueError:
                    return False
            arr = []
            string = ''
            for i in range(len(lis)):
                if type(lis[i]) is list:
                    if string != '':
                        if string.isdigit():
                            arr += [int(string)]
                        elif isfloat(string):
                            arr += [float(string)]
                        else:
                            arr += [string]
                    string = ''
                    arr += [cleaner(lis[i])]
                elif type(lis[i]) is str:
                    if lis[i] == ' ':
                        if string != '':
                            if string.isdigit():
                                arr += [int(string)]
                            elif isfloat(string):
                                arr += [float(string)]
                            else:
                                arr += [string]
                        string = ''
                    else:
                        string += lis[i]
            if string != '':
                if string.isdigit():
                    arr += [int(string)]
                elif isfloat(string):
                    arr += [float(string)]
                else:
                    arr += [string]
            return arr
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].replace("\n", '')
        for line in lines:
            p = parse(line)
            if p != []:
                data_rcg += [cleaner(p)]
        f.close()
        self.data_rcg = data_rcg

    def get_data_rcg(self):
        return self.data_rcg

    def set_data_rcl(self):
        """
        Extract data from rcl files and store in dict.
        Current available dicts are:
            - self.rcl_kick_tackle: get all cycles that simultaneously have a "kick" and a "tackle" action;
            - self.rcl_referee: get all referee messages (e.g.: play_modes);
            - self.rcl_kicks: get all cycles where a "kick" action occurs.
        """
        try:
            f = open(self.path+'.rcl', 'r')
        except:
            print("RCL file does not exist")
            exit(1)

        self.set_teams_name()

        self.rcl_kick_tackle = {}
        self.rcl_referee = {}
        self.rcl_kicks = {}

        lines = f.readlines()
        kick_tackle = {}
        for line in lines:
            # Get all cycles that simultaneously have a "kick" and a "tackle" action
            if ("kick" in line or "tackle" in line) and ("kick_" not in line) and ("_kick" not in line):
                cycle = int(line.split(',')[0])
                number = line.split(':')[0].split('_')[-1]
                team = line.split(':')[0].split(' ')[1].replace("_"+number, '')    
                words = line.split(':')[1].split(')')
                for word in words:
                    if '(kick' in word:
                        action = 'kick'
                        try:
                            degree = word.split(' ')[3]
                            degree = float(degree)
                            cycle_data = {'team': team, 'number': int(
                                number), 'action': action, 'degree': degree}
                            break
                        except:
                            print("error")
                    elif 'tackle' in word:
                        action = 'tackle'
                        cycle_data = {'team': team, 'number': int(
                            number), 'action': action}
                        break

                if cycle in kick_tackle:
                    if self.left_team in line:
                        kick_tackle[cycle] = [cycle_data] + kick_tackle[cycle]
                    elif self.right_team in line:
                        kick_tackle[cycle] += [cycle_data]

                else:
                    kick_tackle[cycle] = [cycle_data]

            # Get all referee messages (e.g.: play_modes)
            if "referee" in line:
                cycle = int(line.split(",")[0])
                referee_msg = line.split(" ")[-1].split(")")[0]
                if cycle in self.rcl_referee:
                    self.rcl_referee[cycle].append(referee_msg)
                else:
                    self.rcl_referee.update({
                        cycle: [referee_msg]
                    })

            # Get all cycles where a "kick" action occurs
            if "kick " in line:
                cycle = int(line.split(",")[0])
                number = line.split(':')[0].split('_')[-1]
                team = line.split(':')[0].split(' ')[1].replace("_"+number, '') 
                kick_msg = line.split("(")[1].split(")")[0]
                _, power, angle = kick_msg.split(" ")
                self.rcl_kicks.update({
                    cycle: {
                        "team": team,
                        "player_num": number,
                        "power": float(power),
                        "angle": float(angle)
                    }
                })
        for cycle in kick_tackle:
            if len(kick_tackle[cycle]) > 1:
                self.rcl_kick_tackle[cycle] = kick_tackle[cycle]

        f.close()

    def get_data_rcl(self):
        return self.data_rcl

    def set_teams_name(self):
        for cycle in self.data_rcg:
            if cycle[0][0] == 'team':
                self.left_team = cycle[0][2]
                self.right_team = cycle[0][3]

                return
