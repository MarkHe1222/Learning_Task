
import pandas as pd
import csv,time

def calculate_data(List, count):
    data_min, data_max, data_sum= min(List), max(List), sum(List)
    data_avg = data_sum / float(count)
    return data_min, data_max, data_avg

if __name__ == '__main__':
    start = time.clock()
    df = pd.read_csv ('colla.csv', encoding = "ISO-8859-1")
    with open('Test_file.csv', mode = 'w', newline = '') as wf:
	headers = ['degree', 'col_min', 'col_max', 'col_avg', 'coa_min', 'coa_max', 'coa_avg', 'count' ]
	writer = csv.writer(wf)#开始写
	writer.writerow(headers)#写入列名
	df1, df2 = max(df.degree1), max(df.degree2)#分别求出，指定列的最大值，这样才能知道后面索要遍历的范围
	for i in range(df1 + 1):#因为range的范围df1本事是遍历不到的，所以要+1
	    for j in range(df2 + 1):#同上
		row_nums = df[(df.degree1 == i) & (df.degree2 == j)]
#		1：&在python中本来是按位与的意思，打死我都不知道有这个事情，之前使用and的时候，一直报错；
#		2：（df.degree1 == i）& （df.degree2 == j）判断出存在这个组合，就为true，而df[true]的话，就输出所有符合组合的整行
#		3：row_nums相当于新的一个由符合前面组合的 DataFrame， 
		nums, col_time, coa_num =(i, j), row_nums['colla_time'], row_nums['coarticle_num']#nums最为组合的列名输出，之后是取出符合条件的列元素
		count = len(col_time)#列元素有几个，说明就有几个是相同组合
		if count == 0:#因为在这个组合中，还有很多不能存在的，当然组合长度为0
		    continue#不存在，跳出本次循环，进行下一次的判断
		col_min, col_max, col_avg = calculate_data(col_time, count)#调用函数求最值，均值
		coa_min, coa_max, coa_avg = calculate_data(coa_num, count)#同上
		rows = [nums, col_min, col_max, col_avg, coa_min, coa_max, coa_avg, count]#按照前面的列名，输出对应的列的元素
		writer.writerow(rows)
    elapsed = (time.clock() - start)#代码运行时间，计时结束
    print("Time used", elapsed)



