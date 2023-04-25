#include <WiFi.h>
#include <ArduinoHttpClient.h>
#include <ArduinoJson.h>



WiFiClient wifiClient;
HttpClient httpClient = HttpClient(wifiClient, "https://" + String(supabase_host), supabase_port);

void setup()
{
    Serial.begin(115200);

    // Operate in WiFi Station mode
    WiFi.mode(WIFI_STA);

    // Start WiFi with supplied parameters
    WiFi.begin(ssid, password);

    // Print periods on monitor while establishing connection
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
        delay(500);
    }

    // Connection established
    Serial.println("");
    Serial.print("Pico W is connected to WiFi network ");
    Serial.println(WiFi.SSID());
    Serial.print("Assigned IP Address: ");
    Serial.println(WiFi.localIP());
}

void loop()
{
    // Generate dummy ECG data
    int ecg_values[] = {random(10000, 20000), random(10000, 20000), random(10000, 20000)};

    // Create a JSON object to store the ECG data
    StaticJsonDocument<64> jsonDocument;
    JsonArray values = jsonDocument.createNestedArray("values");
    values.add(ecg_values[0]);
    values.add(ecg_values[1]);
    values.add(ecg_values[2]);

    String requestBody;
    serializeJson(jsonDocument, requestBody);

    // Send the ECG data to Supabase using an HTTP POST request
    httpClient.beginRequest();
    httpClient.post(supabase_url);
    httpClient.sendHeader("apikey", supabase_api_key);
    httpClient.sendHeader("Content-Type", "application/json");
    httpClient.sendHeader("Prefer", "return=representation");
    httpClient.sendHeader("Content-Length", requestBody.length());
    httpClient.beginBody();
    httpClient.print(requestBody);
    httpClient.endRequest();

    // Check if the request was successful
    int statusCode = httpClient.responseStatusCode();
    String response = httpClient.responseBody();

    if (statusCode == 201)
    {
        Serial.println("ECG data sent to Supabase successfully");
    }
    else
    {
        Serial.print("Failed to send ECG data to Supabase: ");

        Serial.println(statusCode);
        Serial.println("Response: " + response);
    }

    // Wait for 5 seconds before sending the next ECG value
    delay(5000);
}
