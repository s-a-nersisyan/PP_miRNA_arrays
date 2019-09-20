# Convert miRBase source files to dicts and write them into .pkl

import pickle
import re


# Make mapping between hsa-mir-* names and MI ids
name_to_MI = {}
for l in open("miRBase/hairpin.fa"):
    if not l.startswith(">") or "hsa" not in l:
        continue
    split = l.strip().split(" ")
    name = split[0][1:]
    MI = split[1]
    name_to_MI[name] = MI

# Same mapping for hsa-miR-* and MIMAT
name_to_MIMAT = {}
for l in open("miRBase/mature.fa"):
    if not l.startswith(">") or "hsa" not in l:
        continue
    split = l.strip().split(" ")
    name = split[0][1:]
    MIMAT = split[1]
    name_to_MIMAT[name] = MIMAT

# Mapping between precursors and corresponding mature miRNAs
MI_to_MIMAT = {}
for l in open("miRBase/miRNA.str"):
    if not l.startswith(">") or not "hsa" in l:
        continue
    s = re.sub(r">", r"", l)
    s = re.sub(r"\(.*\)", r"", s)
    s = re.sub(r" +", r"\t", s)
    s = s.split("\t")
    MI = name_to_MI[s[0]]
    for name in s[1:]:
        name = name.strip()
        name = re.sub(r"\[", r"", name)
        name = re.sub(r":.*\]", r"", name)
        MI_to_MIMAT[MI] = MI_to_MIMAT.get(MI, []) + [name_to_MIMAT[name]]


pickle.dump((name_to_MI, name_to_MIMAT, MI_to_MIMAT), open("miRBase/miRBase.pkl", "wb"))
