from sklearn import tree
import csv
from enum import Enum


def generateKnockTree():

	SHAVE = 0
	BASIC = 1

	shave_and_haircut_file = open('knock_spacings.csv', 'r')
	basic_knock_file = open('knock_spacings_basic.csv', 'r')

	shave_reader = csv.reader(shave_and_haircut_file)
	basic_reader = csv.reader(basic_knock_file)


	shave_data = list(shave_reader)
	basic_data = list(basic_reader)

	total_data = shave_data + basic_data


	knock_label = []

	for i in range(len(shave_data)):
		knock_label.append(SHAVE)

	for i in range(len(basic_data)):
		knock_label.append(BASIC)

	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(total_data, knock_label)

	return clf

