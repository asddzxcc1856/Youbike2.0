from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import math
import warnings
import time as ti
import requests

GOOGLE_MAPS_API_KEY = 'AIzaSyCbNK-66CA8By6GQ6qC0bG5p_u-Wm8V1h0'  # 替換為你的 Google Maps API 金鑰
    
warnings.simplefilter('ignore')

app = Flask(__name__)
CORS(app)  # 啟用CORS

# 載入模型
model = joblib.load('random_forest_model.pkl')

@app.route('/calculate_distance', methods=['GET'])
def calculate_distance():
    user_lat = request.args.get('user_lat')
    user_lon = request.args.get('user_lon')
    station_lat = request.args.get('station_lat')
    station_lon = request.args.get('station_lon')

    if not user_lat or not user_lon or not station_lat or not station_lon:
        return jsonify({'error': 'Missing parameters'}), 400

    distance = get_distance(user_lat, user_lon, station_lat, station_lon)
    return jsonify({'distance': distance})

def get_distance(user_lat, user_lon, station_lat, station_lon):
    endpoint = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    params = {
        'origins': f'{user_lat},{user_lon}',
        'destinations': f'{station_lat},{station_lon}',
        'key': GOOGLE_MAPS_API_KEY,
        'units': 'metric'
    }

    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        result = response.json()
        if result['rows'][0]['elements'][0]['status'] == 'OK':
            distance = result['rows'][0]['elements'][0]['distance']['value'] / 1000  # 轉換為公里
            return distance
        else:
            return None
    else:
        return None

@app.route('/api/recommend', methods=['POST'])
def recommend():
    s = ti.time()
    data = request.json
    date = data.get('date')
    time = data.get('time')
    user_location = data.get('location')
    user_latitude = user_location.get('lat')
    user_longitude = user_location.get('lng')

    #if(query 查詢過):
    # print("服務時間 : ",e - s)
    #
    # return
    # 讀取數據
    df = pd.read_csv('youbike_data.csv')

    # 選取初始特徵
    selected_features = df[['sno', 'sna', 'total', 'available_rent_bikes', 'latitude', 'longitude', 'infoTime']]

    # 轉換 infoTime 為 datetime
    selected_features['infoTime'] = pd.to_datetime(selected_features['infoTime'])

    # 提取時間特徵
    future_time = pd.to_datetime(f'{date} {time}')
    future_hour = future_time.hour
    future_minute = future_time.minute
    future_second = future_time.second

    # 計算用戶位置與每個站點的距離
    selected_features['distance_to_user'] = selected_features.apply(lambda row: get_distance(user_longitude, user_latitude, row['longitude'], row['latitude']), axis=1)

    # 構建預測資料
    future_features = pd.DataFrame({
        'sno': selected_features['sno'],
        'total': selected_features['total'],
        'latitude': selected_features['latitude'],
        'longitude': selected_features['longitude'],
        'act': selected_features['act'],
        'hour': future_hour,
        'minute': future_minute,
        'second': future_second,
    })

    # 預測未來車輛數量
    future_predictions = model.predict(future_features)

    # 將預測結果加入原始數據
    selected_features['predicted_available_bikes'] = future_predictions

    # 過濾有剩餘車輛的站點
    selected_features_with_bikes = selected_features[selected_features['predicted_available_bikes'] > 0]

    # 按照距離排序，推薦最近的站點
    recommended_station = selected_features_with_bikes.sort_values(by='distance_to_user').iloc[0]

    result = {
        "location": {
            "lat": recommended_station['latitude'],
            "lng": recommended_station['longitude']
        },
        "station": recommended_station['sna'],
        "distance": recommended_station['distance_to_user'],
        "predicted_available_bikes": int(recommended_station['predicted_available_bikes'])
    }
    e = ti.time()
    print("服務時間 : ",e - s)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
