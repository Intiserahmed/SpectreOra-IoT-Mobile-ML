import http.client
import json

conn = http.client.HTTPSConnection("nwaxhrmexpccjbphkjte.supabase.co")

headersList = {
 "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53YXhocm1leHBjY2picGhranRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODI1MTI4OTUsImV4cCI6MTk5ODA4ODg5NX0.c1BU9hMESWuTxTRcEm7hcpS3gqTpvAMb1byd5DymZZE",
 "Content-Type": "application/json" 
}

payload = json.dumps({
  "values": [11100, 15000, 20110]
}
)

conn.request("POST", "/rest/v1/ecg", payload, headersList)
response = conn.getresponse()
result = response.read()

print(result.decode("utf-8"))