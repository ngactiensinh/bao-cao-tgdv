import streamlit as st
import requests
import base64

st.set_page_config(page_title="Báo cáo TGDV - Tuyên Quang", page_icon="🌟", layout="centered")

MAT_KHAU_HE_THONG = "TGDV@2026"

if "dang_nhap_thanh_cong" not in st.session_state:
    st.session_state["dang_nhap_thanh_cong"] = False

st.markdown("""
<style>
    .main-title { font-size: 26px; font-weight: bold; color: #C8102E; text-align: center; text-transform: uppercase;}
    .sub-title { font-size: 16px; font-weight: bold; color: #004B87; text-align: center; margin-bottom: 20px;}
    .section-header { font-size: 18px; font-weight: bold; color: #ffffff; background-color: #004B87; padding: 10px; border-radius: 5px; margin-top: 20px; margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 6])
with col1:
    try: st.image("Logo TGDV.png", width=80)
    except: st.write("🌟")
with col2:
    st.markdown('<div class="main-title">HỆ THỐNG THU THẬP BÁO CÁO</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">BAN TUYÊN GIÁO VÀ DÂN VẬN TỈNH ỦY TUYÊN QUANG</div>', unsafe_allow_html=True)
st.write("---")

if not st.session_state["dang_nhap_thanh_cong"]:
    st.markdown('<div class="section-header" style="text-align:center;">🔒 ĐĂNG NHẬP HỆ THỐNG</div>', unsafe_allow_html=True)
    mat_khau_nhap = st.text_input("Vui lòng nhập mật khẩu dành cho cán bộ cơ sở:", type="password")
    if st.button("🔑 Mở khóa", use_container_width=True):
        if mat_khau_nhap == MAT_KHAU_HE_THONG:
            st.session_state["dang_nhap_thanh_cong"] = True
            st.rerun() 
        else:
            st.error("❌ Mật khẩu không chính xác! Đồng chí vui lòng kiểm tra lại.")
            
else:
    col_empty, col_logout = st.columns([4, 1])
    with col_logout:
        if st.button("🚪 Đăng xuất"):
            st.session_state["dang_nhap_thanh_cong"] = False
            st.rerun()
            
    with st.form("form_bao_cao"):
        st.markdown('<div class="section-header">📍 PHẦN 1: THÔNG TIN CHUNG</div>', unsafe_allow_html=True)
        danh_sach_don_vi = [
            "Chọn đơn vị...", "Phường Mỹ Lâm", "Phường Minh Xuân", "Phường Nông Tiến", "Phường An Tường", "Phường Bình Thuận", "Phường Hà Giang 1", "Phường Hà Giang 2",
            "Xã Thượng Lâm", "Xã Lâm Bình", "Xã Minh Quang", "Xã Bình An", "Xã Côn Lôn", "Xã Yên Hoa", "Xã Thượng Nông", "Xã Hồng Thái", "Xã Nà Hang", "Xã Tân Mỹ", "Xã Yên Lập", "Xã Tân An", "Xã Chiêm Hóa", "Xã Hòa An", "Xã Kiên Đài", "Xã Tri Phú", "Xã Kim Bình", "Xã Yên Nguyên", "Xã Yên Phú", "Xã Bạch Xa", "Xã Phù Lưu", "Xã Hàm Yên", "Xã Bình Xa", "Xã Thái Sơn", "Xã Thái Hòa", "Xã Hùng Lợi", "Xã Trung Sơn", "Xã Thái Bình", "Xã Tân Long", "Xã Xuân Vân", "Xã Lực Hành", "Xã Yên Sơn", "Xã Nhữ Khê", "Xã Tân Trào", "Xã Minh Thanh", "Xã Sơn Dương", "Xã Bình Ca", "Xã Tân Thanh", "Xã Sơn Thủy", "Xã Phú Lương", "Xã Trường Sinh", "Xã Hồng Sơn", "Xã Đông Thọ", "Xã Lũng Cú", "Xã Đồng Văn", "Xã Sà Phìn", "Xã Phố Bảng", "Xã Lũng Phìn", "Xã Sủng Máng", "Xã Sơn Vĩ", "Xã Mèo Vạc", "Xã Khâu Vai", "Xã Niêm Sơn", "Xã Tát Ngà", "Xã Thắng Mố", "Xã Bạch Đích", "Xã Yên Minh", "Xã Mậu Duệ", "Xã Du Già", "Xã Đường Thượng", "Xã Lùng Tám", "Xã Cán Tỷ", "Xã Nghĩa Thuận", "Xã Quản Bạ", "Xã Tùng Vài", "Xã Yên Cường", "Xã Đường Hồng", "Xã Bắc Mê", "Xã Minh Ngọc", "Xã Ngọc Đường", "Xã Lao Chải", "Xã Thanh Thủy", "Xã Phú Linh", "Xã Linh Hồ", "Xã Bạch Ngọc", "Xã Vị Xuyên", "Xã Việt Lâm", "Xã Tân Quang", "Xã Đồng Tâm", "Xã Liên Hiệp", "Xã Bằng Hành", "Xã Bắc Quang", "Xã Hùng An", "Xã Vĩnh Tuy", "Xã Đồng Yên", "Xã Tiên Yên", "Xã Xuân Giang", "Xã Bằng Lang", "Xã Yên Thành", "Xã Quang Bình", "Xã Tân Trịnh", "Xã Thông Nguyên", "Xã Hồ Thầu", "Xã Nậm Dịch", "Xã Tân Tiến", "Xã Hoàng Su Phì", "Xã Thàng Tín", "Xã Bản Máy", "Xã Pờ Ly Ngài", "Xã Xín Mần", "Xã Pà Vầy Sủ", "Xã Nấm Dẩn", "Xã Trung Thịnh", "Xã Khuôn Lùng", "Xã Trung Hà", "Xã Kiến Thiết", "Xã Hùng Đức", "Xã Minh Sơn", "Xã Minh Tân", "Xã Thuận Hòa", "Xã Tùng Bá", "Xã Thượng Sơn", "Xã Cao Bồ", "Xã Ngọc Long", "Xã Giáp Trung", "Xã Tiên Nguyên", "Xã Quảng Nguyên"
        ]
        don_vi = st.selectbox("Tên đơn vị:", danh_sach_don_vi)
        col1, col2 = st.columns(2)
        with col1: ky_bao_cao = st.selectbox("Kỳ báo cáo:", [f"Tháng {i}" for i in range(1, 13)])
        with col2: nguoi_lap = st.text_input("Họ tên người lập biểu:")

        st.markdown('<div class="section-header">📊 PHẦN 2: CÔNG TÁC TUYÊN GIÁO & DÂN VẬN</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            so_hoi_nghi = st.number_input("1. Số hội nghị tuyên truyền (cuộc):", min_value=0)
            tin_bai = st.number_input("2. Số tin, bài đấu tranh phản bác:", min_value=0)
            mo_hinh_dv = st.number_input("3. Số mô hình Dân vận khéo:", min_value=0)
            vu_viec = st.number_input("4. Số vụ việc đã giải quyết:", min_value=0)
        with c2:
            ty_le_dang_vien = st.number_input("5. Tỷ lệ đảng viên học tập (%):", min_value=0.0, max_value=100.0)
            du_luan = st.text_area("6. Nắm bắt dư luận (Tóm tắt):", height=200)

        # PHỤ LỤC 1 (ĐƯỢC GẬP GỌN)
        st.markdown('<div class="section-header">📑 PHẦN 3: VĂN BẢN THAM MƯU (Phụ lục 1)</div>', unsafe_allow_html=True)
        with st.expander("👉 Bấm vào đây để kê khai chi tiết các Văn bản tham mưu"):
            st.info("💡 Hướng dẫn: Nhập số lượng và liệt kê tên văn bản (Nghị quyết, Chỉ thị, KH...), Số/Ngày ban hành, Trích yếu nội dung.")
            c3, c4 = st.columns(2)
            with c3:
                sl_vb_capuy = st.number_input("Số lượng VB Cấp ủy ban hành:", min_value=0)
                dm_vb_capuy = st.text_area("Danh mục VB Cấp ủy:", placeholder="VD: 1. Nghị quyết 01 (12/01/2026) về...")
            with c4:
                sl_vb_tgdv = st.number_input("Số lượng VB Ban TG-DV tham mưu:", min_value=0)
                dm_vb_tgdv = st.text_area("Danh mục VB Ban TG-DV:", placeholder="VD: 1. Kế hoạch 02 (15/01/2026) về...")

        # PHỤ LỤC 2 (ĐƯỢC GẬP GỌN)
        st.markdown('<div class="section-header">🎓 PHẦN 4: ĐÀO TẠO, BỒI DƯỠNG (Phụ lục 2)</div>', unsafe_allow_html=True)
        with st.expander("👉 Bấm vào đây để nhập liệu các Lớp đào tạo, bồi dưỡng"):
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
        zalo_oa = st.radio("2. Tiến độ thực hiện Kế hoạch CĐS:", ["Đã hoàn thành tốt", "Đang triển khai", "Chưa thực hiện"])
        c5, c6 = st.columns(2)
        with c5: dl_truc_tuyen = st.number_input("3. Tỷ lệ nắm dư luận qua MXH (%):", min_value=0, max_value=100)
        with c6: nhan_luc_ai = st.number_input("4. Số cán bộ được tập huấn CĐS:", min_value=0)

        st.markdown('<div class="section-header">📝 PHẦN 6: MINH CHỨNG</div>', unsafe_allow_html=True)
        file_minh_chung = st.file_uploader("Tải lên File báo cáo / Kế hoạch (Nếu có):", type=["pdf", "docx", "xlsx"])

        st.write("---")
        submitted = st.form_submit_button("🚀 GỬI HOẶC CẬP NHẬT BÁO CÁO", use_container_width=True)

        if submitted:
            if don_vi == "Chọn đơn vị...": st.error("⚠️ Vui lòng chọn tên đơn vị!")
            elif not nguoi_lap: st.warning("⚠️ Vui lòng điền họ tên người lập biểu!")
            else:
                with st.spinner("⏳ Đang mã hóa và gửi dữ liệu..."):
                    file_base64 = ""
                    file_name = ""
                    file_mimeType = ""
                    if file_minh_chung is not None:
                        file_base64 = base64.b64encode(file_minh_chung.getvalue()).decode('utf-8')
                        file_name = f"{don_vi}_{ky_bao_cao}_{file_minh_chung.name}"
                        file_mimeType = file_minh_chung.type

                    data = {
                        "don_vi": don_vi, "ky_bao_cao": ky_bao_cao, "nguoi_lap": nguoi_lap,
                        "so_hoi_nghi": so_hoi_nghi, "ty_le_dang_vien": ty_le_dang_vien, "tin_bai": tin_bai,
                        "mo_hinh_dv": mo_hinh_dv, "vu_viec": vu_viec, "ky_so": ky_so, "zalo_oa": zalo_oa, 
                        "dl_truc_tuyen": dl_truc_tuyen, "nhan_luc_ai": nhan_luc_ai,
                        "sl_vb_capuy": sl_vb_capuy, "dm_vb_capuy": dm_vb_capuy, 
                        "sl_vb_tgdv": sl_vb_tgdv, "dm_vb_tgdv": dm_vb_tgdv,
                        "lop_socap": lop_socap, "hv_socap": hv_socap, 
                        "lop_dvmoi": lop_dvmoi, "hv_dvmoi": hv_dvmoi,
                        "lop_nhanthuc": lop_nhanthuc, "hv_nhanthuc": hv_nhanthuc,
                        "lop_capuy": lop_capuy, "hv_capuy": hv_capuy,
                        "lop_mttq": lop_mttq, "hv_mttq": hv_mttq,
                        "lop_khac": lop_khac, "hv_khac": hv_khac,
                        "file_base64": file_base64, "file_name": file_name, "file_mimeType": file_mimeType
                    }
                    
                    # ---> DÁN LINK ỐNG NƯỚC MỚI VÀO ĐÂY <---
                    WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyozMgtncYG4QjqogmoG0SzWXx-JaEV7Q3u7DQMUVBV3wy2JjOeUdm9-oDXrSNMiNJW/exec"
                    
                    try:
                        response = requests.post(WEB_APP_URL, json=data)
                        if response.status_code == 200:
                            st.success(f"✅ Báo cáo {ky_bao_cao} của {don_vi} đã được cập nhật!")
                            st.balloons()
                        else: st.error("❌ Lỗi máy chủ.")
                    except Exception as e: st.error(f"❌ Lỗi mạng: {e}")
