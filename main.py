import dotlis as dl
import datkit

table = dl.read_tsv("buycom.txt")

X, y = table.exclass("buys_computer")

clf = datkit.DecisionTree()
clf = clf.fit(X, y)

print(clf.root.info)
