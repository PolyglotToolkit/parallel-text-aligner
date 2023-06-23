class SentenceTransformer:
    def __init__(self) -> None:
        ...

    def __call__(
        self,
    ) -> None:
        raise NotImplementedError(
            "The 'sentence-transformers' package is not available."
            " Please install it or, alternatively, run `pip install parallel-text-finisher[sentence-transformers]`."
        )
