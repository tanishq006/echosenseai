"""
MongoDB Connection Test and Diagnostics Script
"""
from pymongo import MongoClient
from config import get_settings
import sys
import subprocess

def check_service_status():
    """Check if MongoDB Windows service is running"""
    try:
        result = subprocess.run(
            ['powershell', '-Command', 'Get-Service -Name MongoDB* | Select-Object Name, Status, StartType'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            print("\n📋 MongoDB Service Status:")
            print(result.stdout)
            return True
        else:
            print("\n⚠️  MongoDB service not found in Windows Services")
            return False
    except Exception as e:
        print(f"\n⚠️  Could not check service status: {e}")
        return False

def check_port_listening():
    """Check if MongoDB is listening on port 27017"""
    try:
        result = subprocess.run(
            ['powershell', '-Command', 'netstat -an | Select-String "27017"'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and '27017' in result.stdout:
            print("\n🔌 Port Status:")
            print("   MongoDB is listening on port 27017")
            return True
        else:
            print("\n⚠️  Port 27017 is not in use (MongoDB may not be running)")
            return False
    except Exception as e:
        print(f"\n⚠️  Could not check port status: {e}")
        return False

def test_mongodb():
    settings = get_settings()
    print("=" * 70)
    print("MongoDB Connection Test - Echosense AI")
    print("=" * 70)
    print(f"\nMongoDB URL: {settings.mongodb_url}")
    
    # Check service status first
    service_ok = check_service_status()
    port_ok = check_port_listening()
    
    try:
        # Create MongoDB client with timeout
        print("\n🔄 Attempting to connect to MongoDB...")
        client = MongoClient(settings.mongodb_url, serverSelectionTimeoutMS=5000)
        
        # Test connection by getting server info
        server_info = client.server_info()
        
        print("\n" + "=" * 70)
        print("✅ SUCCESS - MongoDB is WORKING!")
        print("=" * 70)
        print(f"\n📊 Server Information:")
        print(f"   Version: {server_info.get('version', 'Unknown')}")
        print(f"   Git Version: {server_info.get('gitVersion', 'Unknown')[:12]}")
        print(f"   Platform: {server_info.get('sysInfo', 'Unknown')}")
        
        # Get database
        db = client.get_database()
        print(f"\n💾 Database Information:")
        print(f"   Database Name: {db.name}")
        
        # List collections
        collections = db.list_collection_names()
        if collections:
            print(f"   Collections ({len(collections)}): {', '.join(collections)}")
        else:
            print("   Collections: None (database is empty)")
        
        # Test write operation
        print(f"\n🧪 Testing Write Operations...")
        test_collection = db['connection_test']
        test_doc = {"test": "connection", "status": "success", "timestamp": "now"}
        result = test_collection.insert_one(test_doc)
        print(f"   ✅ Write successful! Document ID: {result.inserted_id}")
        
        # Test read operation
        read_doc = test_collection.find_one({"_id": result.inserted_id})
        print(f"   ✅ Read successful! Document: {read_doc['status']}")
        
        # Clean up test document
        test_collection.delete_one({"_id": result.inserted_id})
        print(f"   ✅ Delete successful! Test document cleaned up")
        
        print("\n" + "=" * 70)
        print("🎉 All tests passed! MongoDB is ready for Echosense AI analytics")
        print("=" * 70)
        
        client.close()
        return True
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ FAILED - MongoDB is NOT WORKING!")
        print("=" * 70)
        print(f"\n🔴 Error Details:")
        print(f"   {type(e).__name__}: {str(e)}")
        
        print(f"\n💡 Troubleshooting Steps:")
        
        if not service_ok:
            print("\n   1. MongoDB service is not installed or not found")
            print("      → Install MongoDB from: https://www.mongodb.com/try/download/community")
            print("      → Make sure to check 'Install MongoDB as a Service' during installation")
        elif not port_ok:
            print("\n   1. MongoDB service exists but is not running")
            print("      → Start it with: net start MongoDB")
            print("      → Or use Services app (services.msc)")
        else:
            print("\n   1. Service is running but connection failed")
            print("      → Check MongoDB logs in: C:\\Program Files\\MongoDB\\Server\\*\\log\\")
            print("      → Verify connection URL in .env file")
            print("      → Check firewall settings for port 27017")
        
        print("\n   2. Verify MongoDB installation:")
        print("      → Run: mongod --version")
        print("      → Should show MongoDB version info")
        
        print("\n   3. Check Windows Services:")
        print("      → Press Win+R, type 'services.msc'")
        print("      → Look for 'MongoDB' service")
        print("      → Status should be 'Running'")
        
        return False

if __name__ == "__main__":
    success = test_mongodb()
    sys.exit(0 if success else 1)

