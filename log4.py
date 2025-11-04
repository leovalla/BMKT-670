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

df_result_training = pd.DataFrame([y_train, y_prob_train, y_pred_train])
df_result_training = df_result_training.T
df_result_training.columns = ["Label_GT", "Label_Prob", "Label_Pred"]

prob_click = df_result_training.loc[df_result_training["Label_GT"] == 1, "Label_Prob"]
prob_noclick = df_result_training.loc[df_result_training["Label_GT"] == 0, "Label_Prob"]

fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# sns.kdeplot(x=prob_click.values, ax=axes[0, 0], label="Click")
# sns.kdeplot(x=prob_noclick.values, ax=axes[0, 0], label="No click")
# axes[0, 0].axvline(x=0.5, ymin=0, ymax=4, color="r", label="Threshold")
# xx = axes[0, 0].get_lines()[0].get_data()
# shade = xx[0][xx[0] >= 0.5]
# kde = xx[1][xx[0] >= 0.5]
# axes[0, 0].fill_between(shade, kde, alpha=0.3, color="royalblue", label="TP")
# axes[0, 0].legend(loc="upper left")
# axes[0, 0].set_xlabel("$p$")
# axes[0, 0].set_ylabel("Density")

# sns.kdeplot(x=prob_click.values, ax=axes[0, 1], label="Click")
# sns.kdeplot(x=prob_noclick.values, ax=axes[0, 1], label="No click")
# axes[0, 1].axvline(x=0.5, ymin=0, ymax=4, color="r", label="Threshold")
# xx = axes[0, 1].get_lines()[1].get_data()
# shade = xx[0][xx[0] <= 0.5]
# kde = xx[1][xx[0] <= 0.5]
# axes[0, 1].fill_between(shade, kde, alpha=0.3, color="orange", label="TN")
# axes[0, 1].legend(loc="upper left")
# axes[0, 1].set_xlabel("$p$")
# axes[0, 1].set_ylabel("Density")

# sns.kdeplot(x=prob_click.values, ax=axes[1, 0], label="Click")
# sns.kdeplot(x=prob_noclick.values, ax=axes[1, 0], label="No click")
# axes[1, 0].axvline(x=0.5, ymin=0, ymax=4, color="r", label="Threshold")
# xx = axes[1, 0].get_lines()[0].get_data()
# shade = xx[0][xx[0] < 0.5]
# kde = xx[1][xx[0] < 0.5]
# axes[1, 0].fill_between(shade, kde, alpha=0.3, color="royalblue", label="FN")
# axes[1, 0].legend(loc="upper left")
# axes[1, 0].set_xlabel("$p$")
# axes[1, 0].set_ylabel("Density")

# sns.kdeplot(x=prob_click.values, ax=axes[1, 1], label="Click")
# sns.kdeplot(x=prob_noclick.values, ax=axes[1, 1], label="No click")
# axes[1, 1].axvline(x=0.5, ymin=0, ymax=4, color="r", label="Threshold")
# xx = axes[1, 1].get_lines()[1].get_data()
# shade = xx[0][xx[0] >= 0.5]
# kde = xx[1][xx[0] >= 0.5]
# axes[1, 1].fill_between(shade, kde, alpha=0.3, color="orange", label="FP")
# axes[1, 1].legend(loc="upper left")
# axes[1, 1].set_xlabel("$p$")
# axes[1, 1].set_ylabel("Density")

plt.show()

from sklearn.metrics import confusion_matrix

cf_matrix = confusion_matrix(y_train, y_pred_train)

group_names = ["TN", "FP", "FN", "TP"]
group_counts = ["{0:0.0f}".format(value) for value in cf_matrix.flatten()]
group_percentages = [
    "{0:.2%}".format(value) for value in cf_matrix.flatten() / np.sum(cf_matrix)
]
labels = [
    f"{v1}\n{v2}\n{v3}"
    for v1, v2, v3 in zip(group_names, group_counts, group_percentages)
]
labels = np.asarray(labels).reshape(2, 2)

fig = plt.figure()
sns.heatmap(cf_matrix, annot=labels, fmt="", cmap="Blues")
plt.show()