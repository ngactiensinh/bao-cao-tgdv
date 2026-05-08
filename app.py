import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
import plotly.graph_objects as go
import io
from datetime import datetime
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

st.set_page_config(page_title="Hệ thống Báo cáo TGDV", page_icon="📊", layout="wide")

# ==========================================
# CẤU HÌNH LƯU TRỮ & DANH SÁCH 128 ĐƠN VỊ
# ==========================================
DATA_FILE = "dulieu_baocao.json"
CONFIG_FILE = "config_donvi.json"

DEFAULT_UNITS = [
    "Đảng ủy Công an tỉnh", "Đảng ủy Quân sự tỉnh", "Đảng ủy các cơ quan Đảng tỉnh", "Đảng ủy Ủy ban nhân dân tỉnh",
    "Phường Mỹ Lâm", "Phường Minh Xuân", "Phường Nông Tiến", "Phường An Tường", "Phường Bình Thuận", "Phường Hà Giang 1", "Phường Hà Giang 2",
    "Xã Thượng Lâm", "Xã Lâm Bình", "Xã Minh Quang", "Xã Bình An", "Xã Côn Lôn", "Xã Yên Hoa", "Xã Thượng Nông", "Xã Hồng Thái", "Xã Nà Hang", "Xã Tân Mỹ", "Xã Yên Lập", "Xã Tân An", "Xã Chiêm Hóa", "Xã Hòa An", "Xã Kiên Đài", "Xã Tri Phú", "Xã Kim Bình", "Xã Yên Nguyên", "Xã Yên Phú", "Xã Bạch Xa", "Xã Phù Lưu", "Xã Hàm Yên", "Xã Bình Xa", "Xã Thái Sơn", "Xã Thái Hòa", "Xã Hùng Lợi", "Xã Trung Sơn", "Xã Thái Bình", "Xã Tân Long", "Xã Xuân Vân", "Xã Lực Hành", "Xã Yên Sơn", "Xã Nhữ Khê", "Xã Tân Trào", "Xã Minh Thanh", "Xã Sơn Dương", "Xã Bình Ca", "Xã Tân Thanh", "Xã Sơn Thủy", "Xã Phú Lương", "Xã Trường Sinh", "Xã Hồng Sơn", "Xã Đông Thọ",
    "Xã Lũng Cú", "Xã Đồng Văn", "Xã Sà Phìn", "Xã Phố Bảng", "Xã Lũng Phìn", "Xã Sủng Máng", "Xã Sơn Vĩ", "Xã Mèo Vạc", "Xã Khâu Vai", "Xã Niêm Sơn", "Xã Tát Ngà", "Xã Thắng Mố", "Xã Bạch Đích", "Xã Yên Minh", "Xã Mậu Duệ", "Xã Du Già", "Xã Đường Thượng", "Xã Lùng Tám", "Xã Cán Tỷ", "Xã Nghĩa Thuận", "Xã Quản Bạ", "Xã Tùng Vài", "Xã Yên Cường", "Xã Đường Hồng", "Xã Bắc Mê", "Xã Minh Ngọc", "Xã Ngọc Đường", "Xã Lao Chải", "Xã Thanh Thủy", "Xã Phú Linh", "Xã Linh Hồ", "Xã Bạch Ngọc", "Xã Vị Xuyên", "Xã Việt Lâm", "Xã Tân Quang", "Xã Đồng Tâm", "Xã Liên Hiệp", "Xã Bằng Hành", "Xã Bắc Quang", "Xã Hùng An", "Xã Vĩnh Tuy", "Xã Đồng Yên", "Xã Tiên Yên", "Xã Xuân Giang", "Xã Bằng Lang", "Xã Yên Thành", "Xã Quang Bình", "Xã Tân Trịnh", "Xã Thông Nguyên", "Xã Hồ Thầu", "Xã Nậm Dịch", "Xã Tân Tiến", "Xã Hoàng Su Phì", "Xã Thàng Tín", "Xã Bản Máy", "Xã Pờ Ly Ngài", "Xã Xín Mần", "Xã Pà Vầy Sủ", "Xã Nấm Dẩn", "Xã Trung Thịnh", "Xã Khuôn Lùng", "Xã Trung Hà", "Xã Kiến Thiết", "Xã Hùng Đức", "Xã Minh Sơn", "Xã Minh Tân", "Xã Thuận Hòa", "Xã Tùng Bá", "Xã Thượng Sơn", "Xã Cao Bồ", "Xã Ngọc Long", "Xã Giáp Trung", "Xã Tiên Nguyên", "Xã Quảng Nguyên"
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
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)

def load_units():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return DEFAULT_UNITS

def save_units(units):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f: json.dump(units, f, ensure_ascii=False, indent=4)

def get_months_for_filter(filter_type):
    if filter_type == "Quý I": return ["Tháng 1", "Tháng 2", "Tháng 3"]
    if filter_type == "Quý II": return ["Tháng 4", "Tháng 5", "Tháng 6"]
    if filter_type == "Quý III": return ["Tháng 7", "Tháng 8", "Tháng 9"]
    if filter_type == "Quý IV": return ["Tháng 10", "Tháng 11", "Tháng 12"]
    if filter_type == "6 Tháng Đầu Năm": return [f"Tháng {i}" for i in range(1, 7)]
    if filter_type == "6 Tháng Cuối Năm": return [f"Tháng {i}" for i in range(7, 13)]
    if filter_type == "9 Tháng": return [f"Tháng {i}" for i in range(1, 10)]
    return DANH_SACH_THANG

# ==========================================
# CẤU HÌNH SUPABASE & HÀM ĐẾM LƯỢT TRUY CẬP
# ==========================================
from supabase import create_client, Client
SUPABASE_URL = "https://qqzsdxhqrdfvxnlurnyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFxenNkeGhxcmRmdnhubHVybnliIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU2MjY0NjAsImV4cCI6MjA5MTIwMjQ2MH0.H62F5zYEZ5l47fS4IdAE2JdRdI7inXQqWG0nvXhn2P8"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except: pass

def log_access(app_name):
    key_name = f"da_dem_truy_cap_{app_name}"
    if key_name not in st.session_state:
        try:
            supabase.table("thong_ke_truy_cap").insert({"ten_app": app_name}).execute()
            st.session_state[key_name] = True
        except: pass 

log_access("Thu thập Báo cáo")

# ==========================================
# CSS ĐỎ SẪM - XANH NAVY - TRẮNG
# ==========================================
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
    .status-tag {padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; color: white;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# HỆ THỐNG ĐĂNG NHẬP PHÂN QUYỀN 3 CẤP
# ==========================================
if "role" not in st.session_state:
    st.session_state.role = None

if st.session_state.role is None:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
        with st.form("login_form"):
            c_logo1, c_logo2, c_logo3 = st.columns([1, 2, 1])
            with c_logo2:
                try: st.image("Logo TGDV.png", use_container_width=True)
                except: pass
            st.markdown("<h2 style='color: #004B87; font-weight: 900; text-align: center;'>ĐĂNG NHẬP BÁO CÁO TGDV</h2>", unsafe_allow_html=True)
            pwd = st.text_input("🔑 Mật khẩu truy cập:", type="password")
            if st.form_submit_button("Vào hệ thống", use_container_width=True):
                if pwd == "TGDV@2026": st.session_state.role = "user"; st.rerun()
                elif pwd == "BaoCao@2026": st.session_state.role = "chuyen_vien"; st.rerun()
                elif pwd == "Admin@2026": st.session_state.role = "admin"; st.rerun()
                else: st.error("❌ Mật khẩu không đúng!")
    st.stop()

with st.sidebar:
    role_map = {"admin": "ADMIN", "chuyen_vien": "CHUYÊN VIÊN TỔNG HỢP", "user": "CƠ SỞ"}
    st.markdown(f"<div style='background:#004B87; color:white; padding:10px; border-radius:5px; text-align:center;'>👤 Quyền: <b>{role_map.get(st.session_state.role)}</b></div>", unsafe_allow_html=True)
    if st.button("🚪 Đăng xuất"):
        st.session_state.role = None; st.rerun()

# ==========================================
# CẤU TRÚC TAB
# ==========================================
st.markdown("<h1 class='main-header'>HỆ THỐNG THU THẬP BÁO CÁO CƠ SỞ</h1>", unsafe_allow_html=True)

if st.session_state.role == "admin":
    tabs = st.tabs(["📝 NHẬP BÁO CÁO", "📊 THỐNG KÊ & BIỂU ĐỒ", "⚙️ QUẢN TRỊ ADMIN"])
    tab_nhap, tab_bieudo, tab_admin = tabs[0], tabs[1], tabs[2]
elif st.session_state.role == "chuyen_vien":
    tabs = st.tabs(["📝 NHẬP BÁO CÁO", "📊 THỐNG KÊ & BIỂU ĐỒ"])
    tab_nhap, tab_bieudo = tabs[0], tabs[1]
else:
    tabs = st.tabs(["📝 NHẬP BÁO CÁO"])
    tab_nhap = tabs[0]

# ==========================================
# TAB NHẬP BÁO CÁO (CƠ CHẾ AUTO-FILL FULL 9 MỤC)
# ==========================================
with tab_nhap:
    st.markdown("### 1️⃣ XÁC ĐỊNH ĐƠN VỊ & KỲ BÁO CÁO")
    c_top1, c_top2, c_top3 = st.columns([2, 1.5, 1.5])
    don_vi = c_top1.selectbox("🏢 Đơn vị báo cáo:", load_units(), index=None, placeholder="Gõ tìm đơn vị...")
    ky_bao_cao = c_top3.selectbox("🗓️ Tháng báo cáo:", DANH_SACH_THANG, index=None, placeholder="Chọn tháng...")
    
    old_data = {}
    nguoi_bc_default = ""
    if don_vi and ky_bao_cao:
        all_data = load_data()
        for d in all_data:
            if d.get('don_vi') == don_vi and d.get('ky_bao_cao') == ky_bao_cao:
                old_data = d
                nguoi_bc_default = d.get('nguoi_bao_cao', '')
                break
    nguoi_bao_cao = c_top2.text_input("👤 Người báo cáo / SĐT:", value=nguoi_bc_default)

    if don_vi and ky_bao_cao:
        if old_data: 
            st.success(f"💡 Hệ thống đã điền sẵn số liệu cũ của **{don_vi}** - **{ky_bao_cao}**. Đồng chí chỉ cần sửa những ô bị sai!")
        else: 
            st.info(f"✨ Đang lập báo cáo mới cho **{don_vi}** - **{ky_bao_cao}**.")
            
        st.markdown("<div class='step-header'>2️⃣ BƯỚC 2: CẬP NHẬT SỐ LIỆU VÀ GỬI</div>", unsafe_allow_html=True)
        with st.form("form_bao_cao"):
            
            with st.expander("1. CÔNG TÁC LÃNH ĐẠO, CHỈ ĐẠO", expanded=False):
                c1, c2, c3 = st.columns(3)
                ld_vanban = c1.number_input("Số văn bản cấp ủy xã ban hành", min_value=0, value=int(old_data.get('ld_vanban', 0)))
                ld_thammuu = c2.number_input("Số văn bản tham mưu cấp trên", min_value=0, value=int(old_data.get('ld_thammuu', 0)))
                ld_cuochop = c3.number_input("Số cuộc họp, hội nghị triển khai", min_value=0, value=int(old_data.get('ld_cuochop', 0)))

            with st.expander("2. HỌC TẬP, QUÁN TRIỆT NGHỊ QUYẾT", expanded=False):
                c1, c2, c3, c4 = st.columns(4)
                nq_hoinghi = c1.number_input("Số hội nghị tổ chức ", min_value=0, value=int(old_data.get('nq_hoinghi', 0)))
                nq_nguoi = c2.number_input("Số người tham gia học tập", min_value=0, value=int(old_data.get('nq_nguoi', 0)))
                nq_vanban = c3.number_input("Số văn bản đã triển khai", min_value=0, value=int(old_data.get('nq_vanban', 0)))
                nq_tyle = c4.number_input("Tỷ lệ đảng viên tham gia (%)", min_value=0.0, max_value=100.0, value=float(old_data.get('nq_tyle', 0.0)))

            with st.expander("3. CÔNG TÁC TUYÊN TRUYỀN", expanded=False):
                st.markdown("<p style='color:#C8102E; font-weight:bold;'>3.1 Tuyên truyền chung & Miệng</p>", unsafe_allow_html=True)
                c1, c2, c3, c4 = st.columns(4)
                tt_tinbai = c1.number_input("Số tin, bài, pano, khẩu hiệu", min_value=0, value=int(old_data.get('tt_tinbai', 0)))
                tt_loa = c2.number_input("Số lượt loa truyền thanh", min_value=0, value=int(old_data.get('tt_loa', 0)))
                tt_buoi = c3.number_input("Số buổi tuyên truyền miệng", min_value=0, value=int(old_data.get('tt_buoi', 0)))
                tt_nguoi = c4.number_input("Số người nghe TT miệng", min_value=0, value=int(old_data.get('tt_nguoi', 0)))
                
                st.markdown("<p style='color:#C8102E; font-weight:bold;'>3.2 Báo chí, Mạng xã hội</p>", unsafe_allow_html=True)
                c5, c6 = st.columns(2)
                tt_mxh_bai = c5.number_input("Số tin, bài trên trang thông tin/Cổng TT", min_value=0, value=int(old_data.get('tt_mxh_bai', 0)))
                tt_mxh_tuongtac = c6.number_input("Lượt chia sẻ/tương tác MXH", min_value=0, value=int(old_data.get('tt_mxh_tuongtac', 0)))

            with st.expander("4. DƯ LUẬN XÃ HỘI", expanded=False):
                c1, c2, c3 = st.columns(3)
                dl_baocao = c1.number_input("Số báo cáo dư luận gửi cấp trên", min_value=0, value=int(old_data.get('dl_baocao', 0)))
                dl_vande = c2.number_input("Số vấn đề nổi cộm được phát hiện", min_value=0, value=int(old_data.get('dl_vande', 0)))
                dl_xuly = c3.number_input("Số vụ việc đã giải quyết", min_value=0, value=int(old_data.get('dl_xuly', 0)))

            with st.expander("5. KHOA GIÁO, VĂN HÓA - VĂN NGHỆ", expanded=False):
                st.markdown("<p style='color:#C8102E; font-weight:bold;'>5.1 Lĩnh vực Khoa giáo (Y tế, Giáo dục, KHCN...)</p>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                kg_chuongtrinh = c1.number_input("Số chương trình tuyên truyền giáo dục", min_value=0, value=int(old_data.get('kg_chuongtrinh', 0)))
                kg_lop = c2.number_input("Số buổi liên quan y tế, môi trường", min_value=0, value=int(old_data.get('kg_lop', 0)))

                st.markdown("<p style='color:#C8102E; font-weight:bold;'>5.2 Lĩnh vực Văn hóa - Nghệ thuật, Thể thao</p>", unsafe_allow_html=True)
                c3, c4 = st.columns(2)
                kg_bd_chuyennghiep = c3.number_input("Số buổi BD nghệ thuật chuyên nghiệp", min_value=0, value=int(old_data.get('kg_bd_chuyennghiep', 0)))
                kg_bd_quanchung = c4.number_input("Số buổi BD nghệ thuật quần chúng", min_value=0, value=int(old_data.get('kg_bd_quanchung', 0)))

                c5, c6 = st.columns(2)
                kg_clb_thanhlap = c5.number_input("Số câu lạc bộ Văn hóa, Nghệ thuật thành lập", min_value=0, value=int(old_data.get('kg_clb_thanhlap', 0)))
                kg_clb_thanhvien = c6.number_input("Số thành viên các câu lạc bộ", min_value=0, value=int(old_data.get('kg_clb_thanhvien', 0)))

                c7, c8 = st.columns(2)
                kg_hoatdong = c7.number_input("Số HĐ Văn hóa - VN chung", min_value=0, value=int(old_data.get('kg_hoatdong', 0)))
                kg_hd_vhtt = c8.number_input("Số HĐ Văn hóa-Thể thao (lễ hội, giải đấu...)", min_value=0, value=int(old_data.get('kg_hd_vhtt', 0)))

                kg_khokhan = st.text_area("Những khó khăn, vướng mắc (Khoa giáo, VH-VN):", value=str(old_data.get('kg_khokhan', '')))

            with st.expander("6. CÔNG TÁC DÂN VẬN (DÂN VẬN KHÉO)", expanded=False):
                st.markdown("<p style='color:#C8102E; font-weight:bold;'>6.1 Phong trào Dân vận khéo</p>", unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                dv_mh_dangky = c1.number_input("Số mô hình đăng ký mới", min_value=0, value=int(old_data.get('dv_mh_dangky', 0)))
                dv_mh_hieuqua = c2.number_input("Số mô hình hoạt động hiệu quả", min_value=0, value=int(old_data.get('dv_mh_hieuqua', 0)))
                dv_mh_moi = c3.number_input("Số mô hình mới trong kỳ", min_value=0, value=int(old_data.get('dv_mh_moi', 0)))
                
                st.markdown("<p style='color:#C8102E; font-weight:bold;'>6.2 Hoạt động dân vận chung</p>", unsafe_allow_html=True)
                c4, c5, c6 = st.columns(3)
                dv_cuocvandong = c4.number_input("Số cuộc vận động, tuyên truyền", min_value=0, value=int(old_data.get('dv_cuocvandong', 0)))
                dv_nguoithamgia = c5.number_input("Số lượt người tham gia", min_value=0, value=int(old_data.get('dv_nguoithamgia', 0)))
                dv_tiepxuc = c6.number_input("Số buổi đối thoại với Nhân dân", min_value=0, value=int(old_data.get('dv_tiepxuc', 0)))

            with st.expander("7. NHIỆM VỤ TRỌNG TÂM", expanded=False):
                c1, c2, c3 = st.columns(3)
                nv_duocgiao = c1.number_input("Số nhiệm vụ được giao trong kỳ", min_value=0, value=int(old_data.get('nv_duocgiao', 0)))
                nv_hoanthanh = c2.number_input("Số nhiệm vụ đã hoàn thành", min_value=0, value=int(old_data.get('nv_hoanthanh', 0)))
                nv_dangtrienkhai = c3.number_input("Số nhiệm vụ đang triển khai", min_value=0, value=int(old_data.get('nv_dangtrienkhai', 0)))
                nv_ketqua = st.text_area("Kết quả mô hình thí điểm nổi bật (Nếu có):", value=str(old_data.get('nv_ketqua', '')))

            with st.expander("8. CHUYÊN ĐỀ: BÌNH DÂN HỌC VỤ SỐ", expanded=False):
                st.markdown("<p style='color:#004B87; font-weight:bold;'>- Công tác tuyên truyền & Tổ công nghệ:</p>", unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                bd_tinbai = c1.number_input("Số tin bài về chuyển đổi số", min_value=0, value=int(old_data.get('bd_tinbai', 0)))
                bd_cuocthi = c2.number_input("Số cuộc thi về kỹ năng số", min_value=0, value=int(old_data.get('bd_cuocthi', 0)))
                kq_tocongnghe = c3.number_input("Số Tổ công nghệ số cộng đồng", min_value=0, value=int(old_data.get('kq_tocongnghe', 0)))
                
                st.markdown("<p style='color:#004B87; font-weight:bold;'>- Đối với Chi bộ & Cán bộ (Điền Số lượng/Tổng số):</p>", unsafe_allow_html=True)
                ts_chibo = st.number_input("Tổng số chi bộ của toàn địa phương/đơn vị", min_value=0, value=int(old_data.get('ts_chibo', 0)))
                c4, c5 = st.columns(2)
                kq_chibo_cd = c4.number_input("Số chi bộ đã sinh hoạt chuyên đề Kỹ năng số", min_value=0, value=int(old_data.get('kq_chibo_cd', 0)))
                kq_chibo_sotay = c5.number_input("Số chi bộ sử dụng Sổ tay đảng viên điện tử", min_value=0, value=int(old_data.get('kq_chibo_sotay', 0)))
                
                ts_cbccvc = st.number_input("Tổng số cán bộ, công chức, viên chức của đơn vị", min_value=0, value=int(old_data.get('ts_cbccvc', 0)))
                c6, c7 = st.columns(2)
                kq_cb_ai = c6.number_input("Số cán bộ biết và ứng dụng công cụ AI", min_value=0, value=int(old_data.get('kq_cb_ai', 0)))
                kq_cb_khoahoc = c7.number_input("Số cán bộ hoàn thành khóa học chuyển đổi số", min_value=0, value=int(old_data.get('kq_cb_khoahoc', 0)))
                
                st.markdown("<p style='color:#004B87; font-weight:bold;'>- Đối với Người dân & Người lao động:</p>", unsafe_allow_html=True)
                ts_nd_truongthanh = st.number_input("Tổng số người dân trong độ tuổi trưởng thành", min_value=0, value=int(old_data.get('ts_nd_truongthanh', 0)))
                c8, c9 = st.columns(2)
                kq_nd_kynang = c8.number_input("Số người dân có kỹ năng số cơ bản", min_value=0, value=int(old_data.get('kq_nd_kynang', 0)))
                kq_nd_vneid = c9.number_input("Số người dân phổ cập kỹ năng trên VNeID", min_value=0, value=int(old_data.get('kq_nd_vneid', 0)))
                
                c10, c11 = st.columns(2)
                kq_nd_smartphone = c10.number_input("Số người dân có sử dụng Smartphone", min_value=0, value=int(old_data.get('kq_nd_smartphone', 0)))
                kq_lop_nd = c11.number_input("Số buổi học cộng đồng cho người dân", min_value=0, value=int(old_data.get('kq_lop_nd', 0)))

            with st.expander("9. ĐÁNH GIÁ CHUNG & KHÓ KHĂN", expanded=False):
                tl_mohinh = st.text_area("Nêu các mô hình, cách làm sáng tạo hiệu quả:", value=str(old_data.get('tl_mohinh', '')))
                tl_khokhan = st.text_area("Các khó khăn, vướng mắc chung:", value=str(old_data.get('tl_khokhan', '')))

            st.markdown("<style>.stButton>button[kind='primary'] {background-color: #C8102E; border:none;}</style>", unsafe_allow_html=True)
            
            if st.form_submit_button("🚀 GỬI / CẬP NHẬT BÁO CÁO", type="primary", use_container_width=True):
                if not don_vi or not ky_bao_cao or not nguoi_bao_cao: st.error("⚠️ Vui lòng điền đủ Đơn vị, Tháng và Người báo cáo!")
                else:
                    rec = {
                        "don_vi": don_vi, "nguoi_bao_cao": nguoi_bao_cao, "ky_bao_cao": ky_bao_cao, "ngay_nop": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "ld_vanban": ld_vanban, "ld_thammuu": ld_thammuu, "ld_cuochop": ld_cuochop,
                        "nq_hoinghi": nq_hoinghi, "nq_nguoi": nq_nguoi, "nq_vanban": nq_vanban, "nq_tyle": nq_tyle,
                        "tt_tinbai": tt_tinbai, "tt_loa": tt_loa, "tt_buoi": tt_buoi, "tt_nguoi": tt_nguoi, "tt_mxh_bai": tt_mxh_bai, "tt_mxh_tuongtac": tt_mxh_tuongtac,
                        "dl_baocao": dl_baocao, "dl_vande": dl_vande, "dl_xuly": dl_xuly,
                        "kg_hoatdong": kg_hoatdong, "kg_chuongtrinh": kg_chuongtrinh, "kg_lop": kg_lop,
                        "kg_bd_chuyennghiep": kg_bd_chuyennghiep, "kg_bd_quanchung": kg_bd_quanchung,
                        "kg_clb_thanhlap": kg_clb_thanhlap, "kg_clb_thanhvien": kg_clb_thanhvien,
                        "kg_hd_vhtt": kg_hd_vhtt, "kg_khokhan": kg_khokhan,
                        "dv_mh_dangky": dv_mh_dangky, "dv_mh_hieuqua": dv_mh_hieuqua, "dv_mh_moi": dv_mh_moi, "dv_cuocvandong": dv_cuocvandong, "dv_nguoithamgia": dv_nguoithamgia, "dv_tiepxuc": dv_tiepxuc,
                        "nv_duocgiao": nv_duocgiao, "nv_hoanthanh": nv_hoanthanh, "nv_dangtrienkhai": nv_dangtrienkhai, "nv_ketqua": nv_ketqua,
                        "bd_tinbai": bd_tinbai, "bd_cuocthi": bd_cuocthi, "kq_tocongnghe": kq_tocongnghe,
                        "ts_chibo": ts_chibo, "kq_chibo_cd": kq_chibo_cd, "kq_chibo_sotay": kq_chibo_sotay,
                        "ts_cbccvc": ts_cbccvc, "kq_cb_ai": kq_cb_ai, "kq_cb_khoahoc": kq_cb_khoahoc,
                        "ts_nd_truongthanh": ts_nd_truongthanh, "kq_nd_kynang": kq_nd_kynang, "kq_nd_vneid": kq_nd_vneid,
                        "kq_nd_smartphone": kq_nd_smartphone, "kq_lop_nd": kq_lop_nd,
                        "tl_mohinh": tl_mohinh, "tl_khokhan": tl_khokhan
                    }
                    data = load_data(); data = [d for d in data if not (d['don_vi'] == don_vi and d.get('ky_bao_cao') == ky_bao_cao)]
                    data.append(rec); save_data(data); st.success(f"✅ Đã ghi nhận thành công báo cáo của {don_vi} - {ky_bao_cao}!")

# ==========================================
# TAB THỐNG KÊ - NÂNG CẤP THEO DÕI TIẾN ĐỘ
# ==========================================
if st.session_state.role in ["admin", "chuyen_vien"]:
    with tab_bieudo:
        data = load_data()
        st.markdown("<h3 style='color:#004B87;'>🗓️ LỌC TỔNG HỢP & THEO DÕI TIẾN ĐỘ</h3>", unsafe_allow_html=True)
        c_f1, c_f2 = st.columns(2)
        loai_bc = c_f1.selectbox("Chọn kỳ tổng hợp:", ["Tháng", "Quý I", "Quý II", "Quý III", "Quý IV", "Cả Năm"])
        if loai_bc == "Tháng":
            th_bc = c_f2.selectbox("Tháng cụ thể:", DANH_SACH_THANG)
            df = pd.DataFrame([d for d in data if d['ky_bao_cao'] == th_bc])
        else:
            m_list = get_months_for_filter(loai_bc)
            df = pd.DataFrame([d for d in data if d['ky_bao_cao'] in m_list])

        # --- TÍNH TOÁN TIẾN ĐỘ ---
        all_units = load_units()
        units_done = df['don_vi'].unique().tolist() if not df.empty else []
        units_missing = [u for u in all_units if u not in units_done]

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='metric-card'><p class='metric-title'>Đã nộp</p><p class='metric-number' style='color:#28a745;'>{len(units_done)}</p></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-card'><p class='metric-title'>Chưa nộp</p><p class='metric-number'>{len(units_missing)}</p></div>", unsafe_allow_html=True)
        rate = (len(units_done)/len(all_units)*100) if all_units else 0
        c3.markdown(f"<div class='metric-card'><p class='metric-title'>Tỷ lệ hoàn thành</p><p class='metric-number' style='color:#004B87;'>{rate:.1f}%</p></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='metric-card'><p class='metric-title'>Tổng số đơn vị</p><p class='metric-number'>{len(all_units)}</p></div>", unsafe_allow_html=True)

        # --- HIỂN THỊ DANH SÁCH CHI TIẾT ---
        st.markdown("<div class='section-title'>📊 CHI TIẾT TIẾN ĐỘ NỘP BÁO CÁO</div>", unsafe_allow_html=True)
        col_list1, col_list2 = st.columns(2)
        
        with col_list1:
            st.markdown(f"<p style='color:#28a745; font-weight:bold;'>✅ DANH SÁCH ĐÃ NỘP ({len(units_done)})</p>", unsafe_allow_html=True)
            if units_done:
                df_done = df[['don_vi', 'ngay_nop', 'nguoi_bao_cao']].drop_duplicates(subset=['don_vi'], keep='last')
                st.dataframe(df_done.rename(columns={'don_vi':'Đơn vị', 'ngay_nop':'Nộp lúc', 'nguoi_bao_cao':'Người nộp'}), use_container_width=True, hide_index=True)
                st.caption("*(Lưu ý: Các đơn vị nộp sau ngày 18 sẽ được coi là nộp muộn)*")
            else: st.write("Chưa có đơn vị nào nộp.")

        with col_list2:
            st.markdown(f"<p style='color:#C8102E; font-weight:bold;'>❌ DANH SÁCH CHƯA NỘP ({len(units_missing)})</p>", unsafe_allow_html=True)
            if units_missing:
                st.info("Đồng chí có thể copy danh sách này để nhắc nhở trên Zalo:")
                st.code(", ".join(units_missing))
                for u in sorted(units_missing):
                    st.markdown(f"🔸 {u}")
            else: st.success("🎉 Tuyệt vời! 100% đơn vị đã hoàn thành báo cáo.")

        if not df.empty:
            st.write("---")
            
            # --- CODE TẠO EXCEL TỔNG HỢP ---
            num_cols = df.select_dtypes(include='number').columns
            agg_dict = {}
            for col in num_cols:
                if col == 'nq_tyle': agg_dict[col] = 'mean'  
                else: agg_dict[col] = 'sum'                  
                
            def gop_chu(x):
                text_list = [str(i).strip() for i in x if pd.notna(i) and str(i).strip() != ""]
                unique_texts = list(dict.fromkeys(text_list)) 
                return "\n".join([f"- {t}" for t in unique_texts]) if unique_texts else ""
            
            if 'nv_ketqua' in df.columns: agg_dict['nv_ketqua'] = gop_chu
            if 'tl_mohinh' in df.columns: agg_dict['tl_mohinh'] = gop_chu
            if 'tl_khokhan' in df.columns: agg_dict['tl_khokhan'] = gop_chu
            if 'kg_khokhan' in df.columns: agg_dict['kg_khokhan'] = gop_chu 
            
            if 'nguoi_bao_cao' in df.columns: 
                agg_dict['nguoi_bao_cao'] = lambda x: ", ".join(list(dict.fromkeys([str(i).strip() for i in x if pd.notna(i) and str(i).strip() != ""])))

            df_sum = df.groupby('don_vi').agg(agg_dict).reset_index()
            df_sum['ky_bao_cao'] = loai_bc 

            for col in DICT_DICH_THUAT.keys():
                if col not in df_sum.columns:
                    df_sum[col] = 0 if col in num_cols else ""
            
            df_export = df_sum[list(DICT_DICH_THUAT.keys())].rename(columns=DICT_DICH_THUAT)
            
            total_row = {}
            for col in df_export.columns:
                if pd.api.types.is_numeric_dtype(df_export[col]):
                    if col == DICT_DICH_THUAT.get('nq_tyle'):
                        total_row[col] = round(df_export[col].mean(), 2) 
                    else:
                        total_row[col] = df_export[col].sum()
                else:
                    total_row[col] = "" 
            
            total_row[DICT_DICH_THUAT['don_vi']] = "TỔNG CỘNG"
            df_export = pd.concat([df_export, pd.DataFrame([total_row])], ignore_index=True)
            
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_export.to_excel(writer, index=False, sheet_name='Bao_Cao', startrow=1)
                worksheet = writer.sheets['Bao_Cao']
                thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
                
                super_headers = [
                    (1, 3, "THÔNG TIN CHUNG", "004B87"), 
                    (4, 6, "1. LÃNH ĐẠO, CHỈ ĐẠO", "C8102E"),
                    (7, 10, "2. QUÁN TRIỆT NGHỊ QUYẾT", "004B87"), 
                    (11, 16, "3. CÔNG TÁC TUYÊN TRUYỀN", "C8102E"),
                    (17, 19, "4. DƯ LUẬN XÃ HỘI", "004B87"), 
                    (20, 28, "5. KHOA GIÁO, VH-VN", "C8102E"),
                    (29, 34, "6. CÔNG TÁC DÂN VẬN", "004B87"), 
                    (35, 38, "7. NHIỆM VỤ TRỌNG TÂM", "C8102E"),
                    (39, 52, "8. BÌNH DÂN HỌC VỤ SỐ", "004B87"), 
                    (53, 54, "9. ĐÁNH GIÁ CHUNG", "C8102E")
                ]
                for start_col, end_col, title, color in super_headers:
                    worksheet.merge_cells(start_row=1, start_column=start_col, end_row=1, end_column=end_col)
                    cell = worksheet.cell(row=1, column=start_col)
                    cell.value = title
                    cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
                    cell.font = Font(bold=True, color="FFFFFF", size=12)
                    cell.alignment = Alignment(horizontal='center', vertical='center')
                    for col in range(start_col, end_col + 1): worksheet.cell(row=1, column=col).border = thin_border
                
                for col_num, col_name in enumerate(df_export.columns, 1):
                    cell = worksheet.cell(row=2, column=col_num)
                    cell.fill = PatternFill(start_color="E6E6E6", end_color="E6E6E6", fill_type="solid")
                    cell.font = Font(bold=True, color="000000")
                    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
                    cell.border = thin_border
                    
                for i, col in enumerate(worksheet.columns, 1):
                    max_length = 0
                    column_letter = get_column_letter(i)
                    for cell in col:
                        try:
                            if len(str(cell.value)) > max_length: max_length = len(str(cell.value))
                        except: pass
                        cell.border = thin_border
                    worksheet.column_dimensions[column_letter].width = min(max(max_length + 2, 12), 40)
                    
                worksheet.row_dimensions[1].height = 25
                worksheet.row_dimensions[2].height = 35
                
                last_row = worksheet.max_row
                for col_idx in range(1, worksheet.max_column + 1):
                    cell = worksheet.cell(row=last_row, column=col_idx)
                    cell.font = Font(bold=True, color="C8102E")
                    cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid") 
            
            col_btn1, col_btn2 = st.columns([2, 1.5])
            with col_btn2:
                st.download_button(label="📥 TẢI BẢNG TỔNG HỢP CHUYÊN NGHIỆP (EXCEL)", data=buffer.getvalue(), file_name=f"Bao_Cao_TGDV_{loai_bc}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", type="primary", use_container_width=True)

# --- TAB ADMIN (GIỮ NGUYÊN) ---
if st.session_state.role == "admin":
    with tab_admin:
        st.markdown("### ⚙️ QUẢN TRỊ HỆ THỐNG")
        c_del1, c_del2 = st.columns(2)
        with c_del1:
            st.markdown("#### 🗑️ Xóa báo cáo sai (Dọn dẹp Test)")
            current_data = load_data()
            if current_data:
                dv_del = st.selectbox("Chọn đơn vị muốn xóa:", list(set([d['don_vi'] for d in current_data])), key="del_dv")
                th_del = st.selectbox("Chọn tháng muốn xóa:", list(set([d['ky_bao_cao'] for d in current_data if d['don_vi'] == dv_del])), key="del_th")
                if st.button("🔥 XÁC NHẬN XÓA BÁO CÁO NÀY"):
                    new_data = [d for d in current_data if not (d['don_vi'] == dv_del and d['ky_bao_cao'] == th_del)]
                    save_data(new_data); st.success(f"Đã dọn dẹp sạch sẽ dữ liệu của {dv_del} - {th_del}"); st.rerun()
            else: st.info("Chưa có dữ liệu báo cáo nào để xóa.")
            
        with c_del2:
            st.markdown("#### 🏢 Quản lý danh sách Đơn vị")
            u_list = load_units()
            new_u = st.text_input("Thêm đơn vị mới:")
            if st.button("➕ Thêm"):
                if new_u and new_u not in u_list: u_list.append(new_u); save_units(u_list); st.rerun()
            rem_u = st.selectbox("Xóa đơn vị khỏi danh sách:", ["-- Chọn --"] + u_list)
            if st.button("🗑️ Xóa khỏi DS"):
                if rem_u != "-- Chọn --": u_list.remove(rem_u); save_units(u_list); st.rerun()
