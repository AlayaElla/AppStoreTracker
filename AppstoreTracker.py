#coding=utf-8
import urllib.request
import os
import time
import json
import smtplib
import smtplib
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
import datetime
import MyTools
import sys

def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode()
    return html

def wirteTrackIDList(list,campanyPath):
    for key,value in list.items():
        if(len(value)==0):
            continue
        with open(campanyPath+key+'.txt','a') as f:
            for line in value:
                f.write(str(line['trackId'])+"\n")
            f.close()

def parseInfo(html,campanyPath):
    infolist = json.loads(html)
    writelist = {}
    trackIDList = {}

    for info in infolist['results']:
        if(str(info['artistName']) not in trackIDList):
            trackIDList[info['artistName']] = MyTools.get_file_to_list(campanyPath,info['artistName'])
            writelist[info['artistName']] = []
            #os.system(f"echo '{str(info['artistName'])}'")

        if(info['wrapperType'] != "artist"):
            if(str(info['trackId']) not in trackIDList[info['artistName']]):
                writelist[info['artistName']].append(info)
                trackIDList[info['artistName']].append(str(info['trackId']))
    return writelist

def sendEmail(newlist,receivers,common_conifg):
    #邮件内容设置
    msgstr = ""
    logstr = ''
    tatallcount = 0
    msg_tatall_str = ""

    timestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    title = common_conifg['titlestr']+timestr
    logstr = title
    for key,value in newlist.items():
        if(len(value)==0):
            continue

        msgstr = msgstr + f"<h1>{key} 更新了 {len(value)} 个产品！</h1>"
        for line in value:

            str_screenshot =""
            count = 0
            for img in line['screenshotUrls']:
                str_screenshot += f"<img src='{img}'width='200'/>  "
                count = count+1
                if count>4: break

            tatallcount = tatallcount+1
            msgstr = msgstr + f"<p><a name='{line['bundleId']}'><b>{line['trackCensoredName']}</b></a><br><img src='{line['artworkUrl100']}'/><br>预览：<br>{str_screenshot}<br><br><a href='{line['trackViewUrl']}'>{line['trackViewUrl']}</a><br>上线日期：{line['releaseDate']}  <a href='#title'>返回</a></p><hr />"
            msg_tatall_str = msg_tatall_str+f"<a href='#{line['bundleId']}'><img src='{line['artworkUrl100']}' width='75'/></a>"

    if(msgstr==''):
        logstr= '没有更新'
        return logstr

    msgstr = f"<h1><b><a name='title'>本次更新了{tatallcount}个新产品</a></b><br>{msg_tatall_str}</h1><br>"+msgstr
    message = MIMEText(msgstr, "html", 'utf-8')
    #邮件主题
    message['Subject'] = title
    #发送方信息
    message['From'] = common_conifg['sender']
    #接受方信息
    message['To'] = receivers[0]

    #登录并发送邮件
    try:
        smtp = SMTP_SSL(common_conifg['mail_host'])
        #smtp.set_debuglevel(1)
        smtp.ehlo(common_conifg['mail_host'])
        smtp.login(common_conifg['mail_user'], common_conifg['mail_pass'])

        smtp.sendmail(common_conifg['sender'],receivers,message.as_string())
        smtp.quit()
    except smtplib.SMTPException as e:
        print('error',e)
    return logstr

#主函数
def main(path):
    campanyPath = path+"/TrackCampanyData/"
    configPath = path+"/"
    logPath = path+"/_Log/"

    #获取通用配置
    common_conifg = MyTools.get_file_to_dict(configPath,'=',"CommonConfig")

    #获取关注厂商列表并且分隔列表
    campanyList = MyTools.get_file_to_list(configPath,"CampanyList")
    campanyList = MyTools.split_liststr_to_list(campanyList,":")
    campanyList = MyTools.list_deduplication(campanyList)
    campanyList_split = MyTools.list_of_groups(campanyList,10)

    #分次抓取
    all_new_applist ={}
    for l in campanyList_split:
        campany = MyTools.list_to_str(l,",")
        #url = f"https://itunes.apple.com/lookup?id={0}&media=software&entity=software&country=us&limit=500"
        url = common_conifg['url'].format(f"{campany}")

        new_applist = parseInfo(getHtml(url),campanyPath)
        #all_new_applist = MyTools.merge_dicts(all_new_applist,new_applist)
        all_new_applist = dict(all_new_applist,**new_applist)
    wirteTrackIDList(all_new_applist,campanyPath)

    #发送邮件列表
    receivers = MyTools.get_file_to_list(configPath,"EmailList")
    #发送邮件
    logstring = sendEmail(all_new_applist,receivers,common_conifg)

    ##写入记录
    logfile=open(logPath+"log.txt",'a')
    logstr='更新时间: '+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + ' ' + logstring + '\n'
    os.system(f"echo '{logstr}'")
    logfile.write(logstr)
    logfile.close()

main(sys.argv[1])