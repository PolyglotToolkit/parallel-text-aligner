from pathlib import Path


class Locations:
    DIR_ROOT = Path(__file__).parent.parent
    DIR_CONFIG = DIR_ROOT / "configs"
    DIR_EXAMPLES = DIR_ROOT / "examples"
    DIR_MODULE = DIR_ROOT / "src" / "parallel_text_finisher"
    DIR_RESOURCES = DIR_ROOT / "resources"
    DIR_TEST = DIR_ROOT / "test"
