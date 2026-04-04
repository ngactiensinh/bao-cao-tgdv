import streamlit as st
import requests
import base64

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Báo cáo TGDV - Tuyên Quang", page_icon="🌟", layout="centered")

# CSS tuỳ chỉnh giao diện
st.markdown("""
<style>
    .main-title { font-size: 26px; font-weight: bold; color: #C8102E; text-align: center; text-transform: uppercase;}
    .sub-title { font-size: 16px; font-weight: bold; color: #004B87; text-align: center; margin-bottom: 20px;}
    .section-header { font-size: 18px; font-weight: bold; color: #ffffff; background-color: #004B87; padding: 10px; border-radius: 5px; margin-top: 20px; margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

# --- TIÊU ĐỀ & LOGO ---
col1, col2 = st.columns([1, 6])
with col1:
    try:
        st.image("Logo TGDV.png", width=80)
    except:
        st.write("🌟")
with col2:
    st.markdown('<div class="main-title">HỆ THỐNG THU THẬP BÁO CÁO</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">BAN TUYÊN GIÁO VÀ DÂN VẬN TỈNH ỦY TUYÊN QUANG</div>', unsafe_allow_html=True)
st.write("---")

# --- BIỂU MẪU NHẬP LIỆU ---
with st.form("form_bao_cao"):
    
    st.markdown('<div class="section-header">📍 PHẦN 1: THÔNG TIN ĐƠN VỊ</div>', unsafe_allow_html=True)
    
    # Danh sách 124 đơn vị hành chính cấp xã, phường tỉnh Tuyên Quang
    danh_sach_don_vi = [
        "Chọn đơn vị...", 
        # CÁC PHƯỜNG
        "Phường Mỹ Lâm", "Phường Minh Xuân", "Phường Nông Tiến", "Phường An Tường", "Phường Bình Thuận", "Phường Hà Giang 1", "Phường Hà Giang 2",
        # CÁC XÃ
        "Xã Thượng Lâm", "Xã Lâm Bình", "Xã Minh Quang", "Xã Bình An", "Xã Côn Lôn", "Xã Yên Hoa", "Xã Thượng Nông", "Xã Hồng Thái", "Xã Nà Hang", "Xã Tân Mỹ", "Xã Yên Lập", "Xã Tân An", "Xã Chiêm Hóa", "Xã Hòa An", "Xã Kiên Đài", "Xã Tri Phú", "Xã Kim Bình", "Xã Yên Nguyên", "Xã Yên Phú", "Xã Bạch Xa", "Xã Phù Lưu", "Xã Hàm Yên", "Xã Bình Xa", "Xã Thái Sơn", "Xã Thái Hòa", "Xã Hùng Lợi", "Xã Trung Sơn", "Xã Thái Bình", "Xã Tân Long", "Xã Xuân Vân", "Xã Lực Hành", "Xã Yên Sơn", "Xã Nhữ Khê", "Xã Tân Trào", "Xã Minh Thanh", "Xã Sơn Dương", "Xã Bình Ca", "Xã Tân Thanh", "Xã Sơn Thủy", "Xã Phú Lương", "Xã Trường Sinh", "Xã Hồng Sơn", "Xã Đông Thọ", "Xã Lũng Cú", "Xã Đồng Văn", "Xã Sà Phìn", "Xã Phố Bảng", "Xã Lũng Phìn", "Xã Sủng Máng", "Xã Sơn Vĩ", "Xã Mèo Vạc", "Xã Khâu Vai", "Xã Niêm Sơn", "Xã Tát Ngà", "Xã Thắng Mố", "Xã Bạch Đích", "Xã Yên Minh", "Xã Mậu Duệ", "Xã Du Già", "Xã Đường Thượng", "Xã Lùng Tám", "Xã Cán Tỷ", "Xã Nghĩa Thuận", "Xã Quản Bạ", "Xã Tùng Vài", "Xã Yên Cường", "Xã Đường Hồng", "Xã Bắc Mê", "Xã Minh Ngọc", "Xã Ngọc Đường", "Xã Lao Chải", "Xã Thanh Thủy", "Xã Phú Linh", "Xã Linh Hồ", "Xã Bạch Ngọc", "Xã Vị Xuyên", "Xã Việt Lâm", "Xã Tân Quang", "Xã Đồng Tâm", "Xã Liên Hiệp", "Xã Bằng Hành", "Xã Bắc Quang", "Xã Hùng An", "Xã Vĩnh Tuy", "Xã Đồng Yên", "Xã Tiên Yên", "Xã Xuân Giang", "Xã Bằng Lang", "Xã Yên Thành", "Xã Quang Bình", "Xã Tân Trịnh", "Xã Thông Nguyên", "Xã Hồ Thầu", "Xã Nậm Dịch", "Xã Tân Tiến", "Xã Hoàng Su Phì", "Xã Thàng Tín", "Xã Bản Máy", "Xã Pờ Ly Ngài", "Xã Xín Mần", "Xã Pà Vầy Sủ", "Xã Nấm Dẩn", "Xã Trung Thịnh", "Xã Khuôn Lùng", "Xã Trung Hà", "Xã Kiến Thiết", "Xã Hùng Đức", "Xã Minh Sơn", "Xã Minh Tân", "Xã Thuận Hòa", "Xã Tùng Bá", "Xã Thượng Sơn", "Xã Cao Bồ", "Xã Ngọc Long", "Xã Giáp Trung", "Xã Tiên Nguyên", "Xã Quảng Nguyên"
    ]
    don_vi = st.selectbox("Tên đơn vị (Xã/Phường/Thị trấn):", danh_sach_don_vi)
    
    col1, col2 = st.columns(2)
    with col1:
        ky_bao_cao = st.selectbox("Kỳ báo cáo:", [f"Tháng {i}" for i in range(1, 13)])
    with col2:
        nguoi_lap = st.text_input("Họ tên người lập biểu:")

    st.markdown('<div class="section-header">📊 PHẦN 2: CÔNG TÁC TUYÊN GIÁO</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        so_hoi_nghi = st.number_input("1. Số hội nghị tuyên truyền (cuộc):", min_value=0, step=1)
        tin_bai = st.number_input("3. Số tin, bài đấu tranh phản bác:", min_value=0, step=1)
    with c2:
        ty_le_dang_vien = st.number_input("2. Tỷ lệ đảng viên học tập (%):", min_value=0.0, max_value=100.0, step=0.1)
        du_luan = st.text_area("4. Nắm bắt dư luận (Tóm tắt):", height=100)

    st.markdown('<div class="section-header">🤝 PHẦN 3: CÔNG TÁC DÂN VẬN</div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        mo_hinh_dv = st.number_input("1. Số mô hình Dân vận khéo hiệu quả:", min_value=0, step=1)
    with c4:
        vu_viec = st.number_input("2. Số vụ việc, điểm nóng đã giải quyết:", min_value=0, step=1)

    st.markdown('<div class="section-header">🚀 PHẦN 4: CHUYỂN ĐỔI SỐ (Theo KH 2026)</div>', unsafe_allow_html=True)
    ky_so = st.slider("1. Tỷ lệ văn bản xử lý và ký số (%):", 0, 100, 50)
    zalo_oa = st.radio("2. Tiến độ thực hiện Kế hoạch Chuyển đổi số:", ["Đã hoàn thành tốt các chỉ tiêu", "Đang triển khai thực hiện", "Chưa thực hiện"])
    c5, c6 = st.columns(2)
    with c5:
        dl_truc_tuyen = st.number_input("3. Tỷ lệ thu thập DLXH qua MXH (%):", min_value=0, max_value=100, step=1)
    with c6:
        # ĐÃ SỬA DÒNG NÀY THEO Ý CỦA SẾP
        nhan_luc_ai = st.number_input("4. Số cán bộ được tập huấn về Công nghệ số:", min_value=0, step=1)

    st.markdown('<div class="section-header">📝 PHẦN 5: MINH CHỨNG</div>', unsafe_allow_html=True)
    file_minh_chung = st.file_uploader("Tải lên Báo cáo chi tiết (File Word/PDF có dấu đỏ):", type=["pdf", "docx"])

    st.write("---")
    submitted = st.form_submit_button("🚀 GỬI BÁO CÁO LÊN TỈNH ỦY", use_container_width=True)

    if submitted:
        if don_vi == "Chọn đơn vị...":
            st.error("⚠️ Đồng chí vui lòng chọn tên đơn vị!")
        elif not nguoi_lap:
            st.warning("⚠️ Đồng chí vui lòng điền họ tên người lập biểu!")
        else:
            with st.spinner("⏳ Đang mã hóa file và gửi dữ liệu lên máy chủ Tỉnh ủy..."):
                
                # Xử lý file minh chứng (Mã hóa Base64)
                file_base64 = ""
                file_name = ""
                file_mimeType = ""
                
                if file_minh_chung is not None:
                    bytes_data = file_minh_chung.getvalue()
                    file_base64 = base64.b64encode(bytes_data).decode('utf-8')
                    # Đổi tên file cho dễ quản lý: TenXa_KyBaoCao_TenFileGoc
                    file_name = f"{don_vi}_{ky_bao_cao}_{file_minh_chung.name}"
                    file_mimeType = file_minh_chung.type

                # Gom dữ liệu lại thành 1 gói
                data = {
                    "don_vi": don_vi, "ky_bao_cao": ky_bao_cao, "nguoi_lap": nguoi_lap,
                    "so_hoi_nghi": so_hoi_nghi, "ty_le_dang_vien": ty_le_dang_vien, "tin_bai": tin_bai,
                    "mo_hinh_dv": mo_hinh_dv, "vu_viec": vu_viec,
                    "ky_so": ky_so, "zalo_oa": zalo_oa, "dl_truc_tuyen": dl_truc_tuyen, "nhan_luc_ai": nhan_luc_ai,
                    "file_base64": file_base64, "file_name": file_name, "file_mimeType": file_mimeType
                }
                
                # Link ống nước mới nhất
                WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwD7MM9lYZYfuF-Re7Xq1finPmGTrLNGwPCONjsCWqyIrn3k7a6oDBFsa0J_PjR_-Ew/exec"
                
                try:
                    response = requests.post(WEB_APP_URL, json=data)
                    if response.status_code == 200:
                        st.success(f"✅ Báo cáo {ky_bao_cao} của {don_vi} (kèm File) đã được gửi thành công!")
                        st.balloons()
                    else:
                        st.error("❌ Có lỗi xảy ra ở máy chủ. Vui lòng thử lại.")
                except Exception as e:
                    st.error(f"❌ Lỗi đường truyền mạng: {e}")
