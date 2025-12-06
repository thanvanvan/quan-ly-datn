import streamlit as st
import pandas as pd
from datetime import datetime

# Cấu hình trang
st.set_page_config(
    page_title="Kế Hoạch Đồ Án Tốt Nghiệp 2025",
    page_icon="📚",
    layout="wide"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2563eb 0%, #4f46e5 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-overdue {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    .days-critical {
        background-color: #fef2f2;
        color: #dc2626;
    }
    .days-warning {
        background-color: #fff7ed;
        color: #ea580c;
    }
    .days-normal {
        background-color: #fefce8;
        color: #ca8a04;
    }
</style>
""", unsafe_allow_html=True)

# Dữ liệu kế hoạch
def load_data():
    data = {
        'TT': [1, 2, 3, '', '', '', '', 4, 5],
        'Giai đoạn': [
            'Giai đoạn 1',
            'Giai đoạn 2',
            'Giai đoạn 3 (Tổng)',
            'GĐ 3.1 - Khởi động',
            'GĐ 3.2 - Phát triển',
            'GĐ 3.3 - Hoàn thiện',
            'GĐ 3.4 - Duyệt',
            'Giai đoạn 4',
            'Giai đoạn 5'
        ],
        'Nội dung công việc': [
            'Xét đạo đức thực hiện Học phần tốt nghiệp',
            'SV gặp GVHD nhận nhiệm vụ',
            'THỜI GIAN THỰC HIỆN ĐỒ ÁN (chính)',
            'Nghiên cứu lý thuyết & Chốt công nghệ',
            'Thiết kế hệ thống/Mô hình & Thực hiện',
            'Viết báo cáo & Chạy thử nghiệm/Kiểm tra',
            'Xin chữ ký GVHD & Nộp quyển',
            'Chuẩn bị báo vệ Học phần tốt nghiệp',
            'Lễ tốt nghiệp (Dự kiến)'
        ],
        'Bắt đầu': [
            '10-03', '24-03', '31-03', '31-03', '21-04', 
            '26-05', '23-06', '07-07', '16-08'
        ],
        'Kết thúc': [
            '23/03/2025', '30/03/2025', '06/07/2025', '20/04/2025',
            '25/05/2025', '22/06/2025', '06/07/2025', '20/07/2025', '31/08/2025'
        ],
        'Còn lại (ngày)': [258, 251, 153, 230, 195, 167, 153, 139, 97],
        'Ghi chú': [
            'Chờ danh sách chính thức',
            'Chuẩn bị đề cương số bộ để trình bày',
            'Giai đoạn quan trọng nhất',
            'Viết chương 1, 5m tài liệu tham khảo',
            'Viết chương 2 & 3, Code/Vẽ bản vẽ',
            'Hoàn thiện quyển báo cáo, fix lỗi',
            'Ký duyệt đề được báo vệ',
            'Chuẩn bị slide, poster',
            'Nhận bằng'
        ]
    }
    return pd.DataFrame(data)

# Header
st.markdown("""
<div class="main-header">
    <h1>📚 Kế Hoạch Đồ Án Tốt Nghiệp 2025</h1>
    <p>Theo dõi tiến độ từ tháng 3 đến tháng 8/2025</p>
</div>
""", unsafe_allow_html=True)

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📅 Deadline", "03/08/2025")

with col2:
    st.metric("⏱️ Tiến độ", "0%", delta="-100%")

with col3:
    st.metric("📋 Tổng giai đoạn", "5")

with col4:
    st.metric("⚠️ Trạng thái", "Chưa bắt đầu")

st.markdown("---")

# Sidebar - Bộ lọc
st.sidebar.title("🔍 Bộ lọc")
df = load_data()

# Lọc theo giai đoạn
phases = ['Tất cả'] + [f'Giai đoạn {i}' for i in range(1, 6)]
selected_phase = st.sidebar.selectbox("Chọn giai đoạn", phases)

# Lọc theo số ngày còn lại
st.sidebar.subheader("Lọc theo độ ưu tiên")
filter_critical = st.sidebar.checkbox("Rất gấp (>200 ngày)", value=True)
filter_warning = st.sidebar.checkbox("Gấp (150-200 ngày)", value=True)
filter_normal = st.sidebar.checkbox("Bình thường (<150 ngày)", value=True)

# Áp dụng bộ lọc
filtered_df = df.copy()

if selected_phase != 'Tất cả':
    filtered_df = filtered_df[filtered_df['Giai đoạn'].str.contains(selected_phase, na=False)]

# Lọc theo độ ưu tiên
priority_mask = pd.Series([False] * len(filtered_df))
if filter_critical:
    priority_mask |= filtered_df['Còn lại (ngày)'] > 200
if filter_warning:
    priority_mask |= (filtered_df['Còn lại (ngày)'] >= 150) & (filtered_df['Còn lại (ngày)'] <= 200)
if filter_normal:
    priority_mask |= filtered_df['Còn lại (ngày)'] < 150

filtered_df = filtered_df[priority_mask]

# Hiển thị bảng dữ liệu
st.subheader("📊 Chi tiết kế hoạch")

# Tạo cột trạng thái màu sắc
def get_status_badge(days):
    if days > 200:
        return '🔴 Rất gấp'
    elif days >= 150:
        return '🟠 Gấp'
    else:
        return '🟡 Bình thường'

filtered_df['Độ ưu tiên'] = filtered_df['Còn lại (ngày)'].apply(get_status_badge)

# Hiển thị dataframe với style
st.dataframe(
    filtered_df[['Giai đoạn', 'Nội dung công việc', 'Bắt đầu', 'Kết thúc', 'Còn lại (ngày)', 'Độ ưu tiên', 'Ghi chú']],
    use_container_width=True,
    height=500
)

# Thống kê
st.markdown("---")
st.subheader("📈 Thống kê tổng quan")

col1, col2, col3 = st.columns(3)

with col1:
    critical_tasks = len(df[df['Còn lại (ngày)'] > 200])
    st.metric("🔴 Nhiệm vụ rất gấp", f"{critical_tasks}")

with col2:
    warning_tasks = len(df[(df['Còn lại (ngày)'] >= 150) & (df['Còn lại (ngày)'] <= 200)])
    st.metric("🟠 Nhiệm vụ gấp", f"{warning_tasks}")

with col3:
    normal_tasks = len(df[df['Còn lại (ngày)'] < 150])
    st.metric("🟡 Nhiệm vụ bình thường", f"{normal_tasks}")

# Lời khuyên
st.markdown("---")
st.warning("""
⚠️ **Lời khuyên:** Giai đoạn 3 (31/03 - 06/07) kéo dài hơn 3 tháng. Đừng để quá việc! 
Tốt cá là đúng chia nhỏ từ thành hơn 4 giai đoạn con (3.1 đến 3.4) để theo dõi. 
Hãy cố gắng hoàn thành chương 1 và 2 trước tháng 5.
""")

# Timeline chart
st.markdown("---")
st.subheader("📅 Timeline")

import plotly.express as px
import plotly.graph_objects as go

# Tạo dữ liệu cho timeline
timeline_data = []
for idx, row in df.iterrows():
    if row['Bắt đầu'] and row['Kết thúc']:
        timeline_data.append({
            'Task': row['Giai đoạn'],
            'Start': f"2025-{row['Bắt đầu']}" if '-' in row['Bắt đầu'] else row['Bắt đầu'],
            'Finish': row['Kết thúc'],
            'Days': row['Còn lại (ngày)']
        })

# Tạo Gantt chart đơn giản
fig = go.Figure()

colors = ['#ef4444', '#f97316', '#eab308']
for i, item in enumerate(timeline_data):
    color = colors[0] if item['Days'] > 200 else colors[1] if item['Days'] >= 150 else colors[2]
    fig.add_trace(go.Bar(
        y=[item['Task']],
        x=[item['Days']],
        orientation='h',
        name=item['Task'],
        marker=dict(color=color),
        showlegend=False
    ))

fig.update_layout(
    title="Thời gian còn lại cho mỗi giai đoạn (ngày)",
    xaxis_title="Số ngày còn lại",
    yaxis_title="Giai đoạn",
    height=400,
    barmode='stack'
)

st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 2rem;'>
    <p>💡 Cập nhật tiến độ thường xuyên để đảm bảo hoàn thành đúng hạn!</p>
    <p>Chúc bạn thành công với đồ án tốt nghiệp! 🎓</p>
</div>
""", unsafe_allow_html=True)
