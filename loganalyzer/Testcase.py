import numpy as np
import os

from loganalyzer.custom_analyzers import RiskyPassesAnalyzer, OverallAnalyzer
from loganalyzer.Parser import Parser
from loganalyzer.Game import Game


def __get_logs():
    """Auxiliar function to get the logs to be analyzed by the example runs.

    Returns:
        The path to the logs' folder.
        A list containing the logs path, excluding its extension (.rcl, .rcg).
    """

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    logs_path = __location__ + "/logs"

    files = os.listdir(logs_path)
    logs = [file[:-4] for file in files if file.endswith(".rcg")]
    logs = list(set(logs))

    return logs_path, logs


def run_overall_testcase():
    """Note: to run, the .rcg and .rcl logs must be inside `loganalyzer/logs` folder.
    Testcase that uses OverallAnalyzer to analyze the logs, and get the mean values of
    some of the available statistics provided by this analyzer.
    """
    r_pass = r_wrong_pass = r_pass_accuracy = r_on_target_shoot = r_off_target_shoot = r_shoot_accuracy = r_possession = 0
    l_pass = l_wrong_pass = l_pass_accuracy = l_on_target_shoot = l_off_target_shoot = l_shoot_accuracy = l_possession = 0

    r_used_stamina = [0 for _ in range(11)]
    l_used_stamina = [0 for _ in range(11)]

    logs_path, logs = __get_logs()

    for i, log in enumerate(logs):
        print(f"Starting: {i} - {log}")

        parser = Parser(f"{logs_path}/{log}")
        game = Game(parser)
        analyzer = OverallAnalyzer(game)
        analyzer.analyze()

        r_pass += analyzer.pass_r
        r_wrong_pass += analyzer.intercept_l
        r_pass_accuracy += analyzer.pass_accuracy_r
        r_on_target_shoot += analyzer.on_target_shoot_r
        r_off_target_shoot += analyzer.off_target_shoot_r
        r_shoot_accuracy += analyzer.shoot_accuracy_r
        r_possession += analyzer.possession_r
        r_used_stamina = [x + y for x, y in zip(r_used_stamina, [j[0] for j in analyzer.used_stamina_agents_r])]

        l_pass += analyzer.pass_l
        l_wrong_pass += analyzer.intercept_r
        l_pass_accuracy += analyzer.pass_accuracy_l
        l_on_target_shoot += analyzer.on_target_shoot_l
        l_off_target_shoot += analyzer.off_target_shoot_l
        l_shoot_accuracy += analyzer.shoot_accuracy_l
        l_possession += analyzer.possession_l
        l_used_stamina = [x + y for x, y in zip(l_used_stamina, [j[0] for j in analyzer.used_stamina_agents_l])]

        print(f"Finishing: {i} - {log}")

    total = len(logs)

    analyzer.draw_heatmap()

    print("\nRight team")
    print(f"True pass: {round(r_pass/total, 3)}")
    print(f"Wrong pass: {round(r_wrong_pass/total, 3)}")
    print(f"Pass accuracy: {round(r_pass_accuracy/total, 3)}%")
    print(f"On target shoot: {round(r_on_target_shoot/total, 3)}")
    print(f"Off target shoot: {round(r_off_target_shoot/total, 3)}")
    print(f"Shoot accuracy: {round(r_shoot_accuracy/total, 3)}%")
    print(f"Possession: {round(r_possession/total, 3)}%")
    print("Used stamina: ", [(round(r_used_stamina[k] / total, 3), k + 1) for k in range(11)])

    print("\nLeft team")
    print(f"True pass: {round(l_pass/total, 3)}")
    print(f"Wrong pass: {round(l_wrong_pass/total, 3)}")
    print(f"Pass accuracy: {round(l_pass_accuracy/total, 3)}%")
    print(f"On target shoot: {round(l_on_target_shoot/total, 3)}")
    print(f"Off target shoot: {round(l_off_target_shoot/total, 3)}")
    print(f"Shoot accuracy: {round(l_shoot_accuracy/total, 3)}%")
    print(f"Possession: {round(l_possession/total, 3)}%")
    print("Used stamina: ", [(round(l_used_stamina[k] / total, 3), k + 1) for k in range(11)])


def run_risk_passes_testcase():
    """Example of risky passes analyzer run. Uses RiskyPassesAnalyzer on the logs
    inside the `loganalyzer/logs` folder. The results are in `data.txt` and
    `results.txt`.
    """
    logs_path, logs = __get_logs()

    data = []
    results = []

    for i, log in enumerate(logs):
        print(f"Starting: {i} - {log}")

        parser = Parser(f"{logs_path}/{log}")
        game = Game(parser)
        analyzer = RiskyPassesAnalyzer(game)
        analyzer.analyze()

        for j in range(len(analyzer.agent_left_states)):
            aux = [analyzer.agent_left_states[j]] + analyzer.agent_right_states[j] + [analyzer.ball_positions[j]]
            data.append([item for sublist in aux for item in sublist])
            results.append(analyzer.risky_left[j])
        print(f"Finishing: {i} - {log}")

    data = np.transpose(data)

    np.savetxt("data.txt", data, fmt="%.4f")
    np.savetxt("results.txt", [results], fmt="%d")

    # L.x,L.y,R.1.x,R.1.y,R.2.x,R.2.y,R.3.x,R.3.y,R.4.x,R.4.y,Ball.x,Ball.y,Pass.Angle


if __name__ == "__main__":
    run_overall_testcase()
    # run_risk_passes_testcase()
