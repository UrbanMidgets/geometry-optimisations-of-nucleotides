import os

# === USER SETTINGS ===
input_file = "flower_gmp.docker.struc1.all.optimized.xyz"

# ✅ Define which frames to extract:
#    - Use e.g. [0, 5, 10] for 0-based indexing (Python default)
#    - Leave empty [] to save all frames
frame_list = [4, 8, 11, 14]  # <-- Add your list of frame numbers here

# ✅ Define the output directory
output_dir = "frames"
os.makedirs(output_dir, exist_ok=True)
# ======================

# --- Core splitting logic ---
with open(input_file, "r") as f:
    lines = f.readlines()

i = 0
frame0 = 0
saved = 0

while i < len(lines):
    try:
        n_atoms = int(lines[i].strip())
    except ValueError:
        break  # probably end of file

    frame_lines = lines[i : i + n_atoms + 2]  # atoms + 2 header lines
    frame1 = frame0 + 1

    # ✅ Save all frames if frame_list is empty, or only selected ones
    if not frame_list or frame1 in frame_list:
        output_file = os.path.join(output_dir, f"frame_{frame1:03d}.xyz")
        with open(output_file, "w") as out:
            out.writelines(frame_lines)
        saved += 1

    frame0 += 1
    i += n_atoms + 2

print(f"✅ Done! Extracted {saved} frame(s) to '{output_dir}/'")
print(f"(Selection: {'all frames' if not frame_list else frame_list}, 1-based indexing)")