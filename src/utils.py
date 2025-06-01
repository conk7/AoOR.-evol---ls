import os
from pathlib import Path
import time
from typing import Callable, List
from tqdm import tqdm
from algos.genetic_algorithm import fitness

BENCHMARKS_PATH = Path().resolve() / "benchmarks"
ANSWERS_PATH = Path().resolve() / "report" / "answers"
N = 1


def measure_algo(algorithm: Callable, benchmarks_path: Path, N: int = 100):
    ms = []
    ps = []
    parts = []

    for path in benchmarks_path.glob("*"):
        with open(path, "r") as f:
            m, p = map(int, f.readline().strip().split())
            machine_parts = []
            for _ in range(m):
                tokens = list(map(int, f.readline().strip().split()))
                if not tokens:
                    machine_parts.append(set())
                    continue
                machine_parts.append(set(tokens[1:]))

        ms.append(m)
        ps.append(p)
        parts.append(machine_parts)

        

    avg_times = []
    total_ms = []
    total_ps = []
    total_vals = []
    for part in tqdm(parts, leave=False):
        total_time = 0

        for _ in tqdm(range(N), leave=False):
            start = time.time()
            best_m, best_p, best_val = algorithm(part)
            end = time.time()
            total_time += end - start

        total_ms.append(best_m)
        total_ps.append(best_p)
        total_vals.append(best_val)

        avg_time = total_time / N
        avg_time *= 1000

        avg_times.append(avg_time)

    return (
        [path.stem for path in benchmarks_path.glob("*")],
        avg_times,
        total_ms,
        total_ps,
        total_vals,
    )


def get_val_from_file(benchmark: Path, answer: Path):
    with open(benchmark, "r") as f:
        m, p = map(int, f.readline().strip().split())
        machine_parts = []
        for _ in range(m):
            tokens = list(map(int, f.readline().strip().split()))
            if not tokens:
                machine_parts.append(set())
                continue
            machine_parts.append(set(tokens[1:]))

    with open(answer, "r") as f:
        machine_clusters = list(map(lambda x: int(x.split('_')[1]), f.readline().strip().split()))
        part_clusters = list(map(lambda x: int(x.split('_')[1]), f.readline().strip().split()))

    return fitness(machine_clusters, part_clusters, machine_parts)


def print_results(
    algorithm: str,
    benchmarks: List[Path],
    avg_times: List[float],
    total_ms: List[int],
    total_ps: List[int],
    total_vals: List[int],
    answers_path: Path,
):
    print(f"\n\n{algorithm}")
    print(f"{'Benchmark':<15}{'Average time(ms)':<20}{'Value':<20}")
    print("-" * 60)
    for benchmark, time_ms, m, p, val in zip(
        benchmarks, avg_times, total_ms, total_ps, total_vals
    ):
        print(f"{benchmark:<15}{time_ms:<20.4f}{val:<20.4f}")
        file_path = answers_path / (benchmark.__str__() + ".sol")
        file_path.touch()

        written_val = 0
        if os.path.getsize(file_path) != 0:
            written_val = get_val_from_file(
                str(BENCHMARKS_PATH / benchmark) + ".txt", file_path
            )
        if written_val < val:
            with open(file_path, "w") as f:
                f.write(" ".join(['m' + str(i) + '_' + str(m) for i, m in zip(range(1, len(m) + 1), map(str, m))]) + "\n")
                f.write(" ".join(['p' + str(i) + '_' + str(p) for i, p in zip(range(1, len(p) + 1), map(str, p))]) + "\n")
