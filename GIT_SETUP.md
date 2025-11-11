# 🚀 Hướng dẫn Kết nối với GitHub Repository

## Bước 1: Tạo Repository trên GitHub

1. Đăng nhập vào [GitHub](https://github.com)
2. Click nút **"New"** hoặc **"+"** ở góc trên bên phải → chọn **"New repository"**
3. Điền thông tin:
   - **Repository name**: `personalized-learning-path` (hoặc tên bạn muốn)
   - **Description**: "Hệ thống cá nhân hóa lộ trình học với Gemini API"
   - Chọn **Public** hoặc **Private**
   - **KHÔNG** tích "Add a README file" (vì bạn đã có code)
   - **KHÔNG** tích "Add .gitignore" (đã có sẵn)
   - **KHÔNG** chọn license
4. Click **"Create repository"**

## Bước 2: Kết nối Local Repository với GitHub

Sau khi tạo repository, GitHub sẽ hiển thị hướng dẫn. Bạn có 2 cách:

### Cách 1: Sử dụng HTTPS (Dễ nhất)

```bash
# Thay YOUR_USERNAME và YOUR_REPO_NAME bằng thông tin của bạn
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

**Ví dụ:**
```bash
git remote add origin https://github.com/nguyenvana/personalized-learning-path.git
```

### Cách 2: Sử dụng SSH (Nếu đã setup SSH key)

```bash
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
```

## Bước 3: Thêm và Commit Code

```bash
# Xem các file sẽ được thêm
git status

# Thêm tất cả file (theo .gitignore)
git add .

# Kiểm tra lại các file sẽ commit (đảm bảo KHÔNG có .env, *.db)
git status

# Commit code
git commit -m "Initial commit: Hệ thống cá nhân hóa lộ trình học"
```

## Bước 4: Push Code lên GitHub

```bash
# Đổi tên branch thành main (nếu cần)
git branch -M main

# Push code lên GitHub
git push -u origin main
```

Nếu lần đầu push, GitHub sẽ yêu cầu đăng nhập:
- **HTTPS**: Nhập username và Personal Access Token (không phải password)
- **SSH**: Không cần đăng nhập nếu đã setup SSH key

## ⚠️ Lưu ý quan trọng

### Kiểm tra trước khi commit:

```bash
# Xem các file sẽ được commit
git status
```

**Đảm bảo KHÔNG có:**
- ❌ `.env` (file chứa API key)
- ❌ `*.db` (database files)
- ❌ `__pycache__/`
- ❌ `Scripts/`, `Lib/`, `Include/` (virtual environment)

**Chỉ nên có:**
- ✅ `*.py` (source code)
- ✅ `data/*.csv`, `data/*.txt` (data files)
- ✅ `requirements.txt`
- ✅ `.gitignore`
- ✅ `README.md`, `PROJECT_SUMMARY.txt` (documentation)

### Nếu vô tình commit file nhạy cảm:

```bash
# Xóa file khỏi Git (nhưng giữ lại trên máy)
git rm --cached .env
git commit -m "Remove .env file"
git push
```

## Các lệnh hữu ích

### Xem remote đã thêm:
```bash
git remote -v
```

### Thay đổi remote URL:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

### Xóa remote (nếu cần):
```bash
git remote remove origin
```

### Xem log commit:
```bash
git log --oneline
```

### Xem thay đổi:
```bash
git diff
```

## Tạo Personal Access Token (nếu dùng HTTPS)

Nếu GitHub yêu cầu token thay vì password:

1. Vào GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Đặt tên token (ví dụ: "My Project")
4. Chọn scope: **repo** (full control)
5. Click "Generate token"
6. **Copy token ngay** (chỉ hiển thị 1 lần)
7. Dùng token này thay cho password khi push

## Hoàn tất! 🎉

Sau khi push thành công, bạn có thể:
- Xem code trên GitHub: `https://github.com/YOUR_USERNAME/YOUR_REPO_NAME`
- Clone repository ở máy khác
- Chia sẻ với người khác

