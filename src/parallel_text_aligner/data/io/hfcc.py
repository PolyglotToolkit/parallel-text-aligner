from pathlib import Path
from typing import Dict, Tuple

import yaml


def open_hfcc_yaml(yaml_path: Path) -> Dict[str, int]:
    with open(yaml_path) as f:
        hfcc = yaml.safe_load(f)

    # for
    # return dict(mapped)
