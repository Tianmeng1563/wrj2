import time
import random
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="无人机心跳监测", layout="wide")
st.title("无人机通信心跳监测可视化")

# 初始化数据
if "data" not in st.session_state:
    st.session_state.data = []
if "last" not in st.session_state:
    st.session_state.last = time.time()

# 生成心跳
def heartbeat():
    t = time.time()
    seq = len(st.session_state.data) + 1
    now = datetime.now().strftime("%H:%M:%S")
    # 模拟偶尔丢包
    if random.random() < 0.1:
        return None
    st.session_state.data.append({"序号": seq, "时间": now, "状态": "正常"})
    st.session_state.last = t
    return True

# 掉线检测
def is_down():
    return time.time() - st.session_state.last > 3

# 按钮控制
col1, col2 = st.columns(2)
with col1:
    if st.button("开始监测"):
        heartbeat()
with col2:
    st.info("每1秒自动刷新")

# 状态显示
down = is_down()
if down:
    st.error("🚨 掉线！3秒未收到心跳包")
else:
    st.success("✅ 心跳正常")

# 表格
st.subheader("最近心跳记录")
df = pd.DataFrame(st.session_state.data[-20:])
st.dataframe(df, use_container_width=True)

# 图表
st.subheader("心跳趋势")
if len(df) > 0:
    st.line_chart(df.set_index("时间")["序号"], use_container_width=True)

# 自动刷新
time.sleep(1)
st.rerun()
