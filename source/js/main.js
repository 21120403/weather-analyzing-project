
var inputBtn = document.querySelector(".input__btn")
var tempElement = document.getElementById("temp")
var humidityElement = document.getElementById("humidity")
var visibilityElement = document.getElementById("visibility")
var windspeedElement = document.getElementById("winspeed")
var cloudsElement = document.getElementById("clouds")
var outputHeading = document.querySelector(".output__heading")

inputBtn.onclick = function() {
  if (tempElement.value == '' || humidityElement.value == '' || visibilityElement.value == '' || windspeedElement.value == ''|| cloudsElement.value == ''){
    alert("Please enter full of value!!")
  }
  else{
    sendToBackend(tempElement.value, humidityElement.value, visibilityElement.value,windspeedElement.value, cloudsElement.value)
  }
  
}


  
  function sendToBackend(tempValue, humidityValue, visibilityValue,windspeedValue,cloudsValue) {
    // Gửi dữ liệu hình ảnh imageData tới backend sử dụng fetch API
    fetch('http://127.0.0.1:5000/predict_weather', {
      method: 'POST',
      body: JSON.stringify({ tempValue: tempValue , humidityValue :  humidityValue, visibilityValue :visibilityValue, windspeedValue: windspeedValue,cloudsValue:cloudsValue }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      // Nhận hình ảnh từ server ở đây
      console.log('Kết quả xử lý từ backend:', data);

      
      if (data.predicted_weather == "Clear"){
        outputHeading.innerText = "Current weather is so beautiful. You should have a date with your girlfriend <3"
        outputHeading.style.color = "green"
      }
      else if(data.predicted_weather == "Clouds"){
        outputHeading.innerText = "Current weather is too cloudy. You should bring your umbrella to cover your girlfriend <3"
        outputHeading.style.color = "#0f70e6"
      }
      else{
        outputHeading.innerText = "Current weather is so bad. You shouldn't have a date now. :(("
        outputHeading.style.color = "red"
      }

    })
    .catch(error => console.error('Lỗi:', error));
  }