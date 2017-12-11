import numpy as np
from sklearn import tree
from sklearn.datasets import load_iris
import pandas as pd
import subprocess


iris = load_iris()
test_idx = [0, 50, 100]

# trainng data
train_target = np.delete(iris.target, test_idx)
train_data = np.delete(iris.data, test_idx, axis=0)

# testing data
test_target = iris.target[test_idx]
test_data = iris.data[test_idx]

clf = tree.DecisionTreeClassifier()
clf.fit(train_data, train_target)

print(test_target)
print(clf.predict(test_data))

# converting into the pdf file
with open("iris.dot", "w") as f:
    f = tree.export_graphviz(clf, out_file=f)

subprocess.call("dot -Tpdf iris.dot -o iris_classifier.pdf", shell=True)
