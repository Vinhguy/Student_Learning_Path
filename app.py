import pandas as pd
import streamlit as st
from gemini_client import GeminiClient
from config import VI_TRI_FILE, MON_HOC_FILE, GPA_FILE
from database_manager import DatabaseManager

class DataProcessor:
    """Xử lý dữ liệu từ các file CSV và TXT"""
    
    @staticmethod
    def load_positions():
        """Đọc danh sách vị trí từ file CSV"""
        try:
            df = pd.read_csv(VI_TRI_FILE, encoding='utf-8')
            return df['Tên vi trí'].tolist()
        except Exception as e:
            st.error(f"Lỗi khi đọc file vị trí: {e}")
            return []
    
    @staticmethod
    def load_courses():
        """Đọc danh sách môn học từ file CSV"""
        try:
            df = pd.read_csv(MON_HOC_FILE, encoding='utf-8')
            courses = []
            for _, row in df.iterrows():
                courses.append({
                    'name': row['Tên môn học'],
                    'credits': row['Số tín chỉ']
                })
            return courses
        except Exception as e:
            st.error(f"Lỗi khi đọc file môn học: {e}")
            return []
    
    @staticmethod
    def load_gpa_data():
        """Đọc dữ liệu GPA từ file TXT"""
        try:
            df = pd.read_csv(GPA_FILE, sep='\t', encoding='utf-8')
            return df
        except Exception as e:
            st.error(f"Lỗi khi đọc file GPA: {e}")
            return pd.DataFrame()

class LearningPathApp:
    """Ứng dụng chính cho hệ thống cá nhân hóa lộ trình học"""
    
    def __init__(self):
        self.gemini_client = GeminiClient()
        self.data_processor = DataProcessor()
        self.db_manager = DatabaseManager()
        
    def run(self):
        """Chạy ứng dụng Streamlit"""
        st.set_page_config(
            page_title="Hệ thống Cá nhân hóa Lộ trình Học",
            page_icon="🎓",
            layout="wide"
        )
        
        # CSS để điều chỉnh sidebar
        st.markdown("""
        <style>
        /* Làm sidebar rộng hơn */
        .css-1d391kg {
            width: 350px !important;
        }
        
        /* Căn chỉnh các components trong sidebar */
        .stSidebar .stTextArea textarea {
            width: 100% !important;
        }
        
        .stSidebar .stSelectbox > div > div {
            width: 100% !important;
        }
        
        /* Đảm bảo text areas hiển thị đầy đủ */
        .stSidebar .stTextArea {
            width: 100% !important;
        }
        
        /* Căn chỉnh buttons */
        .stSidebar .stButton button {
            width: 100% !important;
        }
        
        /* Spacing tốt hơn */
        .stSidebar .element-container {
            margin-bottom: 1rem !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.title("🎓 Hệ thống Cá nhân hóa Lộ trình Học")
        st.markdown("---")
        
        # Sidebar cho thông tin sinh viên
        with st.sidebar:
            st.header("📋 Thông tin Sinh viên")
            
            # Chọn sinh viên từ danh sách GPA
            gpa_data = self.data_processor.load_gpa_data()
            if not gpa_data.empty:
                student_options = [f"{row['Họ và tên']} (GPA: {row['TBCHT H4']})" 
                                 for _, row in gpa_data.iterrows() 
                                 if pd.notna(row['TBCHT H4'])]
                
                selected_student = st.selectbox(
                    "Chọn sinh viên:",
                    options=student_options,
                    index=0
                )
                
                # Lấy thông tin sinh viên được chọn
                student_name = selected_student.split(' (GPA: ')[0]
                student_gpa = float(selected_student.split('GPA: ')[1].rstrip(')'))
                
                st.write(f"**Tên:** {student_name}")
                st.write(f"**GPA:** {student_gpa}")
            else:
                student_name = "Sinh viên"
                student_gpa = None
                st.warning("Không có dữ liệu GPA")
            
            # Nhập sở thích (bắt buộc)
            preferences = st.text_area(
                "Sở thích cá nhân: *",
                placeholder="Ví dụ: Thích lập trình web, quan tâm đến AI, muốn làm việc với dữ liệu...",
                height=100,
                help="Thông tin này là bắt buộc để tạo lộ trình học cá nhân hóa"
            )
            
            # Nhập điểm mạnh
            strengths = st.text_area(
                "Điểm mạnh của bạn:",
                placeholder="Ví dụ: Giỏi toán, có khả năng tư duy logic, thích giải quyết vấn đề...",
                height=80
            )
            
            # Nhập điểm yếu
            weaknesses = st.text_area(
                "Điểm yếu cần cải thiện:",
                placeholder="Ví dụ: Chưa có kinh nghiệm lập trình, khó khăn trong việc học ngoại ngữ...",
                height=80
            )
        
        # Main content - chỉ có một tab duy nhất
        self.render_integrated_tab(student_name, student_gpa, preferences, strengths, weaknesses)
        
        # Thêm tab lịch sử và thống kê
        with st.sidebar:
            st.markdown("---")
            
            # Khởi tạo session state cho việc hiển thị lịch sử
            if 'show_history' not in st.session_state:
                st.session_state.show_history = False
            
            # Nút toggle để bật/tắt lịch sử
            if st.session_state.show_history:
                if st.button("❌ Đóng Lịch sử", type="secondary"):
                    st.session_state.show_history = False
                    st.rerun()
            else:
                if st.button("📊 Xem Lịch sử & Thống kê", type="secondary"):
                    st.session_state.show_history = True
                    st.rerun()
            
            # Hiển thị lịch sử nếu được bật
            if st.session_state.show_history:
                st.markdown("---")
                self.show_history_and_stats(student_name)
    
    def render_integrated_tab(self, student_name, student_gpa, preferences, strengths, weaknesses):
        """Hiển thị tab tích hợp lộ trình học và phân tích môn học"""
        st.header("🎯 Lộ trình Học & Phân tích Môn học Tích hợp")
        
        # Kiểm tra validation
        if not preferences or preferences.strip() == "":
            st.warning("⚠️ Vui lòng nhập sở thích cá nhân để tạo lộ trình học!")
            st.info("💡 Sở thích giúp hệ thống tạo lộ trình học phù hợp với định hướng nghề nghiệp của bạn.")
            return
        
        # Chọn vị trí mục tiêu
        positions = self.data_processor.load_positions()
        if positions:
            target_position = st.selectbox(
                "Chọn vị trí mục tiêu:",
                options=positions,
                index=0
            )
            
            if st.button("🚀 Tạo Lộ trình Học & Phân tích Môn học", type="primary"):
                # Load dữ liệu môn học
                courses = self.data_processor.load_courses()
                
                with st.spinner("Đang tạo lộ trình học và phân tích môn học..."):
                    result = self.gemini_client.generate_learning_path(
                        target_position=target_position,
                        student_gpa=student_gpa,
                        preferences=preferences,
                        strengths=strengths,
                        weaknesses=weaknesses,
                        courses_data=courses
                    )
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    # Tự động lưu vào database
                    try:
                        student_data = {
                            'student_name': student_name,
                            'gpa': student_gpa,
                            'preferences': preferences,
                            'strengths': strengths,
                            'weaknesses': weaknesses
                        }
                        learning_path_id = self.db_manager.save_learning_path(student_data, result)
                        st.success(f"✅ Đã tự động lưu vào database! ID: {learning_path_id}")
                    except Exception as e:
                        st.warning(f"⚠️ Lưu vào database thất bại: {str(e)}")
                    
                    self.display_integrated_results(result, student_name, student_gpa, preferences, strengths, weaknesses)
        else:
            st.error("Không thể đọc danh sách vị trí")
    
    def display_integrated_results(self, result, student_name, student_gpa, preferences, strengths, weaknesses):
        """Hiển thị kết quả tích hợp lộ trình học và phân tích môn học"""
        st.success("✅ Đã tạo lộ trình học và phân tích môn học thành công!")
        
        # Thông tin tổng quan
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Vị trí mục tiêu", result.get("target_position", "N/A"))
        with col2:
            st.metric("Tổng thời gian", result.get("overall_timeline", "N/A"))
        with col3:
            course_analysis = result.get("course_analysis", {})
            important_courses = course_analysis.get("important_courses", [])
            st.metric("Môn học quan trọng", f"{len(important_courses)}/5")
        
        # Nút lưu vào database và xuất file
        st.markdown("---")
        # Nút lưu vào database (đã tự động lưu)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("💾 Lưu vào Database", type="secondary", disabled=True):
                st.info("ℹ️ Lộ trình học đã được tự động lưu vào database!")
        
        # Tạo tabs để hiển thị cả hai phần
        tab1, tab2, tab3 = st.tabs(["🗺️ Lộ trình Học", "📚 Phân tích Môn học", "💡 Đề xuất Kỹ năng"])
        
        with tab1:
            self.display_learning_path_section(result)
        
        with tab2:
            self.display_course_analysis_section(result)
        
        with tab3:
            self.display_skill_suggestions_section(result)
    
    def display_learning_path_section(self, result):
        """Hiển thị phần lộ trình học"""
        # Phân tích
        st.subheader("📊 Phân tích Vị trí")
        st.write(result.get("analysis", "Không có phân tích"))
        
        # Lộ trình học chi tiết
        st.subheader("📈 Lộ trình Học Chi tiết")
        learning_path = result.get("learning_path", [])
        
        for i, step in enumerate(learning_path, 1):
            with st.expander(f"Bước {i}: {step.get('domain', 'N/A')} ({step.get('difficulty_level', 'N/A')})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Kỹ năng cần học:**")
                    for skill in step.get("skills", []):
                        st.write(f"• {skill}")
                
                with col2:
                    st.write(f"**Thời gian:** {step.get('timeline', 'N/A')}")
                    st.write("**Tài nguyên:**")
                    for resource in step.get("resources", []):
                        st.write(f"• {resource}")
        
        # Lời khuyên
        st.subheader("💡 Lời khuyên")
        st.write(result.get("recommendations", "Không có lời khuyên"))
    
    def display_course_analysis_section(self, result):
        """Hiển thị phần phân tích môn học"""
        course_analysis = result.get("course_analysis", {})
        
        # Tổng quan phân tích
        st.subheader("📊 Tổng quan Phân tích Môn học")
        st.write(course_analysis.get("analysis_summary", "Không có tổng quan"))
        
        # 5 môn học quan trọng nhất
        st.subheader("⭐ Các môn học Quan trọng")
        important_courses = course_analysis.get("important_courses", [])
        
        for i, course in enumerate(important_courses, 1):
            with st.expander(f"#{i} {course.get('name', 'N/A')} ({course.get('credits', 'N/A')} tín chỉ)"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Điểm quan trọng", f"{course.get('importance_score', 'N/A')}/10")
                    st.write("**Lý do quan trọng:**")
                    st.write(course.get("reason", "Không có lý do"))
                
                with col2:
                    st.write("**Lời khuyên học tập:**")
                    st.write(course.get("study_tips", "Không có lời khuyên"))
        
        # Lời khuyên chung
        st.subheader("💡 Lời khuyên Chung về Học tập")
        st.write(course_analysis.get("general_recommendations", "Không có lời khuyên"))
    
    def display_skill_suggestions_section(self, result):
        """Hiển thị phần đề xuất kỹ năng"""
        skill_suggestions = result.get("skill_suggestions", {})
        
        if not skill_suggestions:
            st.info("Không có đề xuất kỹ năng nào")
            return
        
        st.subheader("🎯 Đề xuất Kỹ năng Cá nhân hóa")
        st.write("Dựa trên điểm mạnh và điểm yếu của bạn, hệ thống đề xuất các kỹ năng bổ sung để:")
        st.write("• Tận dụng tối đa điểm mạnh hiện có")
        st.write("• Cải thiện những điểm yếu cần khắc phục") 
        st.write("• Mở rộng cơ hội nghề nghiệp trong tương lai")
        
        # Kỹ năng dựa trên điểm mạnh
        strength_skills = skill_suggestions.get("strength_based_skills", [])
        if strength_skills:
            st.subheader("💪 Kỹ năng Dựa trên Điểm mạnh")
            st.write("Những kỹ năng này sẽ giúp bạn phát huy tối đa điểm mạnh hiện có:")
            
            for i, skill in enumerate(strength_skills, 1):
                with st.expander(f"#{i} {skill.get('skill_name', 'N/A')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Lý do đề xuất:**")
                        st.write(skill.get("reason", "Không có lý do"))
                        st.write("**Lợi ích:**")
                        st.write(skill.get("benefit", "Không có thông tin"))
                    
                    with col2:
                        st.write("**Cách học:**")
                        st.write(skill.get("learning_path", "Không có hướng dẫn"))
        
        # Kỹ năng cải thiện điểm yếu
        weakness_skills = skill_suggestions.get("weakness_improvement_skills", [])
        if weakness_skills:
            st.subheader("🔧 Kỹ năng Cải thiện Điểm yếu")
            st.write("Những kỹ năng này sẽ giúp bạn khắc phục những điểm yếu hiện tại:")
            
            for i, skill in enumerate(weakness_skills, 1):
                with st.expander(f"#{i} {skill.get('skill_name', 'N/A')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Lý do đề xuất:**")
                        st.write(skill.get("reason", "Không có lý do"))
                        st.write("**Lợi ích:**")
                        st.write(skill.get("benefit", "Không có thông tin"))
                    
                    with col2:
                        st.write("**Cách học:**")
                        st.write(skill.get("learning_path", "Không có hướng dẫn"))
        
        # Kỹ năng mở rộng cơ hội
        expansion_skills = skill_suggestions.get("career_expansion_skills", [])
        if expansion_skills:
            st.subheader("🚀 Kỹ năng Mở rộng Cơ hội")
            st.write("Những kỹ năng này sẽ mở ra nhiều cơ hội nghề nghiệp mới:")
            
            for i, skill in enumerate(expansion_skills, 1):
                with st.expander(f"#{i} {skill.get('skill_name', 'N/A')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Lý do đề xuất:**")
                        st.write(skill.get("reason", "Không có lý do"))
                        st.write("**Lợi ích:**")
                        st.write(skill.get("benefit", "Không có thông tin"))
                    
                    with col2:
                        st.write("**Cách học:**")
                        st.write(skill.get("learning_path", "Không có hướng dẫn"))
        
        # Lời khuyên tổng hợp
        st.markdown("---")
        st.subheader("💡 Lời khuyên Tổng hợp")
        st.write("• **Ưu tiên học tập:** Bắt đầu với những kỹ năng cải thiện điểm yếu")
        st.write("• **Phát huy điểm mạnh:** Tiếp tục phát triển những kỹ năng bạn đã giỏi")
        st.write("• **Mở rộng tầm nhìn:** Khám phá những kỹ năng mới để có nhiều lựa chọn nghề nghiệp")
        st.write("• **Thực hành thường xuyên:** Áp dụng những kỹ năng đã học vào các dự án thực tế")
    
    def save_to_database(self, result, student_name, student_gpa, preferences, strengths, weaknesses):
        """Lưu kết quả vào database"""
        try:
            student_data = {
                'student_name': student_name,
                'gpa': student_gpa,
                'preferences': preferences,
                'strengths': strengths,
                'weaknesses': weaknesses
            }
            
            learning_path_id = self.db_manager.save_learning_path(student_data, result)
            st.success(f"✅ Đã lưu vào database thành công! ID: {learning_path_id}")
            
        except Exception as e:
            st.error(f"❌ Lỗi khi lưu vào database: {str(e)}")
    
    
    def show_history_and_stats(self, student_name):
        """Hiển thị lịch sử và thống kê"""
        st.subheader("📊 Lịch sử & Thống kê")
        
        # Thống kê tổng quan (compact)
        stats = self.db_manager.get_statistics()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Sinh viên", stats['total_students'])
        with col2:
            st.metric("Lộ trình", stats['total_paths'])
        
        # Top vị trí mục tiêu (compact)
        st.write("**🏆 Top Vị trí:**")
        if stats['top_positions']:
            for i, pos in enumerate(stats['top_positions'][:3], 1):
                st.write(f"{i}. {pos['position']} ({pos['count']})")
        else:
            st.write("Chưa có dữ liệu")
        
        # Lịch sử của sinh viên (compact)
        if student_name != "Sinh viên":
            st.write(f"**📚 Lịch sử {student_name}:**")
            history = self.db_manager.get_student_history(student_name)
            
            if history:
                for record in history[:3]:  # Chỉ hiển thị 3 record gần nhất
                    with st.expander(f"{record['target_position'][:20]}... - {record['created_at'][:10]}"):
                        st.write(f"**GPA:** {record['gpa']}")
                        st.write(f"**Ngày:** {record['created_at'][:16]}")
                        
                        if st.button("Xem chi tiết", key=f"view_{record['id']}"):
                            st.session_state[f"show_details_{record['id']}"] = True
                            st.rerun()
                        
                        # Hiển thị chi tiết nếu được yêu cầu
                        if st.session_state.get(f"show_details_{record['id']}", False):
                            self.show_learning_path_details(record['id'])
                            if st.button("Đóng chi tiết", key=f"close_{record['id']}"):
                                st.session_state[f"show_details_{record['id']}"] = False
                                st.rerun()
            else:
                st.info("Chưa có lịch sử")
    
    def show_learning_path_details(self, learning_path_id):
        """Hiển thị chi tiết lộ trình học"""
        details = self.db_manager.get_learning_path_details(learning_path_id)
        
        if details:
            st.markdown("---")
            st.subheader(f"📋 Chi tiết: {details['target_position']}")
            
            # Thông tin cơ bản
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Sinh viên:** {details['student_name']}")
                st.write(f"**GPA:** {details['gpa']}")
            with col2:
                st.write(f"**Ngày tạo:** {details['created_at']}")
                st.write(f"**Timeline:** {details['overall_timeline']}")
            
            # Lộ trình học
            st.subheader("📚 Lộ trình Học")
            for i, step in enumerate(details['learning_path'], 1):
                st.markdown(f"**Bước {i}: {step['domain']}**")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"• **Độ khó:** {step['difficulty_level']}")
                    st.write(f"• **Thời gian:** {step['timeline']}")
                with col2:
                    st.write(f"• **Kỹ năng:** {', '.join(step['skills'])}")
                    st.write(f"• **Tài nguyên:** {', '.join(step['resources'])}")
                st.markdown("---")
            
            # Môn học quan trọng
            st.subheader("⭐ Môn học Quan trọng")
            for course in details['course_analysis']['important_courses']:
                st.write(f"• **{course['name']}** ({course['credits']} tín chỉ) - {course['importance_score']}")
            
            # Lời khuyên chung
            if details['course_analysis'].get('general_recommendations'):
                st.subheader("💡 Lời khuyên Chung")
                st.write(details['course_analysis']['general_recommendations'])
        else:
            st.error("Không tìm thấy chi tiết lộ trình học")
    

if __name__ == "__main__":
    app = LearningPathApp()
    app.run()
