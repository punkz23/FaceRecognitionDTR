#!/usr/bin/env python3
"""
Simple database connection test
"""
import psycopg2
import os

def test_database_connection():
    try:
        # Database connection parameters
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            user='appuser',
            password='StrongPassword123',
            database='appdb'
        )
        
        print("✅ Database connection successful!")
        
        # Test a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"PostgreSQL version: {version[0]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()
