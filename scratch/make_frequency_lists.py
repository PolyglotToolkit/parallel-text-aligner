import yaml

enfunc = "/home/isaac/Learning/parallel-text-aligner/resources/word_lists/function_words/EN_unsorted.yaml"
defunc = "/home/isaac/Learning/parallel-text-aligner/resources/word_lists/function_words/DE_unsorted.yaml"
enfreq = (
    "/home/isaac/Learning/parallel-text-aligner/resources/word_lists/frequency/EN.txt"
)
defreq = (
    "/home/isaac/Learning/parallel-text-aligner/resources/word_lists/frequency/DE.txt"
)

with open(enfunc) as f:
    enfun = set(yaml.load(f, Loader=yaml.CLoader))
with open(defunc) as f:
    defun = set(yaml.load(f, Loader=yaml.CLoader))
with open(enfreq) as f:
    enfre = yaml.load(f, Loader=yaml.CLoader).split()
with open(defreq) as f:
    defre = yaml.load(f, Loader=yaml.CLoader).split()

en = [word for word in enfre if word in enfun]
de = [word for word in defre if word in defun]

with open(enfunc.replace("_unsorted", ""), "w") as f:
    yaml.dump(en, f)
with open(defunc.replace("_unsorted", ""), "w") as f:
    yaml.dump(de, f)
