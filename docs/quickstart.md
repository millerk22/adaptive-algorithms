# Quickstart

This project uses a `src/` layout, so install it from the repository root before importing `adaptive_algorithms`:

```bash
pip install -e .
```

In a notebook, run the install command as a notebook cell:

```python
%pip install -e .
```

To include the test dependency:

```bash
pip install -e ".[test]"
```

Run a small experiment:

```bash
python scripts/run_experiment.py --dataset test --k 10 --energy conic --ntest 500
```

Or use one of the example configs:

```bash
python scripts/run_experiment.py --config configs/iris.yml
```

For an interactive starting point, open `examples/demo.ipynb`.
