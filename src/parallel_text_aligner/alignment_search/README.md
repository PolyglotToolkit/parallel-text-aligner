# Alignment Search

The fundamental problem of bitext sentence alignment involves matching the sentences that correspond to one another.
Under ideal circumstances, this is a trivial problem:
Sentence *i* in language A corresponds to sentence *i* in language B.
In practice, it is more complicated, for a number of reasons:
* sentence tokenization (the way each text is split into tokens) may differ
  between languages, possibly due to errors
* some 'sentences'  may have no equivalent, for example, there may be artifacts
  from OCR, or one language may include section/chapter titles while the other
  language does not. Ancient texts involves some amount of archaeology and
  scholarly debate are especially difficult in this regard. Imagine aligning the
  Catholic Bible to the Protestant Bible, or aligning a text with its censored
  translation
* sometimes a sentence in one language is translated into two or more sentences in
  another language or multiple sentences may be combined into one
* in some rare cases, sentence order may be reversed, for example:
  sentence i → sentence i+1, sentence i+1 → sentence i

## Scoring functions

A sentence pair scoring function (SPSF) takes as input two text strings and
outputs a number between 0 and 1, with 1 suggesting a perfect match and 0
suggesting no match.

SPSFs differ with regard to complexity and what they take into consideration.
The simplest look only at the relative length of the sentence pairs.
To illustrate, consider a candidate alignment where sentence A has 12% of the
total words (or characters; both work well for most languages) in its text,
while sentence B accounts for only 2% of the words in its respective text.
While it may be possible for this to be the result of a bizarrely periphrastic
or laconic translation, it seems intuitively much more likely that the candidate
alignment is incorrect. Empirically, it turns out that this is indeed the case.

Another approach is to harness the full power of contemporary (post-2019) natural
language processing using something like Sentence-BERT embeddings to determine
the semantic similarity of sentence pairs, and then use these scores to find
the highest-scoring permissible path through sentence pair matrix (i.e. the
Cartesian product of sentences). This is also supported.

An interesting question that arises when considering the wide range of
intermediate approaches, beyond the parsimony of Gale-Church and the complexity
and power of Sentence-BERT: What is the most lightweight and efficient approach
that manages to use some semantic information, but is straightforward to train
for any language pair without tremendous computational and labor cost?

One such approach is to use a small vocabulary, words that require little
language-specific linguistic pre-processing such as lemmatization or stemming,
and which also account for a significant proportion of words used. The remaining
words will simply be treated as \<UNKNOWN\>. For example:

I \<UNKNOWN\> to the \<UNKNOWN\> .

Je \<UNKNOWN\> \<UNKNOWN\> au \<UNKNOWN\> .

Is it possible for a neural network to learn that this sentence pair is a good
match? In our experiments, it turned out that TODO


## Preliminary analyses

If a pair of texts each have high-level units, such as chapters or paragraphs,
it makes sense to use a divide-and-conquer approach, first matching high-level
units before moving on to the more fine-grained alignment. this also has the
advantage that there is more data, and more data is usually better; a sentence
pair may easily be misclassified due to higher variance, but pairs of chunks of
text consisting of many sentences will be much less likely to be misclassified.

Some sentences are unique; many are not. Many have near-equivalents elsewhere
in the text. As such, false positives are inevitable, and the hierarchical
approach to alignment serves to prevent the vast majority of possible false
positives from ever being taken into consideration during the fine-grained
alignment.

## Anchor points

Related to the idea of "divide and conquer" is the idea of anchoring: Some
candidate pairs may score especially high, so we can take these as our anchors,
and align the text between them. Under the assumption that the anchor points
are, in fact, correct (and in empirical tests, they nearly always are), any
approach, how ever naive or advanced, will perform better (or at least as well)
on the smaller subset pair than on the entire text pair, as there is less room
for error.

## Masking

With an SPSF selected, the naïve approach would be to score all sentence pairs.
This can be quite wasteful, given that beyond a certain distance from the
diagonal, the probability of a correct alignment is so low as to render any
investigation useless. The solution is the look only at a subset of the
possible sentence pairs, those on the diagonal and those within 'k' of it.

## Search Algorithms

TODO

### Beam Search

TODO

## Learning Search Parameters

There are some parameters that may not be optimal when set arbitrarily by hand
and must instead be learned from data. In fact, this is true of nearly all
parameters and is the motivation for all of machine learning.

In this case, there are certain search parameters that may vary for different
language pairs and as such must be learned on a case-by-case basis. For example,
beam size in beam search, or the value of `k` in the masking step. For hybrid
scoring, it is possible to learn the optimal weighting of the component SPSFs.

TODO

# Manual Post-Processing

Since SPSFs, by definition, output scores, these can also be used to flag
suspicious sentence pairs of the final alignment. Sometimes it happens that
the best alignment found has unusually low scores. In these cases, it may be
worth taking a look at the alignment to see whether it is correct. (Taking a
look at the output is usually just a good idea anyway.)
