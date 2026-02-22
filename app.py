import streamlit as st
import pandas as pd

# 1. 页面基础配置
st.set_page_config(page_title="业财沙盘V2.0", layout="wide")

st.title("🚀 业财融合综合诊断平台")
st.markdown("---")

# 2. 定义核心导航标签页
tab1, tab2 = st.tabs(["🏭 车间底稿扫描", "🌐 多准则转换器"])

# --- 模块一：逻辑开始（注意下方的缩进） ---
with tab1:
    st.header("模块一：车间成本异常扫描")
    
    col_l, col_r = st.columns([1, 2])
    
    with col_l:
        st.write("### 📥 第一步：上传数据")
        uploaded_file = st.file_uploader("上传您的 Excel 或 CSV 底稿", type=['csv', 'xlsx'])
        
        # 备选测试数据
        st.markdown("---")
        test_data = pd.DataFrame({
            '物料代码': ['RM-高筋面粉', 'RM-白糖', 'RM-纸盒'],
            '标准单价': [10.0, 8.0, 2.0],
            '实际采购单价': [10.5, 7.8, 2.0],
            '标准总用量': [2000, 500, 1000],
            '实际领用数量': [2150, 490, 1080]
        })
        csv = test_data.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 下载测试模板", data=csv, file_name='test.csv')

    with col_r:
        st.write("### 🚨 第二步：自动诊断报告")
        if uploaded_file:
            # 读取并计算
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            df['材料价差'] = (df['实际采购单价'] - df['标准单价']) * df['实际领用数量']
            df['材料量差'] = (df['实际领用数量'] - df['标准总用量']) * df['标准单价']
            df['总差异'] = df['材料价差'] + df['材料量差']
            
            # 渲染表格
            st.dataframe(df.style.highlight_max(axis=0, color='lightpink'), use_container_width=True)
            st.success("✅ 诊断完成：请查看上方差异明细。")
        else:
            st.info("👈 请在左侧上传底稿或使用测试模板。")

# --- 模块二：逻辑开始（同样注意缩进） ---
with tab2:
    st.header("模块二：Multi-GAAP 研发转换引擎")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.write("### 🕹️ 业务情景模拟")
        rd_val = st.slider("本期研发投入金额 (万元)", 0, 1000, 200)
        is_cap = st.toggle("业务部门确认满足资本化条件？", value=True)
    
    with c2:
        st.write("### 📊 准则调节底稿")
        # 简单的对比逻辑
        gaap_data = {
            "会计准则": ["🇨🇳 CAS (中国)", "🌍 IFRS (国际)", "🇺🇸 US GAAP (美国)"],
            "确认为资产 (万元)": [rd_val if is_cap else 0, rd_val if is_cap else 0, 0],
            "计入损益 (万元)": [0 if is_cap else rd_val, 0 if is_cap else rd_val, rd_val]
        }
        st.table(pd.DataFrame(gaap_data))
        
        if is_cap:
            st.warning(f"⚠️ **利润预警**：US GAAP 视角下当期利润将比 CAS 少 {rd_val} 万元！")
        else:
            st.success("✅ 三套准则处理一致，无利润调节项。")