import requests
import json
import os
import getpass

# Settings
server = "https://localhost:6443/arcgis"
username = "siteadmin"
password = getpass.getpass("Enter your siteadmin password: ")

# Paths
sd_file = r"C:\GISBootcamp\Assignments\firestations_map_service.sd"
sd_filename = os.path.basename(sd_file)

# 1️⃣ Get token
token_url = f"{server}/admin/generateToken"
token_params = {
    "username": username,
    "password": password,
    "client": "requestip",
    "f": "json"
}

print("🔑 Requesting token...")
token_response = requests.post(token_url, data=token_params, verify=False).json()
if "token" not in token_response:
    print("❌ ERROR getting token:", token_response)
    exit()

token = token_response["token"]
print("✅ Token acquired.")

# 2️⃣ Upload SD
upload_url = f"{server}/admin/uploads/upload"
files = {"itemFile": open(sd_file, "rb")}
upload_params = {
    "f": "json",
    "token": token
}

print("📤 Uploading SD file...")
upload_response = requests.post(upload_url, files=files, data=upload_params, verify=False).json()
if "item" not in upload_response:
    print("❌ ERROR uploading SD:", upload_response)
    exit()

item_id = upload_response["item"]["itemID"]
print(f"✅ SD uploaded. Item ID: {item_id}")

# 3️⃣ Publish Service
publish_url = f"{server}/admin/services/publish"
publish_params = {
    "item": item_id,
    "filetype": "serviceDefinition",
    "f": "json",
    "token": token
}

print("🚀 Publishing service...")
publish_response = requests.post(publish_url, data=publish_params, verify=False).json()
if "services" not in publish_response:
    print("❌ ERROR publishing service:", publish_response)
    exit()

# Success
for svc in publish_response["services"]:
    svc_name = svc["serviceName"]
    svc_type = svc["type"]
    print(f"🎉 Published: {svc_name} ({svc_type})")

print("✅ Done.")