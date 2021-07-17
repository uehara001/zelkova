
# 出走表、タイム含めたレース情報のCSVファイル作成
# --------------------------------------------
# 1.モジュールのインポート、馬柱スープ作成など
import os
import re
import time
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import datetime
import pickle
import math
import shutil
url = input("出馬表のURLは？")
browser = webdriver.Chrome()
browser.get(url)
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

# 2.それぞれの値のリスト作成
# 馬番
num_lst = soup.find_all('td', attrs={'class': 'horseNum'})
num_lst = [soup.text for soup in num_lst]
num_lst.remove('馬番')

# 競走馬名
name_lst = soup.find_all('a', attrs={'class': 'horseName'})
name_lst = [soup.text for soup in name_lst]

# 種牡馬
racetable_soup = soup.find('section', attrs={'class': 'cardTable'})
racetable_soup = racetable_soup.find('tbody')
td_cols3 = racetable_soup.find_all('td', attrs={'colspan': '3'})
father_lst = td_cols3[2::5]
father_lst = [soup.text for soup in father_lst]

# 母父
# gfather_lst = td_cols3[4::5]
# gfather_lst = [soup.text for soup in gfather_lst]
# gfather_lst = [name.replace('（','') for name in gfather_lst]
# gfather_lst = [name.replace('）','') for name in gfather_lst]
# gfather_lst = [name.replace('Ｓｕｎｄａｙ\u3000Ｓｉｌｅｎｃｅ','サンデーサイレンス') for name in gfather_lst]

# 騎手
jockey_lst = soup.find_all('a', attrs={'class': 'jockeyName'})
jockey_lst = [soup.text for soup in jockey_lst]
jockey_lst = [name.replace('（川崎）', '') for name in jockey_lst]
jockey_lst = [name.replace('（大井）', '') for name in jockey_lst]
jockey_lst = [name.replace('（船橋）', '') for name in jockey_lst]
jockey_lst = [name.replace('（浦和）', '') for name in jockey_lst]
jockey_lst = [name.replace('\n', '') for name in jockey_lst]

# 調教師
trainer_lst = soup.find_all('td', attrs={'colspan': '1'})
trainer_lst = [soup.text for soup in trainer_lst]
trainer_lst = trainer_lst[1::4]
trainer_lst = [name.replace('（川崎）', '') for name in trainer_lst]
trainer_lst = [name.replace('（大井）', '') for name in trainer_lst]
trainer_lst = [name.replace('（船橋）', '') for name in trainer_lst]
trainer_lst = [name.replace('（浦和）', '') for name in trainer_lst]
trainer_lst = [name.replace('\n', '') for name in trainer_lst]

# 3.それぞれのリストをまとめて出走表データフレイム作成
table_data = [num_lst, name_lst, father_lst, jockey_lst, trainer_lst]
columns_name = ["馬番", "競走馬", "種牡馬", "騎手", "調教師"]
table_df = pd.DataFrame(table_data).T
table_df.columns = columns_name


# 4.レース成績情報作成
# レース情報リスト作成
rinfo_lst = soup.find_all('div', attrs={'class': 'raceInfo'})
rinfo_lst = rinfo_lst[:-1]
rinfo_lst = [rinfo.text for rinfo in rinfo_lst]
rinfo_lst = [rinfo.replace('\n', '') for rinfo in rinfo_lst]
rinfo_lst = [rinfo.split('\u3000') for rinfo in rinfo_lst]

# レース情報の整理
for rinfo in rinfo_lst:
    place = rinfo[2].split('頭')
    rinfo[2] = place[1].replace('ナ', '')
    distance = re.sub(r"\D", "", rinfo[3])
    rinfo[3] = distance + "ｍ"

# 5.走破タイムリストの作成
# 走破タイムの記載されてるスープの抽出
racetable_soup = soup.find('section', attrs={'class': 'cardTable'})
racetable_soup = racetable_soup.find('tbody')
tr_soup = racetable_soup.find_all('tr')
tr_soup = tr_soup[2:]
tr_soup = tr_soup[9::11]
rtime_lst = []
for tr in tr_soup:
    td_lst = tr.find_all('td')
    tdtext_lst = [td.text for td in td_lst]
    time_lst = [time.replace('\n', '') for time in tdtext_lst[2:]]
    time_lst = [time.split('\u3000') for time in time_lst]
    time_lst = [time[0] for time in time_lst]
    for t in time_lst:
        if t != '':
            t = t.split(':')
            m = int(t[0])
            s = float(t[1])
            td = datetime.timedelta(minutes=m, seconds=s)
            td = td.total_seconds()
            rtime_lst.append(td)
        else:
            rtime_lst.append('中止')

# レース情報に走破タイムを追加
for i in range(len(rtime_lst)):
    rinfo_lst[i].append(rtime_lst[i])
# レース情報から必要な要素を抽出
rdata_lst = []
for rinfo in rinfo_lst:
    lst = [rinfo[2], rinfo[3], rinfo[1], rinfo[5]]
    rdata_lst.append(lst)
# 馬ごとにまとめてデータフレーム作成
l = rdata_lst
n = 5
result_lst = [l[idx:idx + n] for idx in range(0, len(l), n)]
result_df = pd.DataFrame(result_lst)

# スピード指数、平均スピード指数作成-------------------------
# 6.統計量リストの取得
urawa_statis = []
with open("統計量/urawa_statis.pickle", mode="rb") as f:
    urawa_statis = pickle.load(f)
funabashi_statis = []
with open("統計量/funabashi_statis.pickle", mode="rb") as f:
    funabashi_statis = pickle.load(f)
ooi_statis = []
with open("統計量/ooi_statis.pickle", mode="rb") as f:
    ooi_statis = pickle.load(f)
kawasaki_statis = []
with open("統計量/kawasaki_statis.pickle", mode="rb") as f:
    kawasaki_statis = pickle.load(f)
statis_lists = [urawa_statis, funabashi_statis, ooi_statis, kawasaki_statis]

# 7.条件別に統計量を返す関数、指数をする関数の定義


def si_func(p, d, c, t):
    if type(t) == float:
        m = statis_lists[p][d][c][3]
        s = statis_lists[p][d][c][4]
        si = (m - t)/s*10+80
        si = float(format(si, '.1f'))
        return si
    else:
        return float('nan')


def c_func(c):
    if c == "良":
        return 0
    elif c == "稍重":
        return 1
    elif c == "重":
        return 2
    elif c == "不良":
        return 3


def u_d_func(d):
    l = ["800ｍ", "1300ｍ", "1400ｍ", "1500ｍ", "1600ｍ", "1900ｍ", "2000ｍ"]
    d = l.index(d)
    return d


def f_d_func(d):
    l = ["1000ｍ", "1200ｍ", "1500ｍ", "1600ｍ",
         "1700ｍ", "1800ｍ", "2200ｍ", "2400ｍ"]
    d = l.index(d)
    return d


def o_d_func(d):
    l = ["1000ｍ", "1200ｍ", "1400ｍ", "1500ｍ", "1600ｍ",
         "1700ｍ", "1800ｍ", "2000ｍ", "2400ｍ", "2600ｍ"]
    d = l.index(d)
    return d


def k_d_func(d):
    l = ["900ｍ", "1400ｍ", "1500ｍ", "1600ｍ", "2000ｍ", "2100ｍ"]
    d = l.index(d)
    return d


# 8.スピード指数リスト作成
si_lsts = []
for rl in result_lst:
    si_lst = []
    for r in rl:
        p = r[0]
        d = r[1]
        c = r[2]
        t = r[3]

        c = c_func(c)

        if p == "浦和":
            p = 0
            d = u_d_func(d)
            si_lst.append(si_func(p, d, c, t))
        elif p == "船橋":
            p = 1
            d = f_d_func(d)
            si_lst.append(si_func(p, d, c, t))
        elif p == "大井":
            p = 2
            d = o_d_func(d)
            si_lst.append(si_func(p, d, c, t))
        elif p == "川崎":
            p = 3
            d = k_d_func(d)
            si_lst.append(si_func(p, d, c, t))
        else:
            si_lst.append(float('nan'))
    si_lsts.append(si_lst)
si_df = pd.DataFrame(si_lsts)
# 9.馬ごとの指数の平均
sim_lst = []
for l in si_lsts:
    nl = [si for si in l if math.isnan(si) == False]
    if len(nl) == 0:
        sim_lst.append(float('nan'))
    else:
        sim = sum(nl)/len(nl)
        sim = float(format(sim, '.1f'))
        sim_lst.append(sim)
sim_df = pd.DataFrame(sim_lst)

# 10その他指数の呼び出し、全指数のデータフレーム作成
# その他の指数データの読み込み
hn_data = pd.read_pickle("その他指数データフォルダ/hn_data.pickle")
ei_dic = pd.read_pickle("その他指数データフォルダ/sire_dic.pickle")
ji_dic = pd.read_pickle("その他指数データフォルダ/ji_dic.pickle")
ti_dic = pd.read_pickle("その他指数データフォルダ/ti_dic.pickle")
# 馬番について
l = len(num_lst)
if url[-2:] == '18':
    num_in = hn_data[0][0:l]
elif url[-2:] == '19':
    num_in = hn_data[1][0:l]
elif url[-2:] == '20':
    num_in = hn_data[2][0:l]

elif url[-2:] == '21':
    num_in = hn_data[3][0:l]
# # 種牡馬について
f_in = []
for k in father_lst:
    if k in ei_dic:
        f_in.append(ei_dic[k])
    else:
        f_in.append(float('nan'))
# 騎手について
j_in = []
for k in jockey_lst:
    if k in ji_dic:
        j_in.append(ji_dic[k])
    else:
        j_in.append(float('nan'))
# 調教師について
t_in = []
for k in trainer_lst:
    if k in ti_dic:
        t_in.append(ti_dic[k])
    else:
        t_in.append(float('nan'))

# データフレームの作成
itable_data = [num_lst, name_lst, num_in, f_in, j_in, t_in, sim_lst]
itable_df = pd.DataFrame(itable_data).T
icolumns_name = ["", "競走馬", "馬番", "種牡馬", "騎手", "調教師", "速さ"]
itable_df.columns = icolumns_name

# 出走馬プラス指数のデータフレーム作成
nnum_in = [str(num) for num in num_in]
nnum_lst = []
for i in range(len(num_lst)):
    nnum = num_lst[i] + "<br>" + "(" + nnum_in[i] + ")"
    nnum_lst.append(nnum)

nsim_lst = [str(sim) for sim in sim_lst]
nname_lst = []
for i in range(len(num_lst)):
    nsim = name_lst[i] + "<br>" + "(" + nsim_lst[i] + ")"
    nname_lst.append(nsim)

nf_in = [str(num) for num in f_in]
nfather_lst = []
for i in range(len(num_lst)):
    nf = father_lst[i] + "<br>" + "(" + nf_in[i] + ")"
    nfather_lst.append(nf)

nj_in = [str(num) for num in j_in]
nj_lst = []
for i in range(len(num_lst)):
    nj = jockey_lst[i] + "<br>" + "(" + nj_in[i] + ")"
    nj_lst.append(nj)

nt_in = [str(num) for num in t_in]
nt_lst = []
for i in range(len(num_lst)):
    nt = trainer_lst[i] + "<br>" + "(" + nt_in[i] + ")"
    nt_lst.append(nt)
ntable_data = [nnum_lst, nname_lst, nfather_lst, nj_lst, nt_lst]
columns_name = ["馬番", "競走馬", "種牡馬", "騎手", "調教師"]
ntable_df = pd.DataFrame(ntable_data).T
ntable_df.columns = columns_name

# 11.データフレームをcsvファイルで保存
# レース別のフォルダを作成
u = url.replace('%2f', '')
race_id = re.sub(r"\D", "", u)
p = race_id[-2:]
race_id = race_id[:-2]
y = race_id[:4]
d = race_id[4:8]
n = race_id[8:]
race_id = y+"_"+d+"_"+n
os.mkdir(race_id)


# 前５走レース成績
# 全指数
itable_df.to_csv(f'{race_id}/allIndex.csv', index=False)
# 出走表プラス全指数
ntable_df.to_csv(f'{race_id}/raceCard.csv', index=False)

# phpファイルコピー
shutil.copyfile("tool.php", f'{race_id}/raceid{race_id}.php')

browser.close()
browser.quit()
