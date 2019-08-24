import  numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#导入数据
#跳过一些没什么卵用的开头
overdoses=pd.read_excel('overdose_data_1999-2015.xls',sheetname='Online',skiprows=6)
#获取一行数据
def get_date(table,rownum,title):
    data=pd.DataFrame(table.loc[rownum][2:]).astype(float)
    data.columns={title}
    return data

#获取海洛因狗粮死亡的人
title='Heroin Overdoses'
d=get_date(overdoses,18,title)
x=np.array(d.index)
y=np.array(d['Heroin Overdoses'])
overdose=pd.DataFrame(y,x)

overdose.columns={title}
#初始化一个ffmpeg writer并20fps，1800bit录屏
Writer=animation.writers['ffmpeg']
writer=Writer(fps=20,metadata=dict(artist='Me'),bitrate=1800)

#创建图形，便签范围等
fig=plt.figure(figsize=(10,6))
plt.xlim(1999,2016)
plt.ylim(np.min(overdose)[0],np.max(overdose)[0])
plt.xlabel('Year',fontsize=20)
plt.ylabel(title,fontsize=20)
plt.title('Heroin Overdoses per Year',fontsize=20)

#动画函数，每一帧i该干嘛
def animate(i):
    data=overdose.iloc[:int(i+1)]#选择数据范围
    p=sns.lineplot(x=data.index,y=data[title],data=data,color='r')
    p.tick_params(labelsize=17)
    plt.setp(p.lines,linewidth=7)

#调用mat animate函数定义帧的Function开始动画，frames定义调用animate的频率
ani=animation.FuncAnimation(fig,animate,frames=60,repeat=True)
#保存
#ani.save('HeroinOverdosesJumpy.mp4',writer=writer)
plt.show()