from flask import Flask, request, jsonify
from flask_cors import CORS  # Import thư viện CORS
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV


app = Flask(__name__)
CORS(app, resources={r"/predict_weather": {"origins": "http://127.0.0.1:5500"}})
weather_df = pd.read_csv('data/internal/processed/weather_processed.csv')

weather_df = weather_df.drop("Country", axis='columns')
weather_df = weather_df.drop("Name", axis='columns')

# Thay đổi nhãn của các loại thời tiết không thuộc Clear hoặc Clouds thành 'Thời tiết xấu'
weather_df['Weather'] = weather_df['Weather'].replace(['Haze', 'Mist', 'Snow', 'Thunderstorm', 'Rain', 'Drizzle', 'Fog', 'Smoke'], 'Poor weather')

# Lấy các feature và nhãn đã chỉnh sửa
features = weather_df[['Temp', 'Humidity', 'Visibility', 'Wind speed', 'Clouds']]
labels = weather_df['Weather']
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=80)

param_dist = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None],
    'min_samples_split': [2],
    'min_samples_leaf': [1],
    'class_weight': [None]
}

rf_model = RandomForestClassifier(random_state=44)
random_search = RandomizedSearchCV(rf_model, param_distributions=param_dist, n_iter=10, cv=5, scoring='accuracy', random_state=44)
random_search.fit(X_train, y_train)

# Chọn ra mô hình tốt nhất
best_rf_model = random_search.best_estimator_


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
        
        prediction = best_rf_model.predict(user_input)
        predicted_weather = prediction[0]

        if tempValue is None or humidityValue is None or visibilityValue is None or windspeedValue is None or cloudsValue is None:
            return jsonify({'error': 'Không thể xử lý giá trị'}), 500



        return jsonify({'predicted_weather': predicted_weather})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

app.config['DEBUG'] = True

if __name__ == '__main__':
    app.run(debug=True)