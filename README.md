# SpectreOra

> This project is an IoT-based ECG prediction application that uses a Raspberry Pi Pico connected to an AD8232 sensor to send ECG data to the cloud. A pre-trained machine learning model hosted on Heroku predicts the results, and a FastAPI RESTful API writes the predictions back to the Supabase database. A Flutter mobile app fetches the predictions and displays them to the end users.

## 🚀 Architecture
![SpectreOra Arch Screenshot](./Architecture.png)

1. **IoT Device >> Database (Supabase)**: The IoT device sends ECG data to the Supabase database using HTTP requests through C++ or Micropython. The data is encrypted with AES-256 and stored on Supabase's highly secure cloud infrastructure.
2. **Database (Supabase) >> FastAPI RESTful API:**: The FastAPI RESTful API retrieves the ECG data from the Supabase database using SQL queries or Supabase SDK. The API passes the data to the pre-trained machine learning model hosted on Heroku, typically using JSON format.
3. **Pre-trained Machine Learning Model on Heroku >> FastAPI RESTful API:**:The machine learning model processes the ECG data and generates prediction results using advanced neural networks and deep learning techniques. The results are sent back to the FastAPI RESTful API in JSON format.
4. **Database (Supabase) >> Flutter Mobile App:**: The FastAPI RESTful API writes the prediction results back to the Supabase database for storage, which are then securely accessed by the Flutter mobile app.
5. **Flutter Mobile App**: The Flutter mobile app provides a sleek and intuitive user interface for viewing ECG data and prediction results in real-time. Using Supabase subscriptions and advanced reactive programming techniques, the app updates its display automatically as new data becomes available.

## 🛠️ Setup and Installation

### IoT Device

1. Set up the Raspberry Pi Pico with Micropython firmware.
2. Connect the AD8232 sensor to the Raspberry Pi Pico following the manufacturer's guidelines.
3. Write a Micropython script to read ECG data from the AD8232 sensor and send it to the Supabase database using secure HTTP requests.

### Database

1. Set up a Supabase database with built-in security features, such as encrypted data storage, access control, and audit logs.
2. Configure the appropriate access rules and API keys for secure data transmission.

### Machine Learning Model

1. Train and export the ECG prediction machine learning model using cutting-edge deep learning libraries, such as TensorFlow or PyTorch.
2. Host the pre-trained model on Heroku or another cloud platform that supports containerized deployments.

### FastAPI RESTful API

1. Create a FastAPI app with endpoints to fetch ECG data from the database, make predictions using the pre-trained model, and write predictions back to the database.
2. Secure the API with TLS/SSL encryption, JWT authentication, and rate limiting to prevent unauthorized access and attacks.

### Flutter Mobile App

1. Develop a Flutter mobile app with a modern and responsive user interface that integrates with the Supabase database and FastAPI RESTful API.
2. Implement advanced reactive programming patterns, such as the BLoC architecture or Provider pattern, to enable real-time data updates and smooth user experience.

## 💻 Usage

1. Power on the IoT device (Raspberry Pi Pico + AD8232 sensor) and ensure it's connected to the internet.
2. The IoT device will send encrypted ECG data to the Supabase database over a secure HTTPS connection.
3. The FastAPI RESTful API will read the ECG data, make predictions using the pre-trained machine learning model, and write the predictions back to the Supabase database, which are securely stored using advanced encryption algorithms.
4. The Flutter mobile app will fetch the latest ECG data and prediction results from the Supabase database in real-time and display them to the end users using a modern and sleek user interface.

## 📝 License

This project is licensed under the [MIT License](LICENSE).