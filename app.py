import time
import random
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="无人机心跳监测", layout="wide")
st.title("无人机通信心跳监测可视化")

# 初始化数据
if "heartbeat_data" not in st.session_state:
    st.session_state.heartbeat_data = []
if "last_time" not in st.session_state:
    st.session_state.last_time = time.time()

# 模拟心跳
def generate_heartbeat():
    now = time.time()
    seq = len(st.session_state.heartbeat_data) + 1
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # 模拟偶尔掉线
    if random.random() < 0.1:
        return None
    
    st.session_state.heartbeat_data.append({
        "序号": seq,
        "时间": timestamp,
        "状态": "正常"
    })
    st.session_state.last_time = now
    return True

# 检测掉线
def check_disconnect():
    now = time.time()
    if now - st.session_state.last_time > 3:
        return True
    return False

# 主界面
col1, col2 = st.columns(2)
with col1:
    st.subheader("实时心跳状态")
    status_placeholder = st.empty()
with col2:
    st.subheader("掉线报警")
    alert_placeholder = st.empty()

# 图表
st.subheader("心跳时序图")
chart_placeholder = st.empty()

# 循环更新
while True:
    generate_heartbeat()
    is_disconnect = check_disconnect()
    
    # 显示状态
    if is_disconnect:
        status_placeholder.error("⚠️ 心跳丢失！")
        alert_placeholder.error("🚨 无人机通信掉线！3秒未收到心跳！")
    else:
        status_placeholder.success("✅ 心跳正常")
        alert_placeholder.info("📶 连接稳定")
    
    # 画图
    df = pd.DataFrame(st.session_state.heartbeat_data[-50:])
    if not df.empty:
        fig = px.line(df, x="时间", y="序号", title="心跳包序号变化")
        chart_placeholder.plotly_chart(fig, use_container_width=True)
    
    time.sleep(1)
