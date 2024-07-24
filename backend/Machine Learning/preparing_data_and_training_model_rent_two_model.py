import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import joblib

# 初始化資料集列表
all_features_list = []
all_labels_list = []

batch_size = 1000
counter = 0

# 遍歷所有 CSV 檔案
for i in range(500101001, 500119092):
    file_path = f'rentbike/{i}.csv'
    if not os.path.exists(file_path):
        continue
    
    # 讀取數據
    df = pd.read_csv(file_path)
    
    # 選取初始特徵
    df = df[['sno', 'total', 'latitude', 'longitude', 'act', 'srcUpdateTime', 'available_rent_bikes']]

    # 轉換 infoTime 為 datetime
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

# 分割資料集
X_train, X_test, y_train, y_test = train_test_split(all_features, all_labels, test_size=0.2, random_state=42)

# 訓練和評估 GBM 模型
gbm_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
gbm_model.fit(X_train, y_train)
y_pred_gbm = gbm_model.predict(X_test)

mse_gbm = mean_squared_error(y_test, y_pred_gbm)
rmse_gbm = mse_gbm ** 0.5
mae_gbm = mean_absolute_error(y_test, y_pred_gbm)
r2_gbm = r2_score(y_test, y_pred_gbm)

print(f"GBM Mean Squared Error: {mse_gbm}")
print(f"GBM Root Mean Squared Error: {rmse_gbm}")
print(f"GBM Mean Absolute Error: {mae_gbm}")
print(f"GBM R^2 Score: {r2_gbm}")

joblib.dump(gbm_model, 'rent_bike_gbm_model.pkl')

# 訓練和評估 XGBoost 模型
xgb_model = xgb.XGBRegressor(n_estimators=100, random_state=42)
xgb_model.fit(X_train, y_train)
y_pred_xgb = xgb_model.predict(X_test)

mse_xgb = mean_squared_error(y_test, y_pred_xgb)
rmse_xgb = mse_xgb ** 0.5
mae_xgb = mean_absolute_error(y_test, y_pred_xgb)
r2_xgb = r2_score(y_test, y_pred_xgb)

print(f"XGBoost Mean Squared Error: {mse_xgb}")
print(f"XGBoost Root Mean Squared Error: {rmse_xgb}")
print(f"XGBoost Mean Absolute Error: {mae_xgb}")
print(f"XGBoost R^2 Score: {r2_xgb}")

joblib.dump(xgb_model, 'rent_bike_xgb_model.pkl')
