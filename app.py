import streamlit as st
import pandas as pd

# ==========================================
# 1. 网页全局设置与标题
# ==========================================
st.set_page_config(page_title="专家级业财沙盘", layout="wide")
st.title("🏭 业财融合实战沙盘：米制品出口订单的“生死报价”")
st.markdown("""
**真实案例复盘**：欧洲客户急单，目标报价极限压低。
生产厂长按传统经验估算，坚称接单必亏；财务总监亲自下车间，连出三刀，从流水线里“抠”出隐藏利润，最终提前一天交货并实现盈利。
**👉 请在左侧调整“老法师的手术刀”参数，见证利润的奇迹！**
""")
st.divider()

# ==========================================
# 2. 核心假设数据（生产部门的原始“保守”底稿）
# ==========================================
# 假设这批订单欧洲客户的死命令报价是：100,000 元
BID_PRICE = 100000 

# 生产部门提交的原始成本核算
base_material_cost = 45000  # 原材料成本（未考虑边料回收）
base_energy_cost = 30000    # 烘干能耗等制造费用（传送带低速空转）
base_labor_cost = 35000     # 人工成本（包含搬运窝工时间）
base_total_cost = base_material_cost + base_energy_cost + base_labor_cost
base_profit = BID_PRICE - base_total_cost

# ==========================================
# 3. 侧边栏：专家诊断参数输入 (动态沙盘)
# ==========================================
st.sidebar.header("🔧 总监的车间优化指令")
st.sidebar.write("拖动滑块，模拟您在车间现场下达的整改效果：")

# 优化一：水切工序边料回收
opt_material_rate = st.sidebar.slider("1. 水切边料回收利用率 (%)", min_value=0, max_value=15, value=0, step=1)
# 优化二：低温烘干提速节约能耗
opt_energy_rate = st.sidebar.slider("2. 烘干传送带提速/能耗节约率 (%)", min_value=0, max_value=25, value=0, step=1)
# 优化三：动线优化节约无效搬运工时
opt_labor_saved = st.sidebar.slider("3. 动线优化节约无效人工 (元)", min_value=0, max_value=10000, value=0, step=500)

# ==========================================
# 4. L2层核心引擎：动态成本与利润重算
# ==========================================
# 根据拖拽的参数，实时重新计算实际成本
actual_material = base_material_cost * (1 - opt_material_rate / 100)
actual_energy = base_energy_cost * (1 - opt_energy_rate / 100)
actual_labor = base_labor_cost - opt_labor_saved

actual_total_cost = actual_material + actual_energy + actual_labor
actual_profit = BID_PRICE - actual_total_cost

# ==========================================
# 5. L3层前端展示：高管级数据看板
# ==========================================
col1, col2, col3 = st.columns(3)

# 顶部核心指标卡片
with col1:
    st.metric(label="💶 欧洲客户极限报价", value=f"¥{BID_PRICE:,}")
with col2:
    st.metric(label="📉 厂长原始预估利润 (未优化前)", value=f"¥{base_profit:,}", delta="厂长拒签！", delta_color="inverse")
with col3:
    # 动态利润显示
    delta_text = "成功扭亏为盈！" if actual_profit > 0 else "依然亏损，需继续优化车间"
    st.metric(label="📈 总监优化后实际利润", value=f"¥{int(actual_profit):,}", delta=delta_text)

st.subheader("📊 业财穿透对比底稿 (生产经验 vs 财务精益)")

# 构造对比表格
compare_data = {
    '成本项目': ['直接材料 (料)', '制造费用 (费)', '直接人工 (人)', '总成本'],
    '厂长原始账面成本': [base_material_cost, base_energy_cost, base_labor_cost, base_total_cost],
    '您的精益测算成本': [int(actual_material), int(actual_energy), int(actual_labor), int(actual_total_cost)],
    '诊断问题节点': ['水切边料直接废弃', '烘干线低速致能耗空转', '中场到包装线无效搬运', '-']
}
df_compare = pd.DataFrame(compare_data)

# 突出显示成本下降
st.dataframe(df_compare, use_container_width=True)

# 底部风控自动诊断结论
if actual_profit > 0:
    st.success(f"🎉 **战报总结**：通过现场精益改善，成功从车间缝隙中抠出 **{int(actual_profit - base_profit):,} 元** 的隐藏利润！不但满足了客户低价要求，还提前1天交货。这就是业财融合的威力。")
else:
    st.error("⚠️ **系统警告**：目前的优化力度还不够，接单存在实质性亏损风险。请继续在左侧加大车间整改力度（例如提高边料回收率）。")