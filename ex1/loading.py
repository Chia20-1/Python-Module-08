"""
A package is a reusable code written by someone else.
A dependency is a package your project needs in order to turn.
"""
import importlib
import sys
from types import ModuleType
from typing import Any, NamedTuple


REQUIRED_PACKAGES = {
    "numpy": "Numerical computation ready",
    "pandas": "Data manipulation ready",
    "matplotlib.pyplot": "Visualization ready",
}


class MatrixStats(NamedTuple):
    average_latency: float
    average_signal: float
    high_anomaly_count: int
    total_points: int


def print_missing_dependency(package_name: str) -> None:
    display_name = package_name.split(".")[0]
    print(f"Missing dependency: {display_name}")
    print()
    print("Install with pip:")
    print("python -m pip install -r requirements.txt")
    print()
    print("Or install with Poetry:")
    print("poetry install")
    print("poetry run python loading.py")


def check_dependencies() -> dict[str, ModuleType] | None:
    modules = {}
    print("Checking dependencies:")
    for package_name, message in REQUIRED_PACKAGES.items():
        try:
            module = importlib.import_module(package_name)
        except ImportError:
            print_missing_dependency(package_name)
            return None
        root_package_name = package_name.split(".")[0]
        root_module = importlib.import_module(root_package_name)
        version = getattr(root_module, "__version__", "unknown")
        print(f"[OK] {root_package_name} ({version}) - {message}")
        modules[root_package_name] = root_module
        if package_name == "matplotlib.pyplot":
            modules["matplotlib.pyplot"] = module
    print()
    return modules


def simulate_matrix_data(np: ModuleType, pd: ModuleType) -> Any:
    rng = np.random.default_rng(seed=42)
    data = {
        "signal_strength": rng.normal(loc=70, scale=10, size=1000),
        "latency_ms": rng.integers(low=10, high=200, size=1000),
        "anomaly_score": rng.random(1000),
        "energy_usage": rng.normal(loc=50, scale=8, size=1000),
    }
    return pd.DataFrame(data)


def analyze_matrix_data(df: Any) -> MatrixStats:
    print("Analyzing Matrix data...")
    print(f"Processing {len(df)} data points...\n")
    average_latency = float(df["latency_ms"].mean())
    average_signal = float(df["signal_strength"].mean())
    high_anomalies = df[df["anomaly_score"] > 0.95]
    return MatrixStats(
        average_latency=average_latency,
        average_signal=average_signal,
        high_anomaly_count=len(high_anomalies),
        total_points=len(df),
    )


def generate_visualization(
    df: Any,
    stats: MatrixStats,
    plt: ModuleType
) -> None:
    output_file = "matrix_analysis.png"
    print("Generating visualization...")
    plt.figure(figsize=(8, 5))
    plt.hist(df["signal_strength"], bins=30)
    plt.title("Matrix Signal Strength Distribution")
    plt.xlabel("Signal Strength")
    plt.ylabel("Frequency")
    summary_text = (
        f"Points analyzed: {stats.total_points}\n"
        f"Avg signal: {stats.average_signal:.2f}\n"
        f"Avg latency: {stats.average_latency:.2f} ms\n"
        f"High anomalies (>0.95): {stats.high_anomaly_count}"
    )
    plt.gcf().text(
        0.98, 0.98, summary_text,
        ha="right", va="top", fontsize=9,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.6),
    )
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    print("\nAnalysis complete!")
    print(f"Results saved to: {output_file}")


def main() -> int:
    print("\nLOADING STATUS: Loading programs...\n")
    modules = check_dependencies()
    if modules is None:
        return 1
    np = modules["numpy"]
    pd = modules["pandas"]
    plt = modules["matplotlib.pyplot"]
    df = simulate_matrix_data(np, pd)
    stats = analyze_matrix_data(df)
    generate_visualization(df, stats, plt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
