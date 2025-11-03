import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import plotly.graph_objs as go

df = pd.read_csv("ad_click.csv")
print(df.head())

x = df.iloc[:, :-1].to_numpy()
y = df.iloc[:, -1].to_numpy()
print(x[:5])
print(y[:5])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

fig_width = 800
fig_height = 600

plot_data_training = go.Scatter3d(
    x=x_train[:, 0],
    y=x_train[:, 1],
    z=y_train,
    mode="markers",
    marker=dict(color="#1f77b4", size=5, line=dict(color="#7f7f7f", width=1)),
    name="Training data"
)

plot_data_test = go.Scatter3d(
    x=x_test[:, 0],
    y=x_test[:, 1],
    z=y_test,
    opacity=.75,
    mode="markers",
    marker=dict(color="#ff7f0e", size=5, line=dict(color="#7f7f7f", width=1)),
    name="Test data"
)

data = [plot_data_training, plot_data_test]

layout = go.Layout(
    title="3D Scatter plot of training and test data",
    autosize=True,
    width=fig_width,
    height=fig_height,
    margin=dict(l=65, r=50, b=65, t=90),
    scene={
        "xaxis":{"title":"Spending"},
        "yaxis":{"title":"Age"},
        "zaxis":{"title":"Click"},
        "camera":{"eye":{"x":1.5,"y":-1.65,"z":0.9}},
        "aspectmode":"cube",
    },
    showlegend=True,
)

fig = go.Figure(data=data, layout=layout)
fig.show()

clf = LogisticRegression(random_state=0)
clf.fit(x_train, y_train)

plot_data_training = go.Scatter3d(
    x=x_train[:, 0],
    y=x_train[:, 1],
    z=y_train,
    mode="markers",
    marker=dict(color="#1f77b4", size=5, line=dict(color="#7f7f7f", width=1)),
    name="Training data",
)

plot_data_test = go.Scatter3d(
    x=x_test[:, 0],
    y=x_test[:, 1],
    z=y_test,
    opacity=.75,
    mode="markers",
    marker=dict(color="#ff7f0e", size=5, line=dict(color="#7f7f7f", width=1)),
    name="Test data"
)

xx=np.linspace(np.min(x_train[:,0]),np.max(x_train[:,0]),50)
yy=np.linspace(np.min(x_train[:,1]),np.max(x_train[:,1]),50)
xx_yy = np.array(np.meshgrid(xx,yy)).T.reshape(-1,2)
X= pd.DataFrame(xx_yy, columns=['Spending','Age'])

predictions_prob = clf.predict_proba(X.to_numpy())
print(predictions_prob[:5])
predictions_prob = pd.DataFrame(predictions_prob).iloc[:,1].values
print(type(predictions_prob))
print(predictions_prob.shape)
predictions_prob = predictions_prob.reshape(50,-1)
print(predictions_prob.shape)

plot_trace_prob = go.Surface(
    x=xx,
    y=yy,
    z=predictions_prob,
    name="LR model",
    showscale=False,
)

# plot predicted labels (training)
predictions_label_training = clf.predict(x_train)
plot_pred_label_training = go.Scatter3d(
    x=x_train[:, 0],
    y=x_train[:, 1],
    z=predictions_label_training,
    opacity=0.5,
    mode="markers",
    marker=dict(color="#2ca02c", size=5, line=dict(color="#7f7f7f", width=1)),
    name = "Predicted label (training data)",
)

# plot predicted labels (test)
predictions_label_test = clf.predict(x_test)
plot_pred_label_test = go.Scatter3d(
    x=x_test[:, 0],
    y=x_test[:, 1],
    z=predictions_label_test,
    opacity=0.5,
    mode="markers",
    marker=dict(color="#e377c2", size=5, line=dict(color="#7f7f7f", width=1)),
    name = "Predicted label (test data)",
)

data = [plot_data_training, plot_data_test, plot_trace_prob, plot_pred_label_training, plot_pred_label_test]

layout = go.Layout(
    title="",
    autosize=True,
    width=fig_width,
    height=fig_height,
    margin=dict(l=65, r=50, b=65, t=90),
    scene={
        "xaxis":{"title":"Spending"},
        "yaxis":{"title":"Age"},
        "zaxis":{"title":"Click"},
        "camera":{"eye":{"x":1.5,"y":-1.65,"z":0.9}},
        "aspectmode":"cube",
    },
    showlegend=True,
)

fig = go.Figure(data=data, layout=layout)
fig.show()