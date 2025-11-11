#!/usr/bin/env python3
"""
Script test để kiểm tra tất cả imports và dependencies
"""

def test_imports():
    """Test tất cả imports"""
    print("🔍 Kiểm tra imports...")
    
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import streamlit as st
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        import sqlite3
        print("✅ sqlite3 imported successfully")
    except ImportError as e:
        print(f"❌ sqlite3 import failed: {e}")
        return False
    
    try:
        from gemini_client import GeminiClient
        print("✅ GeminiClient imported successfully")
    except ImportError as e:
        print(f"❌ GeminiClient import failed: {e}")
        return False
    
    try:
        from config import VI_TRI_FILE, MON_HOC_FILE, GPA_FILE
        print("✅ config imported successfully")
    except ImportError as e:
        print(f"❌ config import failed: {e}")
        return False
    
    try:
        from export_manager import ExportManager
        print("✅ ExportManager imported successfully")
    except ImportError as e:
        print(f"❌ ExportManager import failed: {e}")
        return False
    
    try:
        from database_manager import DatabaseManager
        print("✅ DatabaseManager imported successfully")
    except ImportError as e:
        print(f"❌ DatabaseManager import failed: {e}")
        return False
    
    print("🎉 Tất cả imports thành công!")
    return True

def test_file_existence():
    """Kiểm tra sự tồn tại của các file cần thiết"""
    print("\n📁 Kiểm tra files...")
    
    required_files = [
        "config.py",
        "gemini_client.py", 
        "export_manager.py",
        "database_manager.py",
        "data/vi_tri.csv",
        "data/danh_sach_monhoc.csv",
        "data/GPA.txt"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - KHÔNG TỒN TẠI")
            all_exist = False
    
    return all_exist

def test_directories():
    """Kiểm tra và tạo thư mục cần thiết"""
    print("\n📂 Kiểm tra thư mục...")
    
    directories = ["exports", "database_backups"]
    
    for dir_name in directories:
        if os.path.exists(dir_name):
            if os.path.isdir(dir_name):
                print(f"✅ {dir_name}/ (thư mục)")
            else:
                print(f"❌ {dir_name} tồn tại nhưng không phải thư mục")
                print(f"🗑️ Xóa file {dir_name}...")
                os.remove(dir_name)
                os.makedirs(dir_name)
                print(f"✅ Đã tạo thư mục {dir_name}/")
        else:
            print(f"📁 Tạo thư mục {dir_name}/...")
            os.makedirs(dir_name)
            print(f"✅ Đã tạo thư mục {dir_name}/")

def main():
    """Hàm main"""
    print("🚀 KIỂM TRA HỆ THỐNG")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Có lỗi imports, vui lòng kiểm tra dependencies")
        return False
    
    # Test files
    if not test_file_existence():
        print("\n❌ Thiếu files cần thiết, vui lòng kiểm tra")
        return False
    
    # Test directories
    test_directories()
    
    print("\n🎉 Hệ thống sẵn sàng!")
    print("💡 Bây giờ bạn có thể chạy: streamlit run app.py")
    
    return True

if __name__ == "__main__":
    import os
    main()
