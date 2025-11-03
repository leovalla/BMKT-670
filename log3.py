import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import plotly.graph_objs as go

df = pd.read_csv("ad_click.csv")
# print(df.head())

x = df.iloc[:, :-1].to_numpy()
y = df.iloc[:, -1].to_numpy()

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

clf = LogisticRegression(random_state=0)
clf.fit(x_train, y_train)

print("Bias: {}; Weights: {}".format(clf.intercept_, clf.coef_))

y_prob_train = clf.predict_proba(x_train)[:, 1]
y_pred_train = clf.predict(x_train)
y_pred_test = clf.predict(x_test)
print("Probabilities (train):")
print(y_prob_train)
print("Predictions (train):")
print(y_pred_train)
print("Predictions (test):")
print(y_pred_test)

df_result_training = pd.DataFrame([y_train, y_prob_train, y_pred_train])
df_result_training = df_result_training.T
df_result_training.columns = ["Label_GT", "Label_Prob", "Label_Pred"]
print(df_result_training.head(10))

prob_click = df_result_training.loc[df_result_training["Label_GT"] == 1, "Label_Prob"]
prob_noclick = df_result_training.loc[df_result_training["Label_GT"] == 0, "Label_Prob"]

fig, axes = plt.subplots(1, 2, figsize=(15, 5))

axes[0].hist(prob_click.values, bins=30, alpha=0.75, label="Click")
axes[0].hist(prob_noclick.values, bins=30, alpha=0.75, label="No click")
axes[0].legend(loc="upper left")
axes[0].set_xlabel("$p$")
axes[0].set_ylabel("Frequency")

sns.kdeplot(x=prob_click.values, ax=axes[1], label="Click")
sns.kdeplot(x=prob_noclick.values, ax=axes[1], label="No click")
axes[1].axvline(x=0.5, ymin=0, ymax=4, color="g", label="Threshold")
axes[1].legend(loc="upper left")
axes[1].set_xlabel("$p$")
axes[1].set_ylabel("Density")

plt.show()

