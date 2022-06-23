import os
import pandas as pd

from .Game import *
from .Parser import *
from .custom_analyzers import DangerAnalyzer, MoiseAnalyzer, OverallAnalyzer, RiskyPassesAnalyzer
from loganalyzer.utils import write_csv, write_json

def analyze(args):
    path = args.path
    save_path = args.save_path

    output_extension = ""

    if save_path.endswith(".csv"):
        output_extension = "csv"
    elif save_path.endswith(".json"):
        output_extension = "json"
    else:
        raise ValueError("Save path must be a json or csv file.")

    if args.recursive:
        files = os.listdir(path)
        logs = [file[:-4] for file in files if file.endswith(".rcg")]
        logs = list(set(logs))
    else:
        logs = [path]

    # Run analyzer and save
    data = []
    for i, log in enumerate(logs):
        parser = Parser(path + "/" + log) if args.recursive else Parser(path)
        game = Game(parser)

        # define analyzer
        if args.mode == "risky_passes":
            analyzer = RiskyPassesAnalyzer(game)
        elif args.mode == "danger":
            analyzer = DangerAnalyzer(game)
        elif args.mode == "moise":
            analyzer = MoiseAnalyzer(game)
        else:
            analyzer = OverallAnalyzer(game)
        analyzer.analyze()
        if output_extension == "csv":
            data += analyzer.to_csv_line()
        else:
            data += analyzer.to_dictionary()
        print(f"Finishing: {i + 1} / {len(logs)} - {log}")

    if save_path.endswith(".json"):
        write_json(save_path, data)
    elif save_path.endswith(".csv"):
        header = analyzer.csv_headers()
        write_csv(save_path, data, header)

    # Drawing Heatmap of the game

    if args.heat_map is not None:
        analyzer.draw_heatmap(right_team=True, left_team=True)
