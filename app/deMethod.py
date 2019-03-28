from pyecharts import Line,Pie,Page

class tool:
    def getShowData(dataframe, start_x, stop_y, start_month, stop_month):
        page=Page()
        line = Line("折线图示例", width=1200, height=500)
        for p in range(int(start_month), int(stop_month) + 1):
            Single_month = dataframe.loc[dataframe['month'] == p]
            data = Single_month.groupby(start_x)[stop_y].sum().reset_index()
            line.add(str(p) + "月份", data[start_x], data[stop_y], xaxis_rotate=30,xaxis_label_textsize =12,is_toolbox_show =False)
        page.add_chart(line)


        data = dataframe.groupby(start_x)[stop_y].sum().reset_index()
        pie = Pie("饼图示例", width=1200, height=500,title_pos="center",extra_html_text_label=["BAR TEXT LABEL"])
        pie.add("",data[start_x], data[stop_y],is_label_show=True,legend_orient="vertical",legend_pos="left")
        page.add_chart(pie)
        page.render(r'show.html')
        htmlf = open('show.html', 'r', encoding="utf-8")
        htmlcont = htmlf.read()
        return htmlcont