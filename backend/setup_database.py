"""
Database setup and initialization script
"""
import sys
from database.connection import engine, init_db
from config import get_settings

def main():
    settings = get_settings()
    print("=" * 60)
    print("Echosense AI - Database Setup")
    print("=" * 60)
    print(f"\nDatabase URL: {settings.database_url}")
    
    if engine is None:
        print("\n❌ ERROR: Database engine not initialized!")
        print("Please check your PostgreSQL installation and .env configuration.")
        sys.exit(1)
    
    print("\n✓ Database engine initialized")
    print("\nInitializing database tables...")
    
    try:
        init_db()
        print("\n✅ Database setup completed successfully!")
        print("\nYou can now start the backend server with:")
        print("  uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: Database initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
