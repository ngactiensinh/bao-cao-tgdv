import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

st.set_page_config(page_title="Hệ thống Báo cáo TGDV", page_icon="📊", layout="wide")

# ==========================================
# CẤU HÌNH LƯU TRỮ
# ==========================================
DATA_FILE = "dulieu_baocao.json"
CONFIG_FILE = "config_donvi.json"
DEFAULT_UNITS = [
    "Ban Tuyên giáo Tỉnh ủy", "Phường Minh Xuân", "Phường Tân Quang", 
    "Phường Phan Thiết", "Xã Tràng Đà", "Xã Kim Phú", "Phường Mỹ Lâm"
]

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

# ==========================================
# HỆ THỐNG ĐĂNG NHẬP (PHÂN QUYỀN)
# ==========================================
if "role" not in st.session_state:
    st.session_state.role = None

if st.session_state.role is None:
    st.markdown("<h2 style='text-align: center; color: #004B87; margin-top: 50px;'>ĐĂNG NHẬP HỆ THỐNG BÁO CÁO</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        pwd = st.text_input("🔑 Nhập mật khẩu truy cập:", type="password")
        if st.button("Đăng nhập", use_container_width=True):
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
    st.markdown(f"👤 Đang đăng nhập: **{'ADMIN' if st.session_state.role == 'admin' else 'CƠ SỞ'}**")
    if st.button("🚪 Đăng xuất"):
        st.session_state.role = None
        st.rerun()

# ==========================================
# GIAO DIỆN CHÍNH
# ==========================================
st.markdown("""
<style>
    .main-header {color: #004B87; font-weight: 900; text-align: center; text-transform: uppercase; margin-bottom: 20px;}
    .metric-card {background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #004B87; margin-bottom: 15px;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>HỆ THỐNG THU THẬP BÁO CÁO CƠ SỞ</h1>", unsafe_allow_html=True)

if st.session_state.role == "admin":
    tabs = st.tabs(["📝 NHẬP BÁO CÁO", "📊 THỐNG KÊ & BIỂU ĐỒ", "⚙️ QUẢN TRỊ ADMIN"])
    tab_nhap, tab_bieudo, tab_admin = tabs[0], tabs[1], tabs[2]
else:
    tabs = st.tabs(["📝 NHẬP BÁO CÁO"])
    tab_nhap = tabs[0]

# ==========================================
# TAB NHẬP BÁO CÁO (ĐẦY ĐỦ CÁC NHÓM)
# ==========================================
with tab_nhap:
    st.info("💡 **Hướng dẫn:** Bấm vào từng nhóm để điền số liệu. Mặc định là 0.")
    with st.form("form_bao_cao"):
        col1, col2 = st.columns(2)
        don_vi = col1.selectbox("🏢 Chọn Đơn vị:", load_units())
        nguoi_bao_cao = col2.text_input("👤 Người báo cáo / SĐT:")
        
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
            st.write("**3.1 Tuyên truyền chung & Miệng**")
            c1, c2, c3, c4 = st.columns(4)
            tt_tinbai = c1.number_input("Số tin/bài/pano", min_value=0, value=0)
            tt_loa = c2.number_input("Số lượt loa truyền thanh", min_value=0, value=0)
            tt_buoi = c3.number_input("Số buổi TT miệng", min_value=0, value=0)
            tt_nguoi = c4.number_input("Số người nghe TT miệng", min_value=0, value=0)
            st.write("**3.2 Báo chí, Mạng xã hội**")
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
            st.write("**6.1 Dân vận khéo**")
            c1, c2, c3 = st.columns(3)
            dv_mh_dangky = c1.number_input("Số mô hình đăng ký", min_value=0, value=0)
            dv_mh_hieuqua = c2.number_input("Số mô hình hiệu quả", min_value=0, value=0)
            dv_mh_moi = c3.number_input("Số mô hình mới", min_value=0, value=0)
            st.write("**6.2 Hoạt động dân vận chung**")
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
            st.write("*(Các mục Tỷ lệ vui lòng điền Số đạt được và Tổng số)*")
            c1, c2 = st.columns(2)
            bd_tinbai = c1.number_input("Số tin/bài CĐS", min_value=0, value=0)
            bd_cuocthi = c2.number_input("Số hội thi/video CĐS", min_value=0, value=0)
            
            kq_tocongnghe = st.number_input("Số lượng Tổ công nghệ số cộng đồng", min_value=0, value=0)
            
            st.write("**- Chi bộ & CBCCVC:**")
            ts_chibo = st.number_input("Tổng số chi bộ của đơn vị:", min_value=0, value=0)
            c3, c4 = st.columns(2)
            kq_chibo_cd = c3.number_input("Số CB sinh hoạt chuyên đề KNS", min_value=0, value=0)
            kq_chibo_sotay = c4.number_input("Số CB dùng Sổ tay ĐV điện tử", min_value=0, value=0)
            
            ts_cbccvc = st.number_input("Tổng số CBCCVC của đơn vị:", min_value=0, value=0)
            c5, c6 = st.columns(2)
            kq_cb_ai = c5.number_input("Số CBCCVC biết ứng dụng AI", min_value=0, value=0)
            kq_cb_khoahoc = c6.number_input("Số CBCCVC hoàn thành khóa học CĐS", min_value=0, value=0)
            
            st.write("**- Người dân & Lao động:**")
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

        if st.form_submit_button("📤 GỬI BÁO CÁO", use_container_width=True):
            new_record = {
                "don_vi": don_vi, "nguoi_bao_cao": nguoi_bao_cao,
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
            data = [d for d in data if d['don_vi'] != don_vi]
            data.append(new_record)
            save_data(data)
            st.success(f"✅ Đã lưu báo cáo toàn diện của {don_vi}!")

# ==========================================
# KHU VỰC ADMIN (BIỂU ĐỒ & QUẢN LÝ)
# ==========================================
if st.session_state.role == "admin":
    with tab_bieudo:
        data = load_data()
        if not data: st.warning("Chưa có báo cáo.")
        else:
            df = pd.DataFrame(data)
            st.markdown("<button onclick='window.print()' style='background:#004B87; color:white; padding:8px 15px; border-radius:5px; cursor:pointer; float:right;'>🖨️ Xuất PDF</button><div style='clear:both;'></div>", unsafe_allow_html=True)
            
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"<div class='metric-card'><b>VB Lãnh đạo cấp ủy:</b><br><h2 style='color:#C8102E;margin:0;'>{df['ld_vanban'].sum()}</h2></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='metric-card'><b>Vấn đề DLXH xử lý:</b><br><h2 style='color:#C8102E;margin:0;'>{df['dl_xuly'].sum()} / {df['dl_vande'].sum()}</h2></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='metric-card'><b>Tổ công nghệ số:</b><br><h2 style='color:#C8102E;margin:0;'>{df['kq_tocongnghe'].sum()}</h2></div>", unsafe_allow_html=True)
            c4.markdown(f"<div class='metric-card'><b>Đơn vị nộp:</b><br><h2 style='color:#C8102E;margin:0;'>{len(df)}/{len(load_units())}</h2></div>", unsafe_allow_html=True)

            st.markdown("### 📊 BIỂU ĐỒ TRỌNG ĐIỂM")
            def safe_pct(tu, mau): return round((tu / mau * 100), 2) if mau and mau > 0 else 0.0
            df['TL_CB_AI'] = df.apply(lambda x: safe_pct(x['kq_cb_ai'], x['ts_cbccvc']), axis=1)
            df['TL_ND_VNeID'] = df.apply(lambda x: safe_pct(x['kq_nd_vneid'], x['ts_nd_truongthanh']), axis=1)

            colA, colB = st.columns(2)
            with colA:
                fig1 = px.bar(df, x='don_vi', y=['TL_CB_AI', 'TL_ND_VNeID'], barmode='group', title="Tỷ lệ CB biết dùng AI & ND phổ cập VNeID")
                st.plotly_chart(fig1, use_container_width=True)
            with colB:
                fig2 = px.bar(df, x='don_vi', y=['dv_mh_dangky', 'dv_mh_hieuqua'], barmode='group', title="Dân vận khéo: Đăng ký vs Hiệu quả")
                st.plotly_chart(fig2, use_container_width=True)

            st.markdown("### 📋 BẢNG SỐ LIỆU ĐẦY ĐỦ")
            st.dataframe(df, use_container_width=True)

    with tab_admin:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 🏢 Thêm/Xóa Đơn vị")
            current_units = load_units()
            new_unit = st.text_input("Tên đơn vị mới:")
            if st.button("➕ Thêm Đơn vị") and new_unit not in current_units:
                current_units.append(new_unit)
                save_units(current_units)
                st.rerun()
            remove_unit = st.selectbox("Chọn đơn vị cần xóa:", ["-- Chọn --"] + current_units)
            if st.button("🗑️ Xóa Đơn vị") and remove_unit != "-- Chọn --":
                current_units.remove(remove_unit)
                save_units(current_units)
                st.rerun()
        with c2:
            st.markdown("### 🛠️ Xóa Báo cáo")
            if data:
                selected_dv_edit = st.selectbox("Chọn báo cáo đơn vị:", [d['don_vi'] for d in data])
                if st.button("⚠️ Xóa Báo Cáo Này"):
                    data = [d for d in data if d['don_vi'] != selected_dv_edit]
                    save_data(data)
                    st.rerun()
