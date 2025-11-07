#!/usr/bin/env python3
import sys, re

if len(sys.argv) < 3:
    print("Usage: python orca_out_to_xyz_manual.py <orca.out> <trajectory.xyz>")
    sys.exit(1)

src, dst = sys.argv[1], sys.argv[2]
coord_header = "CARTESIAN COORDINATES (ANGSTROEM)"

frames = []
with open(src, "r", errors="ignore") as f:
    lines = f.readlines()

i, n = 0, len(lines)
while i < n:
    if coord_header in lines[i]:
        # Skip header and separator lines
        i += 1
        while i < n and re.match(r"^\s*-{2,}", lines[i]):
            i += 1

        atoms = []
        while i < n:
            line = lines[i].strip()
            if not line:
                break
            if "CARTESIAN COORDINATES" in line:
                break
            parts = line.split()
            if len(parts) < 4:
                break
            sym = parts[0]
            try:
                x, y, z = map(float, parts[1:4])
            except ValueError:
                break
            atoms.append((sym, x, y, z))
            i += 1

        if atoms:
            frames.append(atoms)
    i += 1

if not frames:
    print("No coordinate blocks found.")
    sys.exit(2)

with open(dst, "w") as f:
    for idx, atoms in enumerate(frames, start=1):
        f.write(f"{len(atoms)}\nStep={idx}\n")
        for sym, x, y, z in atoms:
            f.write(f"{sym:2s} {x: .8f} {y: .8f} {z: .8f}\n")

print(f"✅ Wrote {len(frames)} frames to {dst}")
