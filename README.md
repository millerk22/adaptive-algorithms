# Adaptive Algorithms

Code accompanying the paper:

> **Adaptive Algorithms for Data Summarization**  
> Ethan Epperly, Kevin Miller, and Robert Webber  


This repository implements a unified framework for selecting a small set of *prototype* points from a dataset by minimizing an objective function ("energy"). The framework supports clustering, low-rank approximation, nonnegative matrix factorization, and archetypal analysis, with adaptive search and adaptive sampling algorithms for both prototype construction and refinement via swaps.

## Installation

This repository uses a standard `src/` layout. That means Python will not find `adaptive_sampling` from a fresh checkout until the package is installed or `src/` is added to `PYTHONPATH`.

From the repository root, install the package in editable mode:

```bash
pip install -e .
```

To also install the test dependency and run the smoke tests:

```bash
pip install -e ".[test]"
pytest
```

Core dependencies are `numpy`, `scipy`, `scikit-learn`, `matplotlib`, `tqdm`, `joblib`, and `PyYAML`. Optional dataset loaders such as `ucimlrepo` and `graphlearning` are only needed for specific datasets.

If you are working in a notebook from a fresh clone, run this in the first notebook cell:

```python
%pip install -e .
```

## Quick Start

Data matrices are expected to have shape `(dim, n)`, with features as rows and samples as columns. In the notation below, this means $X = [x_1, \ldots, x_n] \in \mathbb{R}^{d \times n}$.

```python
from adaptive_sampling import AdaptiveAlgorithm, LowRankEnergy, load_dataset

X, labels = load_dataset("test", n_test=500)
energy = LowRankEnergy(X, p=2)

algorithm = AdaptiveAlgorithm(energy, seed=42, record=True)
algorithm.build_phase(k=10, method="sampling")
algorithm.swap_phase(method="search")

print(energy.indices)
print(energy.energy)
```

See [examples/demo.ipynb](examples/demo.ipynb) for an interactive usage demo.

## Core API

An energy object stores the dataset, the current prototype set, and the current per-point distances. The `AdaptiveAlgorithm` object operates on an energy object to select and refine prototypes.

| Class | Type string | Approximation set $\mathcal{A}(\mathcal{Y})$ | Application |
|---|---:|---|---|
| `ClusteringEnergy` | `cluster` | $\mathcal{Y}$ | $k$-medoids / $k$-means |
| `LowRankEnergy` | `lowrank` | $\mathrm{span}(\mathcal{Y})$ | Low-rank approximation |
| `ConicHullEnergy` | `conic` | $\mathrm{coni}(\mathcal{Y}) = \mathrm{conv}(\mathcal{Y} \cup \{0\})$ | Nonnegative matrix factorization |
| `ConvexHullEnergy` | `convex` | $\mathrm{conv}(\mathcal{Y})$ | Archetypal / archetypoid analysis |

The power $p \in (0, \infty]$ controls the $\ell^p$ aggregation of per-point distances:

$$
f(\mathcal{Y})
= \left(\sum_{i=1}^n d(x_i, \mathcal{A}(\mathcal{Y}))^p\right)^{1/p}.
$$

Using `p=None` corresponds to the infinity case:

$$
f(\mathcal{Y})
= \max_{1 \le i \le n} d(x_i, \mathcal{A}(\mathcal{Y})).
$$

Useful attributes after prototype selection:

- `energy.indices`: selected prototype indices.
- `energy.energy`: current energy value.
- `energy.dists`: per-point distances to the current approximation set.

## Build and Swap Methods

Prototype selection is split into two phases:

- `build`: construct an initial prototype set.
- `swap`: refine an existing prototype set by replacing selected points.

Build methods:

| Method | Description |
|---|---|
| `uniform` | Select prototypes uniformly at random. |
| `sampling` | Sample the next prototype $x_i$ with probability proportional to $d(x_i, \mathcal{A}(\mathcal{Y}))^p$. |
| `search` | Greedily add the point that most decreases $f(\mathcal{Y})$. |

Swap methods:

| Method | Description |
|---|---|
| `sampling` | Cyclically evict prototypes and resample replacements using residual distances. |
| `search` | Use eager swapping to search for replacements that decrease $f(\mathcal{Y})$. |

Common experiment method strings:

| Method string | Build | Swap |
|---|---|---|
| `uniform` | uniform | none |
| `sampling` | sampling | none |
| `search` | search | none |
| `sampling_sampling` | sampling | sampling |
| `sampling_search` | sampling | search |

## Running Experiments

Use [scripts/run_experiment.py](scripts/run_experiment.py) for command-line experiments:

```bash
python3 scripts/run_experiment.py --dataset test --k 10 --energy conic
python3 scripts/run_experiment.py --config configs/iris.yml
```

Key arguments:

| Argument | Default | Description |
|---|---:|---|
| `--dataset` | `test` | Dataset name handled by `adaptive_sampling.datasets.load_dataset`. |
| `--k` | `10` | Number of prototypes to select. |
| `--k_oversample` | `50` | Number of prototypes for oversampled build methods. |
| `--energy` | `conic` | One of `cluster`, `lowrank`, `conic`, or `convex`. |
| `--numseeds` | `1` | Number of random trials. |
| `--njobs` | `12` | CPU cores for parallelized conic/convex computations. |
| `--resultsdir` | `./results` | Output directory for `.pkl` result files. |
| `--save` | `1` | Whether to save results to disk. |
| `--record` | `1` | Whether to record per-iteration timing and energy values. |

Experiment settings can also be specified in YAML:

```yaml
dataset: iris
energy: cluster
k: 3
k_oversample: 10
numseeds: 10
powers: [1, 2, 5, None]
methods: [search, sampling, sampling_search, sampling_sampling]
```

Example configs are available in [configs](configs). Results are written to `results/` by default and are ignored by Git except for the directory placeholder.

## Reproducibility

- Randomized routines use the `seed` argument to `AdaptiveAlgorithm`.
- Experiment sweeps use seeds `42, 43, ..., 42 + numseeds - 1`.
- Saved `.pkl` result files are reused on later runs unless a method is listed under `overwrite` in the config.
- Local datasets are loaded from `data/`; see [data/README.md](data/README.md) and [docs/datasets.md](docs/datasets.md).

## Repository Layout

```text
src/adaptive_sampling/   Core package
scripts/                 Command-line experiment runner
configs/                 Example experiment configurations
examples/                Introductory notebooks
notebooks/               Plotting and reproduction notebooks
data/                    Local datasets and dataset notes
results/                 Generated experiment results
figures/                 Generated figures
docs/                    Additional usage notes
tests/                   Smoke tests
```

## Citation

Forthcoming...
