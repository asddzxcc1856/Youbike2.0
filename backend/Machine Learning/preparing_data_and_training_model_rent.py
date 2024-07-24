#################################################
#                   準備資料                     #
#################################################
import pandas as pd

for i in range(500101001,500119092):
    # 讀取數據
    try:
        df = pd.read_csv(f'rentbike/{i}.csv')
    except:
        continue

    # 選取初始特徵
    df = df[['sno', 'total', 'latitude', 'longitude', 'act', 'srcUpdateTime','available_rent_bikes']]

    # 轉換 infoTime 為 datetime
    df['srcUpdateTime'] = pd.to_datetime(df['srcUpdateTime'])

    # 提取時間特徵
    df['hour'] = df['srcUpdateTime'].dt.hour
    df['minute'] = df['srcUpdateTime'].dt.minute
    df['second'] = df['srcUpdateTime'].dt.second

    # 擴展後的特徵集
    features = df[['sno','total', 'latitude', 'longitude', 'act' ,'hour' , 'minute', 'second']]
    labels = df['available_rent_bikes']  # 預測 available_rent_bikes

    # 分割資料集
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    #################################################
    #                   訓練模型 GBM                 #
    #################################################
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.metrics import mean_squared_error
    import joblib

    # 建立GBM模型
    gbm_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    gbm_model.fit(X_train, y_train)

    # 預測
    y_pred_gbm = gbm_model.predict(X_test)

    # 評估模型
    mse_gbm = mean_squared_error(y_test, y_pred_gbm)
    print(f"GBM Mean Squared Error: {mse_gbm}")

    # 儲存GBM模型
    gbm_model_filename = f'rent_bike_weight_for_each_station/rent_bike_{i}_gbm_model.pkl'
    joblib.dump(gbm_model, gbm_model_filename)

    #################################################
    #                   訓練模型 XGBoost             #
    #################################################

    import xgboost as xgb
    from sklearn.metrics import mean_squared_error
    import joblib

    # 建立XGBoost模型
    xgb_model = xgb.XGBRegressor(n_estimators=100, random_state=42)
    xgb_model.fit(X_train, y_train)

    # 預測
    y_pred_xgb = xgb_model.predict(X_test)

    # 評估模型
    mse_xgb = mean_squared_error(y_test, y_pred_xgb)
    print(f"XGBoost Mean Squared Error: {mse_xgb}")

    # 儲存XGBoost模型
    xgb_model_filename = f'rent_bike_weight_for_each_station/rent_bike_{i}_xgb_model.pkl'
    joblib.dump(xgb_model, xgb_model_filename)
