# 引入所需的库
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import h2o
from h2o.automl import H2OAutoML
from h2o.estimators.xgboost import H2OXGBoostEstimator

# 初始化资料集列表
all_features_list = []
all_labels_list = []

batch_size = 1000
counter = 0



# 遍历所有 CSV 文件
for i in range(500101001, 500119092):
    file_path = f'rentbike/{i}.csv'
    if not os.path.exists(file_path):
        continue
    
    # 读取数据
    df = pd.read_csv(file_path)
    
    # 选择初始特征
    df = df[['sno', 'total', 'latitude', 'longitude', 'act', 'srcUpdateTime', 'available_rent_bikes']]

    # 转换 srcUpdateTime 为 datetime
    df['srcUpdateTime'] = pd.to_datetime(df['srcUpdateTime'])

    # 提取时间特征
    df['hour'] = df['srcUpdateTime'].dt.hour
    df['minute'] = df['srcUpdateTime'].dt.minute
    df['second'] = df['srcUpdateTime'].dt.second
    df['weekday'] = df['srcUpdateTime'].dt.weekday  # 週几

    # 扩展后的特征集
    features = df[['sno', 'total', 'latitude', 'longitude', 'act', 'hour', 'minute', 'second', 'weekday']]
    labels = df['available_rent_bikes']  # 预测 available_rent_bikes

    all_features_list.append(features)
    all_labels_list.append(labels)
    counter += 1

    # 每 batch_size 次进行一次合并，减少内存压力
    if counter % batch_size == 0:
        all_features = pd.concat(all_features_list, ignore_index=True)
        all_labels = pd.concat(all_labels_list, ignore_index=True)
        all_features_list = []
        all_labels_list = []
        print(f"Processed {counter} files.")
        
# 最后一批资料进行合并
if counter % batch_size != 0:
    all_features = pd.concat(all_features_list, ignore_index=True)
    all_labels = pd.concat(all_labels_list, ignore_index=True)
    
# 使用 H2O.ai 进行自动化模型选择
# 初始化 H2O
h2o.init()
# 分割资料集
X_train, X_test, y_train, y_test = train_test_split(all_features, all_labels, test_size=0.2, random_state=42)

# 转换 Pandas DataFrame 为 H2O Frame
train = h2o.H2OFrame(pd.concat([X_train, y_train], axis=1))
test = h2o.H2OFrame(pd.concat([X_test, y_test], axis=1))

# 设置特征和标签
x = train.columns[:-1]
y = train.columns[-1]

# 训练 H2O AutoML 模型
aml = H2OAutoML(max_runtime_secs=3600, seed=42)
aml.train(x=x, y=y, training_frame=train)

# 获取最佳模型
best_model = aml.leader

# 保存模型到指定路径
model_path = h2o.save_model(model=aml.leader, path="models", force=True)
print(f"Model saved to: {model_path}")

# 预测并评估模型
pred = best_model.predict(test)
y_pred_h2o = h2o.as_list(pred['predict'], use_pandas=True)

mse_h2o = mean_squared_error(y_test, y_pred_h2o)
rmse_h2o = mse_h2o ** 0.5
mae_h2o = mean_absolute_error(y_test, y_pred_h2o)
r2_h2o = r2_score(y_test, y_pred_h2o)

print(f"H2O.ai Mean Squared Error: {mse_h2o}")
print(f"H2O.ai Root Mean Squared Error: {rmse_h2o}")
print(f"H2O.ai Mean Absolute Error: {mae_h2o}")
print(f"H2O.ai R^2 Score: {r2_h2o}")

# 可视化实现措施
metrics = {
    'H2O.ai Mean Squared Error': mse_h2o,
    'H2O.ai Root Mean Squared Error': rmse_h2o,
    'H2O.ai Mean Absolute Error': mae_h2o,
    'H2O.ai R^2 Score': r2_h2o
}

# 使用 Seaborn 和 Matplotlib 绘制指标柱状图
plt.figure(figsize=(14, 8))
sns.barplot(x=list(metrics.keys()), y=list(metrics.values()))
plt.title('Model Performance Metrics')
plt.xlabel('Metrics')
plt.ylabel('Values')
plt.xticks(rotation=45)
plt.show()

# 显示预测值和真实值的散点图
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_h2o, alpha=0.3, label='H2O.ai Predictions')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.title('True vs Predicted Values')
plt.xlabel('True Values')
plt.ylabel('Predicted Values')
plt.legend()
plt.show()

# 印出模型排行榜
lb = aml.leaderboard
print(lb)

# 印出所有行数
# lb.head(rows = lb.nrows)

# 顯示最佳模型資訊
print(aml.leader)

# 顯示最佳模型的詳細資訊
print(aml.leader.metalearner)

# 取得最佳模型的model_id，也就是模型資料中的 Model Key
metalearner = h2o.get_model(aml.leader.metalearner()['name'])

# 視覺化: 最佳模型底下的各種演算法模型的標準化係數比較
metalearner.std_coef_plot()

# 拿最佳模型預測測試集資料
preds = aml.leader.predict(test)
print(preds)

# 評估最佳模型的性能表現
score = aml.leader.model_performance(test)
print(score)

# 重新加载模型并进行预测
loaded_model = h2o.load_model(model_path)
preds_loaded_model = loaded_model.predict(test)
print(preds_loaded_model)

# 關閉 H2O
h2o.shutdown()
