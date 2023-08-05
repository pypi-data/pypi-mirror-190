from typing import Any, Dict, List, Optional, Set, Tuple, Union  # noqa
import json
import os


def dummy():
    return True


def help(
    *,
    module_name: str,
    source_dir: str,
    verbose: bool = False,
    ignores: Set[str],
    ignore_docs: bool = False,
):
    files = sorted(
        f for f in os.listdir(source_dir) if f.endswith(".py") and f not in ignores
    )
    from geoview import doc_url

    print(f"{module_name}:")
    for i, f in enumerate(files):
        print(f'\t{i:3d}:\tpython3 -m {module_name}.{f[:f.index(".")]} --help')
    if verbose:
        for f in files:
            cmd = f'python3 -m {module_name}.{f[:f.index(".")]} --help'
            print("\n\n\n", "*" * 80, sep="")
            print(f"$ {cmd}")
            os.system(cmd)

    if not ignore_docs:
        print("\n===== GEOVIEW =====\n\n  - ", end="")
        print(
            "\n  - ".join(
                [
                    f"document: {doc_url}",
                    "installation: python3 -m pip install geoview -U",
                ]
            )
        )
        print("\nversion: " + json.dumps(version(), indent=4))


def version() -> Dict[str, str]:
    try:
        from geoview import (
            __version__,
            package_name,
            git_branch,
            git_commit_hash,
            git_commit_date,
            git_commit_count,
            git_diff_name_only,
            doc_url,
        )

        ret = {
            "__version__": __version__,
            "package_name": package_name,
            "git_branch": git_branch,
            "git_commit_hash": git_commit_hash,
            "git_commit_date": git_commit_date,
            "git_commit_count": git_commit_count,
            "git_diff_name_only": git_diff_name_only,
            "doc_url": doc_url,
        }
    except ImportError as e:
        ret = {
            "error": f"failed to get repolint version info, error: {repr(e)}",
        }
    return ret
