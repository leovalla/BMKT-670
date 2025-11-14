#-------------------------------------------------------------------------------
# Exer_8_neural_network_first_program_lv.py
# This project use neural networks for a holiday rental consumer segmentation 
# dataset and generate classification reports
# Author: Leonardo Valladares
# Date: 2025-11-13
#------------------------------------------------------------------------------

# --------------------------------------
# Import necessary libraries
# --------------------------------------

import pandas as pd
from sklearn.utils import resample
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report

# --------------------------------------
# Load data 
# --------------------------------------

df = pd.read_csv("holiday_rental_consumer_segmentation.csv")

# --------------------------------------
# Feature and label encoding
# --------------------------------------

# Encode categorical variables
df_features = pd.get_dummies(df.iloc[:,:-1], drop_first=True)
# print("\nEncoded feature columns:")
# print(df_features.head())

# Label encoding
le= LabelEncoder()
le.fit(df["Event"])
print("\nEvent classes:")
print(le.classes_)

y = le.transform(df["Event"])
# print("\nEncoded labels:")
# print(y)

# Join features and labels back to a single DataFrame for resampling
df = pd.concat([df_features, pd.Series(y, name="Event")], axis=1)
# print("\nFeature and label encoding dataframe:")
# print(df.head())


# --------------------------------------
# Splitting dataset
# --------------------------------------

my_random_seed = 100

df_train, df_test = train_test_split(
    df, test_size=0.4, random_state=my_random_seed, stratify=y
)

# --------------------------------------
# Resampling training set
# --------------------------------------

# display new class counts 
# print("\nEvent class count original:")
# print(df_train["Event"].value_counts())

# Separate majority and minority classes
df_train_majority = df_train.loc[df_train["Event"] == 2, :]
df_train_minority_1 = df_train.loc[df_train["Event"] == 1, :]
df_train_minority_2 = df_train.loc[df_train["Event"] == 0, :]

# Upsample minority class
df_train_minority_upsampled_1 = resample(
    df_train_minority_1,
    replace=True,  # sample with replacement
    n_samples=69,  # to match majority class
    random_state=my_random_seed,
)  # reproducible results

df_train_minority_upsampled_2 = resample(
    df_train_minority_2,
    replace=True,  # sample with replacement
    n_samples=69,  # to match majority class
    random_state=my_random_seed,
)  # reproducible results

# Combine majority class with upsample minotity class
df_train = pd.concat(
    [df_train_majority, df_train_minority_upsampled_1, df_train_minority_upsampled_2]
)

# display new class counts 
# print("\nEvent class count after resampling:")
# print(df_train["Event"].value_counts())

# --------------------------------------
# Fitting scaler only on the training data
# --------------------------------------

# Transforn to numpy array
x_train = df_train.iloc[:,:-1]
x_train = x_train.to_numpy()

x_test = df_test.iloc[:,:-1]
x_test = x_test.to_numpy()
# print("\nNumpy array of features:")
# print(x_train)

# Fit the sacaler only in the training data
standard_scaler = StandardScaler()
standard_scaler.fit(x_train[:, :5])


# transform both the training and test data
x_train[:, :5] = standard_scaler.transform(x_train[:, :5])
x_test[:, :5] = standard_scaler.transform(x_test[:, :5])

# Response variable 
y_train = df_train["Event"]
y_test = df_test["Event"]

# --------------------------------------
# Model training 
# --------------------------------------

mlp_clf = MLPClassifier(random_state=my_random_seed, max_iter=10000) 
mlp_clf.fit(x_train, y_train)

y_predprob_train = mlp_clf.predict_proba(x_train)
y_predlabel_train = mlp_clf.predict(x_train)

y_predprob_test = mlp_clf.predict_proba(x_test)
y_predlabel_test = mlp_clf.predict(x_test)

# --------------------------------------
# Print out to the terminal the classification report of training data and test data
# --------------------------------------

print("\nResults on the training set:")
print(classification_report(y_train, y_predlabel_train))
print("\nResults on the test set:")
print(classification_report(y_test, y_predlabel_test))

