import pandas as pd

df = pd.read_csv(r"C:\Users\35078\Desktop\BTCUSDT_5m_20200411_to_20250411.csv")
#print(df.columns)
#print(df.head())

df = df[
    (df['close'] > 90000.00) & (df['close'] < 100000.00) &
    (df['open'] > 90000.00) & (df['open'] < 100000.00)
]
#print(df)

import os
import glob

def get_stock_code(csv_file):
    """从CSV文件名中提取股票代码"""
    filename = os.path.basename(csv_file)  # 获取文件名
    stock_code = filename.split('.')[0]  # 去除扩展名，得到股票代码
    return stock_code

def is_unwanted_market(stock_code):
    """检查股票是否属于不需要的市场（如创业板、北交所、科创板）"""
    if stock_code.startswith('30'):
        return True, '创业板'
    if stock_code.startswith(('43', '83', '87')): # 使用元组以提高效率
        return True, '北交所'
    if stock_code.startswith('688'):
        return True, '科创板'
    return False, '正常市场'

def is_st_stock(stock_name):
    """检查股票是否为ST（特殊处理）股票"""
    if pd.isna(stock_name):  # 处理空值
        return False
    stock_name = str(stock_name).upper()  # 转换为大写以便比较
    st_keywords = ['ST', '*ST', 'S*ST', 'SST', '退市', '*', 'S']
    for keyword in st_keywords:
        if keyword in stock_name:
            return True
    return False

# 获取指定目录下所有的CSV文件列表
csv_files = glob.glob(r'C:\Users\35078\Desktop\5000股票数据\*.csv')

# 初始化用于存储过滤后股票和计数的变量
filter_stocks = []
count = 0
# 定义筛选所需的列名和可能的股票名称列名
require_columns = ['总市值(元)', '收盘价', '换手率(%)']
possible_name_columns = ['股票名称', '名称', '证券名称', 'name']

# 遍历所有CSV文件进行处理
for csv_file in csv_files:
     try:
        # 获取股票代码并检查是否属于不需要的市场
        stock_code = get_stock_code(csv_file)
        is_unwanted, market_type = is_unwanted_market(stock_code)

        # 如果是创业板、科创板等，则跳过
        if is_unwanted:
            continue

        # 读取CSV文件到DataFrame
        df = pd.read_csv(csv_file)
        # 检查是否包含所有必需的列，否则跳过
        if not all(col in df.columns for col in require_columns):
            print(f'文件 {csv_file} 缺少必需列，已跳过')
            continue

        # 查找股票名称所在的列
        name_column = None
        for col in possible_name_columns:
            if col in df.columns:
                name_column = col
                break
            
        # 如果找到了股票名称列，则检查是否为ST股票并跳过
        if name_column:
            lastest_data = df.iloc[0] if not df.empty else None
            if lastest_data is not None:
                stock_name = lastest_data[name_column]
                if is_st_stock(stock_name):
                    continue

        # 根据市值、收盘价和换手率筛选数据
        count_df = df[
                ((df['总市值(元)'] > 100000000) & (df['总市值(元)'] < 10000000000)) &
                ((df['收盘价'] < 50) & (df['收盘价'] > 1)) &
                (df['换手率(%)'] > 0.5)
        ]

        # 如果筛选后有数据，则计数器加一
        if not count_df.empty:
            count += 1
        
        # 重置count_df以备下次循环使用（注意：此行原为 count_df = []，可能不是预期行为）
        count_df = pd.DataFrame() # 使用空的DataFrame更安全
     except Exception as e:
         print(f'处理文件 {csv_file} 时发生错误: {e}')

# 注意：下面的打印语句使用的是循环中最后一个df，可能不是预期结果
print(f"在最后一个处理的文件中找到了 {len(df)} 条数据。")
print(f"总共有 {count} 个文件包含符合条件的股票。")
'''
def small_cap_stocks(df):
    """一个根据市值、价格和换手率筛选小盘股的函数"""
    return df[
             ((df['总市值(元)'] > 100000000) & (df['总市值(元)'] < 10000000000)) &
                ((df['收盘价'] < 50) & (df['收盘价'] > 1)) &
                (df['换手率(%)'] > 0.5)
    ]
 '''
# 对最后一个处理的df进行排序，但结果未保存
df.sort_values(['总市值(元)', '收盘价'], ascending=[True, True])
# 对最后一个处理的df进行排序，并获取市值和价格最低的前20只股票
top_20 = df.sort_values(['总市值(元)', '收盘价'], ascending=[True, True]).head(20)
print("最后一个处理文件中的Top 20股票:")
print(top_20)


'demo'

