import time
import random
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="无人机心跳监测", layout="wide")
st.title("无人机通信心跳监测可视化")

# 初始化数据（持久化）
if "data" not in st.session_state:
    st.session_state.data = []
if "last" not in st.session_state:
    st.session_state.last = time.time()
if "running" not in st.session_state:
    st.session_state.running = False

# 按钮控制
col1, col2 = st.columns(2)
with col1:
    if st.button("开始监测"):
        st.session_state.running = True
with col2:
    if st.button("停止"):
        st.session_state.running = False

# 核心逻辑：只在运行时生成
if st.session_state.running:
    t = time.time()
    # 模拟偶尔丢包（10%概率）
    if random.random() >= 0.1:
        seq = len(st.session_state.data) + 1
        now = datetime.now().strftime("%H:%M:%S")
        st.session_state.data.append({"序号": seq, "时间": now, "状态": "正常"})
        st.session_state.last = t
    
    # 掉线检测
    is_disconnect = (time.time() - st.session_state.last) > 3
else:
    is_disconnect = False

# UI 显示
if is_disconnect:
    st.error("🚨 掉线！3秒未收到心跳包")
else:
    if st.session_state.running:
        st.success("✅ 心跳正常")
    else:
        st.info("⏸️ 已暂停，点击「开始监测」")

# 表格：显示最后20条
st.subheader("最近心跳记录")
df = pd.DataFrame(st.session_state.data[-20:])
st.dataframe(df, use_container_width=True)

# 图表
st.subheader("心跳趋势")
if len(df) > 0:
    st.line_chart(df.set_index("时间")["序号"], use_container_width=True)

# 自动刷新：不要while True，用rerun更稳
if st.session_state.running:
    time.sleep(1)
    st.rerun()

# 自动刷新
time.sleep(1)
st.rerun()
