from parallel_text_aligner.common.config import CONFIG
from parallel_text_aligner.pairwise_score.models import basic, neural_nonseq, neural_seq
from parallel_text_aligner.pairwise_score.training.trainer import get_trainer


class Model:
    """ """

    ...


class ModelFactory:
    """ """

    def __init__(self, config) -> None:
        self.config = config

    def get_model(self) -> Model:
        trainer = get_trainer(self.config)
        ...
        return Model()


def get_model(config) -> Model:
    """ """
    factory = ModelFactory(config)
    return factory.get_model()
