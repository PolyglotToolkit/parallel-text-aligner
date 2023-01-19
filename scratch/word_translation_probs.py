# -*- coding: utf-8 -*-
# %%
import re
from itertools import product
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import yaml
from funcy import lfilter, lmap


# %%
class WordTokenizer:
    """ """

    def __init__(self, lang, word_list_type, num_words) -> None:
        self.word_list_path = f"/home/isaac/Learning/parallel-text-aligner/resources/word_lists/{word_list_type}/{lang}.yaml"
        with open(self.word_list_path) as f:
            self.wordlist = yaml.safe_load(f)[:num_words]
        self.wordset = set(self.wordlist)
        self.id2word = dict(enumerate(self.wordlist))
        self.word2id = dict((v, k) for k, v in self.id2word.items())

    def __call__(self, sentence):
        self.sentence = (
            re.sub("( ?[\(\)\.,:;] ?)", r" \1 ", sentence.lower()).strip().split()
        )
        # overlap = list(self.wordset.intersection(sentence.lower().split()))
        # alternative:
        overlap = [word for word in self.sentence if word in self.wordset]
        return lmap(self.word2id.get, overlap)

    def ids2words(self, ids: Iterable):
        return lmap(self.id2word.get, ids)


# %%
tok_en = WordTokenizer("EN", "function_words", 500)
ids_en = tok_en(
    "exalt with the praise of your Lord and ask forgiveness from Him. For indeed, He is the Turner (for the penitent)."
)
print(ids_en)
print(tok_en.ids2words(ids_en))

# %%
tok_de = WordTokenizer("DE", "function_words", 500)
ids_de = tok_de(
    "Dann sing das Lob deines Herrn und bitte Ihn um Vergebung. Siehe, Er wendet sich gnädig wieder zu."
)
print(ids_de)
print(tok_de.ids2words(ids_de))


# %%
class QuranReader:
    def __init__(self, path) -> None:
        self.path = path
        with open(self.path) as f:
            self.lines = lfilter(lambda s: re.match("\d", s), f.readlines())
        self.lines = lmap(
            lambda s: re.split("(?<=\d)\|", s.strip("\n"))[-1], self.lines
        )


qr_de = QuranReader(
    "/home/isaac/Learning/parallel-text-aligner/scratch/data/de.khoury.txt"
)

qr_en = QuranReader(
    "/home/isaac/Learning/parallel-text-aligner/scratch/data/en.qaribullah.txt"
)


# %%
class Counter:
    def __init__(self, tok_a: WordTokenizer, tok_b: WordTokenizer) -> None:
        self.tok_a = tok_a
        self.tok_b = tok_b
        self.dim_a = len(self.tok_a.wordset)
        self.dim_b = len(self.tok_b.wordset)
        self.freqs_a = np.zeros((self.dim_a), dtype=np.int32)
        self.freqs_b = np.zeros((self.dim_b), dtype=np.int32)
        self.counts = np.zeros((self.dim_a, self.dim_b), dtype=np.int32)

    def count(self, list_a: list, list_b: list):
        assert len(list_a) == len(list_b)
        for a, b in zip(list_a, list_b):
            ids_a = self.tok_a(a)
            ids_b = self.tok_b(b)
            for id in ids_a:
                self.freqs_a[id] += 1
            for id in ids_b:
                self.freqs_b[id] += 1
            for id_a, id_b in product(set(ids_a), set(ids_b)):
                self.counts[id_a, id_b] += 1

    def compute_scores(self):
        self.freq_mask_a = np.repeat(self.freqs_a[..., np.newaxis], self.dim_b, axis=1)
        self.freq_mask_b = np.repeat(self.freqs_b[np.newaxis, ...], self.dim_a, axis=0)
        self.scores = np.round(
            self.counts * self.counts / (self.freq_mask_a * self.freq_mask_b + 1e-5), 3
        )


# %%
counter = Counter(tok_en, tok_de)
counter.count(qr_en.lines, qr_de.lines)
counter.compute_scores()

max_ids = [np.argmax(x) for x in counter.counts]
for i, max_id in enumerate(max_ids):
    print(f"{tok_en.id2word[i]:<20}{tok_de.id2word[max_id]}")
max_ids = [np.argmax(x) for x in counter.scores]
for i, max_id in enumerate(max_ids):
    print(f"{tok_en.id2word[i]:<20}{tok_de.id2word[max_id]}")

# %%
plt.imshow(counter.counts[:50, :50])
plt.show()

# %%
plt.imshow(counter.scores[:50, :50])
plt.show()

# %%
# now do the same for incorrect sentence pairs
rotated_list_de = qr_de.lines[-100:] + qr_de.lines[:-100]
counter2 = Counter(tok_en, tok_de)
counter2.count(qr_en.lines, rotated_list_de)
counter2.compute_scores()

# %%
max_ids = [np.argmax(x) for x in counter2.counts]
for i, max_id in enumerate(max_ids):
    print(f"{tok_en.id2word[i]:<20}{tok_de.id2word[max_id]}")

# %%
# max_ids = [np.argmax(x) for x in counter2.scores]
for i, max_id in enumerate(max_ids):
    print(f"{tok_en.id2word[i]:<20}{tok_de.id2word[max_id]}")

# %%
plt.imshow(counter2.counts[:50, :50])
plt.show()

# %%
plt.imshow(counter2.scores[:50, :50])
plt.show()
# next step: compare co-occurrences in correct with co-occurrences in random pairs


# %%
diff_counts = counter.counts - counter2.counts
plt.imshow(diff_counts[:50, :50])
plt.show()

# %%
diff_scores = counter.scores - counter2.scores
plt.imshow(diff_scores[:50, :50])
plt.show()


# %%
max_ids = [np.argmax(x) for x in diff_counts]
for i, max_id in enumerate(max_ids):
    print(f"{tok_en.id2word[i]:<20}{tok_de.id2word[max_id]}")

# %%
max_ids = [np.argmax(x) for x in diff_scores]
for i, max_id in enumerate(max_ids):
    print(f"{tok_en.id2word[i]:<20}{tok_de.id2word[max_id]}")


# %%
# now need to find a way to use scores to score a sentence pair


def score_pair(sent_a, sent_b, tok_a, tok_b, scores):
    ids_a = tok_a(sent_a)
    ids_b = tok_b(sent_b)
    if not min(len(ids_a), len(ids_b)):
        return 0
    pair_scores = np.zeros((len(ids_a), len(ids_b)))
    for (i, id_a), (j, id_b) in product(enumerate(ids_a), enumerate(ids_b)):
        pair_scores[i, j] = scores[id_a, id_b]
    if len(ids_a) >= len(ids_b):
        score = list(np.max(pair_scores, axis=1))
    else:
        score = list(np.max(pair_scores, axis=0))
    score = sum(score) / len(score)
    return score


# %%
block_size = 20
lines_en = qr_en.lines[100 : 100 + block_size]
lines_de = qr_de.lines[100 : 100 + block_size]
wanted = lfilter(lambda t: abs(t[0] - t[1]) < 5, product(range(block_size), repeat=2))
display = np.zeros((block_size, block_size))
for i, j in wanted:
    display[i, j] = 1

plt.imshow(display)
plt.show()

# %%
for i, j in wanted:
    print(i, j)
    score = score_pair(lines_en[i], lines_de[j], tok_en, tok_de, diff_scores)
    display[i, j] = score

plt.imshow(display)
plt.show()

# TODO: use lemmas instead of function words, run on larger and more varied corpora
# also add functionality to keep best predictors
