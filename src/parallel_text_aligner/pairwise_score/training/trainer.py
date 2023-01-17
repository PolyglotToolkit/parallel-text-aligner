

class Trainer():
    """

    """
    ...


class TrainerFactory():
    """
    
    """

    def __init__(self, config) -> None:
        ...

    def get_trainer(self) -> Trainer:
        return Trainer()


def get_trainer(config) -> Trainer:
    factory = TrainerFactory(config)
    return factory.get_trainer()
