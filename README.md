<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
   Hệ thống lộ trình học tập dành cho sinh viên dựa theo điểm số và sở thích
</h2>
<div align="center">
    <p align="center">
      <img src="https://github.com/Tank97king/LapTrinhMang/blob/main/CHAT%20TCP/%E1%BA%A2nh/aiotlab_logo.png?raw=true" alt="AIoTLab Logo" width="170"/>
      <img src="https://github.com/Tank97king/LapTrinhMang/blob/main/CHAT%20TCP/%E1%BA%A2nh/fitdnu_logo.png?raw=true" alt="FITDNU Logo" width="180"/>
      <img src="https://github.com/Tank97king/LapTrinhMang/blob/main/CHAT%20TCP/%E1%BA%A2nh/dnu_logo.png?raw=true" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>



## 📖 1. Giới thiệu hệ thống

**Hệ thống Lộ trình Học tập Cá nhân hóa** là một ứng dụng web thông minh được phát triển bởi **AIoTLab - Khoa Công nghệ Thông tin, Đại học Đại Nam**, sử dụng công nghệ **Trí tuệ Nhân tạo (AI)** thông qua **Google Gemini 2.0 Flash** để hỗ trợ sinh viên xây dựng lộ trình học tập phù hợp với năng lực, sở thích và mục tiêu nghề nghiệp.

### 🎯 Vấn đề giải quyết

Trong quá trình học tập, sinh viên thường gặp phải những thách thức:
- ❌ **Thiếu định hướng học tập rõ ràng**: Không biết nên học môn nào trước, môn nào sau
- ❌ **Khó cá nhân hóa lộ trình**: Mỗi sinh viên có điểm mạnh, điểm yếu và mục tiêu khác nhau nhưng thiếu công cụ phân tích phù hợp
- ❌ **Thiếu thông tin về kỹ năng bổ sung**: Không biết nên phát triển kỹ năng nào ngoài chương trình học chính
- ❌ **Không có hệ thống lưu trữ**: Khó theo dõi và đánh giá tiến độ học tập theo thời gian

### ✨ Tính năng chính

- 🗺️ **Tạo lộ trình học tập cá nhân hóa**: Phân tích GPA, sở thích, điểm mạnh, điểm yếu để xây dựng lộ trình từ cơ bản đến nâng cao với timeline và tài nguyên cụ thể
- 📚 **Phân tích môn học quan trọng**: Đánh giá và đề xuất Top 5 môn học quan trọng nhất cần tập trung dựa trên vị trí nghề nghiệp mục tiêu
- 💡 **Đề xuất kỹ năng bổ sung**: Gợi ý kỹ năng dựa trên điểm mạnh/điểm yếu để mở rộng cơ hội nghề nghiệp và khám phá tiềm năng bản thân
- 💾 **Lưu trữ tự động**: Tự động lưu tất cả lộ trình vào database SQLite để theo dõi lịch sử và thống kê
- 📊 **Quản lý và thống kê**: Xem lịch sử học tập, thống kê tổng quan và phân tích xu hướng

### 🎁 Lợi ích

**Đối với sinh viên:**
- ✅ Định hướng học tập rõ ràng, từng bước từ dễ đến khó
- ✅ Tiết kiệm thời gian, không cần tự tìm hiểu và sắp xếp
- ✅ Cá nhân hóa cao dựa trên profile cá nhân
- ✅ Khám phá điểm mạnh và kỹ năng mới cần phát triển
- ✅ Có hướng dẫn cụ thể để cải thiện điểm yếu

**Đối với nhà trường:**
- ✅ Nâng cao chất lượng đào tạo, hỗ trợ sinh viên học tập hiệu quả hơn
- ✅ Số hóa quy trình tư vấn, giảm tải công việc thủ công
- ✅ Thu thập dữ liệu để phân tích xu hướng và nhu cầu học tập
- ✅ Ứng dụng AI trong giáo dục, thể hiện sự đổi mới

### 📋 Phạm vi ứng dụng

- **8 vị trí nghề nghiệp**: AI Engineer, Data Analyst, Web Developer, Blockchain Developer, System Design, Software Testing, IT Support, Mobile Developer
- **44 môn học IT**: Phân tích các môn học liên quan đến Công nghệ Thông tin
- **Ngôn ngữ**: Tất cả giao diện và kết quả đều bằng tiếng Việt

## 🔧 2. Công nghệ sử dụng

Hệ thống được xây dựng bằng các công nghệ hiện đại và phổ biến trong lĩnh vực phát triển ứng dụng web và AI:

### 🐍 Backend & Core

- **Python 3.x** - Ngôn ngữ lập trình chính
  - Xử lý logic nghiệp vụ
  - Tích hợp với các API và thư viện AI
  - Quản lý dữ liệu và database

- **Streamlit 1.28.1** - Framework web application
  - Xây dựng giao diện người dùng nhanh chóng
  - Tự động tạo UI components (sidebar, tabs, forms)
  - Hỗ trợ responsive design và real-time updates

### 🤖 AI & Machine Learning

- **Google Generative AI (Gemini 2.0 Flash)** - AI Model
  - Model: `gemini-2.0-flash`
  - Temperature: 0.7 (cân bằng giữa sáng tạo và chính xác)
  - Max Output Tokens: 2048
  - Chức năng: Phân tích và tạo lộ trình học tập cá nhân hóa, phân tích môn học, đề xuất kỹ năng

### 💾 Database

- **SQLite** - Embedded database
  - Lưu trữ thông tin sinh viên, lộ trình học, phân tích môn học
  - 7 bảng chính: `students`, `learning_paths`, `learning_steps`, `course_analyses`, `important_courses`, `skill_suggestions`
  - Hỗ trợ foreign keys và indexes để đảm bảo tính toàn vẹn dữ liệu
  - Không cần cấu hình server, dễ triển khai

### 📊 Data Processing

- **Pandas 2.1.4** - Xử lý dữ liệu
  - Đọc và xử lý file CSV (danh sách vị trí, môn học)
  - Đọc file TXT (dữ liệu GPA sinh viên)
  - Chuyển đổi và format dữ liệu cho AI model

- **Tabulate 0.9.0** - Format dữ liệu
  - Hiển thị dữ liệu database dạng bảng
  - Hỗ trợ script quản lý và kiểm tra database

### ⚙️ Configuration & Environment

- **Python-dotenv 1.0.0** - Quản lý biến môi trường
  - Bảo mật API keys trong file `.env`
  - Tách biệt cấu hình giữa môi trường development và production
  - Dễ dàng quản lý các thông tin nhạy cảm



## 🚀 3. Hình ảnh các chức năng

<p align="center">
    <img width="1909" height="888" alt="image" src="https://github.com/user-attachments/assets/7d041817-6559-42d2-83f9-7d20f4865284" />
Giao diện trang chủ
</p>

<p align="center">
    <img width="1358" height="836" alt="image" src="https://github.com/user-attachments/assets/333c2f00-6d94-4067-8033-7d7df11c6a35" />
  <em>Hình 1: Lộ trình học được sinh ra  </em>
</p>

<p align="center">

</p>
<p align="center">
    <img width="1322" height="650" alt="image" src="https://github.com/user-attachments/assets/ad52d984-4779-47b1-8368-c0c131e7278c" />
  <em> Hình 2: Các môn học quan trọng với vị trí chọn</em>
</p>


<p align="center">

</p>
<p align="center">
    <img width="1548" height="798" alt="image" src="https://github.com/user-attachments/assets/8d6b75bb-49e1-4d00-bd26-e2ce1974318f" />
  <em>Hình 3: Đề xuất các kĩ năng tiềm năng</em>
</p>

<p align="center">
<img width="325" height="879" alt="image" src="https://github.com/user-attachments/assets/ccc8475a-3b63-4fa1-9f82-9632b880a3c2" />
</p>
<p align="center">
  <em> Hình 4: Lịch sử các lộ trình học</em>
</p>




## 📝 4. Hướng dẫn cài đặt và sử dụng

### 📋 Yêu cầu hệ thống

- **Python**: 3.8 trở lên
- **Hệ điều hành**: Windows, macOS, hoặc Linux
- **Kết nối Internet**: Để sử dụng Google Gemini API
- **Google Gemini API Key**: Cần đăng ký tại [Google AI Studio](https://makersuite.google.com/app/apikey)

### 🔧 Cài đặt

#### Bước 1: Clone hoặc tải project

```bash
# Nếu có Git repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# Hoặc giải nén file ZIP nếu tải về dạng ZIP
```

#### Bước 2: Tạo Virtual Environment (Khuyến nghị)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Bước 3: Cài đặt Dependencies

Cài đặt tất cả các thư viện cần thiết từ `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Danh sách Dependencies:**

```txt
google-generativeai==0.3.2    # Google Gemini API - Tích hợp AI model
pandas==2.1.4                  # Data processing - Xử lý file CSV/TXT
python-dotenv==1.0.0          # Environment variables - Quản lý API keys
streamlit==1.28.1             # Web framework - Giao diện người dùng
tabulate==0.9.0               # Table formatting - Hiển thị dữ liệu dạng bảng
```

#### Bước 4: Cấu hình môi trường

1. Tạo file `.env` trong thư mục gốc của project:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

2. Mở file `.env` và thêm API key của bạn:

```env
GEMINI_API_KEY=your_api_key_here
```

**Lấy API Key:**
- Truy cập [Google AI Studio](https://makersuite.google.com/app/apikey)
- Đăng nhập bằng tài khoản Google
- Tạo API key mới
- Copy và paste vào file `.env`

#### Bước 5: Khởi tạo Database

Chạy script để tạo database SQLite và các bảng cần thiết:

```bash
python initdb.py
```

Script sẽ:
- Tạo file `learning_paths.db`
- Tạo 7 bảng: `students`, `learning_paths`, `learning_steps`, `course_analyses`, `important_courses`, `skill_suggestions`
- Tạo indexes để tối ưu performance
- (Tùy chọn) Thêm dữ liệu mẫu để test

#### Bước 6: Chạy ứng dụng

```bash
streamlit run app.py
```

Ứng dụng sẽ tự động mở trong trình duyệt tại địa chỉ: `http://localhost:8501`

### 🎮 Hướng dẫn sử dụng

#### 1. Chọn thông tin sinh viên

- Trong sidebar, chọn **"Chọn sinh viên"** từ dropdown
- Hệ thống sẽ tự động load thông tin GPA nếu có trong file `data/GPA.txt`
- Hoặc chọn **"Sinh viên"** để nhập thông tin thủ công

#### 2. Nhập thông tin cá nhân

- **Sở thích cá nhân** (Bắt buộc): Nhập sở thích, định hướng nghề nghiệp
  - Ví dụ: "Thích lập trình web, quan tâm đến AI, muốn làm việc với dữ liệu..."
  
- **Điểm mạnh** (Tùy chọn): Mô tả các điểm mạnh của bạn
  - Ví dụ: "Giỏi toán, có khả năng tư duy logic, thích giải quyết vấn đề..."
  
- **Điểm yếu cần cải thiện** (Tùy chọn): Mô tả các điểm yếu cần khắc phục
  - Ví dụ: "Chưa có kinh nghiệm lập trình, khó khăn trong việc học ngoại ngữ..."

#### 3. Chọn vị trí mục tiêu

- Chọn **"Vị trí mục tiêu"** từ dropdown
- Có 8 vị trí: AI Engineer, Data Analyst, Web Developer, Blockchain Developer, System Design, Software Testing, IT Support, Mobile Developer

#### 4. Tạo lộ trình học

- Nhấn nút **"🗺️ Tạo Lộ trình Học"**
- Hệ thống sẽ:
  - Gửi thông tin đến Gemini API
  - Phân tích và tạo lộ trình cá nhân hóa
  - Phân tích môn học quan trọng
  - Đề xuất kỹ năng bổ sung
  - **Tự động lưu vào database**

#### 5. Xem kết quả

Kết quả được hiển thị trong 3 tabs:

- **🗺️ Lộ trình Học**: 
  - Phân tích vị trí mục tiêu
  - Các bước học từ dễ đến khó
  - Timeline và tài nguyên học tập
  
- **📚 Phân tích Môn học**: 
  - Top 5 môn học quan trọng nhất
  - Lý do và cách học từng môn
  
- **💡 Đề xuất Kỹ năng**: 
  - Kỹ năng dựa trên điểm mạnh
  - Kỹ năng cải thiện điểm yếu
  - Kỹ năng mở rộng cơ hội nghề nghiệp

#### 6. Xem lịch sử và thống kê

- Nhấn **"📊 Xem Lịch sử & Thống kê"** trong sidebar
- Xem:
  - Thống kê tổng quan (số sinh viên, số lộ trình)
  - Top vị trí được chọn nhiều nhất
  - Lịch sử lộ trình của sinh viên
  - Chi tiết từng lộ trình đã lưu


### 📚 Tài liệu tham khảo

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API](https://ai.google.dev/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)


© 2025 AIoTLab, Faculty of Information Technology, DaiNam University. All rights reserved.

---

