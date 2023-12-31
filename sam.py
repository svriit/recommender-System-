# -*- coding: utf-8 -*-
"""sam.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wKvxgPZus_FhqFbIKOlV-Fqfzy6WzWDt
"""

import numpy as np
import pandas as pd
import matplotlib as plt
from sklearn.metrics.pairwise import cosine_similarity

import torch
import pandas as pd
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from google.colab import drive
drive.mount('/content/drive')

from surprise import KNNBasic, KNNBaseline, KNNWithMeans,KNNWithZScore,BaselineOnly, CoClustering,SVD,SVDpp,SlopeOne,NMF
from surprise.model_selection import cross_validate, train_test_split

from plotly.offline import init_notebook_mode, plot, iplot
import plotly.graph_objs as go
init_notebook_mode(connected=True)
from surprise.reader import Reader
from surprise.dataset import Dataset
from surprise import accuracy

rat=pd.read_csv("/content/drive/MyDrive/recomender/ratings.txt",delimiter=" ",names=["user-id","item-id","rating-value"])
rat.shape

"""autotrustee"""

trustval=pd.read_csv("/content/drive/MyDrive/recomender/ratings.txt",delimiter=" ",names=["user-id (trustor)","user-id (trustee)","trust-value"])
trustval.head()
trustval.shape

rat.shape
usercount=rat['user-id'].nunique()
itemcount=rat['item-id'].nunique()

print("User:",usercount)
print("Item:",itemcount)
rat.shape
#1508*2071=31,23,068

max_value = trustval['trust-value'].max()
max_value

max_value = rat['rating-value'].max()
max_value
rat['rating-value'].min()

user_rating_matrix=rat.pivot_table(index='user-id', columns='item-id',values='rating-value',fill_value=0)

User_Item_rat_np=user_rating_matrix.values
User_Item_rat_np

count=0
for i in user_rating_matrix.values:
    for j in i:
        if(j==0):
            count+=1

print(count/(usercount*itemcount))

user_rating_trust=trustval.pivot_table(index='user-id (trustor)', columns='user-id (trustee)',values='trust-value')

user_encoder = LabelEncoder()
item_encoder = LabelEncoder()

reader = Reader(rating_scale=(0.5, 4))
data = Dataset.load_from_df(rat[['user-id','item-id','rating-value']], reader)
trainset = data.build_full_trainset()
testset = trainset.build_testset()

new=[]
for row in testset:
    user_id = row[0]
    item_id = row[1]
    user_trust = trustval[['user-id (trustor)'] == user_id) & (trustval['user-id (trustee)'] == item_id)]
    if not user_trust.empty:
        trust_value = user_trust.iloc[0]['trust-value']
        x= row[2]*trust_value
        new.append({user_id,,x})

results_dict = {}

"""## 1.KNNBasic algorithm"""

# Initialize and fit the KNNBasic model
knn_basic = KNNBasic(k=21,sim_options={'name': 'cosine', 'user_based': False})
knn_basic.fit(trainset)
knn_basic_predictions = knn_basic.test(testset)

rmsebasic= accuracy.rmse(knn_basic_predictions)
maebasic = accuracy.mae(knn_basic_predictions)

# Initialize the KNNBasic model
model = KNNBasic()
cv=[5,10,15,20]
# Perform cross-validation with the model
for i in cv:
    results = cross_validate(model, data, measures=['RMSE', 'MAE'], cv=i, verbose=True)
    if i==10:
        results_dict['knnbasic'] = results

"""## 2. KNNBaseline algorithm"""

# Initialize and fit the KNNBasic model
knn_baseline = KNNBaseline(k=21,sim_options={'name': 'cosine', 'user_based': False})
knn_baseline.fit(trainset)
knn_baseline_predictions = knn_baseline.test(testset)

rmsebaseline = accuracy.rmse(knn_baseline_predictions)
maebaseline = accuracy.mae(knn_baseline_predictions)

# Initialize the KNNBaseline model
model = KNNBaseline()
cv=[5,10,15,20]
# Perform cross-validation with the model
for i in cv:
    results = cross_validate(model, data, measures=['RMSE', 'MAE'], cv=i, verbose=True)
    if i==10:
        results_dict['knnbaseline']=results

"""## 3.KNNwithMeans algorithm"""

# Initialize and fit the KNNBasic model
knn_withmeans = KNNWithMeans(k=40,sim_options={'name': 'cosine', 'user_based': False})
knn_withmeans.fit(trainset)
knn_withmeans_predictions = knn_withmeans.test(testset)

rmseknnwithmeans= accuracy.rmse(knn_withmeans_predictions)
maeknnwithmeans = accuracy.mae(knn_withmeans_predictions)

# Initialize the KNNWithMeans model
model = KNNWithMeans()
cv=[5,10,15,20]
# Perform cross-validation with the model
for i in cv:
    results = cross_validate(model, data, measures=['RMSE', 'MAE'], cv=i, verbose=True)
    if i==10:
        results_dict['knnwithmeans']=results

"""## 4. SVD algorithm"""

# Apply SVD
svd = SVD(n_factors=100, n_epochs=20, init_std_dev=0.01, lr_all=0.007, reg_all=0.02)
svd.fit(trainset)
prediction_svd = svd.test(testset)

rmsesvd= accuracy.rmse(prediction_svd)
maesvd = accuracy.mae(prediction_svd)

# Initialize the SVD model with hyperparameters
svd = SVD(n_factors=100, n_epochs=20,init_std_dev=0.01,lr_all=0.007,reg_all=0.02)

cv=[5,10,15,20]
# Perform cross-validation with the model
for i in cv:
    results = cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=i, verbose=True)
    if i==10:
        results_dict['svd']=results

"""## 5. SVD++ algorithm"""

# Apply SVD++
svdpp = SVDpp(n_factors=20, n_epochs=20, init_std_dev=0.01, lr_all=0.005, reg_all=0.02)
svdpp.fit(trainset)
prediction_svdpp = svdpp.test(testset)

rmsesvdpp= accuracy.rmse(prediction_svdpp)
maesvdpp = accuracy.mae(prediction_svdpp)

# Initialize the SVD model with hyperparameters
svdpp = SVDpp(n_factors=20, n_epochs=20,init_std_dev=0.01,lr_all=0.005,reg_all=0.02)

cv=[5,10,15,20]
# Perform cross-validation with the model
for i in cv:
    results = cross_validate(svdpp, data, measures=['RMSE', 'MAE'], cv=i, verbose=True)
    if i==10:
        results_dict['svd++']=results

"""## 6.Co-clustering algorithm"""

coclustering=CoClustering(n_cltr_u=3,n_cltr_i=4,n_epochs=20)
coclustering.fit(trainset)
coclustering_prediction = coclustering.test(testset)

rmseclustering= accuracy.rmse(coclustering_prediction)
maeclustering = accuracy.mae(coclustering_prediction)

coclustering=CoClustering(n_cltr_u=3,n_cltr_i=4,n_epochs=20)

cv=[5,10,15,20]
# Perform cross-validation with the model
for i in cv:
    results = cross_validate(svdpp, data, measures=['RMSE', 'MAE'], cv=i, verbose=True)
    if i==10:
        results_dict['coclustering']=results

results_dict

'''
k_value = 10

# Initialize the KNNBasic model with the specified k value
knn_model = KNNBasic(k=k_value, sim_options={'name': 'cosine', 'user_based': True})

knn_model.fit(trainset)

user_id = 1
item_id = 1
predicted_rating = knn_basic.predict(user_id, item_id)

# Access the actual_k value from the prediction
actual_k_value = predicted_rating.details['actual_k']

print("Actual_k value used in prediction:", actual_k_value)
'''

'''import matplotlib.pyplot as plt

model_names = results_dict.keys()
rmse_values = [result['test_rmse'].mean() for result in results_dict.values()]
mae_values = [result['test_mae'].mean() for result in results_dict.values()]

plt.figure(figsize=(10, 5))
plt.bar(model_names, rmse_values, label='RMSE', alpha=0.7)
plt.bar(model_names, mae_values, label='MAE', alpha=0.7)
plt.xlabel('Models')
plt.ylabel('Performance')
plt.title('Comparison of Models')
plt.legend()
plt.show()'''

"""## Analysing and comparing models"""

import matplotlib.pyplot as plt

model_names = results_dict.keys()
n_models = len(model_names)
bar_width = 0.35

rmse_values = [result['test_rmse'].mean() for result in results_dict.values()]
mae_values = [result['test_mae'].mean() for result in results_dict.values()]

print(f'RMSE:{rmse_values},MAE:{mae_values}')

index = range(n_models)

plt.figure(figsize=(10, 5))

# Create separate bars for RMSE and MAE
plt.bar(index, rmse_values, bar_width, label='RMSE', alpha=0.7)
plt.bar([i + bar_width for i in index], mae_values, bar_width, label='MAE', alpha=0.7)

plt.xlabel('Models')
plt.ylabel('Performance')
plt.title('Comparison of Models ( CV = 10 )')
plt.xticks([i + bar_width / 2 for i in index], model_names)
plt.legend()
plt.show()



'''# Extract the 'est' values from the list of tuples (3rd element, index 2)
truth=np.array([prediction[2] for prediction in knn_basic_predictions])
estimates = [prediction[3] for prediction in knn_basic_predictions]

# Convert the list of 'est' values to a NumPy array
estimates_array = np.array(estimates)'''

'''
from sklearn.metrics import mean_squared_error

mse = mean_squared_error(truth,estimates_array)
mse'''

user_trust = user_trust_data[(user_trust_data['user_id'] == user_id) & (user_trust_data['trusted_user_id'] == item_id)]