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

# ==========================================
# CẤU HÌNH & CSS TRANG
# ==========================================
st.set_page_config(page_title="Hệ thống Báo cáo TGDV", page_icon="📊", layout="wide")

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
</style>
""", unsafe_allow_html=True)

# ==========================================
# QUẢN LÝ DỮ LIỆU FILE
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
    if filter_type == "Cả Năm": return [f"Tháng {i}" for i in range(1, 13)]
    return DANH_SACH_THANG

# ==========================================
# ĐĂNG NHẬP PHÂN QUYỀN
# ==========================================
if "role" not in st.session_state: st.session_state.role = None
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
    st.stop()

with st.sidebar:
    rm = {"admin": "ADMIN", "chuyen_vien": "CHUYÊN VIÊN TỔNG HỢP", "user": "CƠ SỞ"}
    st.markdown(f"<div style='background:#004B87; color:white; padding:10px; border-radius:5px; text-align:center;'>👤 Quyền: <b>{rm.get(st.session_state.role)}</b></div>", unsafe_allow_html=True)
    if st.button("🚪 Đăng xuất"): st.session_state.role = None; st.rerun()

# ==========================================
# CẤU TRÚC TAB
# ==========================================
st.markdown("<h1 class='main-header'>HỆ THỐNG THU THẬP BÁO CÁO CƠ SỞ</h1>", unsafe_allow_html=True)

if st.session_state.role == "admin":
    tabs = st.tabs(["📝 NHẬP BÁO CÁO", "📈 TIẾN ĐỘ & TRÍCH XUẤT", "📊 PHÂN TÍCH BIỂU ĐỒ", "⚙️ QUẢN TRỊ ADMIN"])
    tab_nhap, tab_tiendo, tab_bieudo, tab_admin = tabs[0], tabs[1], tabs[2], tabs[3]
elif st.session_state.role == "chuyen_vien":
    tabs = st.tabs(["📝 NHẬP BÁO CÁO", "📈 TIẾN ĐỘ & TRÍCH XUẤT", "📊 PHÂN TÍCH BIỂU ĐỒ"])
    tab_nhap, tab_tiendo, tab_bieudo = tabs[0], tabs[1], tabs[2]
else:
    tabs = st.tabs(["📝 NHẬP BÁO CÁO"])
    tab_nhap = tabs[0]

# ------------------------------------------
# TAB 1: NHẬP BÁO CÁO (Full 9 Mục)
# ------------------------------------------
with tab_nhap:
    st.markdown("### 1️⃣ XÁC ĐỊNH ĐƠN VỊ & KỲ BÁO CÁO")
    c1, c2, c3 = st.columns([2, 1.5, 1.5])
    all_units_list = load_units()
    dv = c1.selectbox("🏢 Đơn vị:", all_units_list, index=None, placeholder="Gõ tìm đơn vị...")
    th = c3.selectbox("🗓️ Tháng:", DANH_SACH_THANG, index=None, placeholder="Chọn tháng...")
    
    old = {}
    if dv and th:
        for d in load_data():
            if d.get('don_vi') == dv and d.get('ky_bao_cao') == th:
                old = d; break
    nguoi_bc = c2.text_input("👤 Người báo cáo / SĐT:", value=old.get('nguoi_bao_cao', ''))

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
                tt_tb = c1.number_input("Số tin, bài, pano", min_value=0, value=int(old_data_val := old.get('tt_tinbai',0)))
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
                dv_cv = c3.number_input("Số cuộc vận động, TT", min_value=0, value=int(old.get('dv_cuocvandong',0)))

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
                               "dv_mh_dangky":dv_dk, "dv_mh_hieuqua":dv_hq, "dv_cuocvandong":dv_cv, "nv_duocgiao":nv_dg, "nv_hoanthanh":nv_ht, "nv_ketqua":nv_kq,
                               "bd_tinbai":bd_ti, "ts_chibo":ts_ch, "kq_chibo_cd":kq_cd, "ts_cbccvc":ts_cb, "kq_cb_ai":kq_ai, "tl_mohinh":tl_mo, "tl_khokhan":tl_kh}
                    data = load_data(); data = [d for d in data if not (d['don_vi']==dv and d['ky_bao_cao']==th)]
                    data.append(new_rec); save_data(data); st.success("✅ Thành công!")

# ------------------------------------------
# CHUẨN BỊ DỮ LIỆU CHUNG CHO TIẾN ĐỘ & BIỂU ĐỒ
# ------------------------------------------
if st.session_state.role in ["admin", "chuyen_vien"]:
    all_raw = load_data()
    st.sidebar.markdown("### 🗓️ BỘ LỌC DỮ LIỆU")
    l_bc = st.sidebar.selectbox("Kỳ tổng hợp:", ["Tháng", "Quý I", "Quý II", "Quý III", "Quý IV", "Cả Năm"])
    if l_bc == "Tháng":
        t_bc = st.sidebar.selectbox("Tháng cụ thể:", DANH_SACH_THANG)
        df_cur = pd.DataFrame([d for d in all_raw if d['ky_bao_cao'] == t_bc])
    else:
        m_l = get_months_for_filter(l_bc)
        df_cur = pd.DataFrame([d for d in all_raw if d['ky_bao_cao'] in m_l])
    
    current_units_list = load_units()
    u_done = df_cur['don_vi'].unique().tolist() if not df_cur.empty else []
    u_miss = [u for u in current_units_list if u not in u_done]

    # --------------------------------------
    # TAB 2: TIẾN ĐỘ & TRÍCH XUẤT
    # --------------------------------------
    with tab_tiendo:
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='metric-card'><p class='metric-title'>Đã nộp</p><p class='metric-number' style='color:#28a745;'>{len(u_done)}</p></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-card'><p class='metric-title'>Chưa nộp</p><p class='metric-number'>{len(u_miss)}</p></div>", unsafe_allow_html=True)
        rate = (len(u_done)/len(current_units_list)*100) if current_units_list else 0
        c3.markdown(f"<div class='metric-card'><p class='metric-title'>Tỷ lệ</p><p class='metric-number' style='color:#004B87;'>{rate:.1f}%</p></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='metric-card'><p class='metric-title'>Tổng đơn vị</p><p class='metric-number'>{len(current_units_list)}</p></div>", unsafe_allow_html=True)

        if not df_cur.empty:
            num_cols = df_cur.select_dtypes(include='number').columns
            agg_dict = {col: ('mean' if col=='nq_tyle' else 'sum') for col in num_cols}
            def g_c(x):
                txts = list(dict.fromkeys([str(i).strip() for i in x if pd.notna(i) and str(i).strip()!=""]))
                return "\n".join([f"- {t}" for t in txts]) if txts else ""
            for c in ['nv_ketqua','tl_mohinh','tl_khokhan','kg_khokhan']: 
                if c in df_cur.columns: agg_dict[c] = g_c
            agg_dict['nguoi_bao_cao'] = lambda x: ", ".join(list(dict.fromkeys([str(i).strip() for i in x if pd.notna(i)])))
            
            df_sum = df_cur.groupby('don_vi').agg(agg_dict).reset_index()
            df_sum['ky_bao_cao'] = l_bc
            for c in DICT_DICH_THUAT.keys():
                if c not in df_sum.columns: df_sum[c] = 0 if c in num_cols else ""
            
            df_ex = df_sum[list(DICT_DICH_THUAT.keys())].rename(columns=DICT_DICH_THUAT)
            t_r = {c: (round(df_ex[c].mean(),2) if c==DICT_DICH_THUAT['nq_tyle'] else df_ex[c].sum()) if pd.api.types.is_numeric_dtype(df_ex[c]) else "" for c in df_ex.columns}
            t_r[DICT_DICH_THUAT['don_vi']] = "TỔNG CỘNG"
            df_ex = pd.concat([df_ex, pd.DataFrame([t_r])], ignore_index=True)
            
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine='openpyxl') as wr:
                df_ex.to_excel(wr, index=False, sheet_name='BaoCao', startrow=1)
            
            st.write("")
            st.download_button("📥 TẢI BẢNG TỔNG HỢP GỘP SỐ LIỆU (EXCEL)", buf.getvalue(), f"Tong_hop_{l_bc}.xlsx", type="primary", use_container_width=True)

        st.markdown("<div class='section-title'>📊 CHI TIẾT TIẾN ĐỘ</div>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            st.success(f"✅ ĐÃ NỘP ({len(u_done)})")
            if u_done:
                df_d = df_cur[['don_vi','ngay_nop','nguoi_bao_cao']].drop_duplicates(subset=['don_vi'], keep='last')
                st.dataframe(df_d.rename(columns={'don_vi':'Đơn vị','ngay_nop':'Lúc nộp','nguoi_bao_cao':'Người nộp'}), use_container_width=True, hide_index=True)
        with col_b:
            st.error(f"❌ CHƯA NỘP ({len(u_miss)})")
            if u_miss:
                st.code(", ".join(u_miss))
                for m in sorted(u_miss): st.text(f"🔸 {m}")

    # --------------------------------------
    # TAB 3: PHÂN TÍCH BIỂU ĐỒ (8 Biểu đồ)
    # --------------------------------------
    with tab_bieudo:
        if df_cur.empty: st.warning("Chưa có số liệu.")
        else:
            st.info(f"📊 Phân tích số liệu kỳ: **{l_bc}**")
            st.markdown("<div class='section-title'>1. LÃNH ĐẠO & 2. NGHỊ QUYẾT</div>", unsafe_allow_html=True)
            r1c1, r1c2 = st.columns(2)
            with r1c1:
                f1 = go.Figure(data=[go.Bar(name='VB ban hành', x=df_sum['don_vi'], y=df_sum['ld_vanban'], marker_color='#004B87'),
                                     go.Bar(name='Tham mưu', x=df_sum['don_vi'], y=df_sum['ld_thammuu'], marker_color='#C8102E')])
                f1.update_layout(title="Công tác Lãnh đạo", barmode='group')
                st.plotly_chart(f1, use_container_width=True)
            with r1c2:
                f2 = go.Figure(data=[go.Bar(name='Hội nghị NQ', x=df_sum['don_vi'], y=df_sum['nq_hoinghi'], marker_color='#28a745'),
                                     go.Bar(name='VB triển khai', x=df_sum['don_vi'], y=df_sum['nq_vanban'], marker_color='#ffc107')])
                f2.update_layout(title="Quán triệt Nghị quyết", barmode='group')
                st.plotly_chart(f2, use_container_width=True)

            st.markdown("<div class='section-title'>3. TUYÊN TRUYỀN & 4. DƯ LUẬN</div>", unsafe_allow_html=True)
            r2c1, r2c2 = st.columns(2)
            with r2c1:
                f3 = px.line(df_sum, x='don_vi', y=['tt_tinbai', 'tt_mxh_bai'], markers=True, title="Tuyên truyền & MXH")
                st.plotly_chart(f3, use_container_width=True)
            with r2c2:
                f4 = px.pie(values=[df_sum['dl_baocao'].sum(), df_sum['dl_vande'].sum(), df_sum['dl_xuly'].sum()], 
                            names=['Báo cáo gửi đi', 'Vấn đề nổi cộm', 'Đã xử lý'], hole=.4, title="Hoạt động Dư luận xã hội")
                st.plotly_chart(f4, use_container_width=True)

            st.markdown("<div class='section-title'>5. KHOA GIÁO & 6. DÂN VẬN</div>", unsafe_allow_html=True)
            r3c1, r3c2 = st.columns(2)
            with r3c1:
                f5 = px.bar(df_sum, x='don_vi', y=['kg_chuongtrinh', 'kg_bd_chuyennghiep'], title="Văn hóa & Khoa giáo")
                st.plotly_chart(f5, use_container_width=True)
            with r3c2:
                f6 = go.Figure(data=[go.Bar(name='Mô hình DVK', x=df_sum['don_vi'], y=df_sum['dv_mh_dangky'], marker_color='#17a2b8'),
                                     go.Bar(name='Hiệu quả', x=df_sum['don_vi'], y=df_sum['dv_mh_hieuqua'], marker_color='#004B87')])
                f6.update_layout(barmode='stack', title="Dân vận khéo")
                st.plotly_chart(f6, use_container_width=True)

            st.markdown("<div class='section-title'>7. NHIỆM VỤ & 8. HỌC VỤ SỐ</div>", unsafe_allow_html=True)
            r4c1, r4c2 = st.columns(2)
            with r4c1:
                f7 = go.Figure(data=[go.Bar(name='Giao', x=df_sum['don_vi'], y=df_sum['nv_duocgiao'], marker_color='#E6E6E6'),
                                     go.Bar(name='Hoàn thành', x=df_sum['don_vi'], y=df_sum['nv_hoanthanh'], marker_color='#C8102E')])
                st.plotly_chart(f7, use_container_width=True)
            with r4c2:
                f8 = px.bar(df_sum, x='don_vi', y='kq_cb_ai', color='kq_cb_ai', title="Cán bộ biết dùng AI")
                st.plotly_chart(f8, use_container_width=True)

# ------------------------------------------
# TAB 4: QUẢN TRỊ ADMIN (KHÔI PHỤC ĐỦ TÍNH NĂNG)
# ------------------------------------------
if st.session_state.role == "admin":
    with tab_admin:
        st.markdown("<h3 style='color:#C8102E;'>⚠️ KHU VỰC QUẢN TRỊ HỆ THỐNG</h3>", unsafe_allow_html=True)
        col_adm1, col_adm2 = st.columns(2)
        
        with col_adm1:
            st.markdown("#### 🗑️ QUẢN LÝ XÓA DỮ LIỆU")
            current_data = load_data()
            if current_data:
                dv_del = st.selectbox("Chọn đơn vị muốn xóa:", list(set([d['don_vi'] for d in current_data])), key="dv_xoa")
                th_del = st.selectbox("Chọn tháng muốn xóa:", list(set([d['ky_bao_cao'] for d in current_data if d['don_vi']==dv_del])), key="th_xoa")
                if st.button("🔥 XÁC NHẬN XÓA BÁO CÁO"):
                    new_data = [d for d in current_data if not (d['don_vi']==dv_del and d['ky_bao_cao']==th_del)]
                    save_data(new_data); st.success(f"Đã xóa dữ liệu của {dv_del}!"); st.rerun()
            else: st.info("Chưa có dữ liệu báo cáo.")

        with col_adm2:
            st.markdown("#### 🏢 QUẢN LÝ DANH SÁCH ĐƠN VỊ")
            u_list = load_units()
            
            # --- Mục thêm đơn vị đây sếp ơi! ---
            st.write("---")
            new_u = st.text_input("➕ Tên đơn vị mới cần thêm:")
            if st.button("XÁC NHẬN THÊM ĐƠN VỊ"):
                if new_u and new_u not in u_list:
                    u_list.append(new_u)
                    save_units(u_list)
                    st.success(f"Đã thêm thành công: {new_u}!")
                    st.rerun()
                else: st.warning("Tên đơn vị trống hoặc đã tồn tại!")
            
            # --- Mục xóa đơn vị khỏi danh sách ---
            st.write("---")
            rem_u = st.selectbox("🗑️ Chọn đơn vị cần xóa khỏi danh sách:", ["-- Chọn --"] + u_list)
            if st.button("XÁC NHẬN XÓA ĐƠN VỊ"):
                if rem_u != "-- Chọn --":
                    u_list.remove(rem_u)
                    save_units(u_list)
                    st.success(f"Đã xóa {rem_u} khỏi danh sách đơn vị!")
                    st.rerun()
