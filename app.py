import streamlit as st
import pandas as pd

# 1. 页面基础配置
st.set_page_config(page_title="财务数字化沙盘 | 专家版", layout="wide", page_icon="⚖️")

# --- 修复版 Logo 放置方式 ---
# 我们在侧边栏最上方放一个图标和一行字，这在所有版本里都能显示
with st.sidebar:
    st.markdown("### 🛡️ 财务专家系统")
    st.image("https://cdn-icons-png.flaticon.com/512/2611/2611152.png", width=100)
    st.markdown("---")
    st.write("版本：V2.1 (专家定制版)")
    st.write("状态：公网运行中 🌐")

# 2. 顶部大标题
st.title("🛡️ 专家级业财与准则转换沙盘")
st.markdown("*深度穿透业务底层，动态映射全球准则*")
st.divider()

# 2. 定义导航标签页：增加“收入确认”模块
tab1, tab2, tab3 = st.tabs([
    "🏭 车间底稿扫描 (业财融合)", 
    "🌐 Multi-GAAP 转换 (研发支出)", 
    "📈 收入确认五步法 (IFRS15/CAS14)"
])

# --- 模块一：车间成本风控 ---
with tab1:
    st.subheader("车间领料单异常智能扫描")
    col_l, col_r = st.columns([1, 2])
    with col_l:
        st.write("### 📥 数据上传")
        uploaded_file = st.file_uploader("上传您的 CSV/Excel 业务底稿", type=['csv', 'xlsx'])
        # 测试数据模板
        test_data = pd.DataFrame({
            '物料': ['RM-高筋面粉', 'RM-白糖', 'RM-纸盒'],
            '标准价': [10.0, 8.0, 2.0], '实际价': [10.5, 7.8, 2.0],
            '标准量': [2000, 500, 1000], '实际量': [2150, 490, 1080]
        })
        st.download_button("📥 获取测试模板", data=test_data.to_csv(index=False).encode('utf-8-sig'), file_name='test_template.csv')

    with col_r:
        st.write("### 🚨 审计诊断结果")
        if uploaded_file:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            df['总差异'] = ((df['实际价']-df['标准价'])*df['实际量']) + ((df['实际量']-df['标准量'])*df['标准价'])
            def judge(row): return '🔴 风险' if abs(row['总差异']) > (row['标准价']*row['标准量']*0.05) else '🟢 正常'
            df['风控状态'] = df.apply(judge, axis=1)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("👈 等待接收底稿数据...")

# --- 模块二：研发支出转换 ---
with tab2:
    st.subheader("研发支出：CAS / IFRS / US GAAP 差异测算")
    c1, c2 = st.columns([1, 2])
    with c1:
        rd_amount = st.slider("当期研发总支出 (万元)", 0, 1000, 200)
        is_cap = st.toggle("确认满足资产化条件", value=True)
    with c2:
        gaap_df = pd.DataFrame({
            "准则": ["🇨🇳 CAS / 🌍 IFRS", "🇺🇸 US GAAP"],
            "资本化金额": [rd_amount if is_cap else 0, 0],
            "费用化金额": [0 if is_cap else rd_amount, rd_amount]
        })
        st.table(gaap_df)
        if is_cap: st.warning(f"💡 决策提示：US GAAP 下利润将因全额费用化而比 CAS 减少 {rd_amount} 万元。")

# --- 模块三：收入确认 (新增) ---
with tab3:
    st.subheader("新收入准则：五步法模型动态判定")
    st.markdown("> **核心逻辑：** 模拟 IFRS 15 与 CAS 14 趋同后的收入确认路径。")
    
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.info("🎯 **五步法判定模拟**")
        step1 = st.checkbox("1. 识别客户合同 (具备商业实质)", value=True)
        step2 = st.checkbox("2. 识别单项履约义务 (多重交付项目需拆分)", value=True)
        step3 = st.number_input("3. 确定交易价格 (不含税/考虑可变对价)", value=100.0)
        step4 = st.slider("4. 分摊交易价格至各单项履约义务 (%)", 0, 100, 100)
        step5 = st.radio("5. 履行时间点判断", ["某一时点履行", "某一时段内履行"])

    with col_b:
        st.success("📝 **财务核算建议**")
        if step1 and step2:
            recognize_amount = step3 * (step4/100)
            if step5 == "某一时点履行":
                st.write(f"建议：确认收入 **{recognize_amount}** 万元（控制权转移时）。")
            else:
                st.write(f"建议：按完工百分比/履约进度在时段内确认收入。")
            st.caption("注：IFRS 15 与新 CAS 14 已高度趋同，此处模拟主流会计处理建议。")
        else:
            st.error("合同或履约义务未明确，暂不符合收入确认条件。")