# %%
import pandas as pd
from sklearn.model_selection import train_test_split
from datetime import datetime 
import numpy as np
from sklearn.preprocessing import StandardScaler
                                                    
dataStreamer = pd.read_excel(r'D:\fyp\蝉妈妈主播数据（摘选） - 副本.xlsx')

dataLive = pd.read_excel(r'D:\fyp\蝉妈妈单场数据（摘选） - 副本.xlsx')

# Merge the two dataframes on the "liveStreamer_name" column
merged_df = pd.merge(dataStreamer, dataLive, on='liveStreamer_name',how='inner')

# Save the merged dataframe to a new file
# me rged_df.to_csv('merged_file.csv', index=False)

# Get the copy of merged data
data = merged_df.copy()

# %%
# Data processing
# Check the missing values in the dataframe
missing_values = data.isna().sum()
print(missing_values)

# %%
# use last live data to predict next live data
import math
for i in range(len(data)-1):
    if  data.iloc[i, 0] == data.iloc[i+1, 0]:
        data.iloc[i,32] = data.iloc[i+1, 32]
    else:
        data.iloc[i,32] = np.nan
        
# Drop rows with NaN values in the third column
data.dropna(subset=['sales_amount'], inplace=True)

# save for the heatmap
data1 = data.copy()

# %%
# Let's also draw a heatmap visualization of the correlation matrix
# import seaborn as sns
# import matplotlib.pyplot as plt
#
# corr_matrix = data1.corr(method='spearman')
# f, ax = plt.subplots(figsize=(16,8))
# sns.heatmap(corr_matrix, annot=True, fmt='.2f', linewidth=0.8,
#             annot_kws={"size": 5}, cmap='coolwarm', ax=ax)
# plt.xticks(fontsize=10)
# plt.yticks(fontsize=10)
# plt.show()

# %%
from sklearn.preprocessing import OneHotEncoder

# 使用独热编码将商品类别变量转换为二元变量
encoder = OneHotEncoder()
encoded_data = encoder.fit_transform(data[['product_interest']])

# 将独热编码后的结果转换为DataFrame格式
onehot_data = pd.DataFrame(encoded_data.toarray(), columns=encoder.get_feature_names_out(['product_interest']))

# 将独热编码后的结果存回原始数据集中
data = data.assign(**onehot_data)

# 删除原始数据集中的类别变量列
data = data.drop(columns=['product_interest'])

# 将时间戳转换为周期性编码的特征
# data['start_time'] = pd.to_datetime(data['start_time'])
# data['hour_of_day'] = data['start_time'].apply(lambda x: x.hour)
# hour_features = np.eye(24)[data['hour_of_day']]
# for i in range(24):
#     data['hour_{}'.format(i)] = hour_features[:,i]
    

# 删除原始的时间戳和小时数特征 , 'ProductConversion_rate','hour_of_day', 'start_time'
data = data.dropna()
data2 = data.copy()
data.drop(['live_number_within30','start_time', 'liveStreamer_name','hour_of_day','sales_amount',
           'average_sales_volume', 'average_sales_revenue', 'average_living_time(s)', 'averageViewer_number',
           'average_videoCollect_number','average_videoShare_number', 'start_time'], axis=1, inplace=True)

from sklearn.preprocessing import scale
# define predictor and response variables
X = data.copy()
y = data2['sales_amount'].copy()

# devide the train set and test set
x_train, x_test, y_train, y_test = train_test_split(X, y,test_size = 0.3, random_state=22)

# 假设需要标准化的列为第1列到第32列
features_to_scale_x_train = x_train.iloc[:, 1:32].values
features_to_scale_x_test= x_test.iloc[:, 1:32].values

# 创建StandardScaler类的实例
scaler = StandardScaler()

# 对需要标准化的列进行标准化
scaled_features_x_train = scaler.fit_transform(features_to_scale_x_train)
scaled_features_x_test = scaler.transform(features_to_scale_x_test)

# 将标准化后的列替换原始数据集中的列
x_train.iloc[:, 1:32] = scaled_features_x_train
x_test.iloc[:, 1:32] = scaled_features_x_test

# 标准化 y_train 和 y_test
scaler_y = StandardScaler()
y_train = scaler_y.fit_transform(y_train.values.reshape(-1, 1)).flatten()
y_test = scaler_y.transform(y_test.values.reshape(-1, 1)).flatten()

# %%
X.to_csv('databaseYcy.csv', index=False)

# %%
# Ridge regression
import pandas as pd
from numpy import arange
from sklearn.linear_model import Ridge
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import RepeatedKFold
from sklearn.metrics import mean_squared_error

# define cross-validation method to evaluate model
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)

# define model
model = RidgeCV(alphas=arange(0.01, 1, 0.01), cv=cv, scoring='neg_mean_absolute_error')

# fit model
model.fit(x_train, y_train)

# display lambda that produced the lowest test MSE
print(model.alpha_)

# test the model
# 预测训练集结果
y_pred = model.predict(x_train)

# 预测训练集结果
mse = mean_squared_error(y_train, y_pred)
print('Mean squared error of train set: %.8f' % mse)
      
# 预测测试集结果
y_pred2 = model.predict(x_test)

# 计算均方误差
mse2 = mean_squared_error(y_test, y_pred2)
print('Mean squared error of test set: %.8f' % mse2)

# %%
import pickle
filename = "modelproj.sav"
pickle.dump(model, open(filename, 'wb'))

# %%

import joblib

# Save the trained model to disk
joblib.dump(model, 'model.pkl')

# Save the scaler x and y to disk
joblib.dump(scaler, 'scaler_x.pkl')
joblib.dump(scaler_y, 'scaler_y.pkl')

# %%

# 还原特征矩阵
x_train.iloc[:, 1:32] = scaler.inverse_transform(x_train.iloc[:, 1:32])
x_test.iloc[:, 1:32] = scaler.inverse_transform(x_test.iloc[:, 1:32])

# 还原目标变量y
y_pred2 = scaler_y.inverse_transform(y_test.reshape(-1, 1)).flatten()

# %%
# Let's also draw a heatmap visualization of the correlation matrix
import seaborn as sns
import matplotlib.pyplot as plt

corr_matrix = x_train.corr(method='spearman')
f, ax = plt.subplots(figsize=(16,8))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', linewidth=0.5,
            annot_kws={"size": 5}, cmap='coolwarm', ax=ax)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.show()

# %%
# 1529268247387884
# 1025373967147655
# 1067055383568368

# %%
# 用这些来看dataframe 数据
# data1.info()
# x_train.describe()

# %%
# 特征工程
from sklearn.feature_selection import RFE 
from sklearn.linear_model import Ridge

# Create a Ridge regression estimator
estimator = Ridge()

# Create an RFE selector with 10 features
selector = RFE(estimator, n_features_to_select=50)

# Fit the selector to the training data
selector.fit(x_train, y_train)

# Print the selected features
print("Selected Features:", x_train.columns[selector.support_])

# %%
# Set the max_columns option to None to display all columns
pd.options.display.max_columns = None

# Check where the missing values are located
missing_values = x_train.isna().any()
print(missing_values)

# Check if the DataFrame contains any infinite number
if np.isinf(x_train).any().any():
    print("DataFrame contains infinite number")
else:
    print("DataFrame does not contain infinite number")
    
# Check if the DataFrame contains any missing values
if x_train.isna().any().any():
    print("DataFrame contains missing values")
else:
    print("DataFrame does not contain missing values")
