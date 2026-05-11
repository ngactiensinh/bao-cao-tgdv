"""
HỆ THỐNG THU THẬP BÁO CÁO TGDV - PHIÊN BẢN NÂNG CẤP
Cải tiến: giao diện chuyên nghiệp, sửa lỗi logic, tối ưu trích xuất dữ liệu
"""

import streamlit as st
import pandas as pd
import json
@@ -10,448 +15,1159 @@
from openpyxl.utils import get_column_letter

# ==========================================
# CẤU HÌNH & CSS TRANG
# CẤU HÌNH TRANG
# ==========================================
st.set_page_config(page_title="Hệ thống Báo cáo TGDV", page_icon="📊", layout="wide")
st.set_page_config(
    page_title="Hệ thống Báo cáo TGDV",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #f4f6f9; }
    .main-header {color: #004B87; font-weight: 900; text-align: center; text-transform: uppercase; margin-bottom: 25px;}
    .stButton>button {background-color: #004B87; color: white; font-weight: bold; border-radius: 6px;}
    .stButton>button:hover {background-color: #C8102E; color: white;}
    [data-testid="stForm"] {background-color: #ffffff; padding: 25px; border-radius: 12px; border-top: 5px solid #004B87;}
    [data-testid="stExpander"] {background-color: #ffffff; border-left: 4px solid #C8102E; border-radius: 5px; margin-bottom: 10px;}
    .metric-card {background-color: #ffffff; padding: 20px; border-radius: 10px; border-top: 4px solid #C8102E; box-shadow: 0 4px 10px rgba(0,0,0,0.05); text-align: center;}
    .metric-title {font-size: 14px; color: #004B87; font-weight: bold; text-transform: uppercase; margin-bottom: 5px;}
    .metric-number {font-size: 28px; color: #C8102E; font-weight: 900; margin: 0;}
    .section-title {color: #004B87; border-bottom: 3px solid #C8102E; padding-bottom: 5px; margin-top: 30px; margin-bottom: 20px; font-weight: bold; font-size: 20px;}
    .step-header {color: #C8102E; font-weight: bold; margin-top: 20px; margin-bottom: 10px;}
    @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Be Vietnam Pro', sans-serif;
    }

    /* ---- NỀN & LAYOUT CHÍNH ---- */
    .stApp { background-color: #F0F4F8; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    /* ---- HEADER CHÍNH ---- */
    .main-header {
        background: linear-gradient(135deg, #003A6E 0%, #005BAA 60%, #C8102E 100%);
        color: white;
        font-weight: 900;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        padding: 22px 30px;
        border-radius: 14px;
        margin-bottom: 28px;
        font-size: 1.35rem;
        box-shadow: 0 8px 30px rgba(0,74,132,0.25);
    }
    .main-header span { color: #FFD700; }

    /* ---- METRIC CARDS ---- */
    .metric-row { display: flex; gap: 16px; margin-bottom: 24px; }
    .metric-card {
        flex: 1;
        background: white;
        padding: 20px 16px;
        border-radius: 12px;
        border-left: 5px solid #004B87;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        text-align: center;
    }
    .metric-card.red { border-left-color: #C8102E; }
    .metric-card.green { border-left-color: #1A9E5C; }
    .metric-card.gold { border-left-color: #E8A800; }
    .metric-title { font-size: 11px; color: #6B7280; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
    .metric-number { font-size: 32px; color: #003A6E; font-weight: 900; margin: 0; line-height: 1.1; }
    .metric-number.red { color: #C8102E; }
    .metric-number.green { color: #1A9E5C; }
    .metric-number.gold { color: #E8A800; }
    .metric-sub { font-size: 11px; color: #9CA3AF; margin-top: 3px; }

    /* ---- SECTION TITLES ---- */
    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #003A6E;
        font-weight: 800;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-left: 4px solid #C8102E;
        padding-left: 12px;
        margin: 28px 0 16px 0;
    }

    /* ---- FORM & EXPANDERS ---- */
    [data-testid="stForm"] {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 14px;
        border: 1px solid #E5EAF0;
        box-shadow: 0 2px 16px rgba(0,0,0,0.06);
    }
    [data-testid="stExpander"] {
        background-color: #FAFBFD !important;
        border: 1px solid #E5EAF0 !important;
        border-radius: 10px !important;
        margin-bottom: 12px !important;
    }
    [data-testid="stExpander"] summary {
        font-weight: 700 !important;
        color: #003A6E !important;
    }

    /* ---- BUTTONS ---- */
    .stButton>button {
        background-color: #004B87;
        color: white;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #C8102E;
        color: white;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(200,16,46,0.3);
    }

    /* ---- SIDEBAR ---- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #002E5A 0%, #004B87 100%);
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] .stSelectbox label { color: #A8C8E8 !important; font-weight: 600; font-size: 12px; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] { color: #A8C8E8 !important; }
    [data-testid="stSidebar"] .stButton>button { background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3); }
    [data-testid="stSidebar"] .stButton>button:hover { background: #C8102E; }

    /* ---- BADGE TRẠNG THÁI ---- */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 99px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .badge-success { background: #D1FAE5; color: #065F46; }
    .badge-danger { background: #FEE2E2; color: #991B1B; }
    .badge-info { background: #DBEAFE; color: #1E40AF; }

    /* ---- PROGRESS BAR ---- */
    .progress-wrap { background: #E5EAF0; border-radius: 99px; height: 12px; overflow: hidden; margin: 8px 0; }
    .progress-fill { background: linear-gradient(90deg, #004B87, #1A9E5C); height: 100%; border-radius: 99px; transition: width 0.6s ease; }

    /* ---- INFO BOX ---- */
    .info-box {
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-left: 4px solid #3B82F6;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 13px;
        color: #1E40AF;
        margin-bottom: 16px;
    }
    .warning-box {
        background: #FFFBEB;
        border: 1px solid #FDE68A;
        border-left: 4px solid #F59E0B;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 13px;
        color: #92400E;
        margin-bottom: 16px;
    }

    /* ---- TABS ---- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: white;
        padding: 8px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 8px 18px !important;
        color: #6B7280 !important;
    }
    .stTabs [aria-selected="true"] {
        background: #004B87 !important;
        color: white !important;
    }

    /* ---- INPUT FIELDS ---- */
    .stNumberInput label, .stTextInput label, .stSelectbox label, .stTextArea label {
        font-weight: 600 !important;
        font-size: 13px !important;
        color: #374151 !important;
    }

    /* ---- DATAFRAME ---- */
    .stDataFrame { border-radius: 10px; overflow: hidden; }

    /* ---- DIVIDER ---- */
    hr { border: none; border-top: 1px solid #E5EAF0; margin: 20px 0; }

    /* ---- ĐĂNG NHẬP ---- */
    .login-wrap {
        max-width: 420px;
        margin: 60px auto;
        background: white;
        border-radius: 18px;
        padding: 40px 36px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.12);
        border-top: 6px solid #004B87;
    }
    .login-logo {
        text-align: center;
        margin-bottom: 28px;
    }
    .login-logo h2 { color: #003A6E; font-weight: 900; font-size: 1.3rem; margin: 8px 0 4px; }
    .login-logo p { color: #6B7280; font-size: 13px; }
</style>
""", unsafe_allow_html=True)


# ==========================================
# QUẢN LÝ DỮ LIỆU FILE
# CẤU HÌNH DỮ LIỆU
# ==========================================
DATA_FILE = "dulieu_baocao.json"
CONFIG_FILE = "config_donvi.json"

DEFAULT_UNITS = [
    "Đảng ủy Công an tỉnh", "Đảng ủy Quân sự tỉnh", "Đảng ủy các cơ quan Đảng tỉnh", "Đảng ủy Ủy ban nhân dân tỉnh",
    "Phường Mỹ Lâm", "Phường Minh Xuân", "Phường Nông Tiến", "Phường An Tường", "Phường Bình Thuận", "Phường Hà Giang 1", "Phường Hà Giang 2",
    "Xã Thượng Lâm", "Xã Lâm Bình", "Xã Minh Quang", "Xã Bình An", "Xã Côn Lôn", "Xã Yên Hoa", "Xã Thượng Nông", "Xã Hồng Thái", "Xã Nà Hang", "Xã Tân Mỹ", "Xã Yên Lập", "Xã Tân An", "Xã Chiêm Hóa", "Xã Hòa An", "Xã Kiên Đài", "Xã Tri Phú", "Xã Kim Bình", "Xã Yên Nguyên", "Xã Yên Phú", "Xã Bạch Xa", "Xã Phù Lưu", "Xã Hàm Yên", "Xã Bình Xa", "Xã Thái Sơn", "Xã Thái Hòa", "Xã Hùng Lợi", "Xã Trung Sơn", "Xã Thái Bình", "Xã Tân Long", "Xã Xuân Vân", "Xã Lực Hành", "Xã Yên Sơn", "Xã Nhữ Khê", "Xã Tân Trào", "Xã Minh Thanh", "Xã Sơn Dương", "Xã Bình Ca", "Xã Tân Thanh", "Xã Sơn Thủy", "Xã Phú Lương", "Xã Trường Sinh", "Xã Hồng Sơn", "Xã Đông Thọ",
    "Xã Lũng Cú", "Xã Đồng Văn", "Xã Sà Phìn", "Xã Phố Bảng", "Xã Lũng Phìn", "Xã Sủng Máng", "Xã Sơn Vĩ", "Xã Mèo Vạc", "Xã Khâu Vai", "Xã Niêm Sơn", "Xã Tát Ngà", "Xã Thắng Mố", "Xã Bạch Đích", "Xã Yên Minh", "Xã Mậu Duệ", "Xã Du Già", "Xã Đường Thượng", "Xã Lùng Tám", "Xã Cán Tỷ", "Xã Nghĩa Thuận", "Xã Quản Bạ", "Xã Tùng Vài", "Xã Yên Cường", "Xã Đường Hồng", "Xã Bắc Mê", "Xã Minh Ngọc", "Xã Ngọc Đường", "Xã Lao Chải", "Xã Thanh Thủy", "Xã Phú Linh", "Xã Linh Hồ", "Xã Bạch Ngọc", "Xã Vị Xuyên", "Xã Việt Lâm", "Xã Tân Quang", "Xã Đồng Tâm", "Xã Liên Hiệp", "Xã Bằng Hành", "Xã Bắc Quang", "Xã Hùng An", "Xã Vĩnh Tuy", "Xã Đồng Yên", "Xã Tiên Yên", "Xã Xuân Giang", "Xã Bằng Lang", "Xã Yên Thành", "Xã Quang Bình", "Xã Tân Trịnh", "Xã Thông Nguyên", "Xã Hồ Thầu", "Xã Nậm Dịch", "Xã Tân Tiến", "Xã Hoàng Su Phì", "Xã Thàng Tín", "Xã Bản Máy", "Xã Pờ Ly Ngài", "Xã Xín Mần", "Xã Pà Vầy Sủ", "Xã Nấm Dẩn", "Xã Trung Thịnh", "Xã Khuôn Lùng", "Xã Trung Hà", "Xã Kiến Thiết", "Xã Hùng Đức", "Xã Minh Sơn", "Xã Minh Tân", "Xã Thuận Hòa", "Xã Tùng Bá", "Xã Thượng Sơn", "Xã Cao Bồ", "Xã Ngọc Long", "Xã Giáp Trung", "Xã Tiên Nguyên", "Xã Quảng Nguyên"
    "Đảng ủy Công an tỉnh", "Đảng ủy Quân sự tỉnh", "Đảng ủy các cơ quan Đảng tỉnh",
    "Đảng ủy Ủy ban nhân dân tỉnh",
    "Phường Mỹ Lâm", "Phường Minh Xuân", "Phường Nông Tiến", "Phường An Tường",
    "Phường Bình Thuận", "Phường Hà Giang 1", "Phường Hà Giang 2",
    "Xã Thượng Lâm", "Xã Lâm Bình", "Xã Minh Quang", "Xã Bình An", "Xã Côn Lôn",
    "Xã Yên Hoa", "Xã Thượng Nông", "Xã Hồng Thái", "Xã Nà Hang", "Xã Tân Mỹ",
    "Xã Yên Lập", "Xã Tân An", "Xã Chiêm Hóa", "Xã Hòa An", "Xã Kiên Đài",
    "Xã Tri Phú", "Xã Kim Bình", "Xã Yên Nguyên", "Xã Yên Phú", "Xã Bạch Xa",
    "Xã Phù Lưu", "Xã Hàm Yên", "Xã Bình Xa", "Xã Thái Sơn", "Xã Thái Hòa",
    "Xã Hùng Lợi", "Xã Trung Sơn", "Xã Thái Bình", "Xã Tân Long", "Xã Xuân Vân",
    "Xã Lực Hành", "Xã Yên Sơn", "Xã Nhữ Khê", "Xã Tân Trào", "Xã Minh Thanh",
    "Xã Sơn Dương", "Xã Bình Ca", "Xã Tân Thanh", "Xã Sơn Thủy", "Xã Phú Lương",
    "Xã Trường Sinh", "Xã Hồng Sơn", "Xã Đông Thọ",
    "Xã Lũng Cú", "Xã Đồng Văn", "Xã Sà Phìn", "Xã Phố Bảng", "Xã Lũng Phìn",
    "Xã Sủng Máng", "Xã Sơn Vĩ", "Xã Mèo Vạc", "Xã Khâu Vai", "Xã Niêm Sơn",
    "Xã Tát Ngà", "Xã Thắng Mố", "Xã Bạch Đích", "Xã Yên Minh", "Xã Mậu Duệ",
    "Xã Du Già", "Xã Đường Thượng", "Xã Lùng Tám", "Xã Cán Tỷ", "Xã Nghĩa Thuận",
    "Xã Quản Bạ", "Xã Tùng Vài", "Xã Yên Cường", "Xã Đường Hồng", "Xã Bắc Mê",
    "Xã Minh Ngọc", "Xã Ngọc Đường", "Xã Lao Chải", "Xã Thanh Thủy", "Xã Phú Linh",
    "Xã Linh Hồ", "Xã Bạch Ngọc", "Xã Vị Xuyên", "Xã Việt Lâm", "Xã Tân Quang",
    "Xã Đồng Tâm", "Xã Liên Hiệp", "Xã Bằng Hành", "Xã Bắc Quang", "Xã Hùng An",
    "Xã Vĩnh Tuy", "Xã Đồng Yên", "Xã Tiên Yên", "Xã Xuân Giang", "Xã Bằng Lang",
    "Xã Yên Thành", "Xã Quang Bình", "Xã Tân Trịnh", "Xã Thông Nguyên", "Xã Hồ Thầu",
    "Xã Nậm Dịch", "Xã Tân Tiến", "Xã Hoàng Su Phì", "Xã Thàng Tín", "Xã Bản Máy",
    "Xã Pờ Ly Ngài", "Xã Xín Mần", "Xã Pà Vầy Sủ", "Xã Nấm Dẩn", "Xã Trung Thịnh",
    "Xã Khuôn Lùng", "Xã Trung Hà", "Xã Kiến Thiết", "Xã Hùng Đức", "Xã Minh Sơn",
    "Xã Minh Tân", "Xã Thuận Hòa", "Xã Tùng Bá", "Xã Thượng Sơn", "Xã Cao Bồ",
    "Xã Ngọc Long", "Xã Giáp Trung", "Xã Tiên Nguyên", "Xã Quảng Nguyên"
]

DANH_SACH_THANG = [f"Tháng {i}" for i in range(1, 13)]

DICT_DICH_THUAT = {
    "don_vi": "Đơn vị báo cáo", "nguoi_bao_cao": "Người BC / SĐT", "ky_bao_cao": "Kỳ báo cáo", "ngay_nop": "Thời điểm nộp",
    "ld_vanban": "Số VB cấp ủy ban hành", "ld_thammuu": "Số VB tham mưu cấp trên", "ld_cuochop": "Số cuộc họp, hội nghị",
    "nq_hoinghi": "Số hội nghị NQ", "nq_nguoi": "Số người tham gia NQ", "nq_vanban": "Số VB đã triển khai", "nq_tyle": "Tỷ lệ ĐV tham gia (%)",
    "tt_tinbai": "Số tin, bài, pano", "tt_loa": "Số lượt loa truyền thanh", "tt_buoi": "Số buổi TT miệng", "tt_nguoi": "Số người nghe TT", "tt_mxh_bai": "Số bài trên MXH/Cổng TT", "tt_mxh_tuongtac": "Lượt tương tác MXH",
    "dl_baocao": "Số BC DLXH gửi đi", "dl_vande": "Số vấn đề nổi cộm", "dl_xuly": "Số vụ việc đã xử lý",
    "kg_hoatdong": "Số HĐ Văn hóa-Văn nghệ", "kg_chuongtrinh": "Số CT tuyên truyền GD", "kg_lop": "Số buổi Y tế/Môi trường",
    "kg_bd_chuyennghiep": "Số buổi BDNT chuyên nghiệp", "kg_bd_quanchung": "Số buổi BDNT quần chúng", 
    "kg_clb_thanhlap": "Số CLB VH-NT thành lập", "kg_clb_thanhvien": "Số thành viên CLB", 
    "kg_hd_vhtt": "Số HĐ Lễ hội, Thể thao", "kg_khokhan": "Khó khăn Khoa giáo, VH-VN",
    "dv_mh_dangky": "Mô hình DVK đăng ký", "dv_mh_hieuqua": "Mô hình DVK hiệu quả", "dv_mh_moi": "Mô hình mới trong kỳ", "dv_cuocvandong": "Số cuộc vận động, TT", "dv_nguoithamgia": "Số lượt người tham gia", "dv_tiepxuc": "Số buổi đối thoại Nhân dân",
    "nv_duocgiao": "Nhiệm vụ trọng tâm giao", "nv_hoanthanh": "Nhiệm vụ TT hoàn thành", "nv_dangtrienkhai": "Nhiệm vụ đang triển khai", "nv_ketqua": "Kết quả thí điểm nổi bật",
    "bd_tinbai": "Số tin bài CĐS", "bd_cuocthi": "Số cuộc thi CĐS", "kq_tocongnghe": "Số Tổ công nghệ số",
    "ts_chibo": "Tổng số Chi bộ", "kq_chibo_cd": "Số CB SH chuyên đề", "kq_chibo_sotay": "Số CB dùng Sổ tay ĐV",
    "ts_cbccvc": "Tổng số CBCCVC", "kq_cb_ai": "Số CB biết dùng AI", "kq_cb_khoahoc": "Số CB học xong CĐS",
    "ts_nd_truongthanh": "Tổng ND trưởng thành", "kq_nd_kynang": "Số ND có Kỹ năng số", "kq_nd_vneid": "Số ND phổ cập VNeID",
    "kq_nd_smartphone": "Số ND dùng Smartphone", "kq_lop_nd": "Số buổi học cộng đồng",
    "tl_mohinh": "Mô hình hay, sáng tạo", "tl_khokhan": "Khó khăn, vướng mắc chung"
# Schema chuẩn: (key, tên hiển thị, nhóm, kiểu)
# kiểu: "int" | "float" | "text"
SCHEMA = [
    # THÔNG TIN CHUNG
    ("don_vi",               "Đơn vị báo cáo",              "info",   "text"),
    ("nguoi_bao_cao",        "Người BC / SĐT",               "info",   "text"),
    ("ky_bao_cao",           "Kỳ báo cáo",                   "info",   "text"),
    ("ngay_nop",             "Thời điểm nộp",                "info",   "text"),
    # 1. LÃNH ĐẠO CHỈ ĐẠO
    ("ld_vanban",            "VB cấp ủy ban hành",           "ld",     "int"),
    ("ld_thammuu",           "VB tham mưu cấp trên",         "ld",     "int"),
    ("ld_cuochop",           "Cuộc họp, hội nghị",           "ld",     "int"),
    # 2. QUÁN TRIỆT NGHỊ QUYẾT
    ("nq_hoinghi",           "Số hội nghị NQ",               "nq",     "int"),
    ("nq_nguoi",             "Số người tham gia NQ",         "nq",     "int"),
    ("nq_vanban",            "Số VB đã triển khai",          "nq",     "int"),
    ("nq_tyle",              "Tỷ lệ ĐV tham gia (%)",        "nq",     "float"),
    # 3. TUYÊN TRUYỀN
    ("tt_tinbai",            "Số tin, bài, pano",            "tt",     "int"),
    ("tt_loa",               "Lượt loa truyền thanh",        "tt",     "int"),
    ("tt_buoi",              "Số buổi TT miệng",             "tt",     "int"),
    ("tt_nguoi",             "Số người nghe TT",             "tt",     "int"),
    ("tt_mxh_bai",           "Bài trên MXH/Cổng TT",         "tt",     "int"),
    ("tt_mxh_tuongtac",      "Lượt tương tác MXH",           "tt",     "int"),
    # 4. DƯ LUẬN XÃ HỘI
    ("dl_baocao",            "Số BC DLXH gửi đi",           "dl",     "int"),
    ("dl_vande",             "Số vấn đề nổi cộm",           "dl",     "int"),
    ("dl_xuly",              "Số vụ việc đã xử lý",         "dl",     "int"),
    # 5. KHOA GIÁO VH-VN
    ("kg_chuongtrinh",       "Số CT tuyên truyền GD",        "kg",     "int"),
    ("kg_lop",               "Số buổi Y tế/Môi trường",      "kg",     "int"),
    ("kg_bd_chuyennghiep",   "Biểu diễn NT chuyên nghiệp",  "kg",     "int"),
    ("kg_bd_quanchung",      "Biểu diễn NT quần chúng",     "kg",     "int"),
    ("kg_clb_thanhlap",      "Số CLB VH-NT thành lập",      "kg",     "int"),
    ("kg_clb_thanhvien",     "Số thành viên CLB",           "kg",     "int"),
    ("kg_hd_vhtt",           "Số HĐ Lễ hội, Thể thao",     "kg",     "int"),
    ("kg_hoatdong",          "Số HĐ Văn hóa-Văn nghệ",     "kg",     "int"),
    ("kg_khokhan",           "Khó khăn KG, VH-VN",          "kg",     "text"),
    # 6. DÂN VẬN KHÉO
    ("dv_mh_dangky",         "Mô hình DVK đăng ký",         "dv",     "int"),
    ("dv_mh_hieuqua",        "Mô hình DVK hiệu quả",        "dv",     "int"),
    ("dv_mh_moi",            "Mô hình mới trong kỳ",        "dv",     "int"),
    ("dv_cuocvandong",       "Số cuộc vận động, TT",        "dv",     "int"),
    ("dv_nguoithamgia",      "Số lượt người tham gia",      "dv",     "int"),
    ("dv_tiepxuc",           "Số buổi đối thoại ND",        "dv",     "int"),
    # 7. NHIỆM VỤ TRỌNG TÂM
    ("nv_duocgiao",          "Nhiệm vụ TT được giao",       "nv",     "int"),
    ("nv_hoanthanh",         "Nhiệm vụ TT hoàn thành",      "nv",     "int"),
    ("nv_dangtrienkhai",     "Nhiệm vụ đang triển khai",    "nv",     "int"),
    ("nv_ketqua",            "Kết quả nổi bật",             "nv",     "text"),
    # 8. BÌNH DÂN HỌC VỤ SỐ
    ("bd_tinbai",            "Số tin bài CĐS",               "bd",     "int"),
    ("bd_cuocthi",           "Số cuộc thi CĐS",             "bd",     "int"),
    ("kq_tocongnghe",        "Số Tổ công nghệ số",          "bd",     "int"),
    ("ts_chibo",             "Tổng số chi bộ",              "bd",     "int"),
    ("kq_chibo_cd",          "Chi bộ SH chuyên đề số",      "bd",     "int"),
    ("kq_chibo_sotay",       "Chi bộ dùng Sổ tay ĐV",      "bd",     "int"),
    ("ts_cbccvc",            "Tổng số CBCCVC",              "bd",     "int"),
    ("kq_cb_ai",             "CB biết dùng AI",             "bd",     "int"),
    ("kq_cb_khoahoc",        "CB hoàn thành CĐS",           "bd",     "int"),
    ("ts_nd_truongthanh",    "Tổng ND trưởng thành",        "bd",     "int"),
    ("kq_nd_kynang",         "ND có Kỹ năng số",            "bd",     "int"),
    ("kq_nd_vneid",          "ND phổ cập VNeID",            "bd",     "int"),
    ("kq_nd_smartphone",     "ND dùng Smartphone",          "bd",     "int"),
    ("kq_lop_nd",            "Buổi học cộng đồng",          "bd",     "int"),
    # 9. ĐÁNH GIÁ CHUNG
    ("tl_mohinh",            "Mô hình hay, sáng tạo",       "tl",     "text"),
    ("tl_khokhan",           "Khó khăn, vướng mắc chung",   "tl",     "text"),
]

# Tên nhóm cho header Excel
GROUP_LABELS = {
    "info": ("THÔNG TIN CHUNG",              "003A6E"),
    "ld":   ("1. LÃNH ĐẠO, CHỈ ĐẠO",        "C8102E"),
    "nq":   ("2. QUÁN TRIỆT NGHỊ QUYẾT",    "005BAA"),
    "tt":   ("3. CÔNG TÁC TUYÊN TRUYỀN",    "C8102E"),
    "dl":   ("4. DƯ LUẬN XÃ HỘI",           "005BAA"),
    "kg":   ("5. KHOA GIÁO, VH-VN",         "C8102E"),
    "dv":   ("6. DÂN VẬN KHÉO",             "005BAA"),
    "nv":   ("7. NHIỆM VỤ TRỌNG TÂM",       "C8102E"),
    "bd":   ("8. BÌNH DÂN HỌC VỤ SỐ",      "005BAA"),
    "tl":   ("9. ĐÁNH GIÁ CHUNG",           "C8102E"),
}

ALL_KEYS   = [s[0] for s in SCHEMA]
KEY_LABEL  = {s[0]: s[1] for s in SCHEMA}
KEY_GROUP  = {s[0]: s[2] for s in SCHEMA}
KEY_TYPE   = {s[0]: s[3] for s in SCHEMA}
NUM_KEYS   = [s[0] for s in SCHEMA if s[3] in ("int", "float")]
TEXT_KEYS  = [s[0] for s in SCHEMA if s[3] == "text"]


# ==========================================
# HÀM TIỆN ÍCH
# ==========================================
def load_data():
if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f: return json.load(f)
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_units():
if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f: return json.load(f)
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
return DEFAULT_UNITS

def save_units(units):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f: json.dump(units, f, ensure_ascii=False, indent=4)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(units, f, ensure_ascii=False, indent=4)

def get_months_for_filter(filter_type):
    if filter_type == "Quý I": return ["Tháng 1", "Tháng 2", "Tháng 3"]
    if filter_type == "Quý II": return ["Tháng 4", "Tháng 5", "Tháng 6"]
    if filter_type == "Quý III": return ["Tháng 7", "Tháng 8", "Tháng 9"]
    if filter_type == "Quý IV": return ["Tháng 10", "Tháng 11", "Tháng 12"]
    if filter_type == "Cả Năm": return [f"Tháng {i}" for i in range(1, 13)]
    return DANH_SACH_THANG
    mapping = {
        "Quý I":   ["Tháng 1", "Tháng 2", "Tháng 3"],
        "Quý II":  ["Tháng 4", "Tháng 5", "Tháng 6"],
        "Quý III": ["Tháng 7", "Tháng 8", "Tháng 9"],
        "Quý IV":  ["Tháng 10", "Tháng 11", "Tháng 12"],
        "Cả Năm":  [f"Tháng {i}" for i in range(1, 13)],
    }
    return mapping.get(filter_type, DANH_SACH_THANG)

def get_old_val(old, key, default=None):
    """Lấy giá trị cũ với fallback an toàn."""
    val = old.get(key, default)
    if val is None:
        return 0 if KEY_TYPE.get(key) in ("int", "float") else ""
    if KEY_TYPE.get(key) == "int":
        try: return int(val)
        except: return 0
    if KEY_TYPE.get(key) == "float":
        try: return float(val)
        except: return 0.0
    return str(val) if val else ""

def text_agg(series):
    """Gộp nhiều text, loại trùng lặp."""
    items = list(dict.fromkeys([str(v).strip() for v in series if pd.notna(v) and str(v).strip()]))
    return "\n".join([f"• {t}" for t in items]) if items else ""

def build_summary_df(df_cur, ky_label):
    """Tổng hợp dữ liệu theo đơn vị + tính dòng tổng cộng."""
    if df_cur.empty:
        return pd.DataFrame()

    # Đảm bảo tất cả cột tồn tại
    for key in ALL_KEYS:
        if key not in df_cur.columns:
            df_cur[key] = 0 if KEY_TYPE.get(key) in ("int", "float") else ""

    agg_dict = {}
    for key in NUM_KEYS:
        if key in df_cur.columns:
            agg_dict[key] = "mean" if key == "nq_tyle" else "sum"
    for key in TEXT_KEYS:
        if key in df_cur.columns and key not in ("don_vi", "ky_bao_cao"):
            agg_dict[key] = text_agg
    agg_dict["nguoi_bao_cao"] = lambda x: ", ".join(dict.fromkeys([str(v).strip() for v in x if pd.notna(v)]))
    agg_dict["ngay_nop"]      = lambda x: ", ".join(dict.fromkeys([str(v).strip() for v in x if pd.notna(v)]))

    df_sum = df_cur.groupby("don_vi", as_index=False).agg(agg_dict)
    df_sum["ky_bao_cao"] = ky_label

    # Dòng TỔNG CỘNG
    total = {}
    for col in df_sum.columns:
        if col == "don_vi":
            total[col] = "TỔNG CỘNG"
        elif col in NUM_KEYS and pd.api.types.is_numeric_dtype(df_sum[col]):
            total[col] = round(df_sum[col].mean(), 1) if col == "nq_tyle" else df_sum[col].sum()
        else:
            total[col] = ""

    df_sum = pd.concat([df_sum, pd.DataFrame([total])], ignore_index=True)
    return df_sum


def build_excel(df_sum, ky_label):
    """Xuất file Excel chuyên nghiệp với header nhóm màu sắc."""
    # Cột xuất ra (theo schema, loại bỏ ky_bao_cao ra vị trí sau don_vi)
    out_keys = [k for k in ALL_KEYS if k not in ("ky_bao_cao",)]
    # Đặt ky_bao_cao vào sau don_vi
    out_keys.insert(1, "ky_bao_cao")

    display_cols = [KEY_LABEL.get(k, k) for k in out_keys]

    # Chuẩn bị df xuất
    df_ex = pd.DataFrame()
    for k, label in zip(out_keys, display_cols):
        if k in df_sum.columns:
            df_ex[label] = df_sum[k]
        else:
            df_ex[label] = ""

    # Xây dựng super_headers theo nhóm
    super_headers = []
    cur_group = None
    start_col = 1
    for i, k in enumerate(out_keys):
        grp = "info" if k in ("don_vi", "ky_bao_cao", "nguoi_bao_cao", "ngay_nop") else KEY_GROUP.get(k, "tl")
        if cur_group is None:
            cur_group = grp
            start_col = i + 1
        elif grp != cur_group:
            lbl, color = GROUP_LABELS.get(cur_group, ("KHÁC", "666666"))
            super_headers.append((start_col, i, lbl, color))
            cur_group = grp
            start_col = i + 1
    # Thêm nhóm cuối
    if cur_group:
        lbl, color = GROUP_LABELS.get(cur_group, ("KHÁC", "666666"))
        super_headers.append((start_col, len(out_keys), lbl, color))

    # Viết file
    buf = io.BytesIO()
    thin = Border(left=Side(style="thin"), right=Side(style="thin"),
                  top=Side(style="thin"), bottom=Side(style="thin"))

    with pd.ExcelWriter(buf, engine="openpyxl") as wr:
        df_ex.to_excel(wr, index=False, sheet_name="Tong_Hop", startrow=2)
        ws = wr.sheets["Tong_Hop"]

        # --- TIÊU ĐỀ CHÍNH (dòng 1) ---
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(out_keys))
        title_cell = ws.cell(row=1, column=1)
        title_cell.value = f"BẢNG TỔNG HỢP BÁO CÁO TGDV — KỲ: {ky_label.upper()}"
        title_cell.font = Font(bold=True, size=13, color="FFFFFF")
        title_cell.fill = PatternFill(start_color="003A6E", end_color="003A6E", fill_type="solid")
        title_cell.alignment = Alignment(horizontal="center", vertical="center")
        title_cell.border = thin
        ws.row_dimensions[1].height = 28

        # --- SUPER HEADERS (dòng 2) ---
        for start_c, end_c, lbl, color in super_headers:
            ws.merge_cells(start_row=2, start_column=start_c, end_row=2, end_column=end_c)
            cell = ws.cell(row=2, column=start_c)
            cell.value = lbl
            cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
            cell.font = Font(bold=True, color="FFFFFF", size=10)
            cell.alignment = Alignment(horizontal="center", vertical="center")
            for c in range(start_c, end_c + 1):
                ws.cell(row=2, column=c).border = thin
        ws.row_dimensions[2].height = 22

        # --- HEADER CỘT (dòng 3) ---
        for ci, col_name in enumerate(df_ex.columns, 1):
            cell = ws.cell(row=3, column=ci)
            cell.fill = PatternFill(start_color="D9E8F5", end_color="D9E8F5", fill_type="solid")
            cell.font = Font(bold=True, size=9)
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = thin
        ws.row_dimensions[3].height = 38

        # --- DỮ LIỆU (từ dòng 4) ---
        last_data_row = ws.max_row
        for ri in range(4, last_data_row + 1):
            is_total = ws.cell(row=ri, column=1).value == "TỔNG CỘNG"
            for ci in range(1, len(out_keys) + 1):
                cell = ws.cell(row=ri, column=ci)
                cell.border = thin
                cell.alignment = Alignment(vertical="center", wrap_text=True,
                                           horizontal="center" if ci > 4 else "left")
                if is_total:
                    cell.font = Font(bold=True, color="C8102E", size=10)
                    cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
                elif ri % 2 == 0:
                    cell.fill = PatternFill(start_color="F7FAFD", end_color="F7FAFD", fill_type="solid")

        # --- ĐỘ RỘNG CỘT ---
        for ci, col_cells in enumerate(ws.columns, 1):
            lengths = []
            for cell in col_cells:
                try:
                    val = str(cell.value or "")
                    lengths.append(max(len(line) for line in val.split("\n")) if "\n" in val else len(val))
                except:
                    lengths.append(0)
            col_letter = get_column_letter(ci)
            ws.column_dimensions[col_letter].width = min(max(max(lengths, default=6) + 2, 10), 42)

        # Freeze panes: đóng băng 3 dòng header + cột đơn vị
        ws.freeze_panes = "B4"

    return buf


# ==========================================
# CẤU HÌNH SUPABASE & LƯU TRUY CẬP
# KẾT NỐI SUPABASE
# ==========================================
from supabase import create_client, Client
SUPABASE_URL = "https://qqzsdxhqrdfvxnlurnyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFxenNkeGhxcmRmdnhubHVybnliIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU2MjY0NjAsImV4cCI6MjA5MTIwMjQ2MH0.H62F5zYEZ5l47fS4IdAE2JdRdI7inXQqWG0nvXhn2P8"
try:
    from supabase import create_client, Client
    SUPABASE_URL = "https://qqzsdxhqrdfvxnlurnyb.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFxenNkeGhxcmRmdnhubHVybnliIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU2MjY0NjAsImV4cCI6MjA5MTIwMjQ2MH0.H62F5zYEZ5l47fS4IdAE2JdRdI7inXQqWG0nvXhn2P8"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except: pass
    SUPABASE_OK = True
except:
    SUPABASE_OK = False

def log_access(app_name):
key_name = f"da_dem_truy_cap_{app_name}"
    if key_name not in st.session_state:
    if SUPABASE_OK and key_name not in st.session_state:
try:
supabase.table("thong_ke_truy_cap").insert({"ten_app": app_name}).execute()
st.session_state[key_name] = True
        except: pass 
log_access("Thu thập Báo cáo")
        except:
            pass

log_access("Thu thập Báo cáo v2")


# ==========================================
# ĐĂNG NHẬP PHÂN QUYỀN
# ĐĂNG NHẬP
# ==========================================
if "role" not in st.session_state: st.session_state.role = None
PASSWORDS = {
    "TGDV@2026":    "user",
    "BaoCao@2026":  "chuyen_vien",
    "Admin@2026":   "admin",
}
ROLE_LABELS = {
    "user":        ("CƠ SỞ",                   "🏘️"),
    "chuyen_vien": ("CHUYÊN VIÊN TỔNG HỢP",    "📋"),
    "admin":       ("QUẢN TRỊ VIÊN",            "⚙️"),
}

if "role" not in st.session_state:
    st.session_state.role = None

if st.session_state.role is None:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
        with st.form("login"):
            st.markdown("<h2 style='text-align:center; color:#004B87;'>ĐĂNG NHẬP BÁO CÁO TGDV</h2>", unsafe_allow_html=True)
            pwd = st.text_input("🔑 Mật khẩu:", type="password")
            if st.form_submit_button("Vào hệ thống", use_container_width=True):
                if pwd == "TGDV@2026": st.session_state.role = "user"; st.rerun()
                elif pwd == "BaoCao@2026": st.session_state.role = "chuyen_vien"; st.rerun()
                elif pwd == "Admin@2026": st.session_state.role = "admin"; st.rerun()
                else: st.error("❌ Mật khẩu sai!")
    col_l, col_m, col_r = st.columns([1, 1.1, 1])
    with col_m:
        st.markdown("""
        <div class='login-wrap'>
          <div class='login-logo'>
            <div style='font-size:52px;'>📊</div>
            <h2>HỆ THỐNG BÁO CÁO TGDV</h2>
            <p>Ban Tuyên giáo Tỉnh ủy — Nhập mật khẩu để truy cập</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            pwd = st.text_input("🔑 Mật khẩu truy cập", type="password", placeholder="Nhập mật khẩu...")
            submitted = st.form_submit_button("🚀 ĐĂNG NHẬP", use_container_width=True, type="primary")
            if submitted:
                role = PASSWORDS.get(pwd)
                if role:
                    st.session_state.role = role
                    st.rerun()
                else:
                    st.error("❌ Mật khẩu không đúng! Vui lòng thử lại.")
st.stop()


# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    rm = {"admin": "ADMIN", "chuyen_vien": "CHUYÊN VIÊN TỔNG HỢP", "user": "CƠ SỞ"}
    st.markdown(f"<div style='background:#004B87; color:white; padding:10px; border-radius:5px; text-align:center;'>👤 Quyền: <b>{rm.get(st.session_state.role)}</b></div>", unsafe_allow_html=True)
    if st.button("🚪 Đăng xuất"): st.session_state.role = None; st.rerun()
    role_label, role_icon = ROLE_LABELS.get(st.session_state.role, ("?", "?"))
    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.2);
                border-radius:10px; padding:14px; text-align:center; margin-bottom:16px;'>
        <div style='font-size:28px;'>{role_icon}</div>
        <div style='font-size:11px; color:#A8C8E8; text-transform:uppercase; letter-spacing:1px; margin-top:4px;'>Quyền truy cập</div>
        <div style='font-size:14px; font-weight:800; margin-top:2px;'>{role_label}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.role in ("admin", "chuyen_vien"):
        st.markdown("### 🗓️ BỘ LỌC DỮ LIỆU")
        l_bc = st.selectbox("Kỳ tổng hợp", ["Tháng", "Quý I", "Quý II", "Quý III", "Quý IV", "Cả Năm"],
                            label_visibility="collapsed")
        if l_bc == "Tháng":
            t_bc = st.selectbox("Chọn tháng", DANH_SACH_THANG, label_visibility="collapsed")
        st.markdown("---")

    st.markdown("<div style='margin-top:auto;'></div>", unsafe_allow_html=True)
    if st.button("🚪 Đăng xuất", use_container_width=True):
        st.session_state.role = None
        st.rerun()
    st.markdown(f"<div style='font-size:10px; color:#6A8FAA; text-align:center; margin-top:12px;'>Phiên bản 2.1 · {datetime.now().strftime('%d/%m/%Y')}</div>",
                unsafe_allow_html=True)


# ==========================================
# CẤU TRÚC TAB
# HEADER CHÍNH
# ==========================================
st.markdown("<h1 class='main-header'>HỆ THỐNG THU THẬP BÁO CÁO CƠ SỞ</h1>", unsafe_allow_html=True)
st.markdown("<div class='main-header'>📊 HỆ THỐNG THU THẬP BÁO CÁO <span>CƠ SỞ TGDV</span></div>",
            unsafe_allow_html=True)


# ==========================================
# CẤU TRÚC TAB THEO QUYỀN
# ==========================================
if st.session_state.role == "admin":
    tabs = st.tabs(["📝 NHẬP BÁO CÁO", "📈 TIẾN ĐỘ & TRÍCH XUẤT", "📊 PHÂN TÍCH BIỂU ĐỒ", "⚙️ QUẢN TRỊ ADMIN"])
    tab_nhap, tab_tiendo, tab_bieudo, tab_admin = tabs[0], tabs[1], tabs[2], tabs[3]
    tab_nhap, tab_tiendo, tab_bieudo, tab_admin = st.tabs([
        "📝 Nhập Báo cáo", "📈 Tiến độ & Trích xuất", "📊 Phân tích Biểu đồ", "⚙️ Quản trị Admin"
    ])
elif st.session_state.role == "chuyen_vien":
    tabs = st.tabs(["📝 NHẬP BÁO CÁO", "📈 TIẾN ĐỘ & TRÍCH XUẤT", "📊 PHÂN TÍCH BIỂU ĐỒ"])
    tab_nhap, tab_tiendo, tab_bieudo = tabs[0], tabs[1], tabs[2]
    tab_nhap, tab_tiendo, tab_bieudo = st.tabs([
        "📝 Nhập Báo cáo", "📈 Tiến độ & Trích xuất", "📊 Phân tích Biểu đồ"
    ])
else:
    tabs = st.tabs(["📝 NHẬP BÁO CÁO"])
    tab_nhap = tabs[0]
    tab_nhap = st.tabs(["📝 Nhập Báo cáo"])[0]

# ------------------------------------------

# ==========================================
# TAB 1: NHẬP BÁO CÁO
# ------------------------------------------
# ==========================================
with tab_nhap:
    st.markdown("### 1️⃣ XÁC ĐỊNH ĐƠN VỊ & KỲ BÁO CÁO")
    c1, c2, c3 = st.columns([2, 1.5, 1.5])
    dv = c1.selectbox("🏢 Đơn vị:", load_units(), index=None, placeholder="Gõ tìm đơn vị...")
    th = c3.selectbox("🗓️ Tháng:", DANH_SACH_THANG, index=None, placeholder="Chọn tháng...")
    

    # --- XÁC ĐỊNH ĐƠN VỊ & KỲ ---
    st.markdown("<div class='section-title'>🏢 XÁC ĐỊNH ĐƠN VỊ VÀ KỲ BÁO CÁO</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2.5, 1.5, 1.5])
    dv = c1.selectbox("🏢 Đơn vị báo cáo", load_units(), index=None,
                      placeholder="Gõ tên để tìm kiếm đơn vị...")
    nguoi_bc = c2.text_input("👤 Người báo cáo / SĐT", placeholder="Họ tên - Số điện thoại")
    th = c3.selectbox("🗓️ Kỳ báo cáo (tháng)", DANH_SACH_THANG, index=None,
                      placeholder="Chọn tháng...")

    # Load dữ liệu cũ nếu có
old = {}
if dv and th:
for d in load_data():
            if d.get('don_vi') == dv and d.get('ky_bao_cao') == th:
                old = d; break
    nguoi_bc = c2.text_input("👤 Người báo cáo / SĐT:", value=old.get('nguoi_bao_cao', ''))
            if d.get("don_vi") == dv and d.get("ky_bao_cao") == th:
                old = d
                break

    if dv and th:
        if old: st.success(f"💡 Đã load dữ liệu cũ của {dv}. Đồng chí chỉ cần sửa những chỗ sai!")
        else: st.info(f"✨ Đang lập báo cáo mới cho {dv}.")
        
        with st.form("f_nhap"):
            with st.expander("1. CÔNG TÁC LÃNH ĐẠO, CHỈ ĐẠO", expanded=False):
                ca, cb, cc = st.columns(3)
                ld_vb = ca.number_input("Số văn bản cấp ủy ban hành", min_value=0, value=int(old.get('ld_vanban',0)))
                ld_tm = cb.number_input("Số văn bản tham mưu cấp trên", min_value=0, value=int(old.get('ld_thammuu',0)))
                ld_ch = cc.number_input("Số cuộc họp triển khai", min_value=0, value=int(old.get('ld_cuochop',0)))

            with st.expander("2. HỌC TẬP, QUÁN TRIỆT NGHỊ QUYẾT", expanded=False):
                c1, c2, c3, c4 = st.columns(4)
                nq_hn = c1.number_input("Số hội nghị tổ chức", min_value=0, value=int(old.get('nq_hoinghi',0)))
                nq_ng = c2.number_input("Số người tham gia", min_value=0, value=int(old.get('nq_nguoi',0)))
                nq_vb = c3.number_input("Số văn bản triển khai", min_value=0, value=int(old.get('nq_vanban',0)))
                nq_tl = c4.number_input("Tỷ lệ tham gia (%)", min_value=0.0, max_value=100.0, value=float(old.get('nq_tyle',0.0)))

            with st.expander("3. CÔNG TÁC TUYÊN TRUYỀN", expanded=False):
                c1, c2, c3, c4 = st.columns(4)
                tt_tb = c1.number_input("Số tin, bài, pano", min_value=0, value=int(old.get('tt_tinbai',0)))
                tt_lo = c2.number_input("Số lượt loa truyền thanh", min_value=0, value=int(old.get('tt_loa',0)))
                tt_bu = c3.number_input("Số buổi tuyên truyền miệng", min_value=0, value=int(old.get('tt_buoi',0)))
                tt_nn = c4.number_input("Số người nghe TT miệng", min_value=0, value=int(old.get('tt_nguoi',0)))
                c5, c6 = st.columns(2)
                tt_mxh = c5.number_input("Số bài MXH/Cổng TT", min_value=0, value=int(old.get('tt_mxh_bai',0)))
                tt_ttmxh = c6.number_input("Lượt tương tác MXH", min_value=0, value=int(old.get('tt_mxh_tuongtac',0)))

            with st.expander("4. DƯ LUẬN XÃ HỘI", expanded=False):
                c1, c2, c3 = st.columns(3)
                dl_bc = c1.number_input("Số báo cáo DLXH gửi đi", min_value=0, value=int(old.get('dl_baocao',0)))
                dl_vd = c2.number_input("Số vấn đề nổi cộm", min_value=0, value=int(old.get('dl_vande',0)))
                dl_xl = c3.number_input("Số vụ việc đã xử lý", min_value=0, value=int(old.get('dl_xuly',0)))

            with st.expander("5. KHOA GIÁO, VĂN HÓA - VĂN NGHỆ", expanded=False):
                c1, c2, c3, c4 = st.columns(4)
                kg_ct = c1.number_input("Số CT tuyên truyền GD", min_value=0, value=int(old.get('kg_chuongtrinh',0)))
                kg_lo = c2.number_input("Số buổi Y tế/Môi trường", min_value=0, value=int(old.get('kg_lop',0)))
                kg_cn = c3.number_input("Số buổi biểu diễn nghệ thuật", min_value=0, value=int(old.get('kg_bd_chuyennghiep',0)))
                kg_cl = c4.number_input("Số CLB VH-NT thành lập", min_value=0, value=int(old.get('kg_clb_thanhlap',0)))
                kg_kk = st.text_area("Khó khăn vướng mắc Khoa giáo:", value=old.get('kg_khokhan',''))

            with st.expander("6. CÔNG TÁC DÂN VẬN (DÂN VẬN KHÉO)", expanded=False):
                c1, c2, c3 = st.columns(3)
                dv_dk = c1.number_input("Mô hình DVK đăng ký", min_value=0, value=int(old.get('dv_mh_dangky',0)))
                dv_hq = c2.number_input("Mô hình DVK hiệu quả", min_value=0, value=int(old.get('dv_mh_hieuqua',0)))
                dv_moi = c3.number_input("Mô hình mới trong kỳ", min_value=0, value=int(old.get('dv_mh_moi',0)))
                
                c4, c5, c6 = st.columns(3)
                dv_cv = c4.number_input("Số cuộc vận động, TT", min_value=0, value=int(old.get('dv_cuocvandong',0)))
                dv_ntg = c5.number_input("Số lượt người tham gia", min_value=0, value=int(old.get('dv_nguoithamgia',0)))
                dv_tx = c6.number_input("Số buổi đối thoại Nhân dân", min_value=0, value=int(old.get('dv_tiepxuc',0)))

            with st.expander("7. NHIỆM VỤ TRỌNG TÂM", expanded=False):
                c1, c2, c3 = st.columns(3)
                nv_dg = c1.number_input("Số nhiệm vụ được giao", min_value=0, value=int(old.get('nv_duocgiao',0)))
                nv_ht = c2.number_input("Số nhiệm vụ hoàn thành", min_value=0, value=int(old.get('nv_hoanthanh',0)))
                nv_kq = st.text_area("Kết quả nổi bật:", value=old.get('nv_ketqua',''))

            with st.expander("8. CHUYÊN ĐỀ: BÌNH DÂN HỌC VỤ SỐ", expanded=False):
                ca, cb, cc = st.columns(3)
                bd_ti = ca.number_input("Số tin bài về CĐS", min_value=0, value=int(old.get('bd_tinbai',0)))
                ts_ch = cb.number_input("Tổng số chi bộ", min_value=0, value=int(old.get('ts_chibo',0)))
                kq_cd = cc.number_input("Số CB SH chuyên đề số", min_value=0, value=int(old.get('kq_chibo_cd',0)))
                cd, ce = st.columns(2)
                ts_cb = cd.number_input("Tổng số CBCCVC", min_value=0, value=int(old.get('ts_cbccvc',0)))
                kq_ai = ce.number_input("Số CB biết dùng AI", min_value=0, value=int(old.get('kq_cb_ai',0)))

            with st.expander("9. ĐÁNH GIÁ CHUNG", expanded=False):
                tl_mo = st.text_area("Mô hình hay sáng tạo:", value=old.get('tl_mohinh',''))
                tl_kh = st.text_area("Khó khăn chung:", value=old.get('tl_khokhan',''))

            if st.form_submit_button("🚀 GỬI / CẬP NHẬT BÁO CÁO", use_container_width=True, type="primary"):
                if not nguoi_bc: st.error("⚠️ Điền tên người báo cáo!")
                else:
                    new_rec = {"don_vi":dv, "ky_bao_cao":th, "nguoi_bao_cao":nguoi_bc, "ngay_nop":datetime.now().strftime("%d/%m/%Y %H:%M"),
                               "ld_vanban":ld_vb, "ld_thammuu":ld_tm, "ld_cuochop":ld_ch, "nq_hoinghi":nq_hn, "nq_nguoi":nq_ng, "nq_vanban":nq_vb, "nq_tyle":nq_tl,
                               "tt_tinbai":tt_tb, "tt_loa":tt_lo, "tt_buoi":tt_bu, "tt_nguoi":tt_nn, "tt_mxh_bai":tt_mxh, "tt_mxh_tuongtac":tt_ttmxh,
                               "dl_baocao":dl_bc, "dl_vande":dl_vd, "dl_xuly":dl_xl, "kg_chuongtrinh":kg_ct, "kg_lop":kg_lo, "kg_bd_chuyennghiep":kg_cn, "kg_clb_thanhlap":kg_cl, "kg_khokhan":kg_kk,
                               "dv_mh_dangky":dv_dk, "dv_mh_hieuqua":dv_hq, "dv_mh_moi":dv_moi, "dv_cuocvandong":dv_cv, "dv_nguoithamgia":dv_ntg, "dv_tiepxuc":dv_tx, "nv_duocgiao":nv_dg, "nv_hoanthanh":nv_ht, "nv_ketqua":nv_kq,
                               "bd_tinbai":bd_ti, "ts_chibo":ts_ch, "kq_chibo_cd":kq_cd, "ts_cbccvc":ts_cb, "kq_cb_ai":kq_ai, "tl_mohinh":tl_mo, "tl_khokhan":tl_kh}
                    data = load_data(); data = [d for d in data if not (d['don_vi']==dv and d['ky_bao_cao']==th)]
                    data.append(new_rec); save_data(data); st.success("✅ Thành công!")

# ------------------------------------------
# CHUẨN BỊ DỮ LIỆU DÙNG CHUNG CHO TAB 2 & 3
# ------------------------------------------
if st.session_state.role in ["admin", "chuyen_vien"]:
    if not dv or not th:
        st.markdown("""
        <div class='warning-box'>
            ⚠️ Vui lòng chọn <strong>Đơn vị</strong> và <strong>Kỳ báo cáo</strong> trước khi nhập số liệu.
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    if old:
        st.markdown(f"""
        <div class='info-box'>
            💡 <strong>Đã tìm thấy báo cáo cũ</strong> của <em>{dv}</em> — {th}.
            Số liệu đã được điền sẵn. Đồng chí chỉ cần chỉnh sửa các mục cần cập nhật rồi nhấn <strong>Gửi</strong>.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='info-box' style='background:#F0FDF4; border-color:#BBF7D0; border-left-color:#1A9E5C; color:#065F46;'>
            ✨ Đang tạo báo cáo <strong>mới</strong> cho <em>{dv}</em> — {th}.
        </div>
        """, unsafe_allow_html=True)

    # --- FORM NHẬP SỐ LIỆU ---
    with st.form("f_nhap", clear_on_submit=False):

        # ── 1. LÃNH ĐẠO CHỈ ĐẠO ──
        with st.expander("1️⃣  CÔNG TÁC LÃNH ĐẠO, CHỈ ĐẠO", expanded=True):
            c1, c2, c3 = st.columns(3)
            ld_vb  = c1.number_input("📄 Số VB cấp ủy ban hành",       min_value=0, value=get_old_val(old, "ld_vanban"))
            ld_tm  = c2.number_input("📤 Số VB tham mưu cấp trên",     min_value=0, value=get_old_val(old, "ld_thammuu"))
            ld_ch  = c3.number_input("📅 Số cuộc họp, hội nghị",       min_value=0, value=get_old_val(old, "ld_cuochop"))

        # ── 2. QUÁN TRIỆT NQ ──
        with st.expander("2️⃣  HỌC TẬP, QUÁN TRIỆT NGHỊ QUYẾT"):
            c1, c2, c3, c4 = st.columns(4)
            nq_hn  = c1.number_input("🏛️ Số hội nghị NQ",              min_value=0, value=get_old_val(old, "nq_hoinghi"))
            nq_ng  = c2.number_input("👥 Số người tham gia",            min_value=0, value=get_old_val(old, "nq_nguoi"))
            nq_vb  = c3.number_input("📋 Số VB đã triển khai",          min_value=0, value=get_old_val(old, "nq_vanban"))
            nq_tl  = c4.number_input("📊 Tỷ lệ ĐV tham gia (%)",       min_value=0.0, max_value=100.0, step=0.5,
                                     value=get_old_val(old, "nq_tyle", 0.0))

        # ── 3. TUYÊN TRUYỀN ──
        with st.expander("3️⃣  CÔNG TÁC TUYÊN TRUYỀN"):
            c1, c2, c3, c4 = st.columns(4)
            tt_tb   = c1.number_input("📰 Tin, bài, pano",              min_value=0, value=get_old_val(old, "tt_tinbai"))
            tt_lo   = c2.number_input("🔊 Lượt loa truyền thanh",       min_value=0, value=get_old_val(old, "tt_loa"))
            tt_bu   = c3.number_input("🗣️ Buổi TT miệng",               min_value=0, value=get_old_val(old, "tt_buoi"))
            tt_nn   = c4.number_input("👂 Người nghe TT miệng",         min_value=0, value=get_old_val(old, "tt_nguoi"))
            c5, c6  = st.columns(2)
            tt_mxh  = c5.number_input("📱 Bài trên MXH / Cổng TT",     min_value=0, value=get_old_val(old, "tt_mxh_bai"))
            tt_ttmxh = c6.number_input("❤️ Lượt tương tác MXH",         min_value=0, value=get_old_val(old, "tt_mxh_tuongtac"))

        # ── 4. DƯ LUẬN XÃ HỘI ──
        with st.expander("4️⃣  NẮMBẮT DƯ LUẬN XÃ HỘI"):
            c1, c2, c3 = st.columns(3)
            dl_bc   = c1.number_input("📨 Báo cáo DLXH gửi đi",        min_value=0, value=get_old_val(old, "dl_baocao"))
            dl_vd   = c2.number_input("⚠️ Vấn đề nổi cộm",             min_value=0, value=get_old_val(old, "dl_vande"))
            dl_xl   = c3.number_input("✅ Vụ việc đã xử lý",            min_value=0, value=get_old_val(old, "dl_xuly"))

        # ── 5. KHOA GIÁO VH-VN ──
        with st.expander("5️⃣  KHOA GIÁO, VĂN HÓA - VĂN NGHỆ"):
            c1, c2, c3, c4 = st.columns(4)
            kg_ct   = c1.number_input("📚 CT tuyên truyền GD",          min_value=0, value=get_old_val(old, "kg_chuongtrinh"))
            kg_lo   = c2.number_input("🏥 Buổi Y tế/Môi trường",        min_value=0, value=get_old_val(old, "kg_lop"))
            kg_cn   = c3.number_input("🎭 Biểu diễn NT chuyên nghiệp",  min_value=0, value=get_old_val(old, "kg_bd_chuyennghiep"))
            kg_qc   = c4.number_input("🎶 Biểu diễn NT quần chúng",     min_value=0, value=get_old_val(old, "kg_bd_quanchung"))
            c5, c6, c7, c8 = st.columns(4)
            kg_cl   = c5.number_input("🎪 CLB VH-NT thành lập",         min_value=0, value=get_old_val(old, "kg_clb_thanhlap"))
            kg_tv   = c6.number_input("👤 Thành viên CLB",              min_value=0, value=get_old_val(old, "kg_clb_thanhvien"))
            kg_lh   = c7.number_input("🏆 HĐ Lễ hội, Thể thao",        min_value=0, value=get_old_val(old, "kg_hd_vhtt"))
            kg_hd   = c8.number_input("🎨 HĐ Văn hóa-Văn nghệ",        min_value=0, value=get_old_val(old, "kg_hoatdong"))
            kg_kk   = st.text_area("📝 Khó khăn, vướng mắc (Khoa giáo, VH-VN):",
                                   value=get_old_val(old, "kg_khokhan"), height=80)

        # ── 6. DÂN VẬN KHÉO ──
        with st.expander("6️⃣  CÔNG TÁC DÂN VẬN (DÂN VẬN KHÉO)"):
            c1, c2, c3 = st.columns(3)
            dv_dk   = c1.number_input("🏅 Mô hình DVK đăng ký",        min_value=0, value=get_old_val(old, "dv_mh_dangky"))
            dv_hq   = c2.number_input("⭐ Mô hình DVK hiệu quả",        min_value=0, value=get_old_val(old, "dv_mh_hieuqua"))
            dv_moi  = c3.number_input("🆕 Mô hình mới trong kỳ",        min_value=0, value=get_old_val(old, "dv_mh_moi"))
            c4, c5, c6 = st.columns(3)
            dv_cv   = c4.number_input("📢 Số cuộc vận động, TT",        min_value=0, value=get_old_val(old, "dv_cuocvandong"))
            dv_ntg  = c5.number_input("👥 Lượt người tham gia",         min_value=0, value=get_old_val(old, "dv_nguoithamgia"))
            dv_tx   = c6.number_input("🤝 Buổi đối thoại Nhân dân",     min_value=0, value=get_old_val(old, "dv_tiepxuc"))

        # ── 7. NHIỆM VỤ TRỌNG TÂM ──
        with st.expander("7️⃣  NHIỆM VỤ TRỌNG TÂM"):
            c1, c2, c3 = st.columns(3)
            nv_dg   = c1.number_input("📌 Nhiệm vụ TT được giao",       min_value=0, value=get_old_val(old, "nv_duocgiao"))
            nv_ht   = c2.number_input("✅ Nhiệm vụ TT hoàn thành",      min_value=0, value=get_old_val(old, "nv_hoanthanh"))
            nv_dk   = c3.number_input("⏳ Nhiệm vụ đang triển khai",    min_value=0, value=get_old_val(old, "nv_dangtrienkhai"))
            nv_kq   = st.text_area("🏆 Kết quả thí điểm nổi bật:",
                                   value=get_old_val(old, "nv_ketqua"), height=80)

        # ── 8. BÌNH DÂN HỌC VỤ SỐ ──
        with st.expander("8️⃣  CHUYÊN ĐỀ: BÌNH DÂN HỌC VỤ SỐ"):
            st.markdown("**Thông tin chung**")
            c1, c2, c3 = st.columns(3)
            bd_ti   = c1.number_input("📰 Tin bài về CĐS",               min_value=0, value=get_old_val(old, "bd_tinbai"))
            bd_ct   = c2.number_input("🏆 Cuộc thi CĐS",                 min_value=0, value=get_old_val(old, "bd_cuocthi"))
            kq_tc   = c3.number_input("🔧 Số Tổ công nghệ số",           min_value=0, value=get_old_val(old, "kq_tocongnghe"))

            st.markdown("**Đối với Chi bộ**")
            c4, c5, c6 = st.columns(3)
            ts_ch   = c4.number_input("🏛️ Tổng số Chi bộ",               min_value=0, value=get_old_val(old, "ts_chibo"))
            kq_cd   = c5.number_input("📖 CB SH chuyên đề số",            min_value=0, value=get_old_val(old, "kq_chibo_cd"))
            kq_st   = c6.number_input("📓 CB dùng Sổ tay ĐV số",          min_value=0, value=get_old_val(old, "kq_chibo_sotay"))

            st.markdown("**Đối với CBCCVC**")
            c7, c8, c9 = st.columns(3)
            ts_cb   = c7.number_input("👔 Tổng số CBCCVC",                min_value=0, value=get_old_val(old, "ts_cbccvc"))
            kq_ai   = c8.number_input("🤖 CB biết dùng AI",               min_value=0, value=get_old_val(old, "kq_cb_ai"))
            kq_ck   = c9.number_input("🎓 CB hoàn thành khóa CĐS",        min_value=0, value=get_old_val(old, "kq_cb_khoahoc"))

            st.markdown("**Đối với Nhân dân**")
            c10, c11, c12 = st.columns(3)
            ts_nd   = c10.number_input("👨‍👩‍👧 Tổng ND trưởng thành",         min_value=0, value=get_old_val(old, "ts_nd_truongthanh"))
            kq_kn   = c11.number_input("📱 ND có Kỹ năng số",             min_value=0, value=get_old_val(old, "kq_nd_kynang"))
            kq_vi   = c12.number_input("🪪 ND phổ cập VNeID",             min_value=0, value=get_old_val(old, "kq_nd_vneid"))
            c13, c14 = st.columns(2)
            kq_sm   = c13.number_input("📲 ND dùng Smartphone",           min_value=0, value=get_old_val(old, "kq_nd_smartphone"))
            kq_lp   = c14.number_input("🏫 Buổi học cộng đồng",           min_value=0, value=get_old_val(old, "kq_lop_nd"))

        # ── 9. ĐÁNH GIÁ CHUNG ──
        with st.expander("9️⃣  ĐÁNH GIÁ CHUNG & KIẾN NGHỊ"):
            tl_mo   = st.text_area("🌟 Mô hình hay, sáng tạo trong tháng:",
                                   value=get_old_val(old, "tl_mohinh"), height=100,
                                   placeholder="Mô tả các mô hình, cách làm hay, sáng tạo...")
            tl_kh   = st.text_area("⚠️ Khó khăn, vướng mắc và kiến nghị:",
                                   value=get_old_val(old, "tl_khokhan"), height=100,
                                   placeholder="Nêu rõ khó khăn và đề xuất hướng giải quyết...")

        st.markdown("")
        submitted = st.form_submit_button(
            "🚀 GỬI / CẬP NHẬT BÁO CÁO",
            use_container_width=True, type="primary"
        )

        if submitted:
            if not nguoi_bc.strip():
                st.error("⚠️ Vui lòng điền **tên người báo cáo và số điện thoại**!")
            else:
                new_rec = {
                    "don_vi": dv, "ky_bao_cao": th,
                    "nguoi_bao_cao": nguoi_bc.strip(),
                    "ngay_nop": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    # 1
                    "ld_vanban": ld_vb, "ld_thammuu": ld_tm, "ld_cuochop": ld_ch,
                    # 2
                    "nq_hoinghi": nq_hn, "nq_nguoi": nq_ng, "nq_vanban": nq_vb, "nq_tyle": nq_tl,
                    # 3
                    "tt_tinbai": tt_tb, "tt_loa": tt_lo, "tt_buoi": tt_bu, "tt_nguoi": tt_nn,
                    "tt_mxh_bai": tt_mxh, "tt_mxh_tuongtac": tt_ttmxh,
                    # 4
                    "dl_baocao": dl_bc, "dl_vande": dl_vd, "dl_xuly": dl_xl,
                    # 5
                    "kg_chuongtrinh": kg_ct, "kg_lop": kg_lo, "kg_bd_chuyennghiep": kg_cn,
                    "kg_bd_quanchung": kg_qc, "kg_clb_thanhlap": kg_cl, "kg_clb_thanhvien": kg_tv,
                    "kg_hd_vhtt": kg_lh, "kg_hoatdong": kg_hd, "kg_khokhan": kg_kk,
                    # 6
                    "dv_mh_dangky": dv_dk, "dv_mh_hieuqua": dv_hq, "dv_mh_moi": dv_moi,
                    "dv_cuocvandong": dv_cv, "dv_nguoithamgia": dv_ntg, "dv_tiepxuc": dv_tx,
                    # 7
                    "nv_duocgiao": nv_dg, "nv_hoanthanh": nv_ht, "nv_dangtrienkhai": nv_dk,
                    "nv_ketqua": nv_kq,
                    # 8
                    "bd_tinbai": bd_ti, "bd_cuocthi": bd_ct, "kq_tocongnghe": kq_tc,
                    "ts_chibo": ts_ch, "kq_chibo_cd": kq_cd, "kq_chibo_sotay": kq_st,
                    "ts_cbccvc": ts_cb, "kq_cb_ai": kq_ai, "kq_cb_khoahoc": kq_ck,
                    "ts_nd_truongthanh": ts_nd, "kq_nd_kynang": kq_kn, "kq_nd_vneid": kq_vi,
                    "kq_nd_smartphone": kq_sm, "kq_lop_nd": kq_lp,
                    # 9
                    "tl_mohinh": tl_mo, "tl_khokhan": tl_kh,
                }
                data = load_data()
                data = [d for d in data if not (d["don_vi"] == dv and d["ky_bao_cao"] == th)]
                data.append(new_rec)
                save_data(data)
                st.success(f"✅ **Đã lưu thành công** báo cáo của **{dv}** — {th}! Cảm ơn đồng chí.")
                st.balloons()


# ==========================================
# TAB 2 & 3: CHỈ HIỂN THỊ VỚI ADMIN/CHUYEN_VIEN
# ==========================================
if st.session_state.role in ("admin", "chuyen_vien"):
all_raw = load_data()
    st.sidebar.markdown("### 🗓️ BỘ LỌC DỮ LIỆU")
    l_bc = st.sidebar.selectbox("Kỳ tổng hợp:", ["Tháng", "Quý I", "Quý II", "Quý III", "Quý IV", "Cả Năm"])
    all_u   = load_units()

    # Lọc dữ liệu theo bộ lọc sidebar
if l_bc == "Tháng":
        t_bc = st.sidebar.selectbox("Tháng cụ thể:", DANH_SACH_THANG)
        df_cur = pd.DataFrame([d for d in all_raw if d['ky_bao_cao'] == t_bc])
        months_sel = [t_bc]
        ky_label   = t_bc
else:
        m_l = get_months_for_filter(l_bc)
        df_cur = pd.DataFrame([d for d in all_raw if d['ky_bao_cao'] in m_l])
    
    all_u = load_units()
    u_done = df_cur['don_vi'].unique().tolist() if not df_cur.empty else []
    u_miss = [u for u in all_u if u not in u_done]

    # --------------------------------------
    # TAB 2: TIẾN ĐỘ & TRÍCH XUẤT (KÈM TRANG TRÍ EXCEL VIP)
    # --------------------------------------
        months_sel = get_months_for_filter(l_bc)
        ky_label   = l_bc

    df_cur  = pd.DataFrame([d for d in all_raw if d.get("ky_bao_cao") in months_sel])
    u_done  = df_cur["don_vi"].unique().tolist() if not df_cur.empty else []
    u_miss  = [u for u in all_u if u not in u_done]
    rate    = (len(u_done) / len(all_u) * 100) if all_u else 0

    # ── TAB 2: TIẾN ĐỘ & TRÍCH XUẤT ──
with tab_tiendo:
        st.markdown(f"<div class='section-title'>📈 TIẾN ĐỘ NỘP BÁO CÁO — KỲ: {ky_label.upper()}</div>",
                    unsafe_allow_html=True)

        # Metric cards
c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='metric-card'><p class='metric-title'>Đã nộp</p><p class='metric-number' style='color:#28a745;'>{len(u_done)}</p></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-card'><p class='metric-title'>Chưa nộp</p><p class='metric-number'>{len(u_miss)}</p></div>", unsafe_allow_html=True)
        rate = (len(u_done)/len(all_u)*100) if all_u else 0
        c3.markdown(f"<div class='metric-card'><p class='metric-title'>Tỷ lệ</p><p class='metric-number' style='color:#004B87;'>{rate:.1f}%</p></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='metric-card'><p class='metric-title'>Tổng đơn vị</p><p class='metric-number'>{len(all_u)}</p></div>", unsafe_allow_html=True)
        c1.markdown(f"""<div class='metric-card green'>
            <div class='metric-title'>Đã nộp</div>
            <div class='metric-number green'>{len(u_done)}</div>
            <div class='metric-sub'>đơn vị</div></div>""", unsafe_allow_html=True)
        c2.markdown(f"""<div class='metric-card red'>
            <div class='metric-title'>Chưa nộp</div>
            <div class='metric-number red'>{len(u_miss)}</div>
            <div class='metric-sub'>đơn vị</div></div>""", unsafe_allow_html=True)
        c3.markdown(f"""<div class='metric-card' style='border-left-color:#005BAA;'>
            <div class='metric-title'>Tỷ lệ hoàn thành</div>
            <div class='metric-number' style='color:#005BAA;'>{rate:.1f}%</div>
            <div class='metric-sub'>tiến độ</div></div>""", unsafe_allow_html=True)
        c4.markdown(f"""<div class='metric-card gold'>
            <div class='metric-title'>Tổng đơn vị</div>
            <div class='metric-number gold'>{len(all_u)}</div>
            <div class='metric-sub'>trong hệ thống</div></div>""", unsafe_allow_html=True)

        # Progress bar
        st.markdown(f"""
        <div style='background:white; padding:16px 20px; border-radius:10px; margin:16px 0; box-shadow:0 2px 8px rgba(0,0,0,0.06);'>
            <div style='display:flex; justify-content:space-between; font-size:13px; font-weight:600; color:#374151; margin-bottom:8px;'>
                <span>Tiến độ nộp báo cáo</span>
                <span style='color:{"#1A9E5C" if rate >= 80 else "#E8A800" if rate >= 50 else "#C8102E"};'>{rate:.1f}%</span>
            </div>
            <div class='progress-wrap'>
                <div class='progress-fill' style='width:{rate:.1f}%;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Nút trích xuất Excel
if not df_cur.empty:
            num_cols = df_cur.select_dtypes(include='number').columns
            agg_dict = {col: ('mean' if col=='nq_tyle' else 'sum') for col in num_cols}
            def g_c(x):
                txts = list(dict.fromkeys([str(i).strip() for i in x if pd.notna(i) and str(i).strip()!=""]))
                return "\n".join([f"- {t}" for t in txts]) if txts else ""
            for c in ['nv_ketqua','tl_mohinh','tl_khokhan','kg_khokhan']: 
                if c in df_cur.columns: agg_dict[c] = g_c
            agg_dict['nguoi_bao_cao'] = lambda x: ", ".join(list(dict.fromkeys([str(i).strip() for i in x if pd.notna(i)])))
            agg_dict['ngay_nop'] = lambda x: ", ".join(list(dict.fromkeys([str(i).strip() for i in x if pd.notna(i)])))
            
            df_sum = df_cur.groupby('don_vi').agg(agg_dict).reset_index()
            df_sum['ky_bao_cao'] = l_bc
            for c in DICT_DICH_THUAT.keys():
                if c not in df_sum.columns: df_sum[c] = 0 if c in num_cols else ""
            
            df_ex = df_sum[list(DICT_DICH_THUAT.keys())].rename(columns=DICT_DICH_THUAT)
            
            # --- TÍNH TỔNG CỘNG ---
            t_r = {c: (round(df_ex[c].mean(),2) if c==DICT_DICH_THUAT['nq_tyle'] else df_ex[c].sum()) if pd.api.types.is_numeric_dtype(df_ex[c]) else "" for c in df_ex.columns}
            t_r[DICT_DICH_THUAT['don_vi']] = "TỔNG CỘNG"
            df_ex = pd.concat([df_ex, pd.DataFrame([t_r])], ignore_index=True)
            
            # --- VẼ EXCEL SIÊU VIP ---
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine='openpyxl') as wr:
                df_ex.to_excel(wr, index=False, sheet_name='Bao_Cao', startrow=1)
                ws = wr.sheets['Bao_Cao']
                thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
                
                # CHÚ Ý: MẢNG NÀY PHẢI KHỚP ĐÚNG 55 CỘT (Cộng thêm cột Ngày nộp)
                super_headers = [
                    (1, 4, "THÔNG TIN CHUNG", "004B87"), 
                    (5, 7, "1. LÃNH ĐẠO, CHỈ ĐẠO", "C8102E"),
                    (8, 11, "2. QUÁN TRIỆT NGHỊ QUYẾT", "004B87"), 
                    (12, 17, "3. CÔNG TÁC TUYÊN TRUYỀN", "C8102E"),
                    (18, 20, "4. DƯ LUẬN XÃ HỘI", "004B87"), 
                    (21, 29, "5. KHOA GIÁO, VH-VN", "C8102E"),
                    (30, 35, "6. CÔNG TÁC DÂN VẬN", "004B87"), 
                    (36, 39, "7. NHIỆM VỤ TRỌNG TÂM", "C8102E"),
                    (40, 53, "8. BÌNH DÂN HỌC VỤ SỐ", "004B87"), 
                    (54, 55, "9. ĐÁNH GIÁ CHUNG", "C8102E")
                ]
                
                # Đổ màu siêu tiêu đề
                for start_col, end_col, title, color in super_headers:
                    ws.merge_cells(start_row=1, start_column=start_col, end_row=1, end_column=end_col)
                    cell = ws.cell(row=1, column=start_col)
                    cell.value = title
                    cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
                    cell.font = Font(bold=True, color="FFFFFF", size=12)
                    cell.alignment = Alignment(horizontal='center', vertical='center')
                    for col in range(start_col, end_col + 1): ws.cell(row=1, column=col).border = thin_border
                
                # Đổ màu dòng tiêu đề cột
                for col_num, col_name in enumerate(df_ex.columns, 1):
                    cell = ws.cell(row=2, column=col_num)
                    cell.fill = PatternFill(start_color="E6E6E6", end_color="E6E6E6", fill_type="solid")
                    cell.font = Font(bold=True, color="000000")
                    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
                    cell.border = thin_border
                
                # Căn lề tự động và viền cho tất cả
                for i, col in enumerate(ws.columns, 1):
                    max_length = 0
                    column_letter = get_column_letter(i)
                    for cell in col:
                        try:
                            if len(str(cell.value)) > max_length: max_length = len(str(cell.value))
                        except: pass
                        cell.border = thin_border
                    ws.column_dimensions[column_letter].width = min(max(max_length + 2, 12), 40)
                
                ws.row_dimensions[1].height = 25
                ws.row_dimensions[2].height = 35
                
                # TÔ VÀNG DÒNG TỔNG CỘNG
                last_row = ws.max_row
                for col_idx in range(1, ws.max_column + 1):
                    cell = ws.cell(row=last_row, column=col_idx)
                    cell.font = Font(bold=True, color="C8102E")
                    cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
            
            # --- HIỂN THỊ NÚT TẢI XUỐNG ---
            st.write("")
            st.download_button("📥 TẢI BẢNG TỔNG HỢP GỘP SỐ LIỆU (EXCEL ĐÃ TRANG TRÍ)", buf.getvalue(), f"Tong_hop_{l_bc}.xlsx", type="primary", use_container_width=True)
            df_sum = build_summary_df(df_cur.copy(), ky_label)
            if not df_sum.empty:
                excel_buf = build_excel(df_sum, ky_label)
                st.download_button(
                    label=f"📥 TẢI BẢNG TỔNG HỢP SỐ LIỆU — {ky_label.upper()} (EXCEL)",
                    data=excel_buf.getvalue(),
                    file_name=f"TongHop_BaoCao_{ky_label.replace(' ', '_')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary",
                    use_container_width=True
                )

        # Danh sách đơn vị
        st.markdown("<div class='section-title'>📋 CHI TIẾT TIẾN ĐỘ THEO ĐƠN VỊ</div>", unsafe_allow_html=True)
        col_a, col_b = st.columns([1.2, 1])

        st.markdown("<div class='section-title'>📊 CHI TIẾT TIẾN ĐỘ</div>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
with col_a:
            st.success(f"✅ ĐÃ NỘP ({len(u_done)})")
            if u_done:
                df_d = df_cur[['don_vi','ngay_nop','nguoi_bao_cao']].drop_duplicates(subset=['don_vi'], keep='last')
                st.dataframe(df_d.rename(columns={'don_vi':'Đơn vị','ngay_nop':'Lúc nộp','nguoi_bao_cao':'Người nộp'}), use_container_width=True, hide_index=True)
            st.markdown(f"<span class='badge badge-success'>✅ ĐÃ NỘP — {len(u_done)} đơn vị</span>",
                        unsafe_allow_html=True)
            if u_done and not df_cur.empty:
                df_d = (df_cur[["don_vi", "ngay_nop", "nguoi_bao_cao"]]
                        .drop_duplicates(subset=["don_vi"], keep="last")
                        .sort_values("don_vi")
                        .rename(columns={"don_vi": "Đơn vị", "ngay_nop": "Thời điểm nộp", "nguoi_bao_cao": "Người nộp"}))
                st.dataframe(df_d, use_container_width=True, hide_index=True, height=400)
            else:
                st.info("Chưa có đơn vị nào nộp báo cáo.")

with col_b:
            st.error(f"❌ CHƯA NỘP ({len(u_miss)})")
            st.markdown(f"<span class='badge badge-danger'>❌ CHƯA NỘP — {len(u_miss)} đơn vị</span>",
                        unsafe_allow_html=True)
if u_miss:
                st.code(", ".join(u_miss))
                for m in sorted(u_miss): st.text(f"🔸 {m}")
                for m in sorted(u_miss):
                    st.markdown(f"<div style='padding:5px 0; border-bottom:1px solid #F0F4F8; font-size:13px;'>🔸 {m}</div>",
                                unsafe_allow_html=True)
            else:
                st.success("🎉 Tất cả đơn vị đã nộp báo cáo!")

    # --------------------------------------
    # TAB 3: PHÂN TÍCH BIỂU ĐỒ (8 Form)
    # --------------------------------------
    # ── TAB 3: BIỂU ĐỒ ──
with tab_bieudo:
        if df_cur.empty: st.warning("Chưa có số liệu để vẽ biểu đồ.")
        if df_cur.empty:
            st.warning("⚠️ Chưa có số liệu để vẽ biểu đồ. Vui lòng kiểm tra lại bộ lọc.")
else:
            st.info(f"📊 Đang hiển thị số liệu phân tích cho kỳ: **{l_bc}**")
            if "df_sum" not in dir():
                df_sum = build_summary_df(df_cur.copy(), ky_label)

            # Loại dòng TỔNG CỘNG khỏi biểu đồ
            df_plot = df_sum[df_sum["don_vi"] != "TỔNG CỘNG"].copy()

            st.info(f"📊 Đang hiển thị phân tích số liệu kỳ **{ky_label}** — {len(u_done)} đơn vị đã nộp")

            COLORS = ["#003A6E", "#C8102E", "#1A9E5C", "#E8A800", "#7B3FCC", "#0891B2"]

            def make_bar(df, x, ys, names, title, colors=None):
                fig = go.Figure()
                for i, (y, n) in enumerate(zip(ys, names)):
                    if y in df.columns:
                        fig.add_trace(go.Bar(
                            name=n, x=df[x], y=df[y],
                            marker_color=(colors or COLORS)[i % len(COLORS)],
                            text=df[y], textposition="outside", textfont_size=9
                        ))
                fig.update_layout(
                    title=dict(text=title, font=dict(size=13, color="#003A6E")),
                    barmode="group", height=360,
                    plot_bgcolor="white", paper_bgcolor="white",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font_size=11),
                    xaxis=dict(tickangle=-30, tickfont_size=9),
                    margin=dict(t=60, b=60, l=40, r=20)
                )
                return fig

            # ROW 1
st.markdown("<div class='section-title'>1. LÃNH ĐẠO & 2. NGHỊ QUYẾT</div>", unsafe_allow_html=True)
r1c1, r1c2 = st.columns(2)
with r1c1:
                f1 = go.Figure(data=[go.Bar(name='VB ban hành', x=df_sum['don_vi'], y=df_sum['ld_vanban'], marker_color='#004B87'),
                                     go.Bar(name='Tham mưu', x=df_sum['don_vi'], y=df_sum['ld_thammuu'], marker_color='#C8102E')])
                f1.update_layout(title="Công tác Lãnh đạo, chỉ đạo", barmode='group', height=400)
                st.plotly_chart(f1, use_container_width=True)
                st.plotly_chart(make_bar(df_plot, "don_vi",
                    ["ld_vanban", "ld_thammuu", "ld_cuochop"],
                    ["VB ban hành", "VB tham mưu", "Cuộc họp"],
                    "Công tác Lãnh đạo, Chỉ đạo"), use_container_width=True)
with r1c2:
                f2 = go.Figure(data=[go.Bar(name='Hội nghị NQ', x=df_sum['don_vi'], y=df_sum['nq_hoinghi'], marker_color='#28a745'),
                                     go.Bar(name='VB triển khai', x=df_sum['don_vi'], y=df_sum['nq_vanban'], marker_color='#ffc107')])
                f2.update_layout(title="Quán triệt Nghị quyết", barmode='group', height=400)
                st.plotly_chart(f2, use_container_width=True)
                st.plotly_chart(make_bar(df_plot, "don_vi",
                    ["nq_hoinghi", "nq_vanban", "nq_nguoi"],
                    ["Hội nghị NQ", "VB triển khai", "Người tham gia"],
                    "Quán triệt Nghị quyết"), use_container_width=True)

            st.markdown("<div class='section-title'>3. TUYÊN TRUYỀN & 4. DƯ LUẬN</div>", unsafe_allow_html=True)
            # ROW 2
            st.markdown("<div class='section-title'>3. TUYÊN TRUYỀN & 4. DƯ LUẬN XÃ HỘI</div>", unsafe_allow_html=True)
r2c1, r2c2 = st.columns(2)
with r2c1:
                f3 = px.line(df_sum, x='don_vi', y=['tt_tinbai', 'tt_mxh_bai'], markers=True, title="Tin bài Tuyên truyền & MXH")
                st.plotly_chart(f3, use_container_width=True)
                st.plotly_chart(make_bar(df_plot, "don_vi",
                    ["tt_tinbai", "tt_mxh_bai", "tt_buoi"],
                    ["Tin bài", "Bài MXH", "Buổi TT miệng"],
                    "Công tác Tuyên truyền"), use_container_width=True)
with r2c2:
                f4 = px.pie(values=[df_sum['dl_baocao'].sum(), df_sum['dl_vande'].sum(), df_sum['dl_xuly'].sum()], 
                            names=['Báo cáo gửi đi', 'Vấn đề nổi cộm', 'Đã xử lý'], hole=.4, title="Hoạt động Dư luận xã hội")
                st.plotly_chart(f4, use_container_width=True)
                dl_vals = [
                    df_plot["dl_baocao"].sum() if "dl_baocao" in df_plot.columns else 0,
                    df_plot["dl_vande"].sum() if "dl_vande" in df_plot.columns else 0,
                    df_plot["dl_xuly"].sum() if "dl_xuly" in df_plot.columns else 0,
                ]
                fig_pie = go.Figure(go.Pie(
                    labels=["Báo cáo gửi đi", "Vấn đề nổi cộm", "Đã xử lý"],
                    values=dl_vals, hole=0.5,
                    marker_colors=["#003A6E", "#C8102E", "#1A9E5C"],
                    textfont_size=11
                ))
                fig_pie.update_layout(
                    title=dict(text="Tổng hợp Dư luận Xã hội", font=dict(size=13, color="#003A6E")),
                    height=360, paper_bgcolor="white",
                    legend=dict(font_size=11), margin=dict(t=60, b=20)
                )
                st.plotly_chart(fig_pie, use_container_width=True)

            st.markdown("<div class='section-title'>5. KHOA GIÁO & 6. DÂN VẬN</div>", unsafe_allow_html=True)
            # ROW 3
            st.markdown("<div class='section-title'>5. KHOA GIÁO & 6. DÂN VẬN KHÉO</div>", unsafe_allow_html=True)
r3c1, r3c2 = st.columns(2)
with r3c1:
                f5 = px.bar(df_sum, x='don_vi', y=['kg_chuongtrinh', 'kg_bd_chuyennghiep'], title="Văn hóa - Nghệ thuật & Khoa giáo")
                st.plotly_chart(f5, use_container_width=True)
                st.plotly_chart(make_bar(df_plot, "don_vi",
                    ["kg_chuongtrinh", "kg_bd_chuyennghiep", "kg_clb_thanhlap"],
                    ["CT Tuyên truyền GD", "Biểu diễn NT", "CLB thành lập"],
                    "Khoa giáo, Văn hóa - Văn nghệ"), use_container_width=True)
with r3c2:
                f6 = go.Figure(data=[go.Bar(name='Mô hình mới', x=df_sum['don_vi'], y=df_sum['dv_mh_dangky'], marker_color='#17a2b8'),
                                     go.Bar(name='Hiệu quả', x=df_sum['don_vi'], y=df_sum['dv_mh_hieuqua'], marker_color='#004B87')])
                f6.update_layout(title="Phong trào Dân vận khéo", barmode='stack')
                st.plotly_chart(f6, use_container_width=True)
                st.plotly_chart(make_bar(df_plot, "don_vi",
                    ["dv_mh_dangky", "dv_mh_hieuqua", "dv_mh_moi"],
                    ["MH đăng ký", "MH hiệu quả", "MH mới"],
                    "Phong trào Dân vận Khéo"), use_container_width=True)

            st.markdown("<div class='section-title'>7. NHIỆM VỤ & 8. HỌC VỤ SỐ</div>", unsafe_allow_html=True)
            # ROW 4
            st.markdown("<div class='section-title'>7. NHIỆM VỤ TRỌNG TÂM & 8. BÌNH DÂN HỌC VỤ SỐ</div>", unsafe_allow_html=True)
r4c1, r4c2 = st.columns(2)
with r4c1:
                f7 = go.Figure(data=[go.Bar(name='Giao', x=df_sum['don_vi'], y=df_sum['nv_duocgiao'], marker_color='#E6E6E6'),
                                     go.Bar(name='Hoàn thành', x=df_sum['don_vi'], y=df_sum['nv_hoanthanh'], marker_color='#C8102E')])
                f7.update_layout(title="Tiến độ Nhiệm vụ trọng tâm")
                st.plotly_chart(f7, use_container_width=True)
                st.plotly_chart(make_bar(df_plot, "don_vi",
                    ["nv_duocgiao", "nv_hoanthanh", "nv_dangtrienkhai"],
                    ["Được giao", "Hoàn thành", "Đang triển khai"],
                    "Tiến độ Nhiệm vụ Trọng tâm"), use_container_width=True)
with r4c2:
                f8 = px.bar(df_sum, x='don_vi', y='kq_cb_ai', color='kq_cb_ai', title="Cán bộ ứng dụng AI (Bình dân học vụ số)")
                st.plotly_chart(f8, use_container_width=True)
                st.plotly_chart(make_bar(df_plot, "don_vi",
                    ["kq_cb_ai", "kq_nd_kynang", "kq_nd_vneid"],
                    ["CB dùng AI", "ND Kỹ năng số", "ND VNeID"],
                    "Bình dân Học vụ Số — Kết quả nổi bật"), use_container_width=True)

            # ROW 5 - Tỷ lệ NQ
            st.markdown("<div class='section-title'>TỶ LỆ ĐẢNG VIÊN THAM GIA NGHỊ QUYẾT (%)</div>", unsafe_allow_html=True)
            if "nq_tyle" in df_plot.columns:
                fig_rate = px.bar(
                    df_plot.sort_values("nq_tyle", ascending=True),
                    x="nq_tyle", y="don_vi", orientation="h",
                    color="nq_tyle",
                    color_continuous_scale=["#C8102E", "#E8A800", "#1A9E5C"],
                    range_color=[0, 100],
                    title="Tỷ lệ đảng viên tham gia học NQ (%)",
                    labels={"nq_tyle": "Tỷ lệ (%)", "don_vi": ""},
                    text="nq_tyle"
                )
                fig_rate.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
                fig_rate.update_layout(
                    height=max(300, len(df_plot) * 28),
                    plot_bgcolor="white", paper_bgcolor="white",
                    yaxis=dict(tickfont_size=10),
                    margin=dict(l=180, r=60, t=60, b=20),
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_rate, use_container_width=True)

# ------------------------------------------

# ==========================================
# TAB 4: QUẢN TRỊ ADMIN
# ------------------------------------------
# ==========================================
if st.session_state.role == "admin":
with tab_admin:
        st.markdown("### ⚙️ QUẢN TRỊ HỆ THỐNG")
        st.markdown("<div class='section-title'>⚙️ QUẢN TRỊ HỆ THỐNG</div>", unsafe_allow_html=True)

col_adm1, col_adm2 = st.columns(2)

with col_adm1:
            st.markdown("#### 🗑️ XÓA BÁO CÁO")
            st.markdown("#### 🗑️ Xóa Báo cáo")
cur_data = load_data()
if cur_data:
                d_v = st.selectbox("Chọn đơn vị:", list(set([d['don_vi'] for d in cur_data])), key="dv_del")
                t_h = st.selectbox("Chọn tháng:", list(set([d['ky_bao_cao'] for d in cur_data if d['don_vi']==d_v])), key="th_del")
                if st.button("🔥 XÁC NHẬN XÓA"):
                    new_d = [d for d in cur_data if not (d['don_vi']==d_v and d['ky_bao_cao']==t_h)]
                    save_data(new_d); st.success("Đã xóa!"); st.rerun()
                dv_list = sorted(set(d["don_vi"] for d in cur_data))
                d_v = st.selectbox("Chọn đơn vị cần xóa:", dv_list, key="dv_del")
                th_list = sorted(set(d["ky_bao_cao"] for d in cur_data if d["don_vi"] == d_v))
                if th_list:
                    t_h = st.selectbox("Chọn tháng:", th_list, key="th_del")
                    st.warning(f"⚠️ Sẽ xóa báo cáo của **{d_v}** — **{t_h}**. Thao tác không thể hoàn tác!")
                    if st.button("🔥 XÁC NHẬN XÓA BÁO CÁO", type="primary"):
                        new_d = [d for d in cur_data if not (d["don_vi"] == d_v and d["ky_bao_cao"] == t_h)]
                        save_data(new_d)
                        st.success("✅ Đã xóa báo cáo!")
                        st.rerun()
            else:
                st.info("Chưa có dữ liệu báo cáo nào.")

            st.markdown("---")
            st.markdown("#### 📤 Xuất toàn bộ dữ liệu thô (JSON)")
            if cur_data:
                st.download_button(
                    "⬇️ Tải file JSON backup",
                    data=json.dumps(cur_data, ensure_ascii=False, indent=2),
                    file_name=f"backup_baocao_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json"
                )

with col_adm2:
            st.markdown("#### 🏢 QUẢN LÝ ĐƠN VỊ")
            st.markdown("#### 🏢 Quản lý Danh sách Đơn vị")
u_list = load_units()
            new_u = st.text_input("➕ Tên đơn vị mới:")
            if st.button("THÊM ĐƠN VỊ"):
                if new_u and new_u not in u_list:
                    u_list.append(new_u); save_units(u_list); st.success(f"Thêm thành công: {new_u}!"); st.rerun()
            st.write("---")
            rem_u = st.selectbox("🗑️ Chọn đơn vị cần xóa:", ["-- Chọn --"] + u_list)
            if st.button("XÓA ĐƠN VỊ"):
                if rem_u != "-- Chọn --":
                    u_list.remove(rem_u); save_units(u_list); st.success(f"Đã xóa {rem_u}!"); st.rerun()

            with st.form("form_add_unit"):
                new_u = st.text_input("➕ Tên đơn vị mới:")
                if st.form_submit_button("THÊM ĐƠN VỊ", type="primary"):
                    if new_u.strip() and new_u.strip() not in u_list:
                        u_list.append(new_u.strip())
                        save_units(u_list)
                        st.success(f"✅ Đã thêm: **{new_u.strip()}**")
                        st.rerun()
                    elif new_u.strip() in u_list:
                        st.warning("⚠️ Đơn vị đã tồn tại trong danh sách!")
                    else:
                        st.error("⚠️ Tên đơn vị không được để trống!")

            st.markdown("---")
            with st.form("form_del_unit"):
                rem_u = st.selectbox("🗑️ Chọn đơn vị cần xóa:", ["-- Chọn đơn vị --"] + sorted(u_list))
                if st.form_submit_button("XÓA ĐƠN VỊ", type="secondary"):
                    if rem_u != "-- Chọn đơn vị --":
                        u_list.remove(rem_u)
                        save_units(u_list)
                        st.success(f"✅ Đã xóa: **{rem_u}**")
                        st.rerun()
                    else:
                        st.warning("⚠️ Vui lòng chọn đơn vị cần xóa!")

            st.markdown("---")
            st.markdown(f"**Tổng số đơn vị trong hệ thống:** `{len(u_list)}`")
            with st.expander("Xem toàn bộ danh sách đơn vị"):
                for i, u in enumerate(sorted(u_list), 1):
                    st.text(f"{i:3d}. {u}")
