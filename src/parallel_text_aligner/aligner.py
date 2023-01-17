from parallel_text_aligner.alignment_search.searcher import get_searcher
from parallel_text_aligner.common.config import CONFIG
from parallel_text_aligner.data_handling.data_handler import get_data_handler
from parallel_text_aligner.pairwise_score.scorer import get_scorer


class Aligner():
    """

    """
    def __init__(self, config) -> None:
        self.dh = get_data_handler(CONFIG)
        self.searcher = get_searcher(CONFIG)
        self.scorer = get_scorer(CONFIG)
        
        self.dh.load()
    
    def align(self) -> None:
        ...

    def save(self) -> None:
        ...
