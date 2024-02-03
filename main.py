import dotlis as dl
import datkit

table = dl.read_tsv("car.txt")

X, y = table.exclass("class")

clf = datkit.DecisionTree()
clf = clf.fit(X, y)

clf.print_tree()

# print(clf.predict_one(["5.3...6.3","<=2.8","2.4...4.8","0.7...1.7"]))
# print(clf.predict(X))
