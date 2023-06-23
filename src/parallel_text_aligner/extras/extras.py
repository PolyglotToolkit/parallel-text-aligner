try:
    from sentence_transformers import (
        SentenceTransformer,  # pylance: disable=unused-import
    )
except:
    from .mocks import SentenceTransformer


__all__ = [
    "SentenceTransformer",
]
