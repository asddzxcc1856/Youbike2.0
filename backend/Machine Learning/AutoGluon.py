import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from autogluon.tabular import TabularPredictor

# 初始化資料集列表
all_features_list = []
all_labels_list = []

batch_size = 1000
counter = 0

# 遍歷所有 CSV 文件
for i in range(500101001, 500119092):
    file_path = f'rentbike/{i}.csv'
    if not os.path.exists(file_path):
        continue

    # 讀取數據
    df = pd.read_csv(file_path)

    # 選擇初始特徵
    df = df[['sno', 'total', 'latitude', 'longitude', 'act', 'srcUpdateTime', 'available_rent_bikes']]

    # 轉換 srcUpdateTime 為 datetime
    df['srcUpdateTime'] = pd.to_datetime(df['srcUpdateTime'])

    # 提取時間特徵
    df['hour'] = df['srcUpdateTime'].dt.hour
    df['minute'] = df['srcUpdateTime'].dt.minute
    df['second'] = df['srcUpdateTime'].dt.second
    df['weekday'] = df['srcUpdateTime'].dt.weekday  # 週几

    # 擴展後的特徵集
    features = df[['sno', 'total', 'latitude', 'longitude', 'act', 'hour', 'minute', 'second', 'weekday']]
    labels = df['available_rent_bikes']  # 預測 available_rent_bikes

    all_features_list.append(features)
    all_labels_list.append(labels)
    counter += 1

    # 每 batch_size 次進行一次合併，減少內存壓力
    if counter % batch_size == 0:
        all_features = pd.concat(all_features_list, ignore_index=True)
        all_labels = pd.concat(all_labels_list, ignore_index=True)
        all_features_list = []
        all_labels_list = []
        print(f"Processed {counter} files.")

# 最後一批資料進行合併
if counter % batch_size != 0:
    all_features = pd.concat(all_features_list, ignore_index=True)
    all_labels = pd.concat(all_labels_list, ignore_index=True)

# 分割資料集
X_train, X_test, y_train, y_test = train_test_split(all_features, all_labels, test_size=0.2, random_state=42)

# 構建訓練資料和測試資料 DataFrame
train_data = pd.concat([X_train, y_train], axis=1)
train_data.columns = list(X_train.columns) + ['available_rent_bikes']
test_data = pd.concat([X_test, y_test], axis=1)
test_data.columns = list(X_test.columns) + ['available_rent_bikes']




# 自動化模型選擇和訓練
predictor = TabularPredictor(label='available_rent_bikes', problem_type="regression" , eval_metric='mean_squared_error',log_file_path="./Autogluon_AutoML_log/Autogluon_AutoML_log.txt",log_to_file=True).fit(
    train_data,
    verbosity=5
)

# 保存最佳模型
model_dir = 'best_model'
predictor.save(model_dir)

# 重新載入模型
loaded_predictor = TabularPredictor.load(model_dir)

# 預測並評估模型
y_pred = loaded_predictor.predict(X_test)
mse_ag = mean_squared_error(y_test, y_pred)
rmse_ag = mse_ag ** 0.5
mae_ag = mean_absolute_error(y_test, y_pred)
r2_ag = r2_score(y_test, y_pred)

print(f"AutoGluon Mean Squared Error: {mse_ag}")
print(f"AutoGluon Root Mean Squared Error: {rmse_ag}")
print(f"AutoGluon Mean Absolute Error: {mae_ag}")
print(f"AutoGluon R^2 Score: {r2_ag}")

# 可視化結果
metrics = {
    'AutoGluon Mean Squared Error': mse_ag,
    'AutoGluon Root Mean Squared Error': rmse_ag,
    'AutoGluon Mean Absolute Error': mae_ag,
    'AutoGluon R^2 Score': r2_ag
}

plt.figure(figsize=(14, 8))
sns.barplot(x=list(metrics.keys()), y=list(metrics.values()))
plt.title('Model Performance Metrics')
plt.xlabel('Metrics')
plt.ylabel('Values')
plt.xticks(rotation=45)
plt.savefig('model_performance_metrics.png')
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.3, label='AutoGluon Predictions')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.title('True vs Predicted Values')
plt.xlabel('True Values')
plt.ylabel('Predicted Values')
plt.legend()
plt.savefig('true_vs_predicted_values.png')
plt.show()

# 展示所有試驗過的模型的優劣評分表
leaderboard = predictor.leaderboard(test_data, silent=True)
print(leaderboard)

# 顯示更多模型特性指標和圖表
feature_importance = predictor.feature_importance(test_data)
print(feature_importance)