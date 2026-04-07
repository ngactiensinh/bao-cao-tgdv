import streamlit as st
import requests
import base64
import pandas as pd
import os

st.set_page_config(page_title="Báo cáo TGDV - Tuyên Quang", page_icon="🌟", layout="wide")

# --- MẬT KHẨU ---
MAT_KHAU_CO_SO = "TGDV@2026"
MAT_KHAU_LANH_DAO = "Tgdv@2026"

# ---> LINK ỐNG NƯỚC <---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyRK8qCKzwM1cYe-HjPqm4QdAsxq8443Oax3KssvkHjVLo-__vSkXikohz_-v9ugGQm/exec"

# --- CSS TÙY CHỈNH ---
st.markdown("""
<style>
    .header-oval {
        background-color: #ffffff;
        border: 4px solid #C8102E;
        border-radius: 60px;
        padding: 15px 30px;
        margin-bottom: 30px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 25px;
        flex-wrap: wrap;
    }
    .main-title { font-size: 32px; font-weight: 900; color: #C8102E; text-transform: uppercase; margin: 0; line-height: 1.2; text-align: center;}
    .sub-title { font-size: 18px; font-weight: bold; color: #004B87; margin-top: 5px; text-align: center;}
    .section-header { font-size: 18px; font-weight: bold; color: #ffffff; background-color: #004B87; padding: 10px; border-radius: 5px; margin-top: 20px; margin-bottom: 10px;}
    .metric-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); margin-bottom: 15px;}
    .metric-value { font-size: 28px; font-weight: bold; color: #C8102E; }
    .metric-label { font-size: 15px; font-weight: bold; color: #004B87; }
</style>
""", unsafe_allow_html=True)

# --- HÀM TẠO TIÊU ĐỀ ---
def hien_thi_tieu_de(tieu_de_chinh):
    logo_html = ""
    try:
        with open("Logo TGDV.png", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            logo_html = f'<img src="data:image/png;base64,{data}" style="height: 85px;">'
    except:
        logo_html = '<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Qu%E1%BB%91c_huy_Vi%E1%BB%87t_Nam.svg/250px-Qu%E1%BB%91c_huy_Vi%E1%BB%87t_Nam.svg.png" style="height: 85px;">'
    
    st.markdown(f"""
    <div class="header-oval">
        <div>{logo_html}</div>
        <div>
            <div class="main-title">{tieu_de_chinh}</div>
            <div class="sub-title">BAN TUYÊN GIÁO VÀ DÂN VẬN TỈNH ỦY TUYÊN QUANG</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- MENU ĐIỀU HƯỚNG ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Qu%E1%BB%91c_huy_Vi%E1%BB%87t_Nam.svg/250px-Qu%E1%BB%91c_huy_Vi%E1%BB%87t_Nam.svg.png", width=100)
st.sidebar.markdown("### HỆ THỐNG BÁO CÁO TGDV")
menu = st.sidebar.radio("📌 Lựa chọn chức năng:", ["📝 Nhập Báo Cáo (Cơ sở)", "📊 Bảng Điều Khiển (Lãnh đạo)"])
st.sidebar.write("---")

# ==========================================================
# 1. TRANG NHẬP BÁO CÁO
# ==========================================================
if menu == "📝 Nhập Báo Cáo (Cơ sở)":
    if "dang_nhap_co_so" not in st.session_state: st.session_state["dang_nhap_co_so"] = False
    hien_thi_tieu_de("HỆ THỐNG THU THẬP BÁO CÁO")

    if not st.session_state["dang_nhap_co_so"]:
        st.markdown('<div class="section-header" style="text-align:center;">🔒 ĐĂNG NHẬP CƠ SỞ</div>', unsafe_allow_html=True)
        mk_nhap = st.text_input("Nhập mật khẩu cơ sở:", type="password")
        if st.button("🔑 Mở khóa"):
            if mk_nhap == MAT_KHAU_CO_SO:
                st.session_state["dang_nhap_co_so"] = True
                st.rerun()
            else: st.error("❌ Sai mật khẩu!")
    else:
        if st.button("🚪 Đăng xuất"):
            st.session_state["dang_nhap_co_so"] = False
            st.rerun()

        with st.form("form_bao_cao"):
            st.markdown('<div class="section-header">📍 PHẦN 1: THÔNG TIN CHUNG</div>', unsafe_allow_html=True)
            
            danh_sach_don_vi = [
                "Chọn đơn vị...", 
                "Đảng ủy Công an tỉnh", "Đảng ủy Quân sự tỉnh", "Đảng ủy các cơ quan Đảng tỉnh", "Đảng ủy Ủy ban nhân dân tỉnh",
                "Trung tâm chính trị xã Đồng Văn", "Trung tâm chính trị xã Mèo Vạc", "Trung tâm chính trị xã Yên Minh", 
                "Trung tâm chính trị xã Quản Bạ", "Trung tâm chính trị xã Hoàng Su Phì", "Trung tâm chính trị xã Pà Vầy Sủ", 
                "Trung tâm chính trị xã Bắc Mê", "Trung tâm chính trị xã Vị Xuyên", "Trung tâm chính trị xã Bắc Quang", 
                "Trung tâm chính trị xã Quang Bình", "Trung tâm chính trị phường Hà Giang 2", "Trung tâm chính trị xã Lâm Bình", 
                "Trung tâm chính trị xã Nà Hang", "Trung tâm chính trị xã Chiêm Hóa", "Trung tâm chính trị xã Hàm Yên", 
                "Trung tâm chính trị xã Yên Sơn", "Trung tâm chính trị xã An Tường", "Trung tâm chính trị xã Sơn Dương",
                "Phường Mỹ Lâm", "Phường Minh Xuân", "Phường Nông Tiến", "Phường An Tường", "Phường Bình Thuận", "Phường Hà Giang 1", "Phường Hà Giang 2",
                "Xã Thượng Lâm", "Xã Lâm Bình", "Xã Minh Quang", "Xã Bình An", "Xã Côn Lôn", "Xã Yên Hoa", "Xã Thượng Nông", "Xã Hồng Thái", "Xã Nà Hang", "Xã Tân Mỹ", "Xã Yên Lập", "Xã Tân An", "Xã Chiêm Hóa", "Xã Hòa An", "Xã Kiên Đài", "Xã Tri Phú", "Xã Kim Bình", "Xã Yên Nguyên", "Xã Yên Phú", "Xã Bạch Xa", "Xã Phù Lưu", "Xã Hàm Yên", "Xã Bình Xa", "Xã Thái Sơn", "Xã Thái Hòa", "Xã Hùng Lợi", "Xã Trung Sơn", "Xã Thái Bình", "Xã Tân Long", "Xã Xuân Vân", "Xã Lực Hành", "Xã Yên Sơn", "Xã Nhữ Khê", "Xã Tân Trào", "Xã Minh Thanh", "Xã Sơn Dương", "Xã Bình Ca", "Xã Tân Thanh", "Xã Sơn Thủy", "Xã Phú Lương", "Xã Trường Sinh", "Xã Hồng Sơn", "Xã Đông Thọ", "Xã Lũng Cú", "Xã Đồng Văn", "Xã Sà Phìn", "Xã Phố Bảng", "Xã Lũng Phìn", "Xã Sủng Máng", "Xã Sơn Vĩ", "Xã Mèo Vạc", "Xã Khâu Vai", "Xã Niêm Sơn", "Xã Tát Ngà", "Xã Thắng Mố", "Xã Bạch Đích", "Xã Yên Minh", "Xã Mậu Duệ", "Xã Du Già", "Xã Đường Thượng", "Xã Lùng Tám", "Xã Cán Tỷ", "Xã Nghĩa Thuận", "Xã Quản Bạ", "Xã Tùng Vài", "Xã Yên Cường", "Xã Đường Hồng", "Xã Bắc Mê", "Xã Minh Ngọc", "Xã Ngọc Đường", "Xã Lao Chải", "Xã Thanh Thủy", "Xã Phú Linh", "Xã Linh Hồ", "Xã Bạch Ngọc", "Xã Vị Xuyên", "Xã Việt Lâm", "Xã Tân Quang", "Xã Đồng Tâm", "Xã Liên Hiệp", "Xã Bằng Hành", "Xã Bắc Quang", "Xã Hùng An", "Xã Vĩnh Tuy", "Xã Đồng Yên", "Xã Tiên Yên", "Xã Xuân Giang", "Xã Bằng Lang", "Xã Yên Thành", "Xã Quang Bình", "Xã Tân Trịnh", "Xã Thông Nguyên", "Xã Hồ Thầu", "Xã Nậm Dịch", "Xã Tân Tiến", "Xã Hoàng Su Phì", "Xã Thàng Tín", "Xã Bản Máy", "Xã Pờ Ly Ngài", "Xã Xín Mần", "Xã Pà Vầy Sủ", "Xã Nấm Dẩn", "Xã Trung Thịnh", "Xã Khuôn Lùng", "Xã Trung Hà", "Xã Kiến Thiết", "Xã Hùng Đức", "Xã Minh Sơn", "Xã Minh Tân", "Xã Thuận Hòa", "Xã Tùng Bá", "Xã Thượng Sơn", "Xã Cao Bồ", "Xã Ngọc Long", "Xã Giáp Trung", "Xã Tiên Nguyên", "Xã Quảng Nguyên"
            ]
            don_vi = st.selectbox("Tên đơn vị:", danh_sach_don_vi)
            col1, col2 = st.columns(2)
            with col1: ky_bao_cao = st.selectbox("Kỳ báo cáo:", [f"Tháng {i}" for i in range(1, 13)])
            with col2: nguoi_lap = st.text_input("Họ tên người lập biểu:")

            st.markdown('<div class="section-header">📊 PHẦN 2: CÔNG TÁC TUYÊN GIÁO & DÂN VẬN</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                so_hoi_nghi = st.number_input("1. Số hội nghị tuyên truyền:", min_value=0)
                tin_bai = st.number_input("2. Số tin, bài phản bác:", min_value=0)
                mo_hinh_dv = st.number_input("3. Số mô hình Dân vận khéo:", min_value=0)
                vu_viec = st.number_input("4. Số vụ việc đã giải quyết:", min_value=0)
            with c2:
                ty_le_dang_vien = st.number_input("5. Tỷ lệ đảng viên học tập (%):", min_value=0.0, max_value=100.0)
                du_luan = st.text_area("6. Nắm bắt dư luận (Tóm tắt):", height=200)

            st.markdown('<div class="section-header">📑 PHẦN 3: VĂN BẢN THAM MƯU (Phụ lục 1)</div>', unsafe_allow_html=True)
            with st.expander("👉 Kê khai chi tiết Văn bản tham mưu"):
                c3, c4 = st.columns(2)
                with c3:
                    sl_vb_capuy = st.number_input("Số VB Cấp ủy ban hành:", min_value=0)
                    dm_vb_capuy = st.text_area("Danh mục VB Cấp ủy:")
                with c4:
                    sl_vb_tgdv = st.number_input("Số VB Ban TG-DV tham mưu:", min_value=0)
                    dm_vb_tgdv = st.text_area("Danh mục VB Ban TG-DV:")

            st.markdown('<div class="section-header">🎓 PHẦN 4: ĐÀO TẠO, BỒI DƯỠNG (Phụ lục 2)</div>', unsafe_allow_html=True)
            with st.expander("👉 Nhập liệu các Lớp đào tạo, bồi dưỡng"):
                p1, p2 = st.columns(2)
                with p1:
                    st.markdown("**Số LỚP tổ chức/cử đi**")
                    lop_socap = st.number_input("- Sơ cấp LLCT:", min_value=0, key="l1")
                    lop_dvmoi = st.number_input("- Đảng viên mới:", min_value=0, key="l2")
                    lop_nhanthuc = st.number_input("- Nhận thức về Đảng:", min_value=0, key="l3")
                    lop_capuy = st.number_input("- Cấp ủy, Bí thư chi bộ:", min_value=0, key="l4")
                    lop_mttq = st.number_input("- Nghiệp vụ MTTQ & CT-XH:", min_value=0, key="l5")
                    lop_khac = st.number_input("- Lớp bồi dưỡng khác:", min_value=0, key="l6")
                with p2:
                    st.markdown("**Số HỌC VIÊN tham gia**")
                    hv_socap = st.number_input("- HV Sơ cấp LLCT:", min_value=0, key="h1")
                    hv_dvmoi = st.number_input("- HV Đảng viên mới:", min_value=0, key="h2")
                    hv_nhanthuc = st.number_input("- HV Nhận thức về Đảng:", min_value=0, key="h3")
                    hv_capuy = st.number_input("- HV Cấp ủy, Bí thư chi bộ:", min_value=0, key="h4")
                    hv_mttq = st.number_input("- HV Nghiệp vụ MTTQ & CT-XH:", min_value=0, key="h5")
                    hv_khac = st.number_input("- HV bồi dưỡng khác:", min_value=0, key="h6")

            st.markdown('<div class="section-header">🚀 PHẦN 5: CHUYỂN ĐỔI SỐ</div>', unsafe_allow_html=True)
            ky_so = st.slider("1. Tỷ lệ văn bản xử lý và ký số (%):", 0, 100, 50)
            zalo_oa = st.radio("2. Tiến độ Kế hoạch CĐS:", ["Đã hoàn thành tốt", "Đang triển khai", "Chưa thực hiện"])
            c5, c6 = st.columns(2)
            with c5: dl_truc_tuyen = st.number_input("3. Tỷ lệ nắm dư luận qua MXH (%):", min_value=0, max_value=100)
            with c6: nhan_luc_ai = st.number_input("4. Số cán bộ tập huấn CĐS:", min_value=0)

            st.markdown('<div class="section-header">📝 PHẦN 6: MINH CHỨNG</div>', unsafe_allow_html=True)
            file_minh_chung = st.file_uploader("Tải lên File báo cáo:", type=["pdf", "docx", "xlsx"])

            st.write("---")
            submitted = st.form_submit_button("🚀 GỬI HOẶC CẬP NHẬT BÁO CÁO", use_container_width=True)

            if submitted:
                if don_vi == "Chọn đơn vị...": st.error("⚠️ Vui lòng chọn tên đơn vị!")
                else:
                    with st.spinner("⏳ Đang xử lý..."):
                        file_base64 = ""; file_name = ""; file_mimeType = ""
                        if file_minh_chung is not None:
                            file_base64 = base64.b64encode(file_minh_chung.getvalue()).decode('utf-8')
                            file_name = f"{don_vi}_{ky_bao_cao}_{file_minh_chung.name}"
                            file_mimeType = file_minh_chung.type

                        data = {
                            "don_vi": don_vi, "ky_bao_cao": ky_bao_cao, "nguoi_lap": nguoi_lap,
                            "so_hoi_nghi": so_hoi_nghi, "ty_le_dang_vien": ty_le_dang_vien, "tin_bai": tin_bai,
                            "mo_hinh_dv": mo_hinh_dv, "vu_viec": vu_viec, "ky_so": ky_so, "zalo_oa": zalo_oa, 
                            "dl_truc_tuyen": dl_truc_tuyen, "nhan_luc_ai": nhan_luc_ai,
                            "sl_vb_capuy": sl_vb_capuy, "dm_vb_capuy": dm_vb_capuy, "sl_vb_tgdv": sl_vb_tgdv, "dm_vb_tgdv": dm_vb_tgdv,
                            "lop_socap": lop_socap, "hv_socap": hv_socap, "lop_dvmoi": lop_dvmoi, "hv_dvmoi": hv_dvmoi,
                            "lop_nhanthuc": lop_nhanthuc, "hv_nhanthuc": hv_nhanthuc, "lop_capuy": lop_capuy, "hv_capuy": hv_capuy,
                            "lop_mttq": lop_mttq, "hv_mttq": hv_mttq, "lop_khac": lop_khac, "hv_khac": hv_khac,
                            "file_base64": file_base64, "file_name": file_name, "file_mimeType": file_mimeType
                        }
                        try:
                            response = requests.post(WEB_APP_URL, json=data)
                            if response.status_code == 200:
                                st.success(f"✅ Báo cáo của {don_vi} đã cập nhật!")
                                st.balloons()
                            else: st.error("❌ Lỗi máy chủ.")
                        except Exception as e: st.error(f"❌ Lỗi mạng: {e}")

# ==========================================================
# 2. TRANG BẢNG ĐIỀU KHIỂN (DÀNH CHO LÃNH ĐẠO) - ĐÃ NÂNG CẤP VIP
# ==========================================================
elif menu == "📊 Bảng Điều Khiển (Lãnh đạo)":
    if "dang_nhap_lanh_dao" not in st.session_state: st.session_state["dang_nhap_lanh_dao"] = False
    hien_thi_tieu_de("BẢNG ĐIỀU KHIỂN CHIẾN LƯỢC")

    if not st.session_state["dang_nhap_lanh_dao"]:
        mk_lanh_dao = st.text_input("Nhập mật khẩu Lãnh đạo:", type="password")
        if st.button("🔑 Đăng nhập"):
            if mk_lanh_dao == MAT_KHAU_LANH_DAO:
                st.session_state["dang_nhap_lanh_dao"] = True
                st.rerun()
            else: st.error("❌ Mật khẩu không hợp lệ!")
    else:
        if st.button("🚪 Đăng xuất Lãnh đạo"):
            st.session_state["dang_nhap_lanh_dao"] = False
            st.rerun()

        with st.spinner("Đang đồng bộ dữ liệu từ Tỉnh ủy..."):
            try:
                res = requests.get(WEB_APP_URL)
                if res.status_code == 200:
                    data_json = res.json()
                    if len(data_json) > 0:
                        df = pd.DataFrame(data_json)
                        
                        # --- XỬ LÝ SỐ LIỆU ĐỂ TÍNH TOÁN ---
                        # Chuyển các cột cần thiết sang dạng số
                        for col in [4, 5, 6, 7, 8, 9, 18, 20, 22, 24, 26, 28]:
                            df.iloc[:, col] = pd.to_numeric(df.iloc[:, col], errors='coerce').fillna(0)
                        
                        # Tính tổng các chỉ số
                        tong_don_vi = len(df)
                        tong_hoi_nghi = df.iloc[:, 4].sum()
                        tong_mo_hinh = df.iloc[:, 7].sum()
                        tong_vu_viec = df.iloc[:, 8].sum()
                        tb_dang_vien = df.iloc[:, 5].mean()
                        tong_hv = df.iloc[:, [18, 20, 22, 24, 26, 28]].sum().sum()
                        
                        # --- HÀNG METRICS 1 ---
                        m1, m2, m3 = st.columns(3)
                        with m1: st.markdown(f'<div class="metric-box"><div class="metric-label">🏢 Số Báo cáo đã nộp</div><div class="metric-value">{tong_don_vi}</div></div>', unsafe_allow_html=True)
                        with m2: st.markdown(f'<div class="metric-box"><div class="metric-label">🎤 Tổng số Hội nghị</div><div class="metric-value">{int(tong_hoi_nghi)}</div></div>', unsafe_allow_html=True)
                        with m3: st.markdown(f'<div class="metric-box"><div class="metric-label">🤝 Mô hình Dân vận khéo</div><div class="metric-value">{int(tong_mo_hinh)}</div></div>', unsafe_allow_html=True)
                        
                        # --- HÀNG METRICS 2 (MỚI THÊM) ---
                        m4, m5, m6 = st.columns(3)
                        with m4: st.markdown(f'<div class="metric-box"><div class="metric-label">⚖️ Vụ việc đã giải quyết</div><div class="metric-value">{int(tong_vu_viec)}</div></div>', unsafe_allow_html=True)
                        with m5: st.markdown(f'<div class="metric-box"><div class="metric-label">📈 TB Đảng viên học tập</div><div class="metric-value">{tb_dang_vien:.1f}%</div></div>', unsafe_allow_html=True)
                        with m6: st.markdown(f'<div class="metric-box"><div class="metric-label">🎓 Tổng số Học viên ĐT-BD</div><div class="metric-value">{int(tong_hv)}</div></div>', unsafe_allow_html=True)
                        
                        st.write("---")
                        
                        # --- HÀNG BIỂU ĐỒ 1 ---
                        col_chart1, col_chart2 = st.columns(2)
                        with col_chart1:
                            st.markdown("#### 📊 Tỷ lệ Ký số văn bản (%)")
                            df_ky_so = df.iloc[:, [1, 9]] 
                            df_ky_so.columns = ["Đơn vị", "Tỷ lệ Ký số (%)"]
                            st.bar_chart(df_ky_so.set_index("Đơn vị"))
                            
                        with col_chart2:
                            st.markdown("#### 📈 Số lượng Tin bài phản bác")
                            df_tin_bai = df.iloc[:, [1, 6]] 
                            df_tin_bai.columns = ["Đơn vị", "Số tin bài"]
                            st.line_chart(df_tin_bai.set_index("Đơn vị"))
                            
                        st.write("---")
                        
                        # --- HÀNG BIỂU ĐỒ 2 (MỚI THÊM) ---
                        col_chart3, col_chart4 = st.columns(2)
                        with col_chart3:
                            st.markdown("#### 📱 Tiến độ Kế hoạch CĐS (Zalo OA)")
                            # Đếm số lượng các trạng thái Zalo OA
                            df_zalo = df.iloc[:, 10].value_counts()
                            st.bar_chart(df_zalo)
                            
                        with col_chart4:
                            st.markdown("#### 🎓 Cơ cấu Học viên Đào tạo, Bồi dưỡng")
                            # Trích xuất dữ liệu học viên (Phụ lục 2)
                            hv_data = {
                                "Sơ cấp LLCT": df.iloc[:, 18].sum(),
                                "Đảng viên mới": df.iloc[:, 20].sum(),
                                "Nhận thức Đảng": df.iloc[:, 22].sum(),
                                "Cấp ủy, Bí thư": df.iloc[:, 24].sum(),
                                "MTTQ & CT-XH": df.iloc[:, 26].sum(),
                                "Khác": df.iloc[:, 28].sum(),
                            }
                            df_hv = pd.DataFrame(list(hv_data.values()), index=list(hv_data.keys()), columns=["Số lượng"])
                            st.bar_chart(df_hv)
                        
                        st.write("---")
                        st.markdown("#### 📑 Danh sách Dữ liệu mới nhất")
                        st.dataframe(df.iloc[:, [0, 1, 2, 3]]) 
                    else:
                        st.info("Chưa có dữ liệu báo cáo nào trong hệ thống.")
            except Exception as e:
                st.error(f"Không thể tải dữ liệu. Lỗi: {e}")
