import pandas as pd
import matplotlib.pyplot as plt
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

y_prob_train = clf.predict_proba(x_train)[:, 1]

from sklearn.metrics import roc_curve, auc

fpr, tpr, thresholds = roc_curve(y_train, y_prob_train)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=[7, 6])
plt.step(
    fpr, tpr, label="Logistic regression (AUC={:0.2f})".format(roc_auc), linewidth=2
)
plt.plot([0, 1], [0, 1], color="green", linestyle="--", label="Random (AUC=0.50)")
plt.xlabel("FPR", fontsize=13)
plt.ylabel("TPR", fontsize=13)
plt.legend(loc="lower right", fontsize=13)
plt.show()