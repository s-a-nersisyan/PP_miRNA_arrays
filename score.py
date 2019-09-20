# This script inputs a pre-MIRNA - miRNA expression table (see README) and
# calculates a score for each row

import sys
import pickle
import numpy as np
from scipy.stats import spearmanr


def main(input_fname):
    # Open input file and skip the header
    in_f = open(input_fname)
    in_f.readline()
    # Load prepared miRBase data
    name_to_MI, name_to_MIMAT, MI_to_MIMAT = pickle.load(open("miRBase/miRBase.pkl", "rb"))

    # First, collect pre-miRNA and miRNA expression values
    pre_miRNA_expressions = {}
    mature_miRNA_expressions = {}
    for l in in_f:
        split = l.split("\t")
        id_ = split[0]
        expressions = list(map(float, split[1:]))
        if "MIMAT" in id_:
            mature_miRNA_expressions[id_] = expressions
        elif "MI" in id_:
            pre_miRNA_expressions[id_] = expressions

    # Now compute some maximal values for normalizing
    max_mature_expression = max(map(lambda expressions: np.median(expressions), mature_miRNA_expressions.values()))
    max_MIMAT = max(map(lambda id_: int(id_[5:]), mature_miRNA_expressions.keys()))

    # Now make a table with scores
    print("pre-miRNA\tmiRNA\tScore")  # Header
    for MI in pre_miRNA_expressions:
        for MIMAT in MI_to_MIMAT.get(MI, []):
            x = pre_miRNA_expressions[MI]
            y = mature_miRNA_expressions.get(MIMAT)
            if not y:
                continue

            mature_median = np.median(y)
            MIMAT_num = int(MIMAT[5:])
            corr_obj = spearmanr(x, y)
            R = corr_obj[0]

            normalized_expression = mature_median / max_mature_expression
            normalized_MIMAT = 1 - MIMAT_num / max_MIMAT
            normalized_R = (R + 1) / 2

            weights = [0.5, 0.3, 0.2]
            score = 0
            for v, w in zip([normalized_expression, normalized_MIMAT, normalized_R], weights):
                score += v*w

            print("\t".join([MI, MIMAT, str(score)]))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('''Usage: python score.py input_table.txt''')
    else:
        main(sys.argv[1])
