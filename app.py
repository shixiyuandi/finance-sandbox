import streamlit as st
import pandas as pd

# ==========================================
# 1. 网页全局设置与标题
# ==========================================
st.set_page_config(page_title="专家级业财沙盘 - 数据诊断版", layout="wide")
st.title("📂 自动化财务诊断：车间领料单异常扫描")
st.markdown("上传车间实际领用底稿，系统将自动核对标准成本，并按您的 **5%容忍度** 亮起内控红绿灯。")
st.divider()

# ==========================================
# 2. 侧边栏：上传业务底稿
# ==========================================
st.sidebar.header("📥 第一步：上传业务底稿")
st.sidebar.markdown("**请确保您的表格包含以下列名：**\n* 物料代码\n* 标准单价\n* 实际采购单价\n* 标准总用量\n* 实际领用数量")

# 文件上传组件
uploaded_file = st.sidebar.file_uploader("上传表格文件 (.csv 或 .xlsx)", type=['csv', 'xlsx'])

# ==========================================
# 3. 核心引擎：接收数据并执行诊断
# ==========================================
if uploaded_file is not None:
    try:
        # 读取上传的文件
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("📋 步骤一：读取原始业务底稿")
        st.dataframe(df, use_container_width=True)

        # 剥离量价差
        df['材料价差'] = (df['实际采购单价'] - df['标准单价']) * df['实际领用数量']
        df['材料量差'] = (df['实际领用数量'] - df['标准总用量']) * df['标准单价']
        df['总差异'] = df['材料价差'] + df['材料量差']

        # 内控合规熔断逻辑 (5%红线)
        def get_status(row):
            limit = row['标准单价'] * row['标准总用量'] * 0.05
            if abs(row['总差异']) > limit:
                return '🔴 异常需审计'
            return '🟢 正常'

        df['内控状态'] = df.apply(get_status, axis=1)

        st.divider()
        st.subheader("🚨 步骤二：自动化内控诊断报告")
        
        st.dataframe(df, use_container_width=True)

        # 专家级诊断结论输出
        abnormal_items = df[df['内控状态'] == '🔴 异常需审计']
        if not abnormal_items.empty:
            st.error(f"⚠️ **系统高级预警**：发现 {len(abnormal_items)} 项物料成本击穿 5% 容忍底线！")
            for index, row in abnormal_items.iterrows():
                st.warning(f"**诊断追踪 - {row['物料代码']}**：产生总差异 {row['总差异']} 元。需立即启动专项内审程序！")
        else:
            st.success("✅ **系统诊断**：各项波动均在标准容忍度内，未触发红线风险。")

    except Exception as e:
        st.error(f"解析文件出错，请检查表格格式。报错信息：{e}")

else:
    st.info("👈 请在左侧栏上传您的业务底稿 (.csv 或 .xlsx)。")
    st.markdown("---")
    st.markdown("💡 **没有现成的数据？** 点击下方按钮下载一份测试模板：")
    
    # 生成测试数据供下载
    test_data = pd.DataFrame({
        '物料代码': ['RM-高筋面粉', 'RM-进口白糖', 'RM-包装纸盒'],
        '标准单价': [10.0, 8.0, 2.0],
        '实际采购单价': [10.5, 7.8, 2.0],
        '标准总用量': [2000, 500, 1000],
        '实际领用数量': [2150, 490, 1080]
    })
    csv = test_data.to_csv(index=False).encode('utf-8-sig')
    st.download_button(label="📥 下载测试底稿", data=csv, file_name='test_data.csv', mime='text/csv')