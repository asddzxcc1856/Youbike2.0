from flask import *
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import math
import warnings
import time as ti
import requests
import googlemaps
from datetime import datetime
import heapq
from flask_mail import Mail, Message

GOOGLE_MAPS_API_KEY = 'AIzaSyAfsiY7aSUyaoBF5JPN6IY-_f_LxwaLH9k'
warnings.simplefilter('ignore')

app = Flask(__name__)
CORS(app)  # 啟用CORS

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 't7878780@gmail.com'
app.config['MAIL_PASSWORD'] = 'bfkhwvzwdpnamkmj'
app.config['MAIL_DEFAULT_SENDER'] = 't7878780@gmail.com'

mail = Mail(app)

model = joblib.load('rent_bike_tpot_model.pkl')

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

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    r = 6371.0

    distance = c * r
    return distance
    

def get_distance(user_lat, user_lon, station_lat, station_lon):
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    
    distances_h = []
    minheap = []
    for num1, num2 in zip(station_lon, station_lat):
        result = haversine(user_lon, user_lat, num1, num2)
        distances_h.append(result)
        heapq.heappush(minheap, (result, num1, num2))
    
    distances = heapq.nsmallest(3,minheap)

    
    result = []
    for dist, lon, lat in distances:
        matrix = gmaps.distance_matrix((user_lat, user_lon), (lat, lon), mode='walking', units='metric')
        distance_text = matrix['rows'][0]['elements'][0]['distance']['text']
        distance_val = float(distance_text.replace(",", "").split(' ')[0])
        result.append({
            'distance_km': distance_val,
            'station_lat': lat,
            'station_lon': lon
        })

    result_json = json.dumps(result, indent=4)
    
    return distances_h,result_json
    

@app.route('/api/recommend', methods=['POST'])
def recommend():
    s = ti.time()
    data = request.json
    search_type = data.get("search_type")

    # 讀取數據
    df = pd.read_csv('youbike_data.csv')

    # 選取初始特徵
    selected_features = df[['sno','sna', 'total', 'latitude','longitude','act','infoTime']]

    # 轉換 infoTime 為 datetime
    selected_features['infoTime'] = pd.to_datetime(selected_features['infoTime'])

    if search_type == "1" or search_type == "2":
        bor_date = data.get('borrow_date')
        bor_time = data.get('borrow_time')
        bor_location = data.get("borrowLocation")
        bor_latitude = bor_location.get('lat')
        bor_longitude = bor_location.get('lng')
        # 提取時間特徵
        borrow_future_time = pd.to_datetime(f'{bor_date} {bor_time}')
        borrow_future_hour = borrow_future_time.hour
        borrow_future_minute = borrow_future_time.minute
        borrow_future_second = borrow_future_time.second
        borrow_future_weekend = borrow_future_time.weekday()
        
        # 計算用戶位置與每個站點的距離
        selected_features['distance_to_borrow'],distance_to_borrow = get_distance(bor_latitude, bor_longitude,selected_features['latitude'], selected_features['longitude'])
        
        # 構建預測資料
        borrow_future_features = pd.DataFrame({
                'sno': selected_features['sno'],
                'total': selected_features['total'],
                'latitude': selected_features['latitude'],
                'longitude': selected_features['longitude'],
                'act': selected_features['act'],
                'hour': borrow_future_hour,
                'minute': borrow_future_minute,
                'second': borrow_future_second,
                'weekday': borrow_future_weekend
            })
        # 預測未來車輛數量
        borrow_future_predictions = model.predict(borrow_future_features) 
        # 將預測結果加入原始數據
        selected_features['predicted_available_bikes'] = borrow_future_predictions 
        # 過濾有剩餘車輛的站點
        selected_features_with_bikes = selected_features[selected_features['predicted_available_bikes'] > 0] 
        # 按照距離排序，推薦最近的站點
        borrow_recommended_station = selected_features_with_bikes.sort_values(by='distance_to_borrow').iloc[0]
        print(borrow_recommended_station)
    if search_type == "1" or search_type == "3":
        ret_date = data.get("return_date")
        ret_time = data.get("return_time")
        ret_location = data.get('returnLocation')
        ret_latitude = ret_location.get('lat')
        ret_longitude = ret_location.get('lng')
        # 提取時間特徵
        return_future_time = pd.to_datetime(f'{ret_date} {ret_time}')
        return_future_hour = return_future_time.hour
        return_future_minute = return_future_time.minute
        return_future_second = return_future_time.second
        return_future_weekend = return_future_time.weekday()

        # 計算用戶位置與每個站點的距離
        selected_features['distance_to_return'],distance_to_return = get_distance(ret_latitude, ret_longitude,selected_features['latitude'], selected_features['longitude'])
        
        # 構建預測資料
        return_future_features = pd.DataFrame({
            'sno': selected_features['sno'],
            'total': selected_features['total'],
            'latitude': selected_features['latitude'],
            'longitude': selected_features['longitude'],
            'act': selected_features['act'],
            'hour': return_future_hour,
            'minute': return_future_minute,
            'second': return_future_second,
            'weekday': return_future_weekend
        })
        # 預測未來車輛數量
        return_future_predictions = model.predict(return_future_features)
        # 將預測結果加入原始數據
        selected_features['predicted_available_return'] = [a - b for a, b in zip(selected_features['total'], return_future_predictions)]
        # 過濾有剩餘車輛的站點
        selected_features_with_return = selected_features[selected_features['predicted_available_return'] > 0]
        # 按照距離排序，推薦最近的站點
        return_recommended_station = selected_features_with_return.sort_values(by='distance_to_return').iloc[0]
        print(return_recommended_station)
    if search_type == "1":
        result = [{
            "location": {
                "lat": borrow_recommended_station['latitude'],
                "lng": borrow_recommended_station['longitude']
                },
            "station": selected_features[
        (selected_features['latitude'] == borrow_recommended_station['latitude']) &
        (selected_features['longitude'] == borrow_recommended_station['longitude'])]['sna'].iloc[0],
            "distance": borrow_recommended_station['distance_to_borrow'],
            "predicted_available_bikes": int(borrow_recommended_station['predicted_available_bikes'])
            }, 
            {"location": {
                "lat": return_recommended_station['latitude'],
                "lng": return_recommended_station['longitude']
                },
            "station": selected_features[
        (selected_features['latitude'] == return_recommended_station['latitude']) &
        (selected_features['longitude'] == return_recommended_station['longitude'])]['sna'].iloc[0],
            "distance": return_recommended_station['distance_to_return'],
            "predicted_available_return": int(return_recommended_station["total"])-int(return_recommended_station['predicted_available_bikes'])
            }]
    elif search_type == "2":
        result = [{
            "location": {
                "lat": borrow_recommended_station['latitude'],
                "lng": borrow_recommended_station['longitude']
                },
            "station": selected_features[
        (selected_features['latitude'] == borrow_recommended_station['latitude']) &
        (selected_features['longitude'] == borrow_recommended_station['longitude'])]['sna'].iloc[0],
            "distance": borrow_recommended_station['distance_to_borrow'],
            "predicted_available_bikes": int(borrow_recommended_station['predicted_available_bikes'])
            }]
    elif search_type == "3":
        result = [{
            "location": {
                "lat": return_recommended_station['latitude'],
                "lng": return_recommended_station['longitude']
                },
            "station": selected_features[
        (selected_features['latitude'] == return_recommended_station['latitude']) &
        (selected_features['longitude'] == return_recommended_station['longitude'])]['sna'].iloc[0],
            "distance": return_recommended_station['distance_to_return'],
            "predicted_available_return": int(return_recommended_station['predicted_available_return'])
            }]
    
    e = ti.time()
    print("服務時間 : ",e - s)
    return jsonify(result), 200

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    # 設計漂亮的 HTML 電子郵件內容
    html_content = f"""
    <html>
    <body>
        <h2>Youbike2.0推薦及預測系統的聯絡表單 來自 {name} 的信件</h2>
        <p><strong>姓名:</strong> {name}</p>
        <p><strong>電子郵件:</strong> {email}</p>
        <p><strong>訊息:</strong></p>
        <blockquote style="border-left: 2px solid #007bff; padding-left: 10px; margin: 10px 0;">
            {message}
        </blockquote>
        <p>感謝您的聯繫！我們會儘快回覆您。</p>
    </body>
    </html>
    """

    msg = Message(
        subject=f"聯絡表單來自 {name}",
        recipients=['t7878780@gmail.com'],
        html=html_content  # 使用 HTML 格式的內容
    )
    
    try:
        mail.send(msg)
        return jsonify({'message': '郵件已發送！'}), 200
    except Exception as e:
        return jsonify({'message': '郵件發送失敗。', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)