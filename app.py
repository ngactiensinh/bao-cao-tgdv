import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

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
    return DANH_SACH_THANG # Cả Năm

# ==========================================
# CSS TÙY CHỈNH (ĐỎ SẪM - XANH NAVY - TRẮNG)
# ==========================================
st.markdown("""
<style>
    .stApp { background-color: #f4f6f9; }
    .main-header {color: #004B87; font-weight: 900; text-align: center; text-transform: uppercase; margin-bottom: 25px; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);}
    .stButton>button {background-color: #004B87; color: white; font-weight: bold; border-radius: 6px; border: none; transition: all 0.3s;}
    .stButton>button:hover {background-color: #C8102E; color: white; transform: translateY(-2px); box-shadow: 0 4px 8px rgba(200, 16, 46, 0.3);}
    [data-testid="stForm"] {background-color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 5px solid #004B87;}
    [data-testid="stExpander"] {background-color: #ffffff; border-left: 4px solid #C8102E; border-radius: 5px; margin-bottom: 10px;}
    [data-testid="stExpander"] summary p {font-weight: bold; color: #004B87; font-size: 16px;}
    .metric-card {background-color: #ffffff; padding: 20px; border-radius: 10px; border-top: 4px solid #C8102E; box-shadow: 0 4px 10px rgba(0,0,0,0.05); text-align: center;}
    .metric-title {font-size: 14px; color: #004B87; font-weight: bold; text-transform: uppercase; margin-bottom: 5px;}
    .metric-number {font-size: 28px; color: #C8102E; font-weight: 900; margin: 0;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# HỆ THỐNG ĐĂNG NHẬP (HỖ TRỢ ENTER)
# ==========================================
if "role" not in st.session_state:
    st.session_state.role = None

if st.session_state.role is None:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
        # Sử dụng form để có thể ấn Enter khi nhập xong mật khẩu
        with st.form("login_form"):
            c_logo1, c_logo2, c_logo3 = st.columns([1, 2, 1])
            with c_logo2:
                try:
                    st.image("Logo TGDV.png", use_container_width=True)
                except:
                    pass
            st.markdown("<h2 style='color: #004B87; font-weight: 900; font-size: 24px; text-align: center; margin-bottom: 20px;'>ĐĂNG NHẬP HỆ THỐNG<br>BÁO CÁO TGDV</h2>", unsafe_allow_html=True)
            
            pwd = st.text_input("🔑 Nhập mật khẩu truy cập:", type="password")
            submitted = st.form_submit_button("Đăng nhập", use_container_width=True)
            
            if submitted:
                if pwd == "TGDV@2026":
                    st.session_state.role = "user"
                    st.rerun()
                elif pwd == "admin123":
                    st.session_state.role = "admin"
                    st.rerun()
                else:
                    st.error("❌ Mật khẩu không đúng!")
    st.stop() 

with st.sidebar:
    st.markdown(f"<div style='background-color:#004B87; color:white; padding:10px; border-radius:5px; text-align:center; margin-bottom:15px;'>👤 Đang đăng nhập: <b>{'LÃNH ĐẠO / ADMIN' if st.session_state.role == 'admin' else 'CÁN BỘ CƠ SỞ'}</b></div>", unsafe_allow_html=True)
    if st.button("🚪 Đăng xuất an toàn"):
        st.session_state.role = None
        st.rerun()

# ==========================================
# GIAO DIỆN CHÍNH
# ==========================================
st.markdown("<h1 class='main-header'>HỆ THỐNG THU THẬP BÁO CÁO CƠ SỞ</h1>", unsafe_allow_html=True)

if st.session_state.role == "admin":
    tabs = st.tabs(["📝 NHẬP BÁO CÁO", "📊 THỐNG KÊ & BIỂU ĐỒ", "⚙️ QUẢN TRỊ ADMIN"])
    tab_nhap, tab_bieudo, tab_admin = tabs[0], tabs[1], tabs[2]
else:
    tabs = st.tabs(["📝 NHẬP BÁO CÁO"])
    tab_nhap = tabs[0]

# ==========================================
# TAB NHẬP BÁO CÁO
# ==========================================
with tab_nhap:
    st.info("💡 **Hướng dẫn:** Gõ tên đơn vị vào ô trống để tìm kiếm. Nhập lại báo cáo của tháng cũ sẽ tự động **ghi đè** số liệu cũ.")
    with st.form("form_bao_cao"):
        col1, col2, col3 = st.columns([2, 1.5, 1.5])
        # Thiết lập index=None để ô mặc định trống, bắt người dùng gõ/chọn
        don_vi = col1.selectbox("🏢 Chọn Đơn vị báo cáo:", load_units(), index=None, placeholder="Gõ để tìm kiếm hoặc chọn...")
        nguoi_bao_cao = col2.text_input("👤 Người báo cáo / SĐT:")
        ky_bao_cao = col3.selectbox("🗓️ Thời điểm báo cáo:", DANH_SACH_THANG, index=None, placeholder="Chọn tháng...")
        
        with st.expander("1. CÔNG TÁC LÃNH ĐẠO, CHỈ ĐẠO", expanded=False):
            c1, c2, c3 = st.columns(3)
            ld_vanban = c1.number_input("Số VB cấp ủy ban hành", min_value=0, value=0)
            ld_thammuu = c2.number_input("Số VB tham mưu cấp trên", min_value=0, value=0)
            ld_cuochop = c3.number_input("Số cuộc họp, hội nghị", min_value=0, value=0)

        with st.expander("2. HỌC TẬP, QUÁN TRIỆT NGHỊ QUYẾT", expanded=False):
            c1, c2 = st.columns(2)
            nq_hoinghi = c1.number_input("Số hội nghị tổ chức", min_value=0, value=0)
            nq_nguoi = c2.number_input("Số người tham gia", min_value=0, value=0)
            c3, c4 = st.columns(2)
            nq_vanban = c3.number_input("Số VB đã triển khai", min_value=0, value=0)
            nq_tyle = c4.number_input("Tỷ lệ đảng viên tham gia (%)", min_value=0.0, value=0.0)

        with st.expander("3. CÔNG TÁC TUYÊN TRUYỀN", expanded=False):
            st.markdown("<p style='color:#C8102E; font-weight:bold;'>3.1 Tuyên truyền chung & Miệng</p>", unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            tt_tinbai = c1.number_input("Số tin/bài/pano", min_value=0, value=0)
            tt_loa = c2.number_input("Số lượt loa truyền thanh", min_value=0, value=0)
            tt_buoi = c3.number_input("Số buổi TT miệng", min_value=0, value=0)
            tt_nguoi = c4.number_input("Số người nghe TT miệng", min_value=0, value=0)
            st.markdown("<p style='color:#C8102E; font-weight:bold; margin-top:10px;'>3.2 Báo chí, Mạng xã hội</p>", unsafe_allow_html=True)
            c5, c6 = st.columns(2)
            tt_mxh_bai = c5.number_input("Số tin, bài trên cổng/trang xã", min_value=0, value=0)
            tt_mxh_tuongtac = c6.number_input("Số bài chia sẻ Facebook/Zalo", min_value=0, value=0)

        with st.expander("4. DƯ LUẬN XÃ HỘI", expanded=False):
            c1, c2, c3 = st.columns(3)
            dl_baocao = c1.number_input("Số báo cáo DLXH", min_value=0, value=0)
            dl_vande = c2.number_input("Số vấn đề nổi cộm", min_value=0, value=0)
            dl_xuly = c3.number_input("Số vụ việc đã xử lý", min_value=0, value=0)

        with st.expander("5. KHOA GIÁO, VĂN HÓA - VĂN NGHỆ", expanded=False):
            c1, c2, c3 = st.columns(3)
            kg_hoatdong = c1.number_input("Số hoạt động VH-VN", min_value=0, value=0)
            kg_chuongtrinh = c2.number_input("Số chương trình TT giáo dục", min_value=0, value=0)
            kg_lop = c3.number_input("Số lớp/buổi (giáo dục, y tế...)", min_value=0, value=0)

        with st.expander("6. CÔNG TÁC DÂN VẬN", expanded=False):
            st.markdown("<p style='color:#C8102E; font-weight:bold;'>6.1 Phong trào Dân vận khéo</p>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            dv_mh_dangky = c1.number_input("Số mô hình đăng ký", min_value=0, value=0)
            dv_mh_hieuqua = c2.number_input("Số mô hình hiệu quả", min_value=0, value=0)
            dv_mh_moi = c3.number_input("Số mô hình mới", min_value=0, value=0)
            st.markdown("<p style='color:#C8102E; font-weight:bold; margin-top:10px;'>6.2 Hoạt động dân vận chung</p>", unsafe_allow_html=True)
            c4, c5, c6 = st.columns(3)
            dv_cuocvandong = c4.number_input("Số cuộc vận động", min_value=0, value=0)
            dv_nguoithamgia = c5.number_input("Số lượt người tham gia", min_value=0, value=0)
            dv_tiepxuc = c6.number_input("Số buổi đối thoại/tiếp xúc", min_value=0, value=0)

        with st.expander("7. NHIỆM VỤ TRỌNG TÂM", expanded=False):
            c1, c2, c3 = st.columns(3)
            nv_duocgiao = c1.number_input("Số nhiệm vụ được giao", min_value=0, value=0)
            nv_hoanthanh = c2.number_input("Số nhiệm vụ đã hoàn thành", min_value=0, value=0)
            nv_dangtrienkhai = c3.number_input("Số nhiệm vụ đang triển khai", min_value=0, value=0)
            nv_ketqua = st.text_area("Kết quả mô hình thí điểm (Nếu có):")

        with st.expander("8. CHUYÊN ĐỀ: BÌNH DÂN HỌC VỤ SỐ", expanded=False):
            c1, c2 = st.columns(2)
            bd_tinbai = c1.number_input("Số tin/bài CĐS", min_value=0, value=0)
            bd_cuocthi = c2.number_input("Số hội thi/video CĐS", min_value=0, value=0)
            
            kq_tocongnghe = st.number_input("Số lượng Tổ công nghệ số cộng đồng", min_value=0, value=0)
            
            st.markdown("---")
            ts_chibo = st.number_input("Tổng số chi bộ của đơn vị:", min_value=0, value=0)
            c3, c4 = st.columns(2)
            kq_chibo_cd = c3.number_input("Số CB sinh hoạt chuyên đề KNS", min_value=0, value=0)
            kq_chibo_sotay = c4.number_input("Số CB dùng Sổ tay ĐV điện tử", min_value=0, value=0)
            
            ts_cbccvc = st.number_input("Tổng số CBCCVC của đơn vị:", min_value=0, value=0)
            c5, c6 = st.columns(2)
            kq_cb_ai = c5.number_input("Số CBCCVC biết ứng dụng AI", min_value=0, value=0)
            kq_cb_khoahoc = c6.number_input("Số CBCCVC hoàn thành khóa học CĐS", min_value=0, value=0)
            
            st.markdown("---")
            ts_nd_truongthanh = st.number_input("Tổng số ND trưởng thành:", min_value=0, value=0)
            c7, c8 = st.columns(2)
            kq_nd_kynang = c7.number_input("Số ND có kỹ năng số", min_value=0, value=0)
            kq_nd_vneid = c8.number_input("Số ND phổ cập VNeID", min_value=0, value=0)
            
            ts_nd_toanxa = st.number_input("Tổng dân số toàn địa bàn:", min_value=0, value=0)
            kq_nd_smartphone = st.number_input("Số ND dùng Smartphone", min_value=0, value=0)
            
            ts_nld_dn = st.number_input("Tổng số NLĐ trong DN/HTX:", min_value=0, value=0)
            kq_nld_kynang = st.number_input("Số NLĐ có kỹ năng số", min_value=0, value=0)
            
            kq_lop_cb = st.number_input("Số lớp bồi dưỡng cho CBCCVC", min_value=0, value=0)
            kq_lop_nd = st.number_input("Số buổi học CĐ cho nhân dân", min_value=0, value=0)
            kq_dn_hotro = st.number_input("Số DN viễn thông hỗ trợ", min_value=0, value=0)

        with st.expander("9. TỰ LUẬN & ĐÁNH GIÁ CHUNG", expanded=False):
            tl_mohinh = st.text_area("🌟 Mô hình, cách làm hay, sáng tạo (Nêu tên cụ thể):")
            tl_khokhan = st.text_area("⚠️ Khó khăn, vướng mắc chưa số hóa tài liệu:")

        st.markdown("<style>.stButton>button[kind='primary'] {background-color: #C8102E;}</style>", unsafe_allow_html=True)
        # Nút Submit được đổi tên
        submit_btn = st.form_submit_button("📤 GỬI / CẬP NHẬT BÁO CÁO", type="primary", use_container_width=True)
        
        if submit_btn:
            if not don_vi or not ky_bao_cao:
                st.error("⚠️ Lỗi: Vui lòng chọn Đơn vị và Thời điểm báo cáo!")
            else:
                new_record = {
                    "don_vi": don_vi, "nguoi_bao_cao": nguoi_bao_cao, "ky_bao_cao": ky_bao_cao,
                    "ld_vanban": ld_vanban, "ld_thammuu": ld_thammuu, "ld_cuochop": ld_cuochop,
                    "nq_hoinghi": nq_hoinghi, "nq_nguoi": nq_nguoi, "nq_vanban": nq_vanban, "nq_tyle": nq_tyle,
                    "tt_tinbai": tt_tinbai, "tt_loa": tt_loa, "tt_buoi": tt_buoi, "tt_nguoi": tt_nguoi, "tt_mxh_bai": tt_mxh_bai, "tt_mxh_tuongtac": tt_mxh_tuongtac,
                    "dl_baocao": dl_baocao, "dl_vande": dl_vande, "dl_xuly": dl_xuly,
                    "kg_hoatdong": kg_hoatdong, "kg_chuongtrinh": kg_chuongtrinh, "kg_lop": kg_lop,
                    "dv_mh_dangky": dv_mh_dangky, "dv_mh_hieuqua": dv_mh_hieuqua, "dv_mh_moi": dv_mh_moi, "dv_cuocvandong": dv_cuocvandong, "dv_nguoithamgia": dv_nguoithamgia, "dv_tiepxuc": dv_tiepxuc,
                    "nv_duocgiao": nv_duocgiao, "nv_hoanthanh": nv_hoanthanh, "nv_dangtrienkhai": nv_dangtrienkhai, "nv_ketqua": nv_ketqua,
                    "bd_tinbai": bd_tinbai, "bd_cuocthi": bd_cuocthi, "kq_tocongnghe": kq_tocongnghe,
                    "ts_chibo": ts_chibo, "kq_chibo_cd": kq_chibo_cd, "kq_chibo_sotay": kq_chibo_sotay,
                    "ts_cbccvc": ts_cbccvc, "kq_cb_ai": kq_cb_ai, "kq_cb_khoahoc": kq_cb_khoahoc,
                    "ts_nd_truongthanh": ts_nd_truongthanh, "kq_nd_kynang": kq_nd_kynang, "kq_nd_vneid": kq_nd_vneid,
                    "ts_nd_toanxa": ts_nd_toanxa, "kq_nd_smartphone": kq_nd_smartphone,
                    "ts_nld_dn": ts_nld_dn, "kq_nld_kynang": kq_nld_kynang, "kq_lop_cb": kq_lop_cb, "kq_lop_nd": kq_lop_nd, "kq_dn_hotro": kq_dn_hotro,
                    "tl_mohinh": tl_mohinh, "tl_khokhan": tl_khokhan
                }
                data = load_data()
                # THUẬT TOÁN GHI ĐÈ: Xóa bỏ bản ghi cũ nếu trùng Đơn vị VÀ trùng Tháng báo cáo
                data = [d for d in data if not (d['don_vi'] == don_vi and d.get('ky_bao_cao') == ky_bao_cao)]
                data.append(new_record)
                save_data(data)
                st.success(f"✅ Đã ghi nhận / Cập nhật thành công báo cáo của {don_vi} ({ky_bao_cao})!")

# ==========================================
# KHU VỰC ADMIN (BIỂU ĐỒ & LỌC TỔNG HỢP)
# ==========================================
if st.session_state.role == "admin":
    with tab_bieudo:
        data = load_data()
        if not data: st.warning("Hệ thống chưa nhận được báo cáo nào.")
        else:
            df_raw = pd.DataFrame(data)
            
            # --- BỘ LỌC THỜI GIAN THÔNG MINH ---
            st.markdown("<h3 style='color:#004B87; font-size:18px;'>🗓️ LỌC DỮ LIỆU TỔNG HỢP</h3>", unsafe_allow_html=True)
            col_loc1, col_loc2 = st.columns(2)
            loai_loc = col_loc1.selectbox("Khoảng thời gian:", ["Từng Tháng", "Quý I", "Quý II", "Quý III", "Quý IV", "6 Tháng Đầu Năm", "6 Tháng Cuối Năm", "9 Tháng", "Cả Năm"])
            
            if loai_loc == "Từng Tháng":
                thang_loc = col_loc2.selectbox("Chọn tháng cụ thể:", DANH_SACH_THANG)
                df = df_raw[df_raw['ky_bao_cao'] == thang_loc]
            elif loai_loc == "Cả Năm":
                df = df_raw
            else:
                valid_months = get_months_for_filter(loai_loc)
                df = df_raw[df_raw['ky_bao_cao'].isin(valid_months)]

            if df.empty:
                st.warning(f"Chưa có số liệu nào được nộp trong kỳ tổng hợp này.")
            else:
                # Gom nhóm số liệu nếu lọc nhiều tháng cùng lúc
                numeric_cols = df.select_dtypes(include='number').columns
                df_agg = df.groupby('don_vi')[numeric_cols].sum().reset_index()

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown(f"<button onclick='window.print()' style='background:#C8102E; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer; float:right; font-weight:bold;'>🖨️ In Báo Cáo {loai_loc}</button><div style='clear:both; margin-bottom: 20px;'></div>", unsafe_allow_html=True)
                
                c1, c2, c3, c4 = st.columns(4)
                c1.markdown(f"<div class='metric-card'><div class='metric-title'>VB Lãnh đạo cấp ủy</div><div class='metric-number'>{df_agg['ld_vanban'].sum()}</div></div>", unsafe_allow_html=True)
                c2.markdown(f"<div class='metric-card'><div class='metric-title'>Vấn đề DLXH xử lý</div><div class='metric-number'>{df_agg['dl_xuly'].sum()} <span style='font-size:16px; color:#888;'>/ {df_agg['dl_vande'].sum()}</span></div></div>", unsafe_allow_html=True)
                c3.markdown(f"<div class='metric-card'><div class='metric-title'>Tổ công nghệ số</div><div class='metric-number'>{df_agg['kq_tocongnghe'].sum()}</div></div>", unsafe_allow_html=True)
                c4.markdown(f"<div class='metric-card'><div class='metric-title'>Đơn vị đã nộp</div><div class='metric-number'>{len(df_agg)}<span style='font-size:16px; color:#888;'>/{len(load_units())}</span></div></div>", unsafe_allow_html=True)

                st.markdown("<h3 class='main-header' style='text-align:left; font-size:20px; margin-top:30px;'>📊 BIỂU ĐỒ TRỌNG ĐIỂM</h3>", unsafe_allow_html=True)
                def safe_pct(tu, mau): return round((tu / mau * 100), 2) if mau and mau > 0 else 0.0
                df_agg['TL_CB_AI'] = df_agg.apply(lambda x: safe_pct(x['kq_cb_ai'], x['ts_cbccvc']), axis=1)
                df_agg['TL_ND_VNeID'] = df_agg.apply(lambda x: safe_pct(x['kq_nd_vneid'], x['ts_nd_truongthanh']), axis=1)

                colA, colB = st.columns(2)
                with colA:
                    fig1 = px.bar(df_agg, x='don_vi', y=['TL_CB_AI', 'TL_ND_VNeID'], barmode='group', title="Tỷ lệ CB biết dùng AI & ND phổ cập VNeID", color_discrete_sequence=['#004B87', '#C8102E'])
                    st.plotly_chart(fig1, use_container_width=True)
                with colB:
                    fig2 = px.bar(df_agg, x='don_vi', y=['dv_mh_dangky', 'dv_mh_hieuqua'], barmode='group', title="Dân vận khéo: Đăng ký vs Hiệu quả", color_discrete_sequence=['#004B87', '#28a745'])
                    st.plotly_chart(fig2, use_container_width=True)

                st.markdown("<h3 class='main-header' style='text-align:left; font-size:20px;'>📋 BẢNG SỐ LIỆU TỔNG HỢP</h3>", unsafe_allow_html=True)
                st.dataframe(df_agg, use_container_width=True)

    with tab_admin:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<h3 style='color:#004B87;'>🏢 Thêm / Xóa Đơn vị</h3>", unsafe_allow_html=True)
            current_units = load_units()
            new_unit = st.text_input("Tên đơn vị mới cần thêm:")
            if st.button("➕ Thêm Đơn vị") and new_unit and new_unit not in current_units:
                current_units.append(new_unit)
                save_units(current_units)
                st.rerun()
            remove_unit = st.selectbox("Chọn đơn vị cần xóa khỏi danh sách:", ["-- Chọn --"] + current_units)
            if st.button("🗑️ Xóa Đơn vị") and remove_unit != "-- Chọn --":
                current_units.remove(remove_unit)
                save_units(current_units)
                st.rerun()
