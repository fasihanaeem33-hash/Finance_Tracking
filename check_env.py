import importlib
import sys

def check_package(pkg_name):
    try:
        pkg = importlib.import_module(pkg_name)
        version = getattr(pkg, "__version__", "unknown")
        print(f"{pkg_name}: OK, version {version}")
    except Exception as e:
        print(f"{pkg_name}: NOT INSTALLED OR FAILED TO IMPORT — {e}")

if __name__ == "__main__":
    for name in ["streamlit", "pandas"]:
        check_package(name)
    print("Python executable:", sys.executable)
