
import cv2 
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import thư viện CORS
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from sklearn.ensemble import RandomForestClassifier


app = Flask(__name__)
CORS(app, resources={r"/predict_weather": {"origins": "http://127.0.0.1:5500"}})
weather_df = pd.read_csv('./data/internal/weather.csv')

weather_df = weather_df.drop("Country", axis='columns')
weather_df = weather_df.drop("Name", axis='columns')

# Thay đổi nhãn của các loại thời tiết không thuộc Clear hoặc Clouds thành 'Thời tiết xấu'
weather_df['Weather'] = weather_df['Weather'].replace(['Haze', 'Mist', 'Snow', 'Thunderstorm', 'Rain', 'Drizzle', 'Fog', 'Smoke'], 'Poor weather')

# Lấy các feature và nhãn đã chỉnh sửa
features = weather_df[['Temp', 'Humidity', 'Visibility', 'Wind speed', 'Clouds']]
labels = weather_df['Weather']
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Tạo mô hình Random Forest và huấn luyện nó
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)  # Số cây quyết định = 100
rf_model.fit(X_train, y_train)


@app.route('/predict_weather', methods=['POST'])
def handle_image():
    try:
        tempValue = request.json['tempValue']
        humidityValue = request.json['humidityValue']
        visibilityValue = request.json['visibilityValue']
        windspeedValue = request.json['windspeedValue']
        cloudsValue = request.json['cloudsValue']
        
        print(tempValue,humidityValue,visibilityValue,windspeedValue,cloudsValue)
        
        user_input = pd.DataFrame({
            'Temp': [float(tempValue)],
            'Humidity': [int(humidityValue)],
            'Visibility': [int(visibilityValue)],
            'Wind speed': [float(windspeedValue)],
            'Clouds': [int(cloudsValue)]
        })
        
        prediction = rf_model.predict(user_input)
        predicted_weather = prediction[0]

        if tempValue is None or humidityValue is None or visibilityValue is None or windspeedValue is None or cloudsValue is None:
            return jsonify({'error': 'Không thể xử lý giá trị'}), 500



        return jsonify({'predicted_weather': predicted_weather})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

app.config['DEBUG'] = True

if __name__ == '__main__':
    app.run(debug=True)