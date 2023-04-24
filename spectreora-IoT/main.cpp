#include <WiFiNINA.h>
#include <ArduinoHttpClient.h>
#include <ArduinoJson.h>

const char *ssid = "your_wifi_ssid";
const char *password = "your_wifi_password";

const char *supabase_host = "your-supabase-instance.supabase.co";
const int supabase_port = 80;
const char *supabase_api_key = "your-supabase-api-key";
const char *supabase_table_name = "your-table-name";

WiFiClient wifiClient;
HttpClient httpClient = HttpClient(wifiClient, supabase_host, supabase_port);

void setup()
{
    Serial.begin(9600);
    while (!Serial)
    {
        ; // Wait for serial connection
    }

    Serial.print("Connecting to Wi-Fi");
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    Serial.println("Connected to Wi-Fi");
}

void loop()
{
    // Generate dummy ECG data
    int ecg_value = random(10000, 20000);

    // Create a JSON object to store the ECG data
    StaticJsonDocument<64> jsonDocument;
    jsonDocument["ecg_value"] = ecg_value;
    String requestBody;
    serializeJson(jsonDocument, requestBody);

    // Send the ECG data to Supabase using an HTTP POST request
    httpClient.beginRequest();
    httpClient.post(String("/rest/v1/") + supabase_table_name);
    httpClient.sendHeader("apikey", supabase_api_key);
    httpClient.sendHeader("Content-Type", "application/json");
    httpClient.sendHeader("Prefer", "return=representation");
    httpClient.sendHeader("Content-Length", requestBody.length());
    httpClient.beginBody();
    httpClient.print(requestBody);
    httpClient.endRequest();

    // Check if the request was successful
    int statusCode = httpClient.responseStatusCode();
    if (statusCode == 201)
    {
        Serial.println("ECG data sent to Supabase successfully");
    }
    else
    {
        Serial.print("Failed to send ECG data to Supabase: ");
        Serial.println(statusCode);
    }

    // Wait for 5 seconds before sending the next ECG value
    delay(5000);
}
