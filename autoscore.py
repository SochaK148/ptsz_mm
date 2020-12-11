from glob import glob
import numpy as np
import sys
print("[AUTOSCORE]")

PATH_PREFIX = "zadanie2"


def file_read_(path):
    with open(path, 'r') as file:
        data = file.read()
    return data


def get_solution(path):
    vec = open(path, 'r').read().split("\n")
    score, sol = int(vec[0]), vec[1:6]
    J = [[], [], [], [], []]
    for i, sol_i in enumerate(sol):
        J[i] = list(map(int, sol_i.strip().split(" ")))
    return score, J


def get_instance(instance_idx):
    owner_idx = instance_idx.split("_")[0]
    path = f"{PATH_PREFIX}/in/{owner_idx}/{instance_idx}.txt"
    data = file_read_(path).split("\n")
    N, P, R = int(data[0]), [], []
    B = list(map(float, data[1].strip().split(" ")))
    for job in data[2:]:
        if job == '':
            continue
        p, r = list(map(int, job.split(" ")))
        P.append(p)
        R.append(r)
    return B, P, R


def loss(B, P, R, J):
    N, M = len(P), len(B)
    flat = np.hstack(J)
    assert M == len(J)
    # print(flat, len(flat), N)
    assert N == len(flat)
    assert set(flat) == set(range(1, N+1))
    F = 0
    for m in range(M):
        b = B[m]
        t = 0
        for j in J[m]:
            j -= 1  # FIXME: bo indeksy od `1..`
            p, r = P[j], R[j]
            if t < r:
                t = r
            t += p / b
            F += t - r
    F = np.round(F / N)
    return int(F)


status = 0
print(f"[run] path = {PATH_PREFIX}/out/*/")
for path_dir in glob(f"{PATH_PREFIX}/out/*/"):
    person = path_dir.split("/")[-2]
    if not person.isdigit():
        continue
    print(f"\033[92m[{person}]\033[0m verification")
    for path in glob(f"{path_dir}/*.txt"):
        instance_idx = path.replace(path_dir, "").replace(".txt", "")
        print("\t--->", instance_idx, end=" | ")
        try:
            B, P, R = get_instance(instance_idx)
            score, J = get_solution(path)
            score_verify = loss(B, P, R, J)
            print(f"score_out={score} score_verify={score_verify}", end=" ")
            if abs(score - score_verify) <= 1:
                print("\033[92mOK\033[0m")
            else:
                print("\033[91mNO\033[0m")
                status = 1
        except:
            print("\033[91mNO\033[0m")
            status = 1
sys.exit(status)
