from pathlib import Path
from algos import genetic_algorithm
from utils import measure_algo, print_results


BENCHMARKS_PATH = Path().resolve() / "benchmarks"
ANSWERS_PATH = Path().resolve() / "report" / "answers"
N = 1


def main():
    for algo in [genetic_algorithm]:
        (
            benchmarks,
            avg_times,
            total_ms,
            total_ps,
            total_vals,
        ) = measure_algo(algo, BENCHMARKS_PATH, N)
        print_results(
            algo.__name__,
            benchmarks,
            avg_times,
            total_ms,
            total_ps,
            total_vals,
            ANSWERS_PATH,
        )


if __name__ == "__main__":
    main()
