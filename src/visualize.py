import streamlit as st
import pandas as pd
import altair as alt
import json

def main():
    st.title("热词统计与分析系统 - 查询历史回溯")
    st.markdown("通过滑动下方滑块，查看不同查询时刻的 Top-K 热词分布。")

    # 加载数据
    try:
        with open("data/results.json", "r", encoding="utf-8") as f:
            snapshots = json.load(f) 
    except FileNotFoundError:
        st.error("找不到 topK 查询结果文件 (data/results.json)，请先运行 python main.py 生成数据。")
        st.stop()

    if not snapshots:
        st.warning("暂无查询记录")
        return

    total_snapshots = len(snapshots)
    
    # 判断快照数量，决定是否显示滑块
    if total_snapshots > 1:
        # 如果有多条记录，显示滑块
        # slider 返回的是 1, 2, 3... 需要减 1 变成索引 0, 1, 2...
        selected_index = st.slider("选择第几个查询时刻 (Query Index)", 1, total_snapshots, 1)
        page_index = selected_index - 1
    else:
        # 如果只有 1 条记录，直接设为 0，并提示用户
        st.info("当前仅有一条查询记录。")
        page_index = 0
    
    # 获取当前选中的快照数据
    current_snapshot = snapshots[page_index]
    
    # 显示当前时刻的信息
    st.subheader(f"⏱️ 查询时间: {current_snapshot['time']}")
    st.caption(f"当前查询参数: Top-{current_snapshot['k']}")

    # 准备画图数据
    data = current_snapshot['data']
    k = current_snapshot['k']
    
    # 排序逻辑：频次降序，单词字典序升序
    sorted_data = sorted(data.items(), key=lambda x: (-x[1], x[0]))
    
    # 截取 Top K
    sorted_data = sorted_data[:k]
    
    if not sorted_data:
        st.info("当前时间窗口内无热词")
    else:
        df = pd.DataFrame(sorted_data, columns=["Word", "Frequency"])
        
        # 使用 Altair 实现多彩柱状图且强制排序
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Word', sort=None, axis=alt.Axis(labelAngle=0)), 
            y='Frequency',
            color=alt.Color('Word', legend=None), # 隐藏图例让图表更清爽
            tooltip=['Word', 'Frequency']
        ).properties(
            height=400 
        )
        
        # 添加柱子上的数字标签
        text = chart.mark_text(
            align='center',
            baseline='bottom',
            dy=-5 
        ).encode(
            text='Frequency'
        )
        
        # 最终渲染
        st.altair_chart(chart + text, use_container_width=True)

    # 显示原始数据表格
    with st.expander("查看详细数据表"):
        st.table(df)

if __name__ == "__main__":
    main()