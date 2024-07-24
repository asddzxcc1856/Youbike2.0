import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
from tpot import TPOTRegressor
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# 初始化資料集列表
all_features_list = []
all_labels_list = []

batch_size = 1000
counter = 0

# 設置日誌
logging.basicConfig(filename='tpot_progress.log', level=logging.INFO)

# 遍歷所有 CSV 檔案
for i in range(500101001, 500119092):
    file_path = f'rentbike/{i}.csv'
    if not os.path.exists(file_path):
        continue
    
    # 讀取數據
    df = pd.read_csv(file_path)
    
    # 選取初始特徵
    df = df[['sno', 'total', 'latitude', 'longitude', 'act', 'srcUpdateTime', 'available_rent_bikes']]

    # 轉換 srcUpdateTime 為 datetime
    df['srcUpdateTime'] = pd.to_datetime(df['srcUpdateTime'])

    # 提取時間特徵
    df['hour'] = df['srcUpdateTime'].dt.hour
    df['minute'] = df['srcUpdateTime'].dt.minute
    df['second'] = df['srcUpdateTime'].dt.second
    df['weekday'] = df['srcUpdateTime'].dt.weekday  # 週幾

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
    print(f"Processed {counter} files.")

print("train_test_split Start...")
# 分割資料集
X_train, X_test, y_train, y_test = train_test_split(all_features, all_labels, test_size=0.2, random_state=42)
print("train_test_split Finished")

print("TPOTRegressor Start...")
# 使用TPOT進行自動化模型選擇
tpot = TPOTRegressor(verbosity=2, generations=5, population_size=20, random_state=42, periodic_checkpoint_folder='tpot_checkpoints')
tpot.fit(X_train, y_train)
print("TPOTRegressor Finished")

# 保存最佳模型
joblib.dump(tpot.fitted_pipeline_, 'rent_bike_tpot_model.pkl')

# 預測並評估模型
y_pred_tpot = tpot.predict(X_test)

mse_tpot = mean_squared_error(y_test, y_pred_tpot)
rmse_tpot = mse_tpot ** 0.5
mae_tpot = mean_absolute_error(y_test, y_pred_tpot)
r2_tpot = r2_score(y_test, y_pred_tpot)

print(f"TPOT Mean Squared Error: {mse_tpot}")
print(f"TPOT Root Mean Squared Error: {rmse_tpot}")
print(f"TPOT Mean Absolute Error: {mae_tpot}")
print(f"TPOT R^2 Score: {r2_tpot}")

# 可視化實現措施
metrics = {
    'Mean Squared Error': mse_tpot,
    'Root Mean Squared Error': rmse_tpot,
    'Mean Absolute Error': mae_tpot,
    'R^2 Score': r2_tpot
}

# 使用Seaborn和Matplotlib繪製指標柱狀圖
plt.figure(figsize=(10, 6))
sns.barplot(x=list(metrics.keys()), y=list(metrics.values()))
plt.title('Model Performance Metrics')
plt.xlabel('Metrics')
plt.ylabel('Values')
plt.show()

# 顯示預測值和真實值的散點圖
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_tpot, alpha=0.3)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.title('True vs Predicted Values')
plt.xlabel('True Values')
plt.ylabel('Predicted Values')
plt.show()

# 打印最佳模型的參數
print("\nBest Pipeline Steps:")
print(tpot.fitted_pipeline_)

# 打印最佳模型的詳細參數
best_model = tpot.fitted_pipeline_.steps[-1][1]
print("\nBest Model Parameters:")
print(best_model.get_params())

# 定義一個函數來記錄每一代的最佳模型和分數
def log_best_pipeline(pipeline, generation, metrics):
    logging.info(f"Generation {generation}")
    logging.info(f"Best Pipeline: {pipeline}")
    logging.info(f"Metrics: {metrics}")

# 在每一代之後記錄最佳管道和分數
for generation, pipeline in enumerate(tpot.evaluated_individuals_):
    metrics = tpot.evaluated_individuals_[pipeline]['internal_cv_score']
    log_best_pipeline(pipeline, generation, metrics)
