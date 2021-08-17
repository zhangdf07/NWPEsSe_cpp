#!/usr/bin/env python

# For using ABCluster with GROMACS

import sys
import os

AA2nm = 0.1

xyz_fn = sys.argv[1] # $in$
gro_fn = sys.argv[2] # min.gro
tx = float(sys.argv[3])*AA2nm # PX
ty = float(sys.argv[4])*AA2nm # PY
tz = float(sys.argv[5])*AA2nm # PZ

#
# Change only the lines below!
# Do NOT change others!
#
# Add your residues:
#
# ("Resname", num_residues, num_residue_atoms)
#
residues = [
    ("POPC", 100, 52),
    ("SOL",  300, 3)
    ]
#
# Change only the lines above!
# Do NOT change others!
#

coords = []
with open(xyz_fn, 'r') as fd:
    lines = fd.readlines()
    for line in lines[2:]:
        line = line.split()
        coords.append([line[0], float(line[1])*AA2nm, float(line[2])*AA2nm, float(line[3])*AA2nm])

with open(gro_fn, 'w') as fd:    
    fd.write("Generated by ABCluster\n")
    fd.write('%d\n' % (len(coords)))
    
    pres = 0
    patoms = 0
    idx_atom = 0
    idx_residue_start = 0
    idx_residue = 0
    for coord in coords:        
        residue_name = residues[pres][0]
        residue_num  = residues[pres][1]
        residue_size = residues[pres][2]
        fd.write('%5d%4s%6s%5d%8.3f%8.3f%8.3f\n' % (idx_residue_start+idx_residue+1, residue_name, coord[0], idx_atom+1, coord[1], coord[2], coord[3]))
        idx_atom = idx_atom+1
        patoms = patoms+1
        if patoms%residue_size == 0:
            idx_residue = idx_residue+1
            if idx_residue == residue_num:
                idx_residue_start = idx_residue_start+idx_residue
                idx_residue = 0
                pres = pres+1
                patoms = 0
    fd.write('%15.8f %15.8f %15.8f\n' % (tx, ty, tz))