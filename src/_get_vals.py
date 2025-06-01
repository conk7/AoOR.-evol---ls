from utils import BENCHMARKS_PATH, ANSWERS_PATH, get_val_from_file


for bench_path in BENCHMARKS_PATH.glob("*"):
    ans_path = ANSWERS_PATH / (bench_path.stem + ".sol")
    with open(bench_path, "r") as f:
        m, p = map(int, f.readline().strip().split())
        machine_parts = []
        for _ in range(m):
            tokens = list(map(int, f.readline().strip().split()))
            if not tokens:
                machine_parts.append(set())
                continue
            machine_parts.append(set(tokens[1:]))

    with open(ans_path, "r") as f:
        machine_clusters = list(map(lambda x: int(x.split('_')[1]), f.readline().strip().split()))
        part_clusters = list(map(lambda x: int(x.split('_')[1]), f.readline().strip().split()))

    print(f"{get_val_from_file(bench_path, ans_path):.4f}")
