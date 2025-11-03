import pandas as pd
# import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("ad_click.csv")

x = df.iloc[:, :-1].to_numpy()
y = df.iloc[:, -1].to_numpy()

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

clf = LogisticRegression(random_state=0)
clf.fit(x_train, y_train)

y_pred_train = clf.predict(x_train)
y_pred_test = clf.predict(x_test)

from sklearn.metrics import classification_report

print("Training set")
print(classification_report(y_train, y_pred_train))

print("Test set")
print(classification_report(y_test, y_pred_test))