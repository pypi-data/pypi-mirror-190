from .utils import help
import os

if __name__ == "__main__":
    PWD = os.path.abspath(os.path.dirname(__file__))
    help(
        module_name="geoview",
        source_dir=PWD,
        ignores={"__init__.py", "__main__.py", "utils.py"},
        ignore_docs=True,
    )
    help(
        module_name="geoview.cli",
        source_dir=f"{PWD}/cli",
        ignores={"__init__.py", "__main__.py"},
        ignore_docs=False,
    )
