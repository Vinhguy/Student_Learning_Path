#!/usr/bin/env python3
"""
Script khởi tạo database SQLite cho hệ thống cá nhân hóa lộ trình học
"""

import sqlite3
import os
from datetime import datetime

class DatabaseInitializer:
    """Khởi tạo database SQLite"""
    
    def __init__(self, db_path="learning_paths.db"):
        self.db_path = db_path
        self.backup_path = f"{db_path}.backup"
    
    def create_backup(self):
        """Tạo backup database hiện tại nếu có"""
        if os.path.exists(self.db_path):
            print(f"📁 Tạo backup database hiện tại...")
            try:
                # Copy file database
                with open(self.db_path, 'rb') as src:
                    with open(self.backup_path, 'wb') as dst:
                        dst.write(src.read())
                print(f"✅ Đã tạo backup: {self.backup_path}")
            except Exception as e:
                print(f"❌ Lỗi khi tạo backup: {e}")
        else:
            print("ℹ️ Không có database hiện tại để backup")
    
    def init_database(self):
        """Khởi tạo database và tạo các bảng"""
        print(f"🚀 Khởi tạo database: {self.db_path}")
        
        # Tạo backup trước
        self.create_backup()
        
        # Xóa database cũ nếu có
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            print(f"🗑️ Đã xóa database cũ")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Bảng sinh viên
            print("📋 Tạo bảng students...")
            cursor.execute('''
                CREATE TABLE students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_code TEXT UNIQUE,
                    student_name TEXT NOT NULL,
                    gpa REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Bảng lộ trình học
            print("📋 Tạo bảng learning_paths...")
            cursor.execute('''
                CREATE TABLE learning_paths (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    target_position TEXT NOT NULL,
                    preferences TEXT,
                    strengths TEXT,
                    weaknesses TEXT,
                    analysis TEXT,
                    overall_timeline TEXT,
                    recommendations TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students (id)
                )
            ''')
            
            # Bảng các bước học
            print("📋 Tạo bảng learning_steps...")
            cursor.execute('''
                CREATE TABLE learning_steps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    learning_path_id INTEGER,
                    step_order INTEGER,
                    domain TEXT NOT NULL,
                    difficulty_level TEXT,
                    timeline TEXT,
                    skills TEXT, -- JSON array
                    resources TEXT, -- JSON array
                    FOREIGN KEY (learning_path_id) REFERENCES learning_paths (id)
                )
            ''')
            
            # Bảng phân tích môn học
            print("📋 Tạo bảng course_analyses...")
            cursor.execute('''
                CREATE TABLE course_analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    learning_path_id INTEGER,
                    analysis_summary TEXT,
                    general_recommendations TEXT,
                    FOREIGN KEY (learning_path_id) REFERENCES learning_paths (id)
                )
            ''')
            
            # Bảng môn học quan trọng
            print("📋 Tạo bảng important_courses...")
            cursor.execute('''
                CREATE TABLE important_courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_analysis_id INTEGER,
                    course_name TEXT NOT NULL,
                    credits TEXT,
                    importance_score TEXT,
                    reason TEXT,
                    study_tips TEXT,
                    FOREIGN KEY (course_analysis_id) REFERENCES course_analyses (id)
                )
            ''')
            
            # Bảng đề xuất kỹ năng
            print("📋 Tạo bảng skill_suggestions...")
            cursor.execute('''
                CREATE TABLE skill_suggestions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    learning_path_id INTEGER,
                    skill_type TEXT NOT NULL,
                    skill_name TEXT NOT NULL,
                    reason TEXT,
                    benefit TEXT,
                    learning_path TEXT,
                    FOREIGN KEY (learning_path_id) REFERENCES learning_paths (id)
                )
            ''')
            
            # Bảng lịch sử xuất file
            print("📋 Tạo bảng export_history...")
            cursor.execute('''
                CREATE TABLE export_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    learning_path_id INTEGER,
                    export_type TEXT NOT NULL, -- 'json', 'txt', 'pdf'
                    file_path TEXT NOT NULL,
                    file_size INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (learning_path_id) REFERENCES learning_paths (id)
                )
            ''')
            
            # Tạo indexes để tối ưu performance
            print("⚡ Tạo indexes...")
            cursor.execute('CREATE INDEX idx_students_name ON students(student_name)')
            cursor.execute('CREATE INDEX idx_learning_paths_student ON learning_paths(student_id)')
            cursor.execute('CREATE INDEX idx_learning_paths_position ON learning_paths(target_position)')
            cursor.execute('CREATE INDEX idx_learning_steps_path ON learning_steps(learning_path_id)')
            cursor.execute('CREATE INDEX idx_course_analyses_path ON course_analyses(learning_path_id)')
            cursor.execute('CREATE INDEX idx_important_courses_analysis ON important_courses(course_analysis_id)')
            cursor.execute('CREATE INDEX idx_skill_suggestions_path ON skill_suggestions(learning_path_id)')
            cursor.execute('CREATE INDEX idx_skill_suggestions_type ON skill_suggestions(skill_type)')
            cursor.execute('CREATE INDEX idx_export_history_path ON export_history(learning_path_id)')
            
            # Commit tất cả thay đổi
            conn.commit()
            print("✅ Đã commit tất cả thay đổi")
            
            # Kiểm tra database
            self.verify_database(cursor)
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Lỗi khi khởi tạo database: {e}")
            raise e
        finally:
            conn.close()
        
        print(f"🎉 Khởi tạo database thành công: {self.db_path}")
        return True
    
    def verify_database(self, cursor):
        """Kiểm tra database đã được tạo đúng"""
        print("🔍 Kiểm tra database...")
        
        # Lấy danh sách bảng
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        expected_tables = [
            'students', 'learning_paths', 'learning_steps', 
            'course_analyses', 'important_courses', 'export_history'
        ]
        
        actual_tables = [table[0] for table in tables]
        
        print(f"📊 Bảng đã tạo: {len(actual_tables)}")
        for table in actual_tables:
            print(f"  ✓ {table}")
        
        # Kiểm tra tất cả bảng cần thiết đã có
        missing_tables = set(expected_tables) - set(actual_tables)
        if missing_tables:
            print(f"❌ Thiếu bảng: {missing_tables}")
            return False
        
        # Kiểm tra indexes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = cursor.fetchall()
        print(f"⚡ Indexes đã tạo: {len(indexes)}")
        
        print("✅ Database đã được kiểm tra và hoạt động tốt")
        return True
    
    def insert_sample_data(self):
        """Thêm dữ liệu mẫu để test"""
        print("📝 Thêm dữ liệu mẫu...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Thêm sinh viên mẫu
            cursor.execute('''
                INSERT INTO students (student_code, student_name, gpa)
                VALUES (?, ?, ?)
            ''', ('SV001', 'Nguyễn Văn A', 3.2))
            
            student_id = cursor.lastrowid
            
            # Thêm lộ trình học mẫu
            cursor.execute('''
                INSERT INTO learning_paths 
                (student_id, target_position, preferences, strengths, weaknesses, 
                 analysis, overall_timeline, recommendations)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                student_id,
                'AI Engineer',
                'Thích lập trình Python và machine learning',
                'Giỏi toán, tư duy logic tốt',
                'Chưa có kinh nghiệm với deep learning',
                'AI Engineer là vị trí đòi hỏi kiến thức sâu về machine learning và programming',
                '12-18 tháng',
                'Nên tập trung vào Python và các framework ML như TensorFlow, PyTorch'
            ))
            
            learning_path_id = cursor.lastrowid
            
            # Thêm bước học mẫu
            steps = [
                (1, 'Lập trình Python cơ bản', 'Cơ bản', '3-6 tháng', 
                 '["Python syntax", "Data structures", "OOP"]', 
                 '["Python.org tutorial", "LeetCode", "Kaggle"]'),
                (2, 'Machine Learning cơ bản', 'Trung cấp', '6-9 tháng',
                 '["Scikit-learn", "Pandas", "NumPy", "Data visualization"]',
                 '["Coursera ML course", "Hands-on ML book", "Kaggle competitions"]')
            ]
            
            for step_order, domain, difficulty, timeline, skills, resources in steps:
                cursor.execute('''
                    INSERT INTO learning_steps 
                    (learning_path_id, step_order, domain, difficulty_level, timeline, skills, resources)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (learning_path_id, step_order, domain, difficulty, timeline, skills, resources))
            
            # Thêm phân tích môn học mẫu
            cursor.execute('''
                INSERT INTO course_analyses (learning_path_id, analysis_summary, general_recommendations)
                VALUES (?, ?, ?)
            ''', (
                learning_path_id,
                'Các môn học quan trọng cho AI Engineer bao gồm lập trình, toán học và machine learning',
                'Nên học theo thứ tự từ cơ bản đến nâng cao và thực hành nhiều'
            ))
            
            course_analysis_id = cursor.lastrowid
            
            # Thêm môn học quan trọng mẫu
            courses = [
                ('Lập trình cơ bản', '3', '9/10', 'Nền tảng cho tất cả môn học khác', 'Thực hành nhiều bài tập'),
                ('Cấu trúc dữ liệu và giải thuật', '3', '8/10', 'Quan trọng cho tư duy lập trình', 'Làm nhiều bài tập trên LeetCode'),
                ('Trí tuệ nhân tạo', '2', '9/10', 'Core knowledge cho AI Engineer', 'Học lý thuyết và thực hành với Python'),
                ('Học máy', '2', '8/10', 'Essential cho AI career', 'Thực hành với scikit-learn và TensorFlow'),
                ('Toán rời rạc', '3', '7/10', 'Foundation cho algorithms', 'Tập trung vào logic và proofs')
            ]
            
            for course_name, credits, score, reason, tips in courses:
                cursor.execute('''
                    INSERT INTO important_courses 
                    (course_analysis_id, course_name, credits, importance_score, reason, study_tips)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (course_analysis_id, course_name, credits, score, reason, tips))
            
            # Thêm lịch sử xuất file mẫu
            cursor.execute('''
                INSERT INTO export_history (learning_path_id, export_type, file_path, file_size)
                VALUES (?, ?, ?, ?)
            ''', (learning_path_id, 'pdf', 'exports/sample_export.pdf', 1024000))
            
            conn.commit()
            print("✅ Đã thêm dữ liệu mẫu thành công")
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Lỗi khi thêm dữ liệu mẫu: {e}")
            raise e
        finally:
            conn.close()
    
    def show_database_info(self):
        """Hiển thị thông tin database"""
        if not os.path.exists(self.db_path):
            print(f"❌ Database không tồn tại: {self.db_path}")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        print(f"\n📊 Thông tin Database: {self.db_path}")
        print("=" * 50)
        
        # Thông tin file
        file_size = os.path.getsize(self.db_path)
        file_size_mb = round(file_size / (1024 * 1024), 2)
        print(f"📁 Kích thước file: {file_size_mb} MB")
        
        # Đếm records trong mỗi bảng
        tables = ['students', 'learning_paths', 'learning_steps', 'course_analyses', 'important_courses', 'skill_suggestions', 'export_history']
        
        print(f"\n📋 Số lượng records:")
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  {table}: {count} records")
            except Exception as e:
                print(f"  {table}: Lỗi - {e}")
        
        # Thống kê tổng quan
        try:
            cursor.execute("SELECT COUNT(DISTINCT student_id) FROM learning_paths")
            unique_students = cursor.fetchone()[0]
            print(f"\n👥 Số sinh viên unique: {unique_students}")
            
            cursor.execute("SELECT COUNT(*) FROM learning_paths")
            total_paths = cursor.fetchone()[0]
            print(f"🗺️ Tổng lộ trình học: {total_paths}")
            
            cursor.execute("SELECT COUNT(*) FROM export_history")
            total_exports = cursor.fetchone()[0]
            print(f"📄 Tổng file xuất: {total_exports}")
            
        except Exception as e:
            print(f"❌ Lỗi khi lấy thống kê: {e}")
        
        conn.close()

def main():
    """Hàm main để chạy script"""
    print("🚀 Script khởi tạo Database SQLite")
    print("=" * 50)
    
    # Khởi tạo database
    db_init = DatabaseInitializer()
    
    try:
        # Khởi tạo database
        db_init.init_database()
        
        # Hỏi có muốn thêm dữ liệu mẫu không
        print("\n" + "=" * 50)
        add_sample = input("❓ Có muốn thêm dữ liệu mẫu để test không? (y/n): ").lower().strip()
        
        if add_sample in ['y', 'yes', 'có', 'c']:
            db_init.insert_sample_data()
        
        # Hiển thị thông tin database
        print("\n" + "=" * 50)
        db_init.show_database_info()
        
        print("\n🎉 Hoàn thành khởi tạo database!")
        print(f"📁 Database file: {db_init.db_path}")
        print(f"📁 Backup file: {db_init.backup_path}")
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()

