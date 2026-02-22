import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 网页全局配置
st.set_page_config(page_title="财务数智化沙盘 V2.2", layout="wide", page_icon="📊")

# 2. 侧边栏设置 (Logo与系统状态)
with st.sidebar:
    st.markdown("## 🛡️ 财务专家系统")
    # 放置 Logo 图片
    st.image("https://cdn-icons-png.flaticon.com/512/10061/10061734.png", width=100)
    st.markdown("---")
    st.caption("🚀 核心引擎状态")
    st.success("仪表盘模块：已激活")
    st.success("GAAP映射库：已就绪")
    st.markdown("---")
    st.write("**版本：** V2.2 (仪表盘强化版)")
    st.write("**开发者：** 财务专家数字化工作室")

# 3. 主页面头部
st.title("🛡️ 专家级业财与准则转换沙盘")
st.markdown("*深度穿透业务底层，动态映射全球准则*")
st.divider()

# 4. 导航标签页切换
tab1, tab2, tab3 = st.tabs(["📊 业务诊断仪表盘", "🌐 GAAP 转换引擎", "📈 收入确认判定"])

# ==========================================
# 模块一：自动化诊断仪表盘
# ==========================================
with tab1:
    st.subheader("🏭 车间成本实时监控看板")
    
    # 文件上传逻辑
    uploaded_file = st.file_uploader("上传业务底稿 (.csv/.xlsx)", type=['csv', 'xlsx'])
    
    # 默认演示数据逻辑
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"文件读取错误: {e}")
            st.stop()
    else:
        # 演示用的脱敏数据
        df = pd.DataFrame({
            '物料': ['面粉', '白糖', '包装', '油脂', '酵母'],
            '标准价': [10.0, 8.0, 2.0, 15.0, 5.0],
            '实际价': [10.5, 7.8, 2.0, 18.0, 4.8],
            '标准量': [2000, 500, 1000, 300, 100],
            '实际量': [2150, 490, 1080, 320, 105]
        })

    # 核心财务差异计算
    df['价差'] = (df['实际价'] - df['标准价']) * df['实际量']
    df['量差'] = (df['实际量'] - df['标准量']) * df['标准价']
    df['总差异'] = df['价差'] + df['量差']
    df['差异率%'] = (df['总差异'] / (df['标准价'] * df['标准量']) * 100).round(2)

    # --- 仪表盘视觉区 ---
    # 第一行：KPI 指标卡
    m1, m2, m3, m4 = st.columns(4)
    total_diff = df['总差异'].sum()
    budget_total = (df['标准价'] * df['标准量']).sum()
    
    m1.metric("总偏差金额", f"¥{total_diff:,.2f}", delta=f"{(total_diff/budget_total)*100:.2f}%", delta_color="inverse")
    m2.metric("最大风险项", df.loc[df['总差异'].abs().idxmax(), '物料'])
    m3.metric("受控项目数", len(df[df['差异率%'].abs() <= 5]))
    m4.metric("高风险报警", len(df[df['差异率%'].abs() > 5]), delta_color="normal")

    st.divider()

    # 第二行：图表展示
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.write("**📊 物料量价差异分析 (量差 vs 价差)**")
        plot_df = df.melt(id_vars='物料', value_vars=['价差', '量差'], var_name='差异类型', value_name='金额')
        fig = px.bar(plot_df, x='物料', y='金额', color='差异类型', barmode='group',
                     color_discrete_map={'价差': '#FFA07A', '量差': '#20B2AA'}, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.write("**⚖️ 内控合规分布**")
        df['合规性'] = df['差异率%'].abs().apply(lambda x: '正常' if x<=5 else '异常')
        fig_pie = px.pie(df, names='合规性', hole=0.4, 
                         color='合规性', color_discrete_map={'正常': '#2ECC71', '异常': '#E74C3C'})
        fig_pie.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)

    # 第三行：明细表
    with st.expander("🔍 点击展开详细差异调节明细表"):
        st.dataframe(df.style.background_gradient(subset=['差异率%'], cmap='RdYlGn_r'), use_container_width=True)

# ==========================================
# 模块二：GAAP 转换引擎
# ==========================================
with tab2:
    st.subheader("研发支出：跨国准则转换测算")
    c1, c2 = st.columns([1, 2])
    with c1:
        st.write("### 🕹️ 业务情景模拟")
        rd_val = st.slider("当期研发投入总额 (万元)", 0, 1000, 300)
        is_cap = st.toggle("是否满足资本化条件？", value=True)
    with c2:
        st.write("### 📊 准则调节底稿")
        gaap_data = {
            "会计准则": ["🇨🇳 CAS / 🌍 IFRS", "🇺🇸 US GAAP"],
            "确认为资产 (万元)": [rd_val if is_cap else 0, 0],
            "计入损益 (万元)": [0 if is_cap else rd_val, rd_val]
        }
        st.table(pd.DataFrame(gaap_data))
        if is_cap:
            st.warning(f"⚠️ **利润提醒**：US GAAP 下利润将比 CAS 少 {rd_val} 万元。")

# ==========================================
# 模块三：收入确认判定
# ==========================================
with tab3:
    st.subheader("新收入准则：五步法判定模拟")
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.info("🎯 **五步法判定路径**")
        s1 = st.checkbox("1. 识别客户合同", value=True)
        s2 = st.checkbox("2. 识别单项履约义务", value=True)
        price = st.number_input("3. 确定交易价格 (万元)", value=500.0)
        ratio = st.slider("4. 价格分摊比例 (%)", 0, 100, 100)
        timing = st.radio("5. 履行时间点判断", ["某一时点履行", "某一时段内履行"])
    with col_b:
        st.success("📝 **财务处理建议**")
        if s1 and s2:
            amt = price * (ratio/100)
            st.markdown(f"**建议确认收入金额：** `{amt}` 万元")
            st.markdown(f"**确认时点：** {'控制权转移时点' if timing == '某一时点履行' else '按进度确认'}")
        else:
            st.error("不符合确认条件。")