# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:13:54 2017

@author: hzxieshukun
"""

import requests
import time
import random
import re
import json
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
'Accept':'text/html;q=0.9,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Connection':'close',
'Referer':'https://www.jd.com/'
}

cookie={'TrackID':'1u75REUv6kEgYtLCd7-YlAUseP0GD9sIjoF671jkay9iCE-Jbs9luTWc9ieN9fzsr80PMIrlL1rU8De4Ko9FIPQ',
'__jda':'122270672.1490696078674303481197.1490696079.1490696079.1490771194.2',
'__jdb':'122270672.9.1490696078674303481197|2.1490771194',
'__jdc':'122270672',
'__jdu':'1490696078674303481197',
'__jdv':'122270672|www.huihui.cn|-|referral|-|1490696078675',
'pinId':'qMsxAnxs5SU'}

url1 = 'http://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1010&productId='
url2 = '&score=0&sortType=5&page='
url3 = '&pageSize=10&isShadowSku=0'

global_num = 0

def write_html(file_name, html):
    with open(file_name, 'a') as f:
        if html != "":
            f.write(html)
            f.write("\n")

def write_comments(file_name, comments):
    with open(file_name, 'a') as f:
        #f.write("page\ttime\tscore\tcomment\n")
        for k in comments:
            f.write(k + "\n")

def handle_comments(times, scores, product_colors, contents, page,  users, agreements, comments):
    for i in xrange(len(times)):
        k = "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (page + 1, scores[i], users[i], times[i], agreements[i], product_colors[i], contents[i])
        comments.append(k)
    
def get_data(product_id, ran_num):
    global global_num
    count = 0
    for i in ran_num:
        comments = []
        url = url1 + product_id + url2 + str(i) + url3
        print url
        r = requests.get(url=url,headers=headers,cookies=cookie)
        html = r.content
        write_html(product_id + "_comments_html.txt", html)
        times = re.findall(r'"creationTime":"([\d\s:-]+)","isTop".{1,40}"referenceImage"',html)
        scores = re.findall(r'"referenceImage".*?,"score":(.*?),',html)
        product_colors = re.findall(r'"productColor":([^,]+),', html)
        contents = re.findall(r'"guid":.{1,100},"content":"([^"]+)","creationTime".{1,30},"isTop".{1,40}"referenceImage"',html)
        users = re.findall(r'"isReplyGrade":[^"]+"nickname":[^"]*"([^"]+)"', html)
        agreements = re.findall(r'"title":.{1,20},"usefulVoteCount":([^,]+)', html)
#        print times
#        print scores
#        print contents
#        print product_colors
#        print users
#        print agreements
        #write_comments(product_id + "_contents.txt", contents)
        if len(times) == 0 and len(scores) == 0 and len(contents) == 0:
            print "request null and stop"
            global_num = i
            return 1
        print "page: %s--times len:%s, scores len:%s, contents len:%s, product_colors len:%s, users len:%s, agreements len:%s" \
            % (i+1, len(times), len(scores), len(contents), len(product_colors), len(users), len(agreements))
        if (len(agreements) < 10):
            agreements = [0 for j in range(10)]
        handle_comments(times, scores, product_colors, contents, i, users, agreements, comments)
        write_comments(product_id + "_output.txt", comments)
        time.sleep(3)
        count = count + 1
        if (count % 5 == 0):
            print "wait for 8 seconds"
            time.sleep(8)
    return 0
        
print "run the jd.py"
product_id = sys.argv[1]
begin_page = int(sys.argv[2])
end_page = int(sys.argv[3])
global_num = begin_page - 1
#product_id = "4328159"
#begin_page = 1
#end_page = 2
while(1):
    ran_num = [i for i in xrange(global_num, end_page, 1)]
    status = get_data(product_id, ran_num)
    if status == 0:
        break
    print "wait for 20 seconds"
    time.sleep(20)

