# Statistical Physics - Laboratory 1: Microstates & Thermodynamics

This repository contains the code, data analysis, and report generation for **Laboratory 1** of Statistical Physics (Group 2B). The project explores microstates enumeration, multiplicity distributions, and basic thermodynamic functions using numerical methods in Python.

---

## 📦 Project Structure

```text
.
├── AI_STATEMENT.md           # Declaration of AI assistance usage
├── README.md                 # Project documentation
├── environment.yml           # Conda environment definition
├── main.py                   # Main entry point to run full pipeline / analysis
├── pytest.ini                # Pytest configuration file
│
├── notebooks/                # Exploratory Jupyter Notebooks
│   └── microstates.ipynb     # Notebook for analyzing microstate distributions
│
├── report/                   # LaTeX report and output artifacts
│   ├── figures/              # Generated plot files (PDF format)
│   │   ├── enumeration_time.pdf
│   │   ├── multiplicity_distribution.pdf
│   │   └── part2_distribution.pdf
│   ├── main.tex              # Main LaTeX manuscript
│   ├── microstates_N7.txt    # Generated microstates raw output (N=7)
│   ├── multiplicities_1c.txt # Numerical output table for Part 1c
│   └── table3_part2.txt      # Data summary table for Part 2
│
├── src/                      # Source code modules
│   ├── __init__.py
│   ├── combinatorics.py      # Microstate counting & combinatorial methods
│   ├── microstates.py        # Microstate generation and filtering logic
│   └── thermodynamics.py    # Entropy, energy, and thermodynamic functions
│
└── tests/                    # Unit tests suite
    ├── test_combinatorics.py
    ├── test_microstates.py
    └── test_thermodynamics.py
```

---

## 🛠️ Environment Setup & Installation

### Option 1: Conda Environment (Recommended)

To recreate the exact environment with all required dependencies, use the `environment.yml` file:

```bash
# Create the environment
conda env create -f environment.yml

# Activate the environment
conda activate lab1_stats
```

### Option 2: Pip Setup

Alternatively, install the core dependencies via `pip`:

```bash
pip install numpy matplotlib scipy pytest
```

---

## 🚀 Execution & Usage

### 1. Run the Main Pipeline
Execute the main script to generate the dataset output files and plots under the `report/` directory:

```bash
python main.py
```

### 2. Run Test Suite
Run unit tests to verify the core algorithms in `src/`:

```bash
pytest
```

---

## 📊 Modules Description

- **`src/combinatorics.py`**: Implementation of binomial/multinomial coefficients, analytical multiplicity formulations, and exact state-counting algorithms.
- **`src/microstates.py`**: State space generation algorithms for multi-particle, multi-level systems under defined constraints.
- **`src/thermodynamics.py`**: Functions to calculate microcanonical entropy ($S = k_B \ln \Omega$), internal energy, and system temperatures.

---

## 📝 License & Authors

- **Course:** Statistical Physics
- **Lab Group:** Group 2B