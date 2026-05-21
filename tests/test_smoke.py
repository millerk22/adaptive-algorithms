from adaptive_algorithms import AdaptiveAlgorithm, ClusteringEnergy, load_dataset


def test_sampling_build_on_synthetic_dataset():
    X, labels = load_dataset("test", n_test=30)
    energy = ClusteringEnergy(X, p=2)
    algorithm = AdaptiveAlgorithm(energy, seed=42, record=True)

    algorithm.build_phase(k=3, method="sampling")

    assert labels is None
    assert len(energy.indices) == 3
    assert len(set(energy.indices)) == 3
    assert energy.energy is not None
