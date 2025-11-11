import sqlite3
import json
from datetime import datetime
import os

class DatabaseManager:
    """Quản lý cơ sở dữ liệu SQLite để lưu trữ kết quả lộ trình học"""
    
    def __init__(self, db_path="learning_paths.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Khởi tạo cơ sở dữ liệu và tạo các bảng"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Bảng sinh viên
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_code TEXT UNIQUE,
                student_name TEXT NOT NULL,
                gpa REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Bảng lộ trình học
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_paths (
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_steps (
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS course_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                learning_path_id INTEGER,
                analysis_summary TEXT,
                general_recommendations TEXT,
                FOREIGN KEY (learning_path_id) REFERENCES learning_paths (id)
            )
        ''')
        
        # Bảng môn học quan trọng
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS important_courses (
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skill_suggestions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                learning_path_id INTEGER,
                skill_type TEXT NOT NULL, -- 'strength_based', 'weakness_improvement', 'career_expansion'
                skill_name TEXT NOT NULL,
                reason TEXT,
                benefit TEXT,
                learning_path TEXT,
                FOREIGN KEY (learning_path_id) REFERENCES learning_paths (id)
            )
        ''')
        
        # Bảng lịch sử xuất file
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS export_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                learning_path_id INTEGER,
                export_type TEXT NOT NULL, -- 'json', 'txt', 'pdf'
                file_path TEXT NOT NULL,
                file_size INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (learning_path_id) REFERENCES learning_paths (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_learning_path(self, student_data, result):
        """Lưu kết quả lộ trình học vào database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Lưu thông tin sinh viên
            student_id = self._save_student(cursor, student_data)
            
            # Lưu lộ trình học chính
            learning_path_id = self._save_learning_path(cursor, student_id, student_data, result)
            
            # Lưu các bước học
            self._save_learning_steps(cursor, learning_path_id, result.get('learning_path', []))
            
            # Lưu phân tích môn học
            course_analysis_id = self._save_course_analysis(cursor, learning_path_id, result.get('course_analysis', {}))
            
            # Lưu các môn học quan trọng
            self._save_important_courses(cursor, course_analysis_id, result.get('course_analysis', {}).get('important_courses', []))
            
            # Lưu đề xuất kỹ năng
            self._save_skill_suggestions(cursor, learning_path_id, result.get('skill_suggestions', {}))
            
            conn.commit()
            return learning_path_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _save_student(self, cursor, student_data):
        """Lưu thông tin sinh viên"""
        cursor.execute('''
            INSERT OR REPLACE INTO students (student_code, student_name, gpa, updated_at)
            VALUES (?, ?, ?, ?)
        ''', (
            student_data.get('student_code', ''),
            student_data.get('student_name', ''),
            student_data.get('gpa'),
            datetime.now().isoformat()
        ))
        return cursor.lastrowid
    
    def _save_learning_path(self, cursor, student_id, student_data, result):
        """Lưu lộ trình học chính"""
        cursor.execute('''
            INSERT INTO learning_paths 
            (student_id, target_position, preferences, strengths, weaknesses, 
             analysis, overall_timeline, recommendations)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            student_id,
            result.get('target_position', ''),
            student_data.get('preferences', ''),
            student_data.get('strengths', ''),
            student_data.get('weaknesses', ''),
            result.get('analysis', ''),
            result.get('overall_timeline', ''),
            result.get('recommendations', '')
        ))
        return cursor.lastrowid
    
    def _save_learning_steps(self, cursor, learning_path_id, learning_steps):
        """Lưu các bước học"""
        for i, step in enumerate(learning_steps):
            cursor.execute('''
                INSERT INTO learning_steps 
                (learning_path_id, step_order, domain, difficulty_level, timeline, skills, resources)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                learning_path_id,
                i + 1,
                step.get('domain', ''),
                step.get('difficulty_level', ''),
                step.get('timeline', ''),
                json.dumps(step.get('skills', []), ensure_ascii=False),
                json.dumps(step.get('resources', []), ensure_ascii=False)
            ))
    
    def _save_course_analysis(self, cursor, learning_path_id, course_analysis):
        """Lưu phân tích môn học"""
        cursor.execute('''
            INSERT INTO course_analyses (learning_path_id, analysis_summary, general_recommendations)
            VALUES (?, ?, ?)
        ''', (
            learning_path_id,
            course_analysis.get('analysis_summary', ''),
            course_analysis.get('general_recommendations', '')
        ))
        return cursor.lastrowid
    
    def _save_important_courses(self, cursor, course_analysis_id, important_courses):
        """Lưu các môn học quan trọng"""
        for course in important_courses:
            cursor.execute('''
                INSERT INTO important_courses 
                (course_analysis_id, course_name, credits, importance_score, reason, study_tips)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                course_analysis_id,
                course.get('name', ''),
                course.get('credits', ''),
                course.get('importance_score', ''),
                course.get('reason', ''),
                course.get('study_tips', '')
            ))
    
    def _save_skill_suggestions(self, cursor, learning_path_id, skill_suggestions):
        """Lưu đề xuất kỹ năng"""
        # Lưu kỹ năng dựa trên điểm mạnh
        strength_skills = skill_suggestions.get('strength_based_skills', [])
        for skill in strength_skills:
            cursor.execute('''
                INSERT INTO skill_suggestions 
                (learning_path_id, skill_type, skill_name, reason, benefit, learning_path)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                learning_path_id,
                'strength_based',
                skill.get('skill_name', ''),
                skill.get('reason', ''),
                skill.get('benefit', ''),
                skill.get('learning_path', '')
            ))
        
        # Lưu kỹ năng cải thiện điểm yếu
        weakness_skills = skill_suggestions.get('weakness_improvement_skills', [])
        for skill in weakness_skills:
            cursor.execute('''
                INSERT INTO skill_suggestions 
                (learning_path_id, skill_type, skill_name, reason, benefit, learning_path)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                learning_path_id,
                'weakness_improvement',
                skill.get('skill_name', ''),
                skill.get('reason', ''),
                skill.get('benefit', ''),
                skill.get('learning_path', '')
            ))
        
        # Lưu kỹ năng mở rộng cơ hội
        expansion_skills = skill_suggestions.get('career_expansion_skills', [])
        for skill in expansion_skills:
            cursor.execute('''
                INSERT INTO skill_suggestions 
                (learning_path_id, skill_type, skill_name, reason, benefit, learning_path)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                learning_path_id,
                'career_expansion',
                skill.get('skill_name', ''),
                skill.get('reason', ''),
                skill.get('benefit', ''),
                skill.get('learning_path', '')
            ))
    
    def save_export_record(self, learning_path_id, export_type, file_path, file_size):
        """Lưu lịch sử xuất file"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO export_history (learning_path_id, export_type, file_path, file_size)
            VALUES (?, ?, ?, ?)
        ''', (learning_path_id, export_type, file_path, file_size))
        
        conn.commit()
        conn.close()
    
    def get_student_history(self, student_name):
        """Lấy lịch sử lộ trình học của sinh viên"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT lp.id, lp.target_position, lp.created_at, s.gpa
            FROM learning_paths lp
            JOIN students s ON lp.student_id = s.id
            WHERE s.student_name = ?
            ORDER BY lp.created_at DESC
        ''', (student_name,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'target_position': row[1],
                'created_at': row[2],
                'gpa': row[3]
            }
            for row in results
        ]
    
    def get_learning_path_details(self, learning_path_id):
        """Lấy chi tiết lộ trình học"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Lấy thông tin chính
        cursor.execute('''
            SELECT lp.*, s.student_name, s.gpa
            FROM learning_paths lp
            JOIN students s ON lp.student_id = s.id
            WHERE lp.id = ?
        ''', (learning_path_id,))
        
        main_info = cursor.fetchone()
        if not main_info:
            conn.close()
            return None
        
        # Lấy các bước học
        cursor.execute('''
            SELECT step_order, domain, difficulty_level, timeline, skills, resources
            FROM learning_steps
            WHERE learning_path_id = ?
            ORDER BY step_order
        ''', (learning_path_id,))
        
        steps = cursor.fetchall()
        
        # Lấy phân tích môn học
        cursor.execute('''
            SELECT ca.analysis_summary, ca.general_recommendations
            FROM course_analyses ca
            WHERE ca.learning_path_id = ?
        ''', (learning_path_id,))
        
        course_analysis = cursor.fetchone()
        
        # Lấy môn học quan trọng
        cursor.execute('''
            SELECT ic.course_name, ic.credits, ic.importance_score, ic.reason, ic.study_tips
            FROM important_courses ic
            JOIN course_analyses ca ON ic.course_analysis_id = ca.id
            WHERE ca.learning_path_id = ?
            ORDER BY ic.id
        ''', (learning_path_id,))
        
        important_courses = cursor.fetchall()
        
        # Lấy đề xuất kỹ năng
        cursor.execute('''
            SELECT skill_type, skill_name, reason, benefit, learning_path
            FROM skill_suggestions
            WHERE learning_path_id = ?
            ORDER BY skill_type, id
        ''', (learning_path_id,))
        
        skill_suggestions_data = cursor.fetchall()
        
        conn.close()
        
        # Tạo cấu trúc dữ liệu
        result = {
            'id': main_info[0],
            'target_position': main_info[2],
            'preferences': main_info[3],
            'strengths': main_info[4],
            'weaknesses': main_info[5],
            'analysis': main_info[6],
            'overall_timeline': main_info[7],
            'recommendations': main_info[8],
            'created_at': main_info[9],
            'student_name': main_info[10],
            'gpa': main_info[11],
            'learning_path': [
                {
                    'domain': step[1],
                    'difficulty_level': step[2],
                    'timeline': step[3],
                    'skills': json.loads(step[4]) if step[4] else [],
                    'resources': json.loads(step[5]) if step[5] else []
                }
                for step in steps
            ],
            'course_analysis': {
                'analysis_summary': course_analysis[0] if course_analysis else '',
                'general_recommendations': course_analysis[1] if course_analysis else '',
                'important_courses': [
                    {
                        'name': course[0],
                        'credits': course[1],
                        'importance_score': course[2],
                        'reason': course[3],
                        'study_tips': course[4]
                    }
                    for course in important_courses
                ]
            },
            'skill_suggestions': {
                'strength_based_skills': [
                    {
                        'skill_name': skill[1],
                        'reason': skill[2],
                        'benefit': skill[3],
                        'learning_path': skill[4]
                    }
                    for skill in skill_suggestions_data if skill[0] == 'strength_based'
                ],
                'weakness_improvement_skills': [
                    {
                        'skill_name': skill[1],
                        'reason': skill[2],
                        'benefit': skill[3],
                        'learning_path': skill[4]
                    }
                    for skill in skill_suggestions_data if skill[0] == 'weakness_improvement'
                ],
                'career_expansion_skills': [
                    {
                        'skill_name': skill[1],
                        'reason': skill[2],
                        'benefit': skill[3],
                        'learning_path': skill[4]
                    }
                    for skill in skill_suggestions_data if skill[0] == 'career_expansion'
                ]
            }
        }
        
        return result
    
    
    def get_statistics(self):
        """Lấy thống kê tổng quan"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tổng số sinh viên
        cursor.execute('SELECT COUNT(*) FROM students')
        total_students = cursor.fetchone()[0]
        
        # Tổng số lộ trình học
        cursor.execute('SELECT COUNT(*) FROM learning_paths')
        total_paths = cursor.fetchone()[0]
        
        # Tổng số file đã xuất
        cursor.execute('SELECT COUNT(*) FROM export_history')
        total_exports = cursor.fetchone()[0]
        
        # Top vị trí mục tiêu
        cursor.execute('''
            SELECT target_position, COUNT(*) as count
            FROM learning_paths
            GROUP BY target_position
            ORDER BY count DESC
            LIMIT 5
        ''')
        top_positions = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_students': total_students,
            'total_paths': total_paths,
            'total_exports': total_exports,
            'top_positions': [{'position': row[0], 'count': row[1]} for row in top_positions]
        }

