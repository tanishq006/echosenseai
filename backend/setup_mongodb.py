"""
MongoDB Setup Verification and Initialization Script
Checks MongoDB installation, service status, and initializes the database
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, shell=True):
    """Run a command and return output"""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_mongodb_service():
    """Check if MongoDB service is running"""
    print("\n🔍 Checking MongoDB Service Status...")
    print("-" * 70)
    
    success, stdout, stderr = run_command("Get-Service -Name MongoDB -ErrorAction SilentlyContinue", shell=True)
    
    if "Running" in stdout:
        print("✅ MongoDB service is RUNNING")
        return True
    elif "Stopped" in stdout:
        print("⚠️  MongoDB service is STOPPED")
        print("\n💡 Starting MongoDB service...")
        success, _, _ = run_command("net start MongoDB", shell=True)
        if success:
            print("✅ MongoDB service started successfully!")
            return True
        else:
            print("❌ Failed to start MongoDB service")
            print("   Try running as Administrator: net start MongoDB")
            return False
    else:
        print("❌ MongoDB service not found")
        print("   MongoDB may not be installed or not configured as a service")
        return False

def check_mongodb_version():
    """Check MongoDB version"""
    print("\n🔍 Checking MongoDB Version...")
    print("-" * 70)
    
    success, stdout, stderr = run_command("mongod --version", shell=True)
    
    if success:
        version_line = stdout.split('\n')[0] if stdout else "Unknown"
        print(f"✅ MongoDB installed: {version_line}")
        return True
    else:
        print("❌ MongoDB not found in PATH")
        print("   MongoDB may not be installed or PATH not configured")
        return False

def check_mongodb_connection():
    """Test MongoDB connection"""
    print("\n🔍 Testing MongoDB Connection...")
    print("-" * 70)
    
    try:
        from pymongo import MongoClient
        from config import get_settings
        
        settings = get_settings()
        client = MongoClient(settings.mongodb_url, serverSelectionTimeoutMS=5000)
        client.server_info()
        
        db_name = client.get_database().name
        print(f"✅ Successfully connected to MongoDB")
        print(f"   Database: {db_name}")
        print(f"   URL: {settings.mongodb_url}")
        
        client.close()
        return True
        
    except ImportError:
        print("❌ pymongo not installed")
        print("   Run: pip install pymongo")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print("   Make sure MongoDB service is running")
        return False

def initialize_database():
    """Initialize MongoDB database"""
    print("\n🚀 Initializing MongoDB Database...")
    print("-" * 70)
    
    try:
        from init_mongodb import init_mongodb
        success = init_mongodb()
        return success
    except Exception as e:
        print(f"❌ Initialization failed: {str(e)}")
        return False

def main():
    """Main setup verification process"""
    print("=" * 70)
    print("MongoDB Setup Verification - Echosense AI")
    print("=" * 70)
    
    # Check if MongoDB is installed
    version_ok = check_mongodb_version()
    
    if not version_ok:
        print("\n" + "=" * 70)
        print("❌ MongoDB is NOT installed on your system")
        print("=" * 70)
        print("\n📖 Please follow the installation guide:")
        print("   → Open: MONGODB_SETUP_GUIDE.md")
        print("   → Download from: https://www.mongodb.com/try/download/community")
        print("\nAfter installation, run this script again!")
        sys.exit(1)
    
    # Check service status
    service_ok = check_mongodb_service()
    
    if not service_ok:
        print("\n" + "=" * 70)
        print("❌ MongoDB service is not running")
        print("=" * 70)
        print("\n💡 To start MongoDB service:")
        print("   → Run as Administrator: net start MongoDB")
        print("   → Or: Start-Service -Name MongoDB")
        sys.exit(1)
    
    # Test connection
    connection_ok = check_mongodb_connection()
    
    if not connection_ok:
        print("\n" + "=" * 70)
        print("❌ Cannot connect to MongoDB")
        print("=" * 70)
        print("\n💡 Troubleshooting:")
        print("   1. Make sure MongoDB service is running")
        print("   2. Check if port 27017 is available")
        print("   3. Verify MONGODB_URL in .env file")
        sys.exit(1)
    
    # All checks passed
    print("\n" + "=" * 70)
    print("✅ All MongoDB checks passed!")
    print("=" * 70)
    
    # Ask to initialize database
    print("\n📦 Would you like to initialize the Echosense AI database?")
    print("   This will create collections and indexes for analytics.")
    
    response = input("\nInitialize database? (y/n): ").strip().lower()
    
    if response == 'y':
        success = initialize_database()
        if success:
            print("\n" + "=" * 70)
            print("🎉 MongoDB is fully set up and ready!")
            print("=" * 70)
            print("\n✅ You can now start the Echosense AI backend:")
            print("   → python main.py")
            print("   → Or: uvicorn main:app --reload")
        else:
            print("\n❌ Database initialization failed")
            sys.exit(1)
    else:
        print("\n✅ MongoDB is ready, but database not initialized")
        print("   Run 'python init_mongodb.py' when ready")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
