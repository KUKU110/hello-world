# -*- coding: utf-8 -*-
"""
this is a tutorial for time series data from the book 'python for data analysis'
"""

'''
时间序列数据的意义取决于具体的应用场景，主要有以下几种：
1. 时间戳(timestamp)，特定的时刻
2. 固定时间(period),如2007年1月或全年
3. 时间间隔(interval),由起始和结束时间戳表示
pandas提供了一组标准的时间序列处理工具和数据算法，可以高效处理大量时间序列数据
'''

'''
python标准库包含用于日期date和时间time数据的数据类型，而且还有日历方面的功能，
我们主要会用到datetime、time以及calendar模块
'''

from datetime import datetime
import numpy as np
import pandas as pd

now=datetime.now()
yesterday=datetime(2017,2,14) # 直接设置时间
delta=now-yesterday
# 返回时间差的天数和秒数
day=delta.days
sec=delta.seconds

# 可以给datetime对象加上或减去一个或多个timedelta，这样会产生一个新对象
from datetime import timedelta
start=datetime(2011,1,7)
start+timedelta(12)
start-2*timedelta(12)

'''
datetime 模块中的数据类型
date 以公历形式存储日历日期
time 将时间存储为时、分、秒、毫秒
datetime 存储日期和时间
timedelta 表示两个datetime值之间的差（日、秒、毫秒）
'''

# 字符串和datetime的相互转换
'''
利用str和strftime方法，datetime对象和pandas的timestamps对象可以被格式化为字符串
'''
stamp=datetime(2015,5,1)
# 以下两种方法都可以将datetime对象转化为str类型的数据
stamp_str=str(stamp)
stamp_str1=stamp.strftime('%Y-%m-%d-%H')
# 将字符串转换为日期
value='2011-01-03'
value=datetime.strptime(value,'%Y-%m-%d')
# 处理大量时间格式字符串
datestrs=['7/6/2011','9/11/2012']
datelist=[datetime.strptime(x,'%d/%m/%Y') for x in datestrs] # 得到一个datetime的list
# NaT not a time 是pandas中时间戳数据的NA值
# datetime 中的时间格式定义见p305

# 时间序列基础
# pandas中最基本的时间序列类型就是以时间戳（通常以python字符串或datetime对象表示）为索引的Series
dates=[datetime(2011,1,2),datetime(2011,1,5),datetime(2011,1,7)]
ts=pd.Series(np.random.randn(3),index=dates) # standard normal distribution
'''
这些datetime对象实际上是被放在一个DateTimeIndex中的，现在，变量ts就成为一个TimeSeries了
没必要显式的使用TimeSeries的构造函数，当创建一个带有DateTimeIndex的Series时，pandas就会
知道该对象是一个时间序列. DateTimeIndex中的各个标量值是pandas的Timestamp对象
'''
stamp=ts.index[1]
'''
Timestamp 可以随时自动转换为datetime对象，还可以储存频率信息，且知道如何执行时区转换以及其他操作
'''

# 索引、选取、子集构造
# Timeseries是 Series 的一个子类，所以在索引以及数据选取方面它们的行为是一样的
ts[stamp]
ts['20110102'] # 传入一个可被解释为日期的字符串
# 对于较长的时间序列，只需传入“年”或“年月”就可轻松选取数据的切片
longer_ts=pd.Series(np.random.randn(1000),index=pd.date_range('1/1/2000',periods=1000))
longerts_02=longer_ts['2002'] # 利用年份进行时间序列切片
longerts_01=longer_ts[datetime(2002,1,1):]
# 通过日期进行切片的方式只对规则Series有效，如果是dataframe应该怎么做呢？
'''
由于大部分时间序列数据都是按照先后顺序排列的，因此你也可以用不存在于该时间序列中的时间戳
对其进行切片（即范围查询）
'''
longer_ts0001=longer_ts['20000202':'20011201'] # 包括了起始和截止日期
'''
与之前一样，这里可以传入字符串日期、datetime或timestamp，但这样切片所产生的是源数据的
视图，跟numpy数组的切片运算是一样的，此外，还有一个等价的实例方法也可以截取两个日期之间的TimeSeries
'''
ans=longer_ts.truncate(before='20011223') # 20011223日期之后的时间序列数据

'''
上面这些操作对dataframe也有效
'''

# 日期的范围、频率以及移动
'''
pandas中的时间序列一般认为是不规则的，没有固定的频率，对于大部分程序而言无所谓，但是
常常需要以某种相对固定的频率进行分析，pandas有一整套标准时间序列频率以及用于重采样、频率
推断、生成固定频率日期范围的工具。
我们将之前的时间序列转换为一个具有固定频率（每日）的时间序列，只需调用resample即可
'''
newts=ts.resample('D') #这里出来的是一个datetimeindexresamper，我不知道是什么东西
# 生成日期范围，使用pandas.date_range来生成指定长度的datetimeindex
index=pd.date_range('20120401','20120501')
'''
默认情况下，date_range会产生按天计算的时间点，如果只传入初始日期或结束日期，那就还要传入
一个表示一段时间的数字
'''
index=pd.date_range(start='20120401',periods=25)
index=pd.date_range(end='20120601',periods=20)
'''
起始和结束日期定义了日期索引的严格边界，如果想要生成一个由每月最后一个工作日组成的日期索引，
可以传入BM频率，business end of month，
'''
index=pd.date_range('1/1/2000','12/1/2000',freq='BM')

# 频率和日期偏移量
'''
pandas中的频率是由一个基础频率和一个乘数组成的，基础频率通常以一个字符串别名表示，'M','H'
等，对于每个基础频率，都有一个被称为日期偏移量的对象与之对应
'''
from pandas.tseries.offsets import Hour, Minute
hour=Hour()
four_hours=Hour(4)
# 一般无需显式创建这样的对象，只需使用如'H','4H'等字符串别名即可
index=pd.date_range('20000105','20000106',freq='4H')
# 大部分偏移量对象可通过加法进行连接
interval=Hour(2)+Minute(25)
# 同理，也可以传入频率字符串，’2h30min',可被解析为等效的表达式
index=pd.date_range('20000105','20000106',freq='4h15min')
# WOM日期，week of month,是一种非常实用的频率类，以WOM开头，可以获得诸如 每月第三个星期五之类的日期
rng=pd.date_range('20000105','20010106',freq='WOM-3MON')

# 移动（超前和滞后）数据
'''
移动指的是沿着时间轴将数据前移或后移，Series和dataframe都有一个shift方法用于执行单纯的
前移或后移操作，保持索引不变
'''
ts=pd.Series(np.random.randn(4),index=pd.date_range('20000101',periods=4,freq='M'))
ts.shift(1) # 将所有的数据后移一位，但是时间戳不变
per=ts/ts.shift(1)-1
'''
由于单纯的位移操作不会修改索引，部分数据会被丢弃，因此如果频率已知，可以将其传给shift
以便实现对时间戳进行位移而不是对数据进行简单位移
'''
ts.shift(2,freq='M')
# 这里同样可以使用其他频率，我们就能够灵活地对数据进行超前和滞后处理

# 通过偏移量对日期进行位移
# pandas的日期偏移量还可以用在datetime或timestamp对象上
# 时期及其算术运算
'''
时期（period）表示的是时间区间，比如数月、数年等，period类所表示的就是这种数据类型，其
构造函数需要用到一个字符串或整数，
'''
p=pd.Period(2007,freq='A-DEC')
# period_range函数可用于创建规则的时期范围
rng=pd.period_range('20000101','20000630',freq='M')
# periodindex 类保存了一组period，可以在任何pandas数据结构中被用作轴索引

# 时期的频率转换

# 重采样及频率转换
'''
重采样指的是将时间序列从一个频率转换到另一个频率的处理过程，高频数据聚合到低频率称为降采样
低频数据转换到高频数据称为升采样
'''
