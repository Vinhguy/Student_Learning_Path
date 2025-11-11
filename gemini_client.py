import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME, TEMPERATURE, MAX_OUTPUT_TOKENS
import json

class GeminiClient:
    def __init__(self):
        """Khởi tạo client Gemini"""
        if not GEMINI_API_KEY:
            raise ValueError("Vui lòng cung cấp GEMINI_API_KEY trong file .env")
        
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(MODEL_NAME)
        
    def generate_learning_path(self, target_position, student_gpa=None, preferences=None, strengths=None, weaknesses=None, courses_data=None):
        """
        Tạo lộ trình học đến vị trí mục tiêu và phân tích môn học
        
        Args:
            target_position (str): Vị trí mục tiêu
            student_gpa (float): Điểm GPA của sinh viên
            preferences (str): Sở thích cá nhân
            strengths (str): Điểm mạnh của sinh viên
            weaknesses (str): Điểm yếu cần cải thiện
            courses_data (list): Danh sách môn học để phân tích
            
        Returns:
            dict: Lộ trình học và phân tích môn học được cá nhân hóa
        """
        prompt = f"""
        Bạn là một chuyên gia tư vấn nghề nghiệp CNTT. Hãy tạo một lộ trình học chi tiết để đạt được vị trí "{target_position}" và phân tích các môn học quan trọng.

        Thông tin sinh viên:
        - Điểm GPA: {student_gpa if student_gpa else 'Chưa có'}
        - Sở thích: {preferences if preferences else 'Chưa có'}
        - Điểm mạnh: {strengths if strengths else 'Chưa có'}
        - Điểm yếu cần cải thiện: {weaknesses if weaknesses else 'Chưa có'}
        
        Danh sách môn học có sẵn:
        {self._format_courses_for_prompt(courses_data) if courses_data else 'Chưa có danh sách môn học'}
        
        Yêu cầu:
        1. Phân tích vị trí "{target_position}" và xác định các domain kiến thức cần thiết
        2. Sắp xếp các domain từ dễ đến khó
        3. Với mỗi domain, liệt kê các kỹ năng cụ thể cần học
        4. Đưa ra timeline học tập phù hợp với trình độ hiện tại
        5. Gợi ý các tài nguyên học tập (khóa học, sách, project thực hành)
        6. Phân tích và chọn 5 môn học quan trọng nhất từ danh sách có sẵn
        7. Giải thích lý do chọn từng môn và đưa ra lời khuyên học tập
        8. Tận dụng điểm mạnh và đưa ra giải pháp cải thiện điểm yếu
        9. Đưa ra đề xuất kỹ năng bổ sung dựa trên điểm mạnh/điểm yếu để mở rộng cơ hội nghề nghiệp
        
        QUAN TRỌNG: 
        - Chỉ trả về JSON hợp lệ, không có text thêm
        - TẤT CẢ nội dung trong JSON phải được viết bằng TIẾNG VIỆT
        - Không sử dụng tiếng Anh trong bất kỳ phần nào của response
        
        Cấu trúc JSON:
        {{
            "target_position": "{target_position}",
            "analysis": "Phân tích về vị trí này",
            "learning_path": [
                {{
                    "domain": "Tên lĩnh vực",
                    "difficulty_level": "Cơ bản",
                    "skills": ["Kỹ năng 1", "Kỹ năng 2"],
                    "timeline": "Thời gian học",
                    "resources": ["Tài nguyên 1", "Tài nguyên 2"]
                }}
            ],
            "overall_timeline": "Tổng thời gian học",
            "recommendations": "Lời khuyên cá nhân hóa",
            "skill_suggestions": {{
                "strength_based_skills": [
                    {{
                        "skill_name": "Tên kỹ năng",
                        "reason": "Lý do đề xuất dựa trên điểm mạnh",
                        "benefit": "Lợi ích cho nghề nghiệp",
                        "learning_path": "Cách học kỹ năng này"
                    }}
                ],
                "weakness_improvement_skills": [
                    {{
                        "skill_name": "Tên kỹ năng",
                        "reason": "Lý do đề xuất để cải thiện điểm yếu",
                        "benefit": "Lợi ích khi cải thiện",
                        "learning_path": "Cách học kỹ năng này"
                    }}
                ],
                "career_expansion_skills": [
                    {{
                        "skill_name": "Tên kỹ năng",
                        "reason": "Lý do đề xuất để mở rộng cơ hội",
                        "benefit": "Lợi ích cho sự nghiệp",
                        "learning_path": "Cách học kỹ năng này"
                    }}
                ]
            }},
            "course_analysis": {{
                "analysis_summary": "Tổng quan phân tích môn học",
                "important_courses": [
                    {{
                        "name": "Tên môn học",
                        "credits": "Số tín chỉ",
                        "importance_score": "8/10",
                        "reason": "Lý do quan trọng",
                        "study_tips": "Lời khuyên học tập"
                    }}
                ],
                "general_recommendations": "Lời khuyên chung về việc học tập"
            }}
        }}
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=TEMPERATURE,
                    max_output_tokens=MAX_OUTPUT_TOKENS
                )
            )
            
            # Debug: In ra response để kiểm tra
            print(f"Debug - Raw response: {response.text}")
            
            # Kiểm tra response có tồn tại không
            if not response.text:
                return {"error": "API không trả về dữ liệu"}
            
            # Thử parse JSON, nếu thất bại thì tạo JSON từ text
            try:
                cleaned_text = self._clean_json_response(response.text)
                result = json.loads(cleaned_text)
            except json.JSONDecodeError:
                # Nếu không phải JSON hợp lệ, tạo response mẫu
                result = self._create_fallback_response(response.text, target_position, courses_data, strengths, weaknesses)
            
            return result
            
        except Exception as e:
            return {"error": f"Lỗi khi tạo lộ trình học: {str(e)}"}
    
    def analyze_courses(self, courses_data, target_position=None, student_gpa=None):
        """
        Phân tích danh sách môn học để chọn 5 môn quan trọng nhất
        
        Args:
            courses_data (list): Danh sách môn học
            target_position (str): Vị trí mục tiêu
            student_gpa (float): Điểm GPA của sinh viên
            
        Returns:
            dict: Phân tích và 5 môn học quan trọng nhất
        """
        courses_text = "\n".join([f"- {course['name']} ({course['credits']} tín chỉ)" for course in courses_data])
        
        prompt = f"""
        Bạn là một chuyên gia giáo dục CNTT. Hãy phân tích danh sách môn học sau và chọn ra 5 môn học quan trọng nhất:

        Danh sách môn học:
        {courses_text}
        
        Thông tin bổ sung:
        - Vị trí mục tiêu: {target_position if target_position else 'Chưa xác định'}
        - Điểm GPA: {student_gpa if student_gpa else 'Chưa có'}
        
        Yêu cầu:
        1. Phân tích tầm quan trọng của từng môn học
        2. Chọn 5 môn học quan trọng nhất dựa trên:
           - Tính cần thiết cho nghề nghiệp CNTT
           - Nền tảng cho các môn học khác
           - Tính thực tiễn và ứng dụng
           - Phù hợp với vị trí mục tiêu (nếu có)
        3. Giải thích lý do chọn từng môn
        4. Đưa ra lời khuyên học tập cho từng môn
        
        QUAN TRỌNG: Chỉ trả về JSON hợp lệ, không có text thêm. Cấu trúc JSON:
        {{
            "analysis_summary": "Tổng quan phân tích",
            "important_courses": [
                {{
                    "name": "Tên môn học",
                    "credits": "Số tín chỉ",
                    "importance_score": "8/10",
                    "reason": "Lý do quan trọng",
                    "study_tips": "Lời khuyên học tập"
                }}
            ],
            "general_recommendations": "Lời khuyên chung về việc học tập"
        }}
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=TEMPERATURE,
                    max_output_tokens=MAX_OUTPUT_TOKENS
                )
            )
            
            # Debug: In ra response để kiểm tra
            print(f"Debug - Raw response: {response.text}")
            
            # Kiểm tra response có tồn tại không
            if not response.text:
                return {"error": "API không trả về dữ liệu"}
            
            # Thử parse JSON, nếu thất bại thì tạo JSON từ text
            try:
                cleaned_text = self._clean_json_response(response.text)
                result = json.loads(cleaned_text)
            except json.JSONDecodeError:
                # Nếu không phải JSON hợp lệ, tạo response mẫu
                result = self._create_course_fallback_response(response.text, courses_data)
            
            return result
            
        except Exception as e:
            return {"error": f"Lỗi khi phân tích môn học: {str(e)}"}
    
    def _format_courses_for_prompt(self, courses_data):
        """Format danh sách môn học cho prompt"""
        if not courses_data:
            return "Chưa có danh sách môn học"
        
        courses_text = "\n".join([f"- {course['name']} ({course['credits']} tín chỉ)" for course in courses_data])
        return courses_text
    
    def _clean_json_response(self, text):
        """Làm sạch response text để có thể parse JSON"""
        import re
        
        # Loại bỏ markdown formatting
        text = text.replace('```json', '').replace('```', '')
        
        # Tìm JSON block đầu tiên
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json_match.group(0)
        
        # Nếu không tìm thấy, trả về text gốc
        return text.strip()
    
    def _create_fallback_response(self, response_text, target_position, courses_data=None, strengths=None, weaknesses=None):
        """Tạo response mẫu khi không parse được JSON"""
        # Tạo course analysis mẫu
        course_analysis = {
            "analysis_summary": "Phân tích dựa trên tầm quan trọng của các môn học",
            "important_courses": [],
            "general_recommendations": "Hãy học tập có hệ thống và thực hành thường xuyên"
        }
        
        if courses_data:
            sample_courses = courses_data[:5] if len(courses_data) >= 5 else courses_data
            for i, course in enumerate(sample_courses):
                course_analysis["important_courses"].append({
                    "name": course['name'],
                    "credits": course['credits'],
                    "importance_score": f"{9-i}/10",
                    "reason": "Môn học quan trọng cho nền tảng CNTT",
                    "study_tips": "Nên tập trung học kỹ và thực hành nhiều"
                })
        
        # Tạo lời khuyên dựa trên điểm mạnh và điểm yếu
        recommendations = "Hãy tập trung vào việc học từng bước một cách có hệ thống"
        if strengths:
            recommendations += f". Tận dụng điểm mạnh của bạn: {strengths}"
        if weaknesses:
            recommendations += f". Cần cải thiện: {weaknesses}"
        
        return {
            "target_position": target_position,
            "analysis": f"Phân tích về vị trí {target_position}",
            "learning_path": [
                {
                    "domain": "Kiến thức cơ bản",
                    "difficulty_level": "Cơ bản",
                    "skills": ["Kỹ năng cơ bản", "Nền tảng lý thuyết"],
                    "timeline": "3-6 tháng",
                    "resources": ["Tài liệu học tập", "Khóa học trực tuyến"]
                },
                {
                    "domain": "Kỹ năng chuyên môn",
                    "difficulty_level": "Trung cấp", 
                    "skills": ["Kỹ năng chuyên sâu", "Thực hành"],
                    "timeline": "6-12 tháng",
                    "resources": ["Dự án thực tế", "Mentorship"]
                }
            ],
            "overall_timeline": "12-18 tháng",
            "recommendations": recommendations,
            "skill_suggestions": {
                "strength_based_skills": [
                    {
                        "skill_name": "Kỹ năng mềm",
                        "reason": "Dựa trên điểm mạnh của bạn",
                        "benefit": "Tăng cường khả năng làm việc nhóm và giao tiếp",
                        "learning_path": "Tham gia các hoạt động nhóm, khóa học kỹ năng mềm"
                    }
                ],
                "weakness_improvement_skills": [
                    {
                        "skill_name": "Kỹ năng phân tích",
                        "reason": "Giúp cải thiện điểm yếu hiện tại",
                        "benefit": "Tăng khả năng giải quyết vấn đề",
                        "learning_path": "Thực hành với các bài tập phân tích, case study"
                    }
                ],
                "career_expansion_skills": [
                    {
                        "skill_name": "Kỹ năng lãnh đạo",
                        "reason": "Mở rộng cơ hội thăng tiến",
                        "benefit": "Có thể đảm nhận vai trò quản lý trong tương lai",
                        "learning_path": "Tham gia các dự án nhóm, học về quản lý dự án"
                    }
                ]
            },
            "course_analysis": course_analysis,
            "raw_response": response_text[:500] + "..." if len(response_text) > 500 else response_text
        }
    
    def _create_course_fallback_response(self, response_text, courses_data):
        """Tạo response mẫu cho phân tích môn học"""
        # Chọn 5 môn đầu tiên làm mẫu
        sample_courses = courses_data[:5] if len(courses_data) >= 5 else courses_data
        
        important_courses = []
        for i, course in enumerate(sample_courses):
            important_courses.append({
                "name": course['name'],
                "credits": course['credits'],
                "importance_score": f"{9-i}/10",
                "reason": "Môn học quan trọng cho nền tảng CNTT",
                "study_tips": "Nên tập trung học kỹ và thực hành nhiều"
            })
        
        return {
            "analysis_summary": "Phân tích dựa trên tầm quan trọng của các môn học",
            "important_courses": important_courses,
            "general_recommendations": "Hãy học tập có hệ thống và thực hành thường xuyên",
            "raw_response": response_text[:500] + "..." if len(response_text) > 500 else response_text
        }
