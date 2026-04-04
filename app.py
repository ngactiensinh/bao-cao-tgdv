import streamlit as st
import requests

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
    # Danh sách cấp xã/phường trực thuộc tỉnh (Đã cập nhật theo hệ thống chính quyền 2 cấp)
    danh_sach_don_vi = [
        "Chọn đơn vị...", "Phường Minh Xuân", "Phường Tân Quang", "Xã Lưỡng Vượng", 
        "Phường Minh Khai", "Phường Nguyễn Trãi", "Xã Phương Độ", "Xã Thanh Thủy", 
        "Xã Bắc Mê", "Thị trấn Yên Phú", "Xã Yên Lập"
    ]
    don_vi = st.selectbox("Tên đơn vị (Xã/Phường/Thị trấn):", danh_sach_don_vi)
    
    col1, col2 = st.columns(2)
    with col1:
        ky_bao_cao = st.selectbox("Kỳ báo cáo:", ["Tháng 1", "Tháng 2", "Tháng 3", "Quý I", "6 Tháng", "Năm"])
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
    zalo_oa = st.radio("2. Tiến độ triển khai Zalo / Mini App:", ["Đã vận hành thường xuyên", "Đang thử nghiệm", "Chưa triển khai"])
    c5, c6 = st.columns(2)
    with c5:
        dl_truc_tuyen = st.number_input("3. Tỷ lệ thu thập DLXH qua MXH (%):", min_value=0, max_value=100, step=1)
    with c6:
        nhan_luc_ai = st.number_input("4. Số cán bộ được tập huấn AI:", min_value=0, step=1)

    st.write("---")
    submitted = st.form_submit_button("🚀 GỬI BÁO CÁO LÊN TỈNH ỦY", use_container_width=True)

    if submitted:
        if don_vi == "Chọn đơn vị...":
            st.error("⚠️ Đồng chí vui lòng chọn tên đơn vị!")
        elif not nguoi_lap:
            st.warning("⚠️ Đồng chí vui lòng điền họ tên người lập biểu!")
        else:
            with st.spinner("⏳ Đang gửi dữ liệu lên máy chủ Tỉnh ủy..."):
                # Gom dữ liệu lại thành 1 gói
                data = {
                    "don_vi": don_vi, "ky_bao_cao": ky_bao_cao, "nguoi_lap": nguoi_lap,
                    "so_hoi_nghi": so_hoi_nghi, "ty_le_dang_vien": ty_le_dang_vien, "tin_bai": tin_bai,
                    "mo_hinh_dv": mo_hinh_dv, "vu_viec": vu_viec,
                    "ky_so": ky_so, "zalo_oa": zalo_oa, "dl_truc_tuyen": dl_truc_tuyen, "nhan_luc_ai": nhan_luc_ai
                }
                
                # Bắn dữ liệu qua Google Apps Script
                WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyRK8qCKzwM1cYe-HjPqm4QdAsxq8443Oax3KssvkHjVLo-__vSkXikohz_-v9ugGQm/exec"
                
                try:
                    response = requests.post(WEB_APP_URL, json=data)
                    if response.status_code == 200:
                        st.success(f"✅ Báo cáo {ky_bao_cao} của {don_vi} đã được gửi thành công về Ban Tuyên giáo và Dân vận Tỉnh ủy!")
                        st.balloons()
                    else:
                        st.error("❌ Có lỗi xảy ra ở máy chủ. Vui lòng thử lại.")
                except Exception as e:
                    st.error(f"❌ Lỗi đường truyền mạng: {e}")
