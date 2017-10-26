import pandas as pd
import lifelines
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

data = pd.read_csv("data2.csv")

plt.style.use('ggplot')
data.ix[:,'censor']=1

data = pd.DataFrame(data)
duration = data['span']
observed = data.ix[:,'censor']

#kmf = KaplanMeierFitter()
#kmf.fit(duration,observed,label='kmf_mean')
#kmf.plot()
#plt.show()

##atleast 50 innings playe
data['inns'] = pd.to_numeric(data['inns'])
innings = data[:][data['inns']>50]


innings['sr'] = pd.to_numeric(innings['sr'])

vhighsr = innings.ix[innings['sr']>=100]
highsr = innings.ix[innings['sr']>=90]
highsr = highsr.ix[highsr['sr']<100]
goodsr = innings.ix[innings['sr']>=80]
goodsr = goodsr.ix[goodsr['sr']<90]
avgsr = innings.ix[innings['sr']>=70]
avgsr = avgsr.ix[avgsr['sr']<80]
poorsr = innings.ix[innings['sr']>=55]
poorsr = poorsr.ix[innings['sr']<70]
vpoorsr = innings.ix[innings['sr']<55]


kmfvhighsr = KaplanMeierFitter()
kmfvhighsr.fit(vhighsr['span'],vhighsr['censor'],label = ' sr > 100' )

kmfhighsr = KaplanMeierFitter()
kmfhighsr.fit(highsr['span'],highsr['censor'],label = '100 > sr > 90' )

kmfgoodsr = KaplanMeierFitter()
kmfgoodsr.fit(goodsr['span'],goodsr['censor'],label='90 > sr > 80')

kmfavgsr = KaplanMeierFitter()
kmfavgsr.fit(avgsr['span'],avgsr['censor'] , label = '80 > sr > 70')

kmfpoorsr = KaplanMeierFitter()
kmfpoorsr.fit(poorsr['span'],poorsr['censor'],label='70 > sr > 55')

kmfvpoorsr = KaplanMeierFitter()
kmfvpoorsr.fit(vpoorsr['span'],vpoorsr['censor'],label='sr < 55')



kmfmat = KaplanMeierFitter()
kmfmat.fit(innings['span'],innings['censor'],label = 'mean')

bx = plt.subplot(111)

kmfmat.survival_function_.plot(ax=bx)
kmfvhighsr.survival_function_.plot(ax=bx)
kmfhighsr.survival_function_.plot(ax=bx)
kmfgoodsr.survival_function_.plot(ax=bx)
kmfavgsr.survival_function_.plot(ax=bx)
kmfpoorsr.survival_function_.plot(ax=bx)
kmfvpoorsr.survival_function_.plot(ax=bx)
plt.xlabel("career span ( in years )")
plt.ylabel(" probabilty of the players ")
plt.title( " probability of players having given sr. rate vs their career length")


plt.show()