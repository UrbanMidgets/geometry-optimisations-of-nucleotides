#!/usr/bin/env python3
import argparse
from ase.io import read, write
from ase.neighborlist import natural_cutoffs, NeighborList

def connected_components(atoms, mult=1.0):
    cutoffs = natural_cutoffs(atoms, mult=mult)
    nl = NeighborList(cutoffs, self_interaction=False, bothways=True)
    nl.update(atoms)
    visited, comps = set(), []
    for i in range(len(atoms)):
        if i in visited:
            continue
        stack, comp = [i], []
        while stack:
            j = stack.pop()
            if j in visited:
                continue
            visited.add(j)
            comp.append(j)
            neigh, _ = nl.get_neighbors(j)
            for k in neigh:
                if k not in visited:
                    stack.append(k)
        comps.append(sorted(comp))
    return comps

def write_orca_input(xyz_name, out_name, charge, mult, nprocs, maxcore_mb,
                     method_line, dims, add_chelpg):
    d1, d2, d3 = dims
    chelpg = "CHELPG\n" if add_chelpg else ""
    template = f"""! SP {method_line} TightSCF

%pal nprocs {nprocs} end
%maxcore {maxcore_mb}

%plots
  Format Gaussian_Cube
  ElPot true
  Density true
  Dim1 {d1}
  Dim2 {d2}
  Dim3 {d3}
end

{chelpg}* xyzfile {charge} {mult} {xyz_name}
"""
    with open(out_name, "w") as f:
        f.write(template)

def parse_indices(text):
    if not text:
        return None
    return [int(x)-1 for x in text.replace(" ", "").split(",") if x]

def main():
    p = argparse.ArgumentParser(description="Split complex into UMP and surface and make ORCA ESP inputs.")
    p.add_argument("input_xyz", help="Complex structure (.xyz)")
    p.add_argument("--ump-indices", help="1-based indices for UMP override (comma-separated).", default=None)
    p.add_argument("--cutoff-mult", type=float, default=1.0, help="Neighbor cutoff multiplier (default 1.0).")
    p.add_argument("--ump-charge", type=int, default=-1)
    p.add_argument("--ump-mult", type=int, default=1)
    p.add_argument("--surf-charge", type=int, default=0)
    p.add_argument("--surf-mult", type=int, default=1)
    p.add_argument("--nprocs", type=int, default=8)
    p.add_argument("--maxcore", type=int, default=2000, help="MB per core.")
    p.add_argument("--method", default="B3LYP D3BJ def2-TZVP", help='Method/basis line (default: "B3LYP D3BJ def2-TZVP").')
    p.add_argument("--dims", default="120,120,120", help="Cube grid dimensions Dim1,Dim2,Dim3 (default 120,120,120).")
    p.add_argument("--surf-dims", default=None, help="Override grid dims for surface (e.g. 160,160,160).")
    p.add_argument("--chelpg", action="store_true", help="Add CHELPG to fit charges to ESP.")
    args = p.parse_args()

    atoms = read(args.input_xyz)
    symbols = atoms.get_chemical_symbols()
    ump_idxs = parse_indices(args.ump_indices)

    if ump_idxs is None:
        comps = connected_components(atoms, mult=args.cutoff_mult)
        # Pick the component that contains a P as UMP
        with_p = [c for c in comps if any(symbols[i] == "P" for i in c)]
        if with_p:
            ump_idxs = sorted(with_p[0])
        else:
            # Fallback: largest component
            comps_sorted = sorted(comps, key=len, reverse=True)
            ump_idxs = comps_sorted[0]

    all_idx = set(range(len(atoms)))
    surf_idxs = sorted(all_idx - set(ump_idxs))

    ump = atoms[ump_idxs]
    surf = atoms[surf_idxs]

    write("ump.xyz", ump)
    write("surface.xyz", surf)

    d1, d2, d3 = [int(x) for x in args.dims.split(",")]
    if args.surf_dims:
        sd1, sd2, sd3 = [int(x) for x in args.surf_dims.split(",")]
    else:
        sd1, sd2, sd3 = d1, d2, d3

    write_orca_input("ump.xyz", "ump_esp.inp",
                     args.ump_charge, args.ump_mult,
                     args.nprocs, args.maxcore, args.method,
                     (d1, d2, d3), args.chelpg)

    write_orca_input("surface.xyz", "surface_esp.inp",
                     args.surf_charge, args.surf_mult,
                     args.nprocs, args.maxcore, args.method,
                     (sd1, sd2, sd3), args.chelpg)

    print(f"Wrote ump.xyz (n={len(ump)}) and surface.xyz (n={len(surf)})")
    print("Created ump_esp.inp and surface_esp.inp")
    print(f"Charges/mults used: UMP {args.ump_charge}/{args.ump_mult}, Surface {args.surf_charge}/{args.surf_mult}")
    print("Run with:\n  orca ump_esp.inp > ump_esp.out\n  orca surface_esp.inp > surface_esp.out")

if __name__ == "__main__":
    main()
