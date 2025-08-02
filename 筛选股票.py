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
    """��CSV�ļ�������ȡ��Ʊ����"""
    filename = os.path.basename(csv_file)  # ��ȡ�ļ���
    stock_code = filename.split('.')[0]  # ȥ����չ�����õ���Ʊ����
    return stock_code

def is_unwanted_market(stock_code):
    """����Ʊ�Ƿ����ڲ���Ҫ���г����紴ҵ�塢���������ƴ��壩"""
    if stock_code.startswith('30'):
        return True, '��ҵ��'
    if stock_code.startswith(('43', '83', '87')): # ʹ��Ԫ�������Ч��
        return True, '������'
    if stock_code.startswith('688'):
        return True, '�ƴ���'
    return False, '�����г�'

def is_st_stock(stock_name):
    """����Ʊ�Ƿ�ΪST�����⴦����Ʊ"""
    if pd.isna(stock_name):  # �����ֵ
        return False
    stock_name = str(stock_name).upper()  # ת��Ϊ��д�Ա�Ƚ�
    st_keywords = ['ST', '*ST', 'S*ST', 'SST', '����', '*', 'S']
    for keyword in st_keywords:
        if keyword in stock_name:
            return True
    return False

# ��ȡָ��Ŀ¼�����е�CSV�ļ��б�
csv_files = glob.glob(r'C:\Users\35078\Desktop\5000��Ʊ����\*.csv')

# ��ʼ�����ڴ洢���˺��Ʊ�ͼ����ı���
filter_stocks = []
count = 0
# ����ɸѡ����������Ϳ��ܵĹ�Ʊ��������
require_columns = ['����ֵ(Ԫ)', '���̼�', '������(%)']
possible_name_columns = ['��Ʊ����', '����', '֤ȯ����', 'name']

# ��������CSV�ļ����д���
for csv_file in csv_files:
     try:
        # ��ȡ��Ʊ���벢����Ƿ����ڲ���Ҫ���г�
        stock_code = get_stock_code(csv_file)
        is_unwanted, market_type = is_unwanted_market(stock_code)

        # ����Ǵ�ҵ�塢�ƴ���ȣ�������
        if is_unwanted:
            continue

        # ��ȡCSV�ļ���DataFrame
        df = pd.read_csv(csv_file)
        # ����Ƿ�������б�����У���������
        if not all(col in df.columns for col in require_columns):
            print(f'�ļ� {csv_file} ȱ�ٱ����У�������')
            continue

        # ���ҹ�Ʊ�������ڵ���
        name_column = None
        for col in possible_name_columns:
            if col in df.columns:
                name_column = col
                break
            
        # ����ҵ��˹�Ʊ�����У������Ƿ�ΪST��Ʊ������
        if name_column:
            lastest_data = df.iloc[0] if not df.empty else None
            if lastest_data is not None:
                stock_name = lastest_data[name_column]
                if is_st_stock(stock_name):
                    continue

        # ������ֵ�����̼ۺͻ�����ɸѡ����
        count_df = df[
                ((df['����ֵ(Ԫ)'] > 100000000) & (df['����ֵ(Ԫ)'] < 10000000000)) &
                ((df['���̼�'] < 50) & (df['���̼�'] > 1)) &
                (df['������(%)'] > 0.5)
        ]

        # ���ɸѡ�������ݣ����������һ
        if not count_df.empty:
            count += 1
        
        # ����count_df�Ա��´�ѭ��ʹ�ã�ע�⣺����ԭΪ count_df = []�����ܲ���Ԥ����Ϊ��
        count_df = pd.DataFrame() # ʹ�ÿյ�DataFrame����ȫ
     except Exception as e:
         print(f'�����ļ� {csv_file} ʱ��������: {e}')

# ע�⣺����Ĵ�ӡ���ʹ�õ���ѭ�������һ��df�����ܲ���Ԥ�ڽ��
print(f"�����һ��������ļ����ҵ��� {len(df)} �����ݡ�")
print(f"�ܹ��� {count} ���ļ��������������Ĺ�Ʊ��")
'''
def small_cap_stocks(df):
    """һ��������ֵ���۸�ͻ�����ɸѡС�̹ɵĺ���"""
    return df[
             ((df['����ֵ(Ԫ)'] > 100000000) & (df['����ֵ(Ԫ)'] < 10000000000)) &
                ((df['���̼�'] < 50) & (df['���̼�'] > 1)) &
                (df['������(%)'] > 0.5)
    ]
 '''
# �����һ�������df�������򣬵����δ����
df.sort_values(['����ֵ(Ԫ)', '���̼�'], ascending=[True, True])
# �����һ�������df�������򣬲���ȡ��ֵ�ͼ۸���͵�ǰ20ֻ��Ʊ
top_20 = df.sort_values(['����ֵ(Ԫ)', '���̼�'], ascending=[True, True]).head(20)
print("���һ�������ļ��е�Top 20��Ʊ:")
print(top_20)


'demo'

