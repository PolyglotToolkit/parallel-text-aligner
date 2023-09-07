import hydra

from parallel_text_aligner.common.locations import Locations


@hydra.main(version_base=None, config_path=Locations.DIR_CONFIG, config_name="default")
def get_sentence_aligner():
    ...


@hydra.main(version_base=None, config_path=Locations.DIR_CONFIG, config_name="default")
def get_word_aligner():
    ...
