# Experiments

Experiments are run through `scripts/run_experiment.py`.

Common options:

- `--dataset`: dataset name handled by `adaptive_sampling.datasets.load_dataset`.
- `--k`: number of selected prototypes.
- `--k_oversample`: number of prototypes to select for oversampled build methods.
- `--energy`: one of `cluster`, `lowrank`, `conic`, or `convex`.
- `--numseeds`: number of random seeds.
- `--config`: YAML file containing experiment settings.

Results are saved to `results/` by default. The result filename includes the dataset, energy, `k`, power, and number of seeds.

