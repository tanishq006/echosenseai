"""
Test script to diagnose upload issues
"""
import requests
import os

# Test file path
test_file = r"C:\Users\HP\Downloads\2b18-e5ac-4dd8-8f1e-fb75f07e6c24.mp3"

print("=" * 70)
print("Testing Echosense AI Upload Endpoint")
print("=" * 70)

# Check if file exists
if not os.path.exists(test_file):
    print(f"\n❌ Test file not found: {test_file}")
    print("Please provide a valid audio file path")
    exit(1)

file_size = os.path.getsize(test_file)
print(f"\n📁 Test file: {os.path.basename(test_file)}")
print(f"📊 File size: {file_size / (1024*1024):.2f} MB")

# Test health endpoint first
print("\n🔍 Testing backend health...")
try:
    response = requests.get("http://localhost:8000/health", timeout=5)
    print(f"✅ Backend is healthy: {response.json()}")
except Exception as e:
    print(f"❌ Backend health check failed: {e}")
    exit(1)

# Test upload endpoint
print("\n📤 Attempting file upload...")
try:
    with open(test_file, 'rb') as f:
        files = {'file': (os.path.basename(test_file), f, 'audio/mpeg')}
        response = requests.post(
            "http://localhost:8000/api/upload/audio",
            files=files,
            timeout=30
        )
    
    print(f"\n📊 Response Status: {response.status_code}")
    print(f"📄 Response Body:")
    print(response.text)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Upload successful!")
        print(f"   Call ID: {data.get('call_id')}")
        print(f"   Status: {data.get('status')}")
        print(f"   Message: {data.get('message')}")
    else:
        print(f"\n❌ Upload failed with status {response.status_code}")
        try:
            error = response.json()
            print(f"   Error: {error.get('detail', 'Unknown error')}")
        except:
            print(f"   Raw response: {response.text}")

except requests.exceptions.Timeout:
    print("\n❌ Upload timed out (took longer than 30 seconds)")
except requests.exceptions.ConnectionError:
    print("\n❌ Could not connect to backend server")
    print("   Make sure the server is running on http://localhost:8000")
except Exception as e:
    print(f"\n❌ Upload failed with error:")
    print(f"   {type(e).__name__}: {str(e)}")

print("\n" + "=" * 70)
