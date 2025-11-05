#-------------------------------------------------------------------------------
# project_09_heart_disease_part_1_lv.py
# This project create logistic models for a heart disease dataset and generate 
# visualizations
# Author: Leonardo Valladares
# Date: 2025-11-04
#------------------------------------------------------------------------------

# --------------------------------------
# Import necessary libraries
# --------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve, auc

# --------------------------------------
# Load data 
# --------------------------------------

df = pd.read_csv("heart_disease.csv")

# --------------------------------------
# Data Preparation 
# --------------------------------------

# Split data into training and test sets
x = df.iloc[:, :-1].to_numpy()
y = df.iloc[:, -1].to_numpy()

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=0)

# --------------------------------------
# Model
# --------------------------------------

# Create and train the model on the training data
clf = LogisticRegression(random_state=0)
clf.fit(x_train, y_train)

# Generate predictions for training set
y_prob_train = clf.predict_proba(x_train)[:, 1]
y_pred_train = clf.predict(x_train)

# Generate predictions for test set
y_prob_test = clf.predict_proba(x_test)[:, 1]
y_pred_test = clf.predict(x_test)

# Create dataframe with training set results
df_result_training = pd.DataFrame([y_train, y_prob_train, y_pred_train])
df_result_training = df_result_training.T  # transpose to get correct shape
df_result_training.columns = ["Ground_Truth", "Predicted_Probability_of_Heart_Disease", "Predicted_Label"] # I do not like to leave spaces on column names
print(df_result_training.head())

# Create dataframe with test set results
df_result_test = pd.DataFrame([y_test, y_prob_test, y_pred_test])
df_result_test = df_result_test.T # transpose to get correct shape
df_result_test.columns = ["Ground_Truth", "Predicted_Probability_of_Heart_Disease", "Predicted_Label"] 
print(df_result_test.head())

# --------------------------------------
# Model Evaluation
# --------------------------------------

# heatmap of the confusion_matrix of the training set
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
plt.title("Confusion Matrix - Training Set")  
# plt.show()

# Create a heatmap of the confusion_matrix of the test set
cf_matrix = confusion_matrix(y_test, y_pred_test)

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
plt.title("Confusion Matrix - Test Set")  
# plt.show()

# Classification Report of the training set
print("Training set")
print(classification_report(y_train, y_pred_train))

# classification report of the test set
print("Test set")
print(classification_report(y_test, y_pred_test))


# Plot ROC Curve  with AUC
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
plt.title("ROC Curve - Training Set")  
plt.show()