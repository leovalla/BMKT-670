import pandas as pd
from sklearn.utils import resample
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV

df = pd.read_csv("holiday_rental_consumer_segmentation.csv")

# print(df.head())
# print(df.shape)
# print(df.info())
# print(df["Event"].value_counts())

my_random_seed = 100

# Separate majority and minority classes
df_majority = df.loc[df["Event"] == "Spa", :]
df_minority_1 = df.loc[df["Event"] == "Shows", :]
df_minority_2 = df.loc[df["Event"] == "Outdoor activities", :]

# Upsample minority class
df_minority_upsampled_1 = resample(
    df_minority_1,
    replace=True,  # sample with replacement
    n_samples=116,  # to match majority class
    random_state=my_random_seed,
)  # reproducible results

df_minority_upsampled_2 = resample(
    df_minority_2,
    replace=True,  # sample with replacement
    n_samples=116,  # to match majority class
    random_state=my_random_seed,
)  # reproducible results

# Combine majority class with upsample minotity class
df = pd.concat(
    [df_majority, df_minority_upsampled_1, df_minority_upsampled_2]
)

# display new class counts 
# print(df["Event"].value_counts())

# Encode categorical variables
df_features = pd.get_dummies(df.iloc[:,:-1], drop_first=True)
# print(df_features.head())

x = df_features.to_numpy()
# print(x)

le= LabelEncoder()
le.fit(df["Event"])
print(le.classes_)
y = le.transform(df["Event"])
# print(y)

# price = x[:, 0].reshape(-1,1)

# min_max = MinMaxScaler()
# min_max.fit(price)
# price_minmax = min_max.transform(price)

# standard_scaler = StandardScaler()
# standard_scaler.fit(price)
# prices_standard_scaler = standard_scaler.transform(price)

"""
fig = plt.figure(figsize=[16, 8])

plt.subplot(2, 3, 1)
plt.hist(price, bins=50, alpha=0.75)
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.title("original")

plt.subplot(2, 3, 2)
plt.hist(price_minmax, bins=50 , alpha=0.75)
plt.xlabel("Price")
plt.title("MinMaxScaler")

plt.subplot(2, 3, 3)
plt.hist(prices_standard_scaler, bins=50 , alpha=0.75)
plt.xlabel("Price")
plt.title("StandardScaler")

plt.subplot(2, 3, 4)
plt.plot(range(len(price)), price)
plt.xlabel("Index")
plt.title("Price")

plt.subplot(2, 3, 5)
plt.plot(range(len(price_minmax)), price_minmax)
plt.xlabel("Index")

plt.subplot(2, 3, 6)
plt.plot(range(len(prices_standard_scaler)), prices_standard_scaler)
plt.xlabel("Index")

plt.show()
"""

# If you fit the scaler before the train-test split, you will have data leakeage.
# Data leakage occurs when information from outside the training dataset is used
# to create the mode. 

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.4, random_state=100, stratify=y
)

# Fit the sacaler only in the training data
standard_scaler = StandardScaler()
standard_scaler.fit(x_train[:, :5])

# transform both the training and test data
x_train[:, :5] = standard_scaler.transform(x_train[:, :5])
x_test[:, :5] = standard_scaler.transform(x_test[:, :5])

# This is the neural network Classifier - This is before the grid search
# mlp_clf = MLPClassifier(random_state=100, max_iter=10000) - This is before the grid search
# mlp_clf.fit(x_train, y_train)

# y_predprob_train = mlp_clf.predict_proba(x_train)
# y_predlabel_train = mlp_clf.predict(x_train)

# y_predprob_test = mlp_clf.predict_proba(x_test)
# y_predlabel_test = mlp_clf.predict(x_test)

# print(confusion_matrix(y_train, y_predlabel_train))
# print(confusion_matrix(y_test, y_predlabel_test))

# print(classification_report(y_train, y_predlabel_train))
# print(classification_report(y_test, y_predlabel_test))


# This is the neural network Classifier - With grid search
mlp_clf = MLPClassifier(max_iter=5000)

parameter_space = {
    "hidden_layer_sizes": [(50,50,50), (50,100,50,), (100,)],
    "activation": ["tanh", "relu"],
    "solver": ["sgd", "adam"],
    "alpha": [0.0001, 0.05],
    "learning_rate": ["constant", "adaptive"],
}

clf = GridSearchCV(mlp_clf, parameter_space, cv=3, n_jobs=4)
clf.fit(x_train, y_train)
print("Best parameters found:\n", clf.best_params_)

#All Results
means = clf.cv_results_['mean_test_score']
stds = clf.cv_results_['std_test_score']
for mean, std, params in zip(means, stds, clf.cv_results_['params']):
    print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params)) 


y_pred_test = clf.predict(x_test)

print("Results on the test set:")
print(classification_report(y_test, y_pred_test))





