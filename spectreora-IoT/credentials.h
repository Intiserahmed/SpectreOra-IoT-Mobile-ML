// credentials.h

#pragma once

const char *ssid = "";
const char *password = "";

const char *supabase_host = "";
const int supabase_port = 443;
const char *supabase_api_key = "";
const char *supabase_table_name = "";
const String supabase_url = String("/rest/v1/") + supabase_table_name;