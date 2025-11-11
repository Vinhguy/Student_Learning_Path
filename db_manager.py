#!/usr/bin/env python3
"""
Script quản lý database SQLite - Reset, Backup, Restore
"""

import sqlite3
import os
import shutil
from datetime import datetime

class DatabaseManager:
    """Quản lý database SQLite"""
    
    def __init__(self, db_path="learning_paths.db"):
        self.db_path = db_path
        self.backup_dir = "database_backups"
        self._ensure_backup_dir()
    
    def _ensure_backup_dir(self):
        """Tạo thư mục backup nếu chưa có"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def backup_database(self):
        """Tạo backup database với timestamp"""
        if not os.path.exists(self.db_path):
            print(f"❌ Database không tồn tại: {self.db_path}")
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"learning_paths_backup_{timestamp}.db"
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        try:
            shutil.copy2(self.db_path, backup_path)
            print(f"✅ Đã tạo backup: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"❌ Lỗi khi tạo backup: {e}")
            return None
    
    def restore_database(self, backup_path):
        """Khôi phục database từ backup"""
        if not os.path.exists(backup_path):
            print(f"❌ File backup không tồn tại: {backup_path}")
            return False
        
        try:
            # Backup database hiện tại trước
            if os.path.exists(self.db_path):
                self.backup_database()
            
            # Restore từ backup
            shutil.copy2(backup_path, self.db_path)
            print(f"✅ Đã khôi phục database từ: {backup_path}")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi khôi phục: {e}")
            return False
    
    def reset_database(self):
        """Reset database (xóa tất cả dữ liệu)"""
        if not os.path.exists(self.db_path):
            print(f"❌ Database không tồn tại: {self.db_path}")
            return False
        
        # Tạo backup trước khi reset
        backup_path = self.backup_database()
        if not backup_path:
            print("❌ Không thể tạo backup, hủy reset")
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Xóa tất cả dữ liệu nhưng giữ lại cấu trúc bảng
            tables = ['export_history', 'important_courses', 'course_analyses', 
                     'learning_steps', 'learning_paths', 'students']
            
            for table in tables:
                cursor.execute(f"DELETE FROM {table}")
                print(f"🗑️ Đã xóa dữ liệu từ bảng: {table}")
            
            # Reset auto-increment counters
            cursor.execute("DELETE FROM sqlite_sequence")
            
            conn.commit()
            conn.close()
            
            print("✅ Đã reset database thành công")
            print(f"📁 Backup được lưu tại: {backup_path}")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi khi reset database: {e}")
            return False
    
    def list_backups(self):
        """Liệt kê các file backup"""
        if not os.path.exists(self.backup_dir):
            print("📁 Chưa có thư mục backup")
            return []
        
        backup_files = []
        for filename in os.listdir(self.backup_dir):
            if filename.endswith('.db') and 'backup' in filename:
                file_path = os.path.join(self.backup_dir, filename)
                file_size = os.path.getsize(file_path)
                file_size_mb = round(file_size / (1024 * 1024), 2)
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                backup_files.append({
                    'filename': filename,
                    'path': file_path,
                    'size': f"{file_size_mb} MB",
                    'modified': mod_time.strftime('%d/%m/%Y %H:%M')
                })
        
        # Sắp xếp theo thời gian tạo (mới nhất trước)
        backup_files.sort(key=lambda x: x['modified'], reverse=True)
        
        return backup_files
    
    def show_database_status(self):
        """Hiển thị trạng thái database"""
        print(f"\n📊 Trạng thái Database: {self.db_path}")
        print("=" * 50)
        
        if not os.path.exists(self.db_path):
            print("❌ Database không tồn tại")
            return
        
        # Thông tin file
        file_size = os.path.getsize(self.db_path)
        file_size_mb = round(file_size / (1024 * 1024), 2)
        mod_time = datetime.fromtimestamp(os.path.getmtime(self.db_path))
        
        print(f"📁 Kích thước: {file_size_mb} MB")
        print(f"📅 Cập nhật lần cuối: {mod_time.strftime('%d/%m/%Y %H:%M')}")
        
        # Thống kê dữ liệu
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            tables = ['students', 'learning_paths', 'learning_steps', 'course_analyses', 'important_courses', 'export_history']
            
            print(f"\n📋 Số lượng records:")
            total_records = 0
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                total_records += count
                print(f"  {table}: {count}")
            
            print(f"\n📊 Tổng records: {total_records}")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Lỗi khi đọc database: {e}")
    
    def cleanup_old_backups(self, keep_days=30):
        """Xóa các backup cũ (giữ lại 30 ngày gần nhất)"""
        backups = self.list_backups()
        
        if not backups:
            print("📁 Không có backup để cleanup")
            return
        
        cutoff_date = datetime.now().timestamp() - (keep_days * 24 * 60 * 60)
        deleted_count = 0
        
        for backup in backups:
            file_timestamp = os.path.getmtime(backup['path'])
            if file_timestamp < cutoff_date:
                try:
                    os.remove(backup['path'])
                    print(f"🗑️ Đã xóa backup cũ: {backup['filename']}")
                    deleted_count += 1
                except Exception as e:
                    print(f"❌ Lỗi khi xóa {backup['filename']}: {e}")
        
        if deleted_count == 0:
            print("✅ Không có backup cũ để xóa")
        else:
            print(f"✅ Đã xóa {deleted_count} backup cũ")

def show_menu():
    """Hiển thị menu"""
    print("\n" + "=" * 50)
    print("🗄️ QUẢN LÝ DATABASE SQLITE")
    print("=" * 50)
    print("1. 📊 Xem trạng thái database")
    print("2. 💾 Tạo backup")
    print("3. 📋 Liệt kê backups")
    print("4. 🔄 Khôi phục từ backup")
    print("5. 🗑️ Reset database (xóa tất cả dữ liệu)")
    print("6. 🧹 Cleanup backups cũ")
    print("7. ❌ Thoát")
    print("=" * 50)

def main():
    """Hàm main"""
    db_manager = DatabaseManager()
    
    while True:
        show_menu()
        
        try:
            choice = input("Chọn chức năng (1-7): ").strip()
            
            if choice == '1':
                db_manager.show_database_status()
            
            elif choice == '2':
                backup_path = db_manager.backup_database()
                if backup_path:
                    print(f"✅ Backup thành công: {backup_path}")
            
            elif choice == '3':
                backups = db_manager.list_backups()
                if backups:
                    print(f"\n📋 Danh sách backups ({len(backups)} files):")
                    for i, backup in enumerate(backups, 1):
                        print(f"  {i}. {backup['filename']}")
                        print(f"     Kích thước: {backup['size']}")
                        print(f"     Ngày tạo: {backup['modified']}")
                else:
                    print("📁 Chưa có backup nào")
            
            elif choice == '4':
                backups = db_manager.list_backups()
                if not backups:
                    print("📁 Chưa có backup nào để khôi phục")
                    continue
                
                print(f"\n📋 Chọn backup để khôi phục:")
                for i, backup in enumerate(backups, 1):
                    print(f"  {i}. {backup['filename']} ({backup['modified']})")
                
                try:
                    backup_choice = int(input("Nhập số thứ tự backup: ")) - 1
                    if 0 <= backup_choice < len(backups):
                        backup_path = backups[backup_choice]['path']
                        confirm = input(f"Xác nhận khôi phục từ {backups[backup_choice]['filename']}? (y/n): ")
                        if confirm.lower() in ['y', 'yes', 'có', 'c']:
                            db_manager.restore_database(backup_path)
                        else:
                            print("❌ Hủy khôi phục")
                    else:
                        print("❌ Lựa chọn không hợp lệ")
                except ValueError:
                    print("❌ Vui lòng nhập số")
            
            elif choice == '5':
                print("⚠️ CẢNH BÁO: Thao tác này sẽ XÓA TẤT CẢ DỮ LIỆU!")
                confirm = input("Bạn có chắc chắn muốn reset database? (y/n): ")
                if confirm.lower() in ['y', 'yes', 'có', 'c']:
                    db_manager.reset_database()
                else:
                    print("❌ Hủy reset")
            
            elif choice == '6':
                days = input("Số ngày giữ lại backup (mặc định 30): ").strip()
                try:
                    keep_days = int(days) if days else 30
                    db_manager.cleanup_old_backups(keep_days)
                except ValueError:
                    print("❌ Số ngày không hợp lệ")
            
            elif choice == '7':
                print("👋 Tạm biệt!")
                break
            
            else:
                print("❌ Lựa chọn không hợp lệ")
        
        except KeyboardInterrupt:
            print("\n👋 Tạm biệt!")
            break
        except Exception as e:
            print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main()

