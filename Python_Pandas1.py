#骁哥虐我千百遍，我待骁哥如初恋
#功能说明：给出拥有百万行数据的csv文件，要求，按照其中的2列的组合，来索引出同行的其它列的数据，并求出，在所有相同的组合中，前面要求列的最值，均值
#	   个数，并且最后要求输出代码运行时间

#思路说明：python 中 pandas的模块中，有个DataFrame的类型是相当于表格的二维数组，并且对列直接进行处理，所以相当适合本题的要求
#          1：首先把文件数据读入
#	   2：因为要按照指定2列的数字组合来索引其它数据，所以，先把2列的数字范围最大值求出，这样，可以在这个范围内进行遍历所有可能的组合
#          3：每次遍历出一种组合的后，有个骚气的方式，来进行判断现有的组合中，是否有这个存在，在27行代码中，再详细说明
#          4：在遍历的所有组合中，如果有存在的，就把这整行的元素全部读出，然后再读出我们所需要的列的数据，这是一次性把所有相同的组合全部读出
#          5：求出我们所取出列的长度，因为遍历的所有组合中，有的组合是不存在的，所以很有必要判断，这个长度的值，如果长度为0，说明组合不存在，跳过
#             本次循环，直接进入下一次循环，继续判断
#          6：如果长度不为0，组合存在，把我们读到的所有相同组合（一次判断一个）的列数据，传入另外一个函数，求最值，均值
#          7：最后将处理得到的数据，输出到csv文件当中
import pandas as pd#导入pandas 模块
import csv,time#导入csv和time模块，其中csv是写出数据的时候需要用到，time模块，是计算代码运行的时间时，需要用到

def calculate_data(List, count):#传入一列，是serise的类型，和list一样处理，这个函数，就是求最值，均值
    data_min, data_max, data_sum= min(List), max(List), sum(List)
    data_avg = data_sum / float(count)#因为求均值的时候，/是求模，用float就精确多了
    return data_min, data_max, data_avg

if __name__ == '__main__':#骁哥需要的main
    start = time.clock()#代码开始运行，计时开始
    df = pd.read_csv ('colla.csv', encoding = "ISO-8859-1")#使用pandas，读入所要处理的文件，后面是编码模式，开始使用utf8一直报错，坑死
    with open('Test_file.csv', mode = 'w', newline = '') as wf:#这个是创建一个输出的csv文件，写模式，newline为空，这样输出就不用每隔一行就空格了
	headers = ['degree', 'col_min', 'col_max', 'col_avg', 'coa_min', 'coa_max', 'coa_avg', 'count' ]#设置输出列名字
	writer = csv.writer(wf)#开始写
	writer.writerow(headers)#写入列名
	df1, df2 = max(df.degree1), max(df.degree2)#分别求出，指定列的最大值，这样才能知道后面索要遍历的范围
	for i in range(df1 + 1):#因为range的范围df1本事是遍历不到的，所以要+1
	    for j in range(df2 + 1):#同上
		row_nums = df[(df.degree1 == i) & (df.degree2 == j)]#就是这个骚气的方式，折磨我好久，下面详细阐述：
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



