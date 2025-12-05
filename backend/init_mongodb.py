"""
MongoDB Database Initialization Script for Echosense AI Analytics
Creates collections, indexes, and initial configuration
"""
from pymongo import MongoClient, ASCENDING, DESCENDING
from config import get_settings
from datetime import datetime, timezone
import sys

def init_mongodb():
    """Initialize MongoDB database with collections and indexes"""
    settings = get_settings()
    
    print("=" * 70)
    print("MongoDB Database Initialization - Echosense AI Analytics")
    print("=" * 70)
    
    try:
        # Connect to MongoDB
        print("\n🔄 Connecting to MongoDB...")
        client = MongoClient(settings.mongodb_url, serverSelectionTimeoutMS=5000)
        client.server_info()  # Test connection
        
        db = client.get_database()
        print(f"✅ Connected to database: {db.name}")
        
        # Define collections and their indexes
        collections_config = {
            'call_analytics': {
                'description': 'Call performance metrics and analytics',
                'indexes': [
                    ('call_id', ASCENDING),
                    ('timestamp', DESCENDING),
                    ('sentiment_score', ASCENDING),
                    ('agent_id', ASCENDING),
                ]
            },
            'sentiment_logs': {
                'description': 'Detailed sentiment analysis results',
                'indexes': [
                    ('call_id', ASCENDING),
                    ('timestamp', DESCENDING),
                    ('sentiment', ASCENDING),
                ]
            },
            'transcription_logs': {
                'description': 'Transcription metadata and processing logs',
                'indexes': [
                    ('call_id', ASCENDING),
                    ('timestamp', DESCENDING),
                    ('status', ASCENDING),
                ]
            },
            'system_logs': {
                'description': 'Application logs and system events',
                'indexes': [
                    ('timestamp', DESCENDING),
                    ('level', ASCENDING),
                    ('component', ASCENDING),
                ]
            },
            'performance_metrics': {
                'description': 'System performance and processing metrics',
                'indexes': [
                    ('timestamp', DESCENDING),
                    ('metric_type', ASCENDING),
                ]
            }
        }
        
        print(f"\n📦 Creating collections and indexes...")
        print("-" * 70)
        
        for collection_name, config in collections_config.items():
            # Create or get collection
            if collection_name in db.list_collection_names():
                print(f"\n✓ Collection '{collection_name}' already exists")
                collection = db[collection_name]
            else:
                collection = db.create_collection(collection_name)
                print(f"\n✅ Created collection: {collection_name}")
            
            print(f"   Description: {config['description']}")
            
            # Create indexes
            existing_indexes = [idx['name'] for idx in collection.list_indexes()]
            for field, direction in config['indexes']:
                index_name = f"{field}_1" if direction == ASCENDING else f"{field}_-1"
                if index_name not in existing_indexes and index_name != '_id_':
                    collection.create_index([(field, direction)])
                    print(f"   ✅ Created index: {field} ({'ASC' if direction == ASCENDING else 'DESC'})")
        
        # Insert initial system log
        print(f"\n📝 Inserting initial system log...")
        system_log = {
            'timestamp': datetime.now(timezone.utc),
            'level': 'INFO',
            'component': 'database_init',
            'message': 'MongoDB analytics database initialized successfully',
            'version': '1.0.0'
        }
        db['system_logs'].insert_one(system_log)
        print(f"   ✅ Initial log entry created")
        
        # Display summary
        print("\n" + "=" * 70)
        print("✅ MongoDB Initialization Complete!")
        print("=" * 70)
        print(f"\n📊 Database Summary:")
        print(f"   Database: {db.name}")
        print(f"   Collections: {len(collections_config)}")
        
        for collection_name in collections_config.keys():
            count = db[collection_name].count_documents({})
            print(f"   - {collection_name}: {count} documents")
        
        print(f"\n🎉 MongoDB is ready for Echosense AI analytics!")
        print(f"   You can now start the backend server with MongoDB support")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Initialization failed!")
        print(f"   Error: {type(e).__name__}: {str(e)}")
        print(f"\n💡 Make sure MongoDB is running:")
        print(f"   → Check service: Get-Service -Name MongoDB")
        print(f"   → Start service: net start MongoDB")
        return False

if __name__ == "__main__":
    success = init_mongodb()
    sys.exit(0 if success else 1)
