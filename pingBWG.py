#coding: utf-8
import configparser
import os
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

#获取当前工作目录，用于拼接配置文件目录
workpath = os.getcwd()
#print workpath+'\\config.ini'
#主要linux环境下斜杠是反的！ 要用/
cf = configparser.ConfigParser()
cf.read(workpath+'\\config.ini')


'''
# 获取文件中所有的section(一个配置文件中可以有多个配置，如数据库相关的配置，邮箱相关的配置，每个section由[]包裹，即[section])，并以列表的形式返回
secs = cf.sections()
#print secs

# 获取某个section名为Mysql-Database所对应的键
options = cf.options("BWG_host")
#print(options)

# 获取section名为Mysql-Database所对应的全部键值对
items = cf.items("BWG_host")
#print(items)

# 获取[Mysql-Database]中host对应的值
host = cf.get("BWG_host", "addr")
#print(host)
'''
addr = cf.get("BWG_host", "addr")

mail_to = cf.get("Email", "mail_to")
mail_host = cf.get("Email", "mail_host")
mail_user = cf.get("Email", "mail_user")
mail_pass = cf.get("Email", "mail_pass")


'''
getBanwagongIP=cf.get("BWG_host", "addr")
#由于测IP需要时间，所以等待30秒，再去结果
print("detecting IP address, waiting 30s ......")
pingcmd="timeout 30 ping -c 4 " + getBanwagongIP + "|grep transmitted|awk -F ',' {'print $2'}|awk {'print $1'}"
#print pingcmd
sp=subprocess.Popen(pingcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdoutdata = sp.stdout.read().strip()
recvpackages = int(stdoutdata)
#print recvpackages
'''

def sendmail(mail_to,mail_host,mail_user,mail_pass,subject,mailmsg):

  encoding="utf-8"
  msg=MIMEText(mailmsg,'html','utf-8')
  #若需要发送附件，必须采用MIMEMultipart()
  msgRoot = MIMEMultipart()
  msgRoot['Subject']=Header(subject,encoding)
  msgRoot['From'] = mail_user
  msgRoot['To'] = mail_to
  #添加邮件正文
  msgRoot.attach(msg)
  try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host)
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(mail_user,mail_to, msgRoot.as_string())
    smtpObj.close()
    print "mail send success"
  except smtplib.SMTPException:
    print "Error: can't send mail"

recvpackages = 4
if recvpackages == 4:
  detectmsg = "addr can be arrived"
  print detectmsg
  detecttag=0
  sendmail(mail_to,mail_host,mail_user,mail_pass,"BWG can be reached!",detectmsg)
elif recvpackages == 0:
  detectmsg = "addr is refused"
  print detectmsg
  detecttag=2
  #sendmail(mailto,mail_host,mail_user,mail_pass,subject,detectmsg)
else:
  detectmsg = "addr can be arrived"
  print detectmsg
  detecttag=1
  sendmail(mail_to,mail_host,mail_user,mail_pass,"BWG can be reached!",detectmsg)


