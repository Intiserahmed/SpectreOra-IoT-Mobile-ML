#include <iostream>
#include <vector>
#include <random>
#include <cpr/cpr.h>
#include <nlohmann/json.hpp>


const std::string SUPABASE_URL = "https://your-supabase-instance.supabase.co/rest/v1";
const std::string SUPABASE_API_KEY = "your-supabase-api-key";

bool send_ecg_data_to_supabase(const std::vector<int>& ecg_values) {
    // Create a JSON array with the ECG data
    nlohmann::json data = nlohmann::json::array();
    for (const auto& ecg_value : ecg_values) {
        nlohmann::json item;
        item["ecg_value"] = ecg_value;
        data.push_back(item);
    }

    // Send the ECG data to Supabase using an HTTP POST request
    cpr::Response response = cpr::Post(
        cpr::Url{SUPABASE_URL + "/your-table-name"},
        cpr::Header{
            {"apikey", SUPABASE_API_KEY},
            {"Content-Type", "application/json"},
            {"Prefer", "return=representation"}
        },
        cpr::Body{data.dump()}
    );

    // Check if the request was successful
    if (response.status_code == 201) {
        std::cout << "ECG data sent to Supabase successfully" << std::endl;
        return true;
    } else {
        std::cerr << "Failed to send ECG data to Supabase: " << response.text << std::endl;
        return false;
    }
}

int main() {
    // Generate a vector of 10 random integers as dummy ECG values
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(10000, 20000);

    std::vector<int> ecg_values;
    for (int i = 0; i < 10; ++i) {
        ecg_values.push_back(dist(gen));
    }

    send_ecg_data_to_supabase(ecg_values);

    return 0;
}
