import streamlit as st
import pandas as pd
import base64
import json
from supabase import create_client, Client

st.set_page_config(page_title="Báo cáo TGDV - Tuyên Quang", page_icon="🌟", layout="wide")

# ==========================================
# CẤU HÌNH SUPABASE (Thay thế Google Sheet)
# ==========================================
SUPABASE_URL = "https://qqzsdxhqrdfvxnlurnyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFxenNkeGhxcmRmdnhubHVybnliIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU2MjY0NjAsImV4cCI6MjA5MTIwMjQ2MH0.H62F5zYEZ5l47fS4IdAE2JdRdI7inXQqWG0nvXhn2P8"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    pass

# --- MẬT KHẨU ---
MAT_KHAU_CO_SO = "TGDV@2026"
MAT_KHAU_LANH_DAO = "Admin@2026"

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

DANH_SACH_DON_VI = [
    "Chọn đơn vị...", 
    "Đảng ủy Công an tỉnh", "Đảng ủy Quân sự tỉnh", "Đảng ủy các cơ quan Đảng tỉnh", "Đảng ủy Ủy ban nhân dân tỉnh",
    "Phường Mỹ Lâm", "Phường Minh Xuân", "Phường Nông Tiến", "Phường An Tường", "Phường Bình Thuận", "Phường Hà Giang 1", "Phường Hà Giang 2",
    "Xã Thượng Lâm", "Xã Lâm Bình", "Xã Minh Quang", "Xã Bình An", "Xã Côn Lôn", "Xã Yên Hoa", "Xã Thượng Nông", "Xã Hồng Thái", "Xã Nà Hang", "Xã Tân Mỹ", "Xã Yên Lập", "Xã Tân An", "Xã Chiêm Hóa", "Xã Hòa An", "Xã Kiên Đài", "Xã Tri Phú", "Xã Kim Bình", "Xã Yên Nguyên", "Xã Yên Phú", "Xã Bạch Xa", "Xã Phù Lưu", "Xã Hàm Yên", "Xã Bình Xa", "Xã Thái Sơn", "Xã Thái Hòa", "Xã Hùng Lợi", "Xã Trung Sơn", "Xã Thái Bình", "Xã Tân Long", "Xã Xuân Vân", "Xã Lực Hành", "Xã Yên Sơn", "Xã Nhữ Khê", "Xã Tân Trào", "Xã Minh Thanh", "Xã Sơn Dương", "Xã Bình Ca", "Xã Tân Thanh", "Xã Sơn Thủy", "Xã Phú Lương", "Xã Trường Sinh", "Xã Hồng Sơn", "Xã Đông Thọ"
]

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

        with st.form("form_bao_cao", clear_on_submit=True):
            st.markdown('<div class="section-header">📍 THÔNG TIN CHUNG</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1: voi_don_vi = st.selectbox("Tên đơn vị:", DANH_SACH_DON_VI)
            with col2: voi_ky_bc = st.selectbox("Kỳ báo cáo:", ["Chọn kỳ..."] + [f"Tháng {i}" for i in range(1, 13)] + ["Quý I", "Quý II", "Quý III", "Quý IV"])
            
            st.markdown('<div class="section-header">📊 SỐ LIỆU CHI TIẾT (7 NHÓM)</div>', unsafe_allow_html=True)

            # 1. Nhóm Lãnh đạo, chỉ đạo
            with st.expander("1️⃣ NHÓM SỐ LIỆU VỀ CÔNG TÁC LÃNH ĐẠO, CHỈ ĐẠO", expanded=False):
                c1, c2, c3 = st.columns(3)
                g1_1 = c1.number_input("Số VB cấp ủy ban hành", min_value=0, step=1)
                g1_2 = c2.number_input("Số VB tham mưu cấp trên", min_value=0, step=1)
                g1_3 = c3.number_input("Số cuộc họp, hội nghị triển khai", min_value=0, step=1)

            # 2. Nhóm Học tập, quán triệt
            with st.expander("2️⃣ NHÓM SỐ LIỆU VỀ HỌC TẬP, QUÁN TRIỆT", expanded=False):
                c1, c2 = st.columns(2)
                g2_1 = c1.number_input("Số hội nghị tổ chức", min_value=0, step=1)
                g2_2 = c2.number_input("Số người tham gia", min_value=0, step=1)
                g2_3 = c1.number_input("Số văn bản đã quán triệt", min_value=0, step=1)
                g2_4 = c2.number_input("Tỷ lệ đảng viên tham gia (%)", min_value=0.0, max_value=100.0, step=0.1)

            # 3. Nhóm Tuyên truyền
            with st.expander("3️⃣ NHÓM SỐ LIỆU VỀ TUYÊN TRUYỀN", expanded=False):
                st.markdown("**3.1. Tuyên truyền chung**")
                c1, c2 = st.columns(2)
                g3_1 = c1.number_input("Số tin, bài, pano, khẩu hiệu", min_value=0, step=1)
                g3_2 = c2.number_input("Số lượt phát loa truyền thanh", min_value=0, step=1)
                st.markdown("**3.2. Tuyên truyền miệng & MXH**")
                c3, c4 = st.columns(2)
                g3_3 = c3.number_input("Số buổi tuyên truyền miệng", min_value=0, step=1)
                g3_6 = c4.number_input("Số bài chia sẻ FB/Zalo", min_value=0, step=1)

            # 4. Nhóm Dư luận xã hội
            with st.expander("4️⃣ NHÓM SỐ LIỆU VỀ DƯ LUẬN XÃ HỘI", expanded=False):
                c1, c2, c3 = st.columns(3)
                g4_1 = c1.number_input("Số báo cáo DLXH gửi lên", min_value=0, step=1)
                g4_2 = c2.number_input("Số vấn đề nổi cộm", min_value=0, step=1)
                g4_3 = c3.number_input("Số vụ việc đã giải quyết", min_value=0, step=1)

            # 5. Nhóm Khoa giáo, văn hóa
            with st.expander("5️⃣ NHÓM SỐ LIỆU VỀ KHOA GIÁO, VH-VN", expanded=False):
                c1, c2 = st.columns(2)
                g5_1 = c1.number_input("Số hoạt động VH-VN tổ chức", min_value=0, step=1)
                g5_2 = c2.number_input("Số lớp/buổi (GD, Y tế, Môi trường)", min_value=0, step=1)

            # 6. Nhóm Dân vận
            with st.expander("6️⃣ NHÓM SỐ LIỆU VỀ CÔNG TÁC DÂN VẬN", expanded=False):
                c1, c2, c3 = st.columns(3)
                g6_1 = c1.number_input("Số mô hình DVK đăng ký", min_value=0, step=1)
                g6_2 = c2.number_input("Số mô hình HĐ hiệu quả", min_value=0, step=1)
                g6_6 = c3.number_input("Số buổi tiếp xúc, đối thoại", min_value=0, step=1)

            # 7. Nhóm Nhiệm vụ trọng tâm
            with st.expander("7️⃣ NHÓM SỐ LIỆU NHIỆM VỤ TRỌNG TÂM", expanded=False):
                c1, c2, c3 = st.columns(3)
                g7_1 = c1.number_input("Số nhiệm vụ được giao", min_value=0, step=1)
                g7_2 = c2.number_input("Số nhiệm vụ hoàn thành", min_value=0, step=1)
                g7_3 = c3.number_input("Số nhiệm vụ đang làm", min_value=0, step=1)

            st.write("---")
            submitted = st.form_submit_button("🚀 GỬI BÁO CÁO LÊN TỈNH ỦY", use_container_width=True)

            if submitted:
                if voi_don_vi == "Chọn đơn vị..." or voi_ky_bc == "Chọn kỳ...": st.error("⚠️ Vui lòng chọn Đơn vị và Kỳ báo cáo!")
                else:
                    du_lieu_chi_tiet = {
                        "lanh_dao": {"vb_ban_hanh": g1_1, "vb_tham_muu": g1_2, "cuoc_hop": g1_3},
                        "quan_triet": {"hoi_nghi": g2_1, "nguoi_tham_gia": g2_2, "vb_trien_khai": g2_3, "ty_le_dv": g2_4},
                        "tuyen_truyen": {"tt_chung_tin_bai": g3_1, "tt_chung_loa": g3_2, "tt_mieng_buoi": g3_3, "mxh_chia_se": g3_6},
                        "du_luan": {"bc_gui": g4_1, "vd_noi_com": g4_2, "vu_viec_xl": g4_3},
                        "khoa_giao": {"hd_vhvn": g5_1, "lop_buoi": g5_2},
                        "dan_van": {"dvk_dang_ky": g6_1, "dvk_hieu_qua": g6_2, "dv_doi_thoai": g6_6},
                        "trong_tam": {"nv_giao": g7_1, "nv_hoan_thanh": g7_2, "nv_dang_lam": g7_3}
                    }
                    json_str = json.dumps(du_lieu_chi_tiet, ensure_ascii=False)
                    
                    with st.spinner("⏳ Đang đẩy dữ liệu vào máy chủ..."):
                        try:
                            supabase.table("bao_cao").insert({"don_vi": voi_don_vi, "ky_bao_cao": voi_ky_bc, "chi_tiet_so_lieu": json_str}).execute()
                            st.success(f"✅ Báo cáo của {voi_don_vi} đã được nộp thành công!")
                            st.balloons()
                        except Exception as e: st.error(f"❌ Lỗi: {e}")

# ==========================================================
# 2. TRANG BẢNG ĐIỀU KHIỂN (LÃNH ĐẠO)
# ==========================================================
elif menu == "📊 Bảng Điều Khiển (Lãnh đạo)":
    if "dang_nhap_lanh_dao" not in st.session_state: st.session_state["dang_nhap_lanh_dao"] = False
    hien_thi_tieu_de("BẢNG ĐIỀU KHIỂN CHIẾN LƯỢC")

    if not st.session_state["dang_nhap_lanh_dao"]:
        mk_lanh_dao = st.text_input("Nhập mật khẩu Lãnh đạo:", type="password")
        if st.button("🔑 Đăng nhập"):
            if mk_lanh_dao == MAT_KHAU_LANH_DAO:
                st.session_state["dang_nhap_lanh_dao"] = True; st.rerun()
            else: st.error("❌ Mật khẩu không hợp lệ!")
    else:
        if st.button("🚪 Đăng xuất Lãnh đạo"):
            st.session_state["dang_nhap_lanh_dao"] = False; st.rerun()

        with st.spinner("Đang đồng bộ dữ liệu từ Tỉnh ủy..."):
            try:
                # Kéo dữ liệu từ bảng bao_cao
                res = supabase.table("bao_cao").select("*").execute()
                df_goc = pd.DataFrame(res.data)
                
                if not df_goc.empty:
                    # Bóc tách file JSON để phân tích
                    df_goc['vb_tham_muu'] = df_goc['chi_tiet_so_lieu'].apply(lambda x: x.get('lanh_dao', {}).get('vb_tham_muu', 0))
                    df_goc['hoi_nghi_qt'] = df_goc['chi_tiet_so_lieu'].apply(lambda x: x.get('quan_triet', {}).get('hoi_nghi', 0))
                    df_goc['ty_le_dv'] = df_goc['chi_tiet_so_lieu'].apply(lambda x: x.get('quan_triet', {}).get('ty_le_dv', 0))
                    df_goc['chia_se_mxh'] = df_goc['chi_tiet_so_lieu'].apply(lambda x: x.get('tuyen_truyen', {}).get('mxh_chia_se', 0))
                    df_goc['noi_com'] = df_goc['chi_tiet_so_lieu'].apply(lambda x: x.get('du_luan', {}).get('vd_noi_com', 0))
                    df_goc['dvk_hieu_qua'] = df_goc['chi_tiet_so_lieu'].apply(lambda x: x.get('dan_van', {}).get('dvk_hieu_qua', 0))
                    df_goc['nv_hoan_thanh'] = df_goc['chi_tiet_so_lieu'].apply(lambda x: x.get('trong_tam', {}).get('nv_hoan_thanh', 0))
                    df_goc['nv_giao'] = df_goc['chi_tiet_so_lieu'].apply(lambda x: x.get('trong_tam', {}).get('nv_giao', 0))

                    # --- BỘ LỌC THỜI GIAN ---
                    st.markdown("### 🗓️ LỌC DỮ LIỆU THEO KỲ BÁO CÁO")
                    ky_loc = st.selectbox("Chọn kỳ muốn xem:", ["Tất cả (Từ trước đến nay)"] + list(df_goc['ky_bao_cao'].unique()))
                    
                    df = df_goc if ky_loc == "Tất cả (Từ trước đến nay)" else df_goc[df_goc['ky_bao_cao'] == ky_loc]

                    if len(df) == 0:
                        st.warning("Chưa có báo cáo nào cho kỳ này.")
                    else:
                        # --- HÀNG METRICS 1 ---
                        m1, m2, m3 = st.columns(3)
                        with m1: st.markdown(f'<div class="metric-box"><div class="metric-label">🏢 Số Báo cáo đã nộp</div><div class="metric-value">{len(df)}</div></div>', unsafe_allow_html=True)
                        with m2: st.markdown(f'<div class="metric-box"><div class="metric-label">📜 VB Tham mưu Cấp trên</div><div class="metric-value">{int(df["vb_tham_muu"].sum())}</div></div>', unsafe_allow_html=True)
                        with m3: st.markdown(f'<div class="metric-box"><div class="metric-label">🤝 Mô hình Dân vận Khéo HQ</div><div class="metric-value">{int(df["dvk_hieu_qua"].sum())}</div></div>', unsafe_allow_html=True)
                        
                        # --- HÀNG METRICS 2 ---
                        m4, m5, m6 = st.columns(3)
                        with m4: st.markdown(f'<div class="metric-box"><div class="metric-label">⚠️ Vấn đề nổi cộm phát hiện</div><div class="metric-value">{int(df["noi_com"].sum())}</div></div>', unsafe_allow_html=True)
                        with m5: st.markdown(f'<div class="metric-box"><div class="metric-label">📈 Tỷ lệ Đảng viên học tập (TB)</div><div class="metric-value">{df["ty_le_dv"].mean():.1f}%</div></div>', unsafe_allow_html=True)
                        with m6: st.markdown(f'<div class="metric-box"><div class="metric-label">🎯 NV Trọng tâm đã Hoàn thành</div><div class="metric-value">{int(df["nv_hoan_thanh"].sum())}</div></div>', unsafe_allow_html=True)
                        
                        st.write("---")
                        
                        # --- BIỂU ĐỒ ---
                        c_chart1, c_chart2 = st.columns(2)
                        with c_chart1:
                            st.markdown("#### 📱 Lượt chia sẻ Tuyên truyền trên MXH")
                            df_mxh = df.groupby("don_vi")["chia_se_mxh"].sum().reset_index()
                            st.bar_chart(df_mxh.set_index("don_vi"))
                            
                        with c_chart2:
                            st.markdown("#### 🎯 Tỷ lệ giải quyết Nhiệm vụ trọng tâm")
                            # Gom nhóm dữ liệu
                            tong_giao = df["nv_giao"].sum()
                            tong_xong = df["nv_hoan_thanh"].sum()
                            df_nv = pd.DataFrame({
                                "Trạng thái": ["Đã hoàn thành", "Đang/Chưa thực hiện"],
                                "Số lượng": [tong_xong, max(0, tong_giao - tong_xong)]
                            })
                            st.bar_chart(df_nv.set_index("Trạng thái"))

                        st.write("---")
                        st.markdown("#### 📑 Danh sách Đơn vị nộp báo cáo")
                        st.dataframe(df[['created_at', 'don_vi', 'ky_bao_cao']].rename(columns={'created_at': 'Thời gian nộp', 'don_vi': 'Tên Đơn vị', 'ky_bao_cao': 'Kỳ'}))
                else:
                    st.info("Chưa có dữ liệu báo cáo nào trong hệ thống.")
            except Exception as e:
                st.error(f"Lỗi tải dữ liệu: {e}")
