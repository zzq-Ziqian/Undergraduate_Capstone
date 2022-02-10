import requests
import re
import pandas as pd
import time
import json

header = {'Content-Type':'text/html;charset=utf-8',
          'User-Agent':'Mozilla/5.0 (Window NT 10.0; WOW64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
Cookie = {'Cookie':'XSRF-TOKEN=0aa387; WEIBOCN_FROM=1110006030;'
                   ' MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4593581124485795%26luicode%3D20000061%26lfid%3D4593581124485795; '
                   'loginScene=102003; SUB=_2A25Ng9a3DeRhGeNG6lAY8ijKyD6IHXVuj_r_rDV6PUJbkdAKLVHtkW1NS2ooxICK92O0Z1TGb2xjMx-3uKdk8Se1;'
                   ' _T_WM=78215443048'}

#评论翻页的关键字段
max_id = ''

#设置循环
while True:
    #评论第一页max_id为空值
    if max_id == '':
        url = 'https://m.weibo.cn/comments/hotflow?id=4642963496638229&mid=4642963496638229&max_id_type=0'
    else:
        #显示max_id
        print(max_id)
        #评论后一页url中的max_id为前一页传递来的参数
        url = 'https://m.weibo.cn/comments/hotflow?id=4642963496638229&mid=4642963496638229&max_id='+\
              str(max_id)+'&max_id_type='+str(max_id_type)
    print('请求的url是：'+url)
    #request对象获取
    response = requests.get(url,headers=header,cookies=Cookie)
    #json格式解析
    print(response.text)
    comment = response.json()
    print('request请求状态：'+str(comment['ok']))
    #如果Ok值为1，表示解析成功
    if comment['ok'] == 0:
        break
    #获取max_id值
    max_id = comment['data']['max_id']
    max_id_type = comment['data']['max_id_type']
    print('max_id is:'+str(max_id))
    print('max_id_type is:'+str(comment['data']['max_id_type']))

    #获取评论文本，并过滤符号和英文字符
    for comment_data in comment['data']['data']:
        data = comment_data['text']
        p = re.compile(r'(<span.*>.*</span>)*(<a.*>.*</a>)?')
        data = re.sub('[^\u4e00-\u9fa5]','',data)#
        data = p.sub(r'',data)
        data1 = [(comment_data['created_at'],comment_data['user']['id'],comment_data['user']['screen_name'],data)]
        data2 = pd.DataFrame(data1)
        #data2.to_csv('comment_data.csv',header=False,encoding='utf-8-sig',index=False,mode='a+')

    time.sleep(2)

