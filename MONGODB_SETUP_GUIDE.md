# 🍃 MongoDB Setup Guide for Echosense AI

## Quick Start - Installation Steps

### Step 1: Download MongoDB

**Download MongoDB Community Server:**
- Visit: https://www.mongodb.com/try/download/community
- **Version**: Select latest stable (8.0.x or 7.0.x)
- **Platform**: Windows
- **Package**: MSI

### Step 2: Install MongoDB

1. **Run the Installer**
   - Locate the downloaded `.msi` file (e.g., `mongodb-windows-x86_64-8.0.4-signed.msi`)
   - **Right-click** → **Run as Administrator**
   - Click "Yes" when prompted by User Account Control

2. **Installation Wizard Settings**

   #### Welcome Screen
   - Click **Next**

   #### License Agreement
   - Accept the terms → Click **Next**

   #### Setup Type
   - Select **Complete** → Click **Next**

   #### Service Configuration ⚠️ **CRITICAL STEP**
   
   **IMPORTANT**: Make sure to configure MongoDB as a Windows Service!
   
   - ✅ **Check "Install MongoDB as a Service"**
   - Service Name: `MongoDB` (default)
   - Data Directory: `C:\Program Files\MongoDB\Server\8.0\data\` (default)
   - Log Directory: `C:\Program Files\MongoDB\Server\8.0\log\` (default)
   - **Run service as**: Network Service user (default)
   - Click **Next**

   #### MongoDB Compass (Optional)
   - You can install MongoDB Compass (GUI tool) or uncheck to skip
   - Click **Next**

   #### Ready to Install
   - Click **Install**
   - Wait for installation to complete (2-5 minutes)

   #### Completion
   - Click **Finish**

### Step 3: Verify Installation

After installation, I'll help you verify that MongoDB is running properly.

---

## Post-Installation Setup

Once you've completed the installation, run these commands to verify:

```powershell
# Check if MongoDB service is running
Get-Service -Name MongoDB

# Check MongoDB version
mongod --version

# Check MongoDB shell
mongosh --version
```

---

## Initialize Echosense AI MongoDB Database

After MongoDB is installed and running, initialize the analytics database:

```powershell
# Navigate to backend directory
cd d:\project\backend

# Run the initialization script
python init_mongodb.py
```

This will create:
- ✅ `call_analytics` collection
- ✅ `sentiment_logs` collection
- ✅ `transcription_logs` collection
- ✅ `system_logs` collection
- ✅ `performance_metrics` collection
- ✅ All necessary indexes

---

## Troubleshooting

### If MongoDB service doesn't start automatically:

```powershell
# Start MongoDB service manually
net start MongoDB

# Or using PowerShell
Start-Service -Name MongoDB
```

### If installation fails:
- Make sure you ran as Administrator
- Check you have enough disk space (at least 500MB)
- Temporarily disable antivirus if it blocks the installer

### Connection Issues:
- Verify MongoDB is running: `Get-Service -Name MongoDB`
- Check MongoDB logs: `C:\Program Files\MongoDB\Server\8.0\log\mongod.log`
- Ensure port 27017 is not blocked by firewall

### If you need to connect manually:

```powershell
# Connect using MongoDB shell
mongosh "mongodb://localhost:27017/echosense_analytics"
```

---

## Configuration

Your Echosense AI is configured to connect to MongoDB at:
```
mongodb://localhost:27017/echosense_analytics
```

This is set in your `.env` file:
```env
MONGODB_URL=mongodb://localhost:27017/echosense_analytics
```

---

## Next Steps After Installation

1. ✅ Install MongoDB (follow steps above)
2. ✅ Verify service is running
3. ✅ Run `python init_mongodb.py` to initialize database
4. ✅ Start your Echosense AI backend: `python main.py`

---

## Useful MongoDB Commands

```powershell
# Check service status
Get-Service -Name MongoDB

# Start service
Start-Service -Name MongoDB

# Stop service
Stop-Service -Name MongoDB

# Restart service
Restart-Service -Name MongoDB
```

---

## MongoDB Compass (GUI Tool)

If you installed MongoDB Compass, you can connect to your database:
- **Connection String**: `mongodb://localhost:27017`
- **Database**: `echosense_analytics`

This provides a visual interface to browse collections, run queries, and monitor performance.

---

**Ready?** Download MongoDB from the link above and follow the installation steps. Once complete, let me know and I'll help you initialize the database! 🚀
