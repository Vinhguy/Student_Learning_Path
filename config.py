# Cấu hình cho ứng dụng cá nhân hóa lộ trình học
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# File paths
VI_TRI_FILE = 'data/vi_tri.csv'
MON_HOC_FILE = 'data/danh_sach_monhoc.csv'
GPA_FILE = 'data/GPA.txt'

# Model configuration
MODEL_NAME = 'gemini-2.0-flash'
TEMPERATURE = 0.7
MAX_OUTPUT_TOKENS = 2048
