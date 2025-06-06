import random
import math
from typing import List, Set


POP_SIZE = 50
ELITE_SIZE = POP_SIZE // 10
NUM_NEW_RANDOM_SOLUTIONS = POP_SIZE // 10
NUM_GENERATIONS = 25
MUTATION_RATE = 0.1
MUTATION_STRENGTH = 0.1
TOURNAMENT_SIZE = 5


def fitness(
    machine_clusters: List[int], part_clusters: List[int], machine_parts: List[Set[int]]
):
    m = len(machine_clusters)
    p = len(part_clusters)
    n1 = n1_out = n0_in = 0
    for mi in range(m):
        m_cluster = machine_clusters[mi]
        parts = machine_parts[mi]
        n1 += len(parts)
        for pj in range(1, p + 1):
            same_cluster = m_cluster == part_clusters[pj - 1]
            processed = pj in parts
            if processed and not same_cluster:
                n1_out += 1
            if (not processed) and same_cluster:
                n0_in += 1

    return (n1 - n1_out) / (n1 + n0_in) if n1 + n0_in > 0 else 0


def decode(chromosome: List[float], m: int):
    k = max(1, int(math.floor(chromosome[-1] * m)))
    m_clusters = [max(1, math.ceil(g * k)) for g in chromosome[:-1]]
    return m_clusters, k


def assign_parts(machine_clusters: List[int], machine_parts: List[Set[int]], p: int):
    p_clusters = [1] * p
    for pj in range(1, p + 1):
        clusters = [
            machine_clusters[mi]
            for mi, parts in enumerate(machine_parts)
            if pj in parts
        ]
        if clusters:
            p_clusters[pj - 1] = max(set(clusters), key=clusters.count)
    return p_clusters


def local_search(
    m_clusters: List[int], p_clusters: List[int], machine_parts: List[Set[int]], k: int
):
    best_m, best_p = m_clusters[:], p_clusters[:]
    best_val = fitness(best_m, best_p, machine_parts)
    improved = True
    m, p = len(best_m), len(best_p)
    while improved:
        improved = False
        for mi in range(m):
            cur = best_m[mi]
            for c in range(1, k + 1):
                if c == cur:
                    continue
                trial_m = best_m[:]
                trial_m[mi] = c
                val = fitness(trial_m, best_p, machine_parts)
                if val > best_val:
                    best_val, best_m = val, trial_m
                    improved = True
        for pj in range(p):
            cur = best_p[pj]
            for c in range(1, k + 1):
                if c == cur:
                    continue
                trial_p = best_p[:]
                trial_p[pj] = c
                val = fitness(best_m, trial_p, machine_parts)
                if val > best_val:
                    best_val, best_p = val, trial_p
                    improved = True

    return best_m, best_p


def tournament(population: List[List[float]], fitness: List[float]):
    best_idx = max(
        random.sample(range(len(population)), TOURNAMENT_SIZE),
        key=lambda i: fitness[i],
    )
    return population[best_idx]


def crossover(parent1: List[float], parent2: List[float]):
    return [
        parent1[gene] if random.random() < 0.5 else parent2[gene]
        for gene in range(len(parent1))
    ]


def mutate(chromosome: List[float]):
    child = chromosome[:]
    for i in range(len(child)):
        if random.random() < MUTATION_RATE:
            child[i] += random.gauss(0, MUTATION_STRENGTH)
            child[i] = min(1.0, max(0.0, child[i]))
    return child


def genetic_algorithm(
    machine_parts: List[Set[int]],
):
    m = len(machine_parts)
    p = max(part for parts in machine_parts for part in parts)
    k = int(math.sqrt(m + p)) + 1
    population = [[random.random() for _ in range(m + 1)] for _ in range(POP_SIZE)]

    best_m = None
    best_p = None
    best_val = -1
    for _ in range(NUM_GENERATIONS):
        fitnesses = []
        for chrom in population:
            machine_clusters, k = decode(chrom, m)
            part_clusters = assign_parts(machine_clusters, machine_parts, p)

            machine_clusters, part_clusters = local_search(
                machine_clusters, part_clusters, machine_parts, k
            )
            val = fitness(machine_clusters, part_clusters, machine_parts)
            fitnesses.append(val)

            if val > best_val:
                best_val, best_m, best_p = val, machine_clusters, part_clusters

        elite_idx = sorted(
            range(len(population)), key=fitnesses.__getitem__, reverse=True
        )[:ELITE_SIZE]
        new_population = [population[i][:] for i in elite_idx]
        while len(new_population) < POP_SIZE - NUM_NEW_RANDOM_SOLUTIONS:
            parent1 = tournament(population, fitnesses)
            parent2 = tournament(population, fitnesses)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)
        while len(new_population) < POP_SIZE:
            new_population.append([random.random() for _ in range(m + 1)])

        population = new_population

    return best_m, best_p, best_val
