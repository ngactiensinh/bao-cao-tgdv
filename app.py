import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

st.set_page_config(page_title="Hệ thống Báo cáo TGDV", page_icon="📊", layout="wide")

# ==========================================
# CẤU HÌNH & LƯU TRỮ DỮ LIỆU
# ==========================================
DATA_FILE = "dulieu_baocao.json"
CONFIG_FILE = "config_donvi.json"

# Danh sách đơn vị mặc định (Mô hình 2 cấp: Tỉnh và Xã/Phường)
DEFAULT_UNITS = [
    "Ban Tuyên giáo Tỉnh ủy", "Phường Minh Xuân", "Phường Tân Quang", 
    "Phường Phan Thiết", "Xã Tràng Đà", "Xã Kim Phú", "Phường Mỹ Lâm"
]
ADMIN_PASSWORD = "admin123"

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
# GIAO DIỆN CHÍNH (CHIA TAB)
# ==========================================
st.markdown("""
<style>
    .main-header {color: #004B87; font-weight: 900; text-align: center; text-transform: uppercase; margin-bottom: 20px;}
    .sub-header {color: #C8102E; font-weight: bold; border-bottom: 2px solid #C8102E; padding-bottom: 5px; margin-top: 20px;}
    .metric-card {background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #004B87; margin-bottom: 15px;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>HỆ THỐNG THU THẬP BÁO CÁO CƠ SỞ</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 NHẬP BÁO CÁO", "📊 THỐNG KÊ & BIỂU ĐỒ", "⚙️ QUẢN TRỊ ADMIN"])

# ==========================================
# TAB 1: FORM NHẬP BÁO CÁO
# ==========================================
with tab1:
    st.info("💡 **Hướng dẫn:** Các đơn vị điền đầy đủ số liệu vào các trường dưới đây. Các mục tỷ lệ vui lòng điền Số đạt được / Tổng số.")
    don_vi_list = load_units()
    
    with st.form("form_bao_cao"):
        col1, col2 = st.columns(2)
        don_vi = col1.selectbox("🏢 Chọn Đơn vị báo cáo:", don_vi_list)
        nguoi_bao_cao = col2.text_input("👤 Người báo cáo / SĐT:")
        
        st.markdown("<h3 class='sub-header'>I. CÔNG TÁC TUYÊN TRUYỀN (BÌNH DÂN HỌC VỤ SỐ)</h3>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        tt_tinbai = c1.number_input("Số tin, bài tuyên truyền", min_value=0, value=0)
        tt_cuocthi = c2.number_input("Số cuộc thi, hội thi", min_value=0, value=0)
        tt_tailieu = c3.number_input("Số tài liệu, tờ gấp, video...", min_value=0, value=0)
        
        st.markdown("<h3 class='sub-header'>II. KẾT QUẢ THỰC HIỆN</h3>", unsafe_allow_html=True)
        kq_tocongnghe = st.number_input("1. Số lượng tổ công nghệ số cộng đồng", min_value=0, value=0)
        
        st.write("**2. Sinh hoạt chuyên đề & Đảng viên điện tử**")
        c1, c2 = st.columns(2)
        kq_chibo_cd = c1.number_input("Số chi bộ SH chuyên đề Kỹ năng số", min_value=0, value=0)
        kq_chibo_tong1 = c2.number_input("Tổng số chi bộ (Mục 2a)", min_value=1, value=1)
        c3, c4 = st.columns(2)
        kq_chibo_sotay = c3.number_input("Số chi bộ dùng Sổ tay đảng viên ĐT", min_value=0, value=0)
        kq_chibo_tong2 = c4.number_input("Tổng số chi bộ (Mục 2b)", min_value=1, value=1)
        
        st.write("**3. Cán bộ, công chức, viên chức (CBCCVC)**")
        c1, c2 = st.columns(2)
        kq_cb_ai = c1.number_input("Số CBCCVC biết ứng dụng AI", min_value=0, value=0)
        kq_cb_tong1 = c2.number_input("Tổng số CBCCVC (Mục 3a)", min_value=1, value=1)
        c3, c4 = st.columns(2)
        kq_cb_khoahoc = c3.number_input("Số CBCCVC hoàn thành khóa học CĐS", min_value=0, value=0)
        kq_cb_tong2 = c4.number_input("Tổng số CBCCVC (Mục 3b)", min_value=1, value=1)
        
        st.write("**4. Người dân & Người lao động**")
        c1, c2 = st.columns(2)
        kq_nd_kynang = c1.number_input("Số người dân có kỹ năng số", min_value=0, value=0)
        kq_nd_tong1 = c2.number_input("Tổng số người dân trưởng thành (Mục 4a)", min_value=1, value=1)
        c3, c4 = st.columns(2)
        kq_nd_vneid = c3.number_input("Số người dân phổ cập trên VNeID", min_value=0, value=0)
        kq_nd_tong2 = c4.number_input("Tổng số ND trưởng thành (Mục 4b)", min_value=1, value=1)
        c5, c6 = st.columns(2)
        kq_nld_kynang = c5.number_input("Số NLĐ trong DN/HTX có kỹ năng số", min_value=0, value=0)
        kq_nld_tong = c6.number_input("Tổng số NLĐ trong DN/HTX (Mục 4c)", min_value=1, value=1)
        c7, c8 = st.columns(2)
        kq_nd_smartphone = c7.number_input("Số người dân dùng Smartphone", min_value=0, value=0)
        kq_nd_tong3 = c8.number_input("Tổng số người dân (Mục 4d)", min_value=1, value=1)
        
        st.write("**5. Lớp bồi dưỡng & Hỗ trợ**")
        c1, c2, c3 = st.columns(3)
        kq_lop_cb = c1.number_input("Số lớp bồi dưỡng cho CBCCVC", min_value=0, value=0)
        kq_lop_nd = c2.number_input("Số buổi học cộng đồng cấp Xã/Phường", min_value=0, value=0)
        kq_dn_hotro = c3.number_input("Số DN viễn thông hỗ trợ hạ tầng", min_value=0, value=0)
        
        st.markdown("<h3 class='sub-header'>III. TỰ LUẬN & ĐÁNH GIÁ</h3>", unsafe_allow_html=True)
        tl_mohinh = st.text_area("🌟 Số mô hình, cách làm hay, sáng tạo (Nêu cụ thể tên):")
        tl_khokhan = st.text_area("⚠️ Khó khăn, vướng mắc chưa số hóa tài liệu:")
        
        submitted = st.form_submit_button("📤 GỬI BÁO CÁO", use_container_width=True)
        if submitted:
            new_record = {
                "don_vi": don_vi, "nguoi_bao_cao": nguoi_bao_cao,
                "tt_tinbai": tt_tinbai, "tt_cuocthi": tt_cuocthi, "tt_tailieu": tt_tailieu,
                "kq_tocongnghe": kq_tocongnghe, 
                "kq_chibo_cd": kq_chibo_cd, "kq_chibo_tong1": kq_chibo_tong1,
                "kq_chibo_sotay": kq_chibo_sotay, "kq_chibo_tong2": kq_chibo_tong2,
                "kq_cb_ai": kq_cb_ai, "kq_cb_tong1": kq_cb_tong1,
                "kq_cb_khoahoc": kq_cb_khoahoc, "kq_cb_tong2": kq_cb_tong2,
                "kq_nd_kynang": kq_nd_kynang, "kq_nd_tong1": kq_nd_tong1,
                "kq_nd_vneid": kq_nd_vneid, "kq_nd_tong2": kq_nd_tong2,
                "kq_nld_kynang": kq_nld_kynang, "kq_nld_tong": kq_nld_tong,
                "kq_nd_smartphone": kq_nd_smartphone, "kq_nd_tong3": kq_nd_tong3,
                "kq_lop_cb": kq_lop_cb, "kq_lop_nd": kq_lop_nd, "kq_dn_hotro": kq_dn_hotro,
                "tl_mohinh": tl_mohinh, "tl_khokhan": tl_khokhan
            }
            data = load_data()
            # Xóa báo cáo cũ của đơn vị này nếu đã có, để ghi đè báo cáo mới nhất
            data = [d for d in data if d['don_vi'] != don_vi]
            data.append(new_record)
            save_data(data)
            st.success(f"✅ Báo cáo của {don_vi} đã được lưu thành công vào hệ thống!")

# ==========================================
# TAB 2: THỐNG KÊ & BIỂU ĐỒ (DASHBOARD)
# ==========================================
with tab2:
    data = load_data()
    if not data:
        st.warning("Chưa có dữ liệu báo cáo nào được gửi về.")
    else:
        df = pd.DataFrame(data)
        st.markdown("<h3 class='sub-header'>A. TỔNG HỢP TOÀN TỈNH</h3>", unsafe_allow_html=True)
        
        # Nút xuất PDF bằng JavaScript Print
        st.markdown("""
            <button onclick="window.print()" style="background-color:#004B87; color:white; padding:8px 15px; border:none; border-radius:5px; cursor:pointer; float:right; font-weight:bold;">
                🖨️ In Báo Cáo / Lưu PDF
            </button>
            <div style="clear:both;"></div>
        """, unsafe_allow_html=True)
        
        # Tính toán tổng
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='metric-card'><b>Tổng số tin bài:</b><br><h2 style='color:#C8102E;margin:0;'>{df['tt_tinbai'].sum()}</h2></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-card'><b>Tổ công nghệ số:</b><br><h2 style='color:#C8102E;margin:0;'>{df['kq_tocongnghe'].sum()}</h2></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='metric-card'><b>Lớp cộng đồng (Xã/Phường):</b><br><h2 style='color:#C8102E;margin:0;'>{df['kq_lop_nd'].sum()}</h2></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='metric-card'><b>Đơn vị đã nộp:</b><br><h2 style='color:#C8102E;margin:0;'>{len(df)}/{len(load_units())}</h2></div>", unsafe_allow_html=True)

        st.markdown("<h3 class='sub-header'>B. BIỂU ĐỒ TỶ LỆ TRỌNG YẾU (%)</h3>", unsafe_allow_html=True)
        
        # Tính tỷ lệ % cho các chỉ tiêu
        df['TL_ChiBo_CD'] = (df['kq_chibo_cd'] / df['kq_chibo_tong1'] * 100).round(2)
        df['TL_ChiBo_ST'] = (df['kq_chibo_sotay'] / df['kq_chibo_tong2'] * 100).round(2)
        df['TL_CB_AI'] = (df['kq_cb_ai'] / df['kq_cb_tong1'] * 100).round(2)
        df['TL_ND_VNeID'] = (df['kq_nd_vneid'] / df['kq_nd_tong2'] * 100).round(2)
        df['TL_ND_Smart'] = (df['kq_nd_smartphone'] / df['kq_nd_tong3'] * 100).round(2)

        colA, colB = st.columns(2)
        with colA:
            fig1 = px.bar(df, x='don_vi', y=['TL_CB_AI', 'TL_ND_VNeID'], barmode='group', 
                          labels={'value': 'Tỷ lệ (%)', 'variable': 'Chỉ tiêu', 'don_vi': 'Đơn vị'},
                          title="Tỷ lệ CB biết dùng AI và ND phổ cập VNeID")
            st.plotly_chart(fig1, use_container_width=True)
            
        with colB:
            fig2 = px.bar(df, x='don_vi', y=['TL_ChiBo_CD', 'TL_ChiBo_ST'], barmode='group',
                          labels={'value': 'Tỷ lệ (%)', 'variable': 'Chỉ tiêu', 'don_vi': 'Đơn vị'},
                          title="Tỷ lệ Chi bộ Sinh hoạt Chuyên đề & Dùng Sổ tay")
            st.plotly_chart(fig2, use_container_width=True)
            
        st.markdown("<h3 class='sub-header'>C. BẢNG TỔNG HỢP CHI TIẾT & Ý KIẾN TỰ LUẬN</h3>", unsafe_allow_html=True)
        st.dataframe(df.drop(columns=['tl_mohinh', 'tl_khokhan']), use_container_width=True)
        
        for index, row in df.iterrows():
            with st.expander(f"📌 Xem Tự luận & Khó khăn của: {row['don_vi']}"):
                st.write("**Mô hình/Cách làm hay:**", row['tl_mohinh'] if row['tl_mohinh'] else "Không có báo cáo.")
                st.write("**Khó khăn/Vướng mắc chưa số hóa:**", row['tl_khokhan'] if row['tl_khokhan'] else "Không có báo cáo.")

# ==========================================
# TAB 3: QUẢN TRỊ ADMIN
# ==========================================
with tab3:
    pass_input = st.text_input("🔑 Nhập mật khẩu quản trị:", type="password")
    if pass_input == ADMIN_PASSWORD:
        st.success("Mở khóa quyền Admin thành công!")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 🏢 Quản lý Đơn vị")
            current_units = load_units()
            new_unit = st.text_input("Thêm đơn vị mới:")
            if st.button("➕ Thêm"):
                if new_unit and new_unit not in current_units:
                    current_units.append(new_unit)
                    save_units(current_units)
                    st.success(f"Đã thêm: {new_unit}")
                    st.rerun()
            
            remove_unit = st.selectbox("Xóa đơn vị:", ["-- Chọn --"] + current_units)
            if st.button("🗑️ Xóa"):
                if remove_unit != "-- Chọn --":
                    current_units.remove(remove_unit)
                    save_units(current_units)
                    st.success(f"Đã xóa: {remove_unit}")
                    st.rerun()
        
        with c2:
            st.markdown("### 🛠️ Chỉnh sửa Số liệu Data")
            data_to_edit = load_data()
            if data_to_edit:
                selected_dv_edit = st.selectbox("Chọn báo cáo đơn vị cần xóa:", [d['don_vi'] for d in data_to_edit])
                if st.button("⚠️ Xóa Báo Cáo Này"):
                    data_to_edit = [d for d in data_to_edit if d['don_vi'] != selected_dv_edit]
                    save_data(data_to_edit)
                    st.success("Đã xóa báo cáo thành công!")
                    st.rerun()
            else:
                st.info("Chưa có báo cáo nào để quản lý.")
    elif pass_input != "":
        st.error("Mật khẩu không chính xác!")
