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


data['runs'] = pd.to_numeric(data['runs'])

runs8000 = data.ix[data['runs']>=8000]
runs3000 = data.ix[data['runs']<=3000]
#runs3000 = runs3000.ix[runs3000['runs']< 4000]

kmfruns8000 = KaplanMeierFitter()
kmfruns8000.fit(runs8000['span'],runs8000['censor'],label = ' runs > 8000' )

kmfruns3000 = KaplanMeierFitter()
kmfruns3000.fit(runs3000['span'],runs3000['censor'],label = ' runs < 3000')

bx = plt.subplot(111)
kmfruns8000.survival_function_.plot(ax=bx)
kmfruns3000.survival_function_.plot(ax=bx)


plt.xlabel(" career length ( in years )")
plt.ylabel(" probability of players  ")
plt.title("probability of players with specific runs vs their career length")
plt.show()