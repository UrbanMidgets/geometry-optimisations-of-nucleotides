# Geometry Optimisations of Nucleotides

Repository containing data and tools for PUK (Parallel UK-Shell) in geometry optimisations of mononucleotides on slab Si-O surface (001).

## Repository Structure

```
.
├── Data/
│   ├── flower_amp/       # AMP (Adenosine monophosphate) data
│   │   ├── amp_minH.xyz  # Minimized hydrogen structure
│   │   ├── AMP.cif      # Crystallographic Information File
│   │   ├── flower_amp.inp # ORCA input file
│   │   └── frames/      # Extracted trajectory frames
│   ├── flower_cmp/      # CMP (Cytidine monophosphate) data
│   ├── flower_gmp/      # GMP (Guanosine monophosphate) data
│   └── flower_ump/      # UMP (Uridine monophosphate) data
│
└── python_scripts/      # Analysis and processing tools
    ├── extract_frames.py          # Extract frames from trajectories
    ├── generate_trajectory_xyz.py  # Generate XYZ trajectory files
    ├── split_structure.py         # Split complexes and generate ORCA inputs
    └── vis_chdist.ipynb          # Visualization notebook
```

## Data Organization

Each nucleotide directory (`flower_amp/`, `flower_cmp/`, etc.) contains:
- Crystallographic data (`.cif` files)
- XYZ structure files
- ORCA input files (`.inp`)
- Optimized and pre-optimized structures
- Extracted trajectory frames

## Requirements

### Software Dependencies
- Python 3.8+
- ORCA 5.0+ (for quantum chemistry calculations)
- ASE (Atomic Simulation Environment)
- NumPy
- Jupyter Notebook
- Matplotlib

### Hardware Requirements
- Minimum 8GB RAM
- Multi-core processor recommended for ORCA calculations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/UrbanMidgets/geometry-optimisations-of-nucleotides.git
cd geometry-optimisations-of-nucleotides
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Ensure ORCA is installed and added to your PATH

## Python Scripts

- **extract_frames.py**: Extracts specific frames from XYZ trajectory files
- **split_structure.py**: Splits molecular complexes and generates ORCA ESP inputs
- **generate_trajectory_xyz.py**: Creates XYZ trajectory files
- **vis_chdist.ipynb**: Jupyter notebook for visualization

## Usage

### Extracting Frames
```bash
python python_scripts/extract_frames.py
```

### Splitting Structures
```bash
python python_scripts/split_structure.py input.xyz [options]
```

Options include:
- `--ump-charge`: Set UMP charge (default: -1)
- `--nprocs`: Set number of processors
- `--maxcore`: Set memory per core in MB
- `--method`: Specify computational method/basis

### Visualization
```bash
jupyter notebook python_scripts/vis_chdist.ipynb
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```
3. Make your changes and commit:
```bash
git add .
git commit -m "Add your feature description"
```
4. Push to your fork:
```bash
git push origin feature/your-feature-name
```
5. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Include docstrings for all functions
- Add unit tests for new features

## License

To my knowledge, this project is not licensed under any specific license.

## Citation

If you use this code in your research, please cite:

```bibtex
@software{geometry_optimisations_nucleotides,
  author = {Shamim Ekramullah},
  title = {Geometry Optimisations of Nucleotides},
  year = {2025},
  url = {https://github.com/yourusername/geometry-optimisations-of-nucleotides}
}
```

## Contact

- **Project Maintainer**: Shamim Mondol Ekramullah
- **Email**: wbn215@alumni.ku.dk
- **GitHub Issues**: For bug reports and feature requests
- **Discussion Forum**: For general questions and community discussions

## Acknowledgments

I would like to express my deepest gratitude to Associate Professor Lasse (Lars) Hemmingsen for his dedicated supervision, valuable feedback, and continuous guidance throughout this project. His support and scientific insight have been instrumental in shaping both the direction and the quality of this work.

I also wish to thank Associate Professor Tue Hassenkam for kindly serving as censor and for his constructive feedback during the evaluation of the project.

Special thanks are extended to Annika Weisberg Eenholt and Professor Stephan Sauer for their invaluable assistance with ORCA setup, HPC troubleshooting, and general methodological supervision. Their expertise in computational chemistry and practical problem-solving proved essential to the successful completion of the simulations.

Finally, on a more personal note, I wish to acknowledge someone who, though no longer by my side, remains a quiet source of inspiration. Her belief in me and pride in my work continue to remind me why I strive to become better. This ones for you.
