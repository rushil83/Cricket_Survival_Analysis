import pandas as pd
import urllib.request
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter

plt.style.use('ggplot')
###looping to get data from 12 different pages
list=[]
for i in range(1,12):
    ### MAKING SOUP ###
    url = "http://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;filter=advanced;orderby=runs;page=" + str(
        i) + ";size=200;template=results;type=batting"
    url = urllib.request.urlopen(url).read()
    soup = bs(url, 'html.parser')
    table = soup.find_all('table')
    table = table[2]

    ### COLUMN_NAMES ###
    thead = table.findAll('thead')
    thead = thead[0].text
    thead = thead.splitlines()
    thead = thead[2:15]

    ### TABLE FORMING ###
    tbody = table.findAll('tbody')
    row = tbody[0].findAll('tr')
    for i in range(len(row)):
        single_row = row[i].find_all('td')
        single_row = [single_row[int(j)].text for j in range(len(single_row))][:13]
        list.append(single_row)

data = pd.DataFrame(list, columns=thead)

### ELIMINATING CURRENT PLAYER STATS ###
span_data = data.ix[:, 1]
index = []
for i in range(len(span_data)):
    if (span_data[i][5:9] == '2016') or (span_data[i][5:9] == '2017' ):
        index.append(i)

data = data.drop(index)
data = data.reset_index(drop=True)

###CREATING CAREER SPAN YEAR DATA (start,end,span)
span_data1 = data.ix[:, 1]
for i in range(len(span_data1)):
    start = span_data1[i].split('-')[0]
    end = span_data1[i].split('-')[1]
    data.ix[i, 'start'] = start
    data.ix[i, 'end'] = end

for i in range(len(data)):
    data.ix[i, 'span'] = int(data.ix[i, 'end']) - int(data.ix[i, 'start'])


###seprating player-name and team_name(ICC/ASIA/INDIA)
name = data.ix[:, 0]
country_list = []
for i in range(len(name)):
    namelist = name[i].split('(')[0]
    data.ix[i, 'player'] = namelist
    countrylist = name[i].split('(')[1]
    countrylist = countrylist.split(')')[0]
    countrylist = countrylist.split('/')
    country_list.append(countrylist)

countries = ['INDIA', 'SL', 'AUS', 'ENG', 'USA', 'NZ', 'PAK', 'KENYA', 'BMUDA', 'SCOT', 'WI', 'BDESH', 'AFG', 'IRE',
             'NAM', 'ZIM', 'HK', 'Neth', 'UAE', 'Can', 'EAf', 'SA']

###more than 1 team is present in teams_name(ICC/ASIA/INDIA),so seprating and adding
### -- country name to the team
for i in range(len(country_list)):
    for j in range(len(country_list[i])):
        for country in countries:
            if (country_list[i][j] == country):
                data.ix[i, 'country'] = country_list[i][j]

###droping original form of span and name
data = data.drop('Player', axis=1)
data = data.drop('Span', axis=1)

###renaming the column_headings
data.columns = ['mat', 'inns', 'no', 'runs', 'hs', 'avg', 'bf', 'sr', '100', '50', '0', 'start', 'end', 'span','player',
                'country']

###rearranging the columns
data = data[['player', 'country', 'mat', 'inns', 'no', 'runs', 'hs', 'avg', 'bf', 'sr', '100', '50', '0', 'start', 'end',
     'span']]

#batsmen_data = data

#data.to_csv('data.csv', sep=',')
#print(batsmen_data)


#----------------------------------(i) Player's Country vs Career Length -------------------------------------------------------

data = pd.read_csv("data.csv")
data.ix[:,'censor']=1

data = pd.DataFrame(data)
duration = data['span']
observed = data.ix[:,'censor']

kmf = KaplanMeierFitter()
kmf.fit(duration,observed,label='kmf_mean')
#kmf.plot()
#plt.show()

###INDIA kmf

india_data = data.ix[data['country']=='INDIA']
india_duration = india_data['span']
india_observed = india_data['censor']

kmfind = KaplanMeierFitter()
kmfind.fit(india_duration,india_observed,label="india")

###simillarly for other countries
kmfpak =KaplanMeierFitter()
kmfpak.fit((data.ix[data['country']=='PAK'])['span'],(data.ix[data['country']=='PAK'])['censor'],label='pakistan')

kmfaus =KaplanMeierFitter()
kmfaus.fit((data.ix[data['country']=='AUS'])['span'],(data.ix[data['country']=='AUS'])['censor'],label='australia')

kmfsa =KaplanMeierFitter()
kmfsa.fit((data.ix[data['country']=='SA'])['span'],(data.ix[data['country']=='SA'])['censor'],label='south_africa')

kmfbdesh =KaplanMeierFitter()
kmfbdesh.fit((data.ix[data['country']=='BDESH'])['span'],(data.ix[data['country']=='BDESH'])['censor'],label='bangladesh')

kmfnz =KaplanMeierFitter()
kmfnz.fit((data.ix[data['country']=='NZ'])['span'],(data.ix[data['country']=='NZ'])['censor'],label='newzealand')

kmfwi =KaplanMeierFitter()
kmfwi.fit((data.ix[data['country']=='WI'])['span'],(data.ix[data['country']=='WI'])['censor'],label='westindies')

kmfeng =KaplanMeierFitter()
kmfeng.fit((data.ix[data['country']=='ENG'])['span'],(data.ix[data['country']=='ENG'])['censor'],label='england')

kmfsl =KaplanMeierFitter()
kmfsl.fit((data.ix[data['country']=='SL'])['span'],(data.ix[data['country']=='SL'])['censor'],label='srilanka')

kmfcan =KaplanMeierFitter()
kmfcan.fit((data.ix[data['country']=='Can'])['span'],(data.ix[data['country']=='Can'])['censor'],label='canada')

kmfhk =KaplanMeierFitter()
kmfhk.fit((data.ix[data['country']=='HK'])['span'],(data.ix[data['country']=='HK'])['censor'],label='hongkong')

kmfscot =KaplanMeierFitter()
kmfscot.fit((data.ix[data['country']=='SCOT'])['span'],(data.ix[data['country']=='SCOT'])['censor'],label='scotland')

kmfuae =KaplanMeierFitter()
kmfuae.fit((data.ix[data['country']=='UAE'])['span'],(data.ix[data['country']=='UAE'])['censor'],label='uae')

kmfeaf =KaplanMeierFitter()
kmfeaf.fit((data.ix[data['country']=='EAf'])['span'],(data.ix[data['country']=='EAf'])['censor'],label='EAf')

kmfzim =KaplanMeierFitter()
kmfzim.fit((data.ix[data['country']=='ZIM'])['span'],(data.ix[data['country']=='ZIM'])['censor'],label='zimbabwe')

kmfneth =KaplanMeierFitter()
kmfneth.fit((data.ix[data['country']=='Neth'])['span'],(data.ix[data['country']=='Neth'])['censor'],label='netherland')

kmfkenya =KaplanMeierFitter()
kmfkenya.fit((data.ix[data['country']=='KENYA'])['span'],(data.ix[data['country']=='KENYA'])['censor'],label='kenya')

kmfbmuda =KaplanMeierFitter()
kmfbmuda.fit((data.ix[data['country']=='BMUDA'])['span'],(data.ix[data['country']=='BMUDA'])['censor'],label='burmuda')

kmfire =KaplanMeierFitter()
kmfire.fit((data.ix[data['country']=='IRE'])['span'],(data.ix[data['country']=='IRE'])['censor'],label='ireland')

kmfnam =KaplanMeierFitter()
kmfnam.fit((data.ix[data['country']=='NAM'])['span'],(data.ix[data['country']=='NAM'])['censor'],label='namibia')

kmfusa =KaplanMeierFitter()
kmfusa.fit((data.ix[data['country']=='USA'])['span'],(data.ix[data['country']=='USA'])['censor'],label='usa')


kmfafg =KaplanMeierFitter()
kmfafg.fit((data.ix[data['country']=='AFG'])['span'],(data.ix[data['country']=='AFG'])['censor'],label='afghanistan')



####PLOTING kmf in PLOT

ax=plt.subplot(111)
#kmf.survival_function_.plot(ax=ax)
#kmfaus.survival_function_.plot(ax=ax)
#kmfpak.survival_function_.plot(ax=ax)
kmfind.survival_function_.plot(ax=ax)
kmfeng.survival_function_.plot(ax=ax)
#kmfsa.survival_function_.plot(ax=ax)
kmfwi.survival_function_.plot(ax=ax)
#kmfbdesh.survival_function_.plot(ax=ax)
#kmfsl.survival_function_.plot(ax=ax)
#kmfnz.survival_function_.plot(ax=ax)
#kmfusa.survival_function_.plot(ax=ax)
#kmfzim.survival_function_.plot(ax=ax)
#kmfhk.survival_function_.plot(ax=ax)
#kmfbmuda.survival_function_.plot(ax=ax)
#kmfeaf.survival_function_.plot(ax=ax)
#kmfneth.survival_function_.plot(ax=ax)
#kmfscot.survival_function_.plot(ax=ax)
#kmfafg.survival_function_.plot(ax=ax)
#kmfnam.survival_function_.plot(ax=ax)
#kmfkenya.survival_function_.plot(ax=ax)
#kmfuae.survival_function_.plot(ax=ax)
#kmfcan.survival_function_.plot(ax=ax)
#kmfire.survival_function_.plot(ax=ax)

plt.show()


#-------------------------------------(ii) Strike Rate vs Career length------------------------------------------------------------
## creating the probability of career length of player vs their strike rate
##atleast 50 innings player
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


plt.show()


#-------------------------------- (iii) Runs vs Career_Length ------------------------------------------------------------------------------------------------


data['runs'] = pd.to_numeric(data['runs'])

runs8000 = data.ix[data['runs']>=8000]
runs3000 = data.ix[data['runs']<=3000]
#runs3000 = runs3000.ix[runs3000['runs']< 3000]

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