# Sentence Pair Scoring Models

# Basic: derived from Gale-Church Algorithm (length-based)



# LPSGC (Language Pair-Specific Gale Church)

The same basic length-based approach as Gale-Church, but with additional parameters
to be learned on a case-by-case basis for each language pair.

# PBS (Punctuation-Based Scorer)

Enhances the basic length-based approach to take into account punctuation,
including quotation marks.
This is obviously language-pair specific. Essentially, this approach learns
the probabilities for all relevant punctuation marks that symbol A occurs or
does not occur when symbol B is present. These probabilities are then combined
into an overall probability, which must be learned via a training algorithm. TODO

It is intuitively easy to see why, for many language pairs, this is a sensible
approach. It would be unusual, for example, to see an English sentence containing
4 commas to be translated into a German sentence containing only one comma or no
commas at all. Similarly, it is normal (not obligatory, but normal) for a sentence
ending in an exclamation mark or a question mark to be translated into a sentence
ending with the same punctuation mark.

This is far from perfect, since punctuation usage may vary considerably between
texts of the same language and particularly between genres. However, the beauty
of bitext alignment is that any additional information, as long as it is on
average more likely to be correct, can be used to improve the alignment.

# PBSP (PBS with Position)

Same approach as PBS, but using information about the quantized relative position of the
punctuation within the sentence, such as first 25%, middle 50%, last 25%.

# LVSPS (Limited-Vocabulary Sentence Pair Scorer)

Designed to be especially fast and lightweight for a sequential neural model, the LVSPS defines a small set of words (n=50, 100, 200, etc.) which are among the most frequently occurring and which generally serve a syntactic function.

This is usable with a variety of architectures. One of the best is the BiLSTM (bidirectional recurrent neural network with long short-term memory) with attention, trained with triplet loss (or alternatively with a binary classification objective).

Intuitively and at a high level, this approach involves learning to recognize correct matches from reduced form of the sentence with most semantic information stripped away and mostly syntactic information remaining.

While it is less powerful than a large model such as Sentence-BERT, it is sufficient for many purposes and has significant advantages in terms of speed and efficiency.

One of the interesting results is the difference in performance between bag-of-words (i.e. using word occurrence but not word order) models and sequential models. TODO

# Sentence Transformer

TODO

# Hybrid Approaches

TODO
