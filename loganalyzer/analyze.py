import os
from multiprocessing import Process, Queue

import pandas as pd

from loganalyzer.Game import Game
from loganalyzer.Parser import Parser
from loganalyzer.custom_analyzers import (
    DangerAnalyzer,
    MoiseAnalyzer,
    OverallAnalyzer,
    RiskyPassesAnalyzer,
    RegularPassesAnalyzer
)
from loganalyzer.utils import write_csv, write_json, split_list


def analyze_game(log, i, logs, data, args, path, output_extension):
    parser = Parser(path + "/" + log) if args.recursive else Parser(path)
    game = Game(parser)

    # define analyzer
    if args.mode == "risky_passes":
        analyzer = RiskyPassesAnalyzer(game)
    elif args.mode == "danger":
        analyzer = DangerAnalyzer(game)
    elif args.mode == "moise":
        analyzer = MoiseAnalyzer(game)
    elif args.mode == "regular_passes":
        analyzer = RegularPassesAnalyzer(game)
    else:
        analyzer = OverallAnalyzer(game)
    try:
        analyzer.analyze()
        if output_extension == "csv":
            data += analyzer.to_csv_line()
        else:
            data += analyzer.to_dictionary()
        print(f"Finishing: {i + 1} / {len(logs)} - {log}")

        # Drawing Heatmap of the game
        if args.heat_map is not None:
            analyzer.draw_heatmap(right_team=True, left_team=True)
    except Exception as e:
        print(e)
        print(f"[ERROR] Skipping: {i + 1} / {len(logs)} - {log}")

def analyze_thread(data_queue, logs, args, path, output_extension):
    thread_data = []
    for i, log in enumerate(logs):
        try:
            analyze_game(log, i, logs, thread_data, args, path, output_extension)
        except Exception as e:
            print(e)
            print(f"\n[ERROR] Skipping: {i + 1} / {len(logs)} - {log}")
    data_queue.put(thread_data)

def analyze(args):
    path = args.path
    save_path = args.save_path

    output_extension = ""
    number_of_jobs = 1

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
    
    if args.jobs:
        number_of_jobs = int(args.jobs)

    # Run analyzer and save
    data = []
    logs_split = split_list(logs, number_of_jobs)

    data_queue = Queue()
    processes = [Process(target=analyze_thread, args=(data_queue, log_list, args, path, output_extension)) for log_list in logs_split]

    for process in processes:
        process.start()

    while any(process.is_alive() for process in processes):
        while data_queue.qsize() != 0:
            data += data_queue.get()

    for process in processes:
        process.join()

    if save_path.endswith(".json"):
        write_json(save_path, data)
    elif save_path.endswith(".csv"):
        if args.mode == "risky_passes":
            header = RiskyPassesAnalyzer.csv_headers()
        elif args.mode == "regular_passes":
            header = RegularPassesAnalyzer.csv_headers()
        elif args.mode == "danger":
            header = DangerAnalyzer.csv_headers()
        elif args.mode == "moise":
            header = MoiseAnalyzer.csv_headers()
        else:
            header = OverallAnalyzer.csv_headers()
        write_csv(save_path, data, header)
