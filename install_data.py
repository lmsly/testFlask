import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:654321@192.168.170.70:3306/flasktest?charset=utf8', convert_unicode=True)
lisdata = []
i = 1
lisurl = ["医院送检项目明细表", "医院送检项目明细表 (1)", "医院送检项目明细表 (2)", "医院送检项目明细表 (3)", "医院送检项目明细表 (4)", "医院送检项目明细表 (5)",
          "医院送检项目明细表 (6)", "医院送检项目明细表 (7)", "医院送检项目明细表 (8)", "医院送检项目明细表 (9)", "医院送检项目明细表 (10)", "医院送检项目明细表 (11)"]
# lisurl = ["医院送检项目明细表"]

for url in lisurl:
    data = pd.DataFrame(pd.read_excel('F:/111111/' + str(url) + '.xlsx', skiprows=1,header = 0,names=['id','region','small_area','hospname','marketing_package','department','doctor','number','standard_price','not_price','ture_price','actual_price'] ))
    data['month']=i
    print(data['month'])
    # pd.io.sql.to_sql(data, 'month_' + str(i) + '', con=engine, index=False, if_exists='replace')
    pd.io.sql.to_sql(data, 'month_1', con=engine, index=False, if_exists='append')
    i = i + 1