#coding=GBK
__author__ = 'DM_'
import os,re,time

def __WriteFile(SaveUrls, FilePath, Regex=False):
    if Regex:
        LogFile = open(FilePath, "a")

        for url in SaveUrls:
            if re.findall(Regex, url):
#                url = re.findall(Regex, url)
#                LogFile.write(url[0] + '\n')
                LogFile.write(url + '\n')

        print(u"�ļ��ѱ����� %s" % FilePath)
    else:
        LogFile = open(FilePath, "a")
        for url in SaveUrls:
            LogFile.write(url + '\n')
        print(u"�ļ��ѱ�����ָ���ļ���,·���� %s." % FilePath)

def SaveLog(SaveUrls,FilePath,Regex=False):
    DefaultFilePath = "output\\%s_LogUrls" % str(time.strftime('%Y-%m-%d-%S',time.localtime(time.time())))

    if FilePath is False:
        FilePath = DefaultFilePath + "_Default.txt"

    if Regex is False:
            if os.path.exists(FilePath):
                print(u"[!]�ļ��Ѵ���,�Ƿ񸲸�?[y/n]")
                Fj = raw_input()
                if Fj == 'y' or Fj == '':
                    __WriteFile(SaveUrls, FilePath)
                else:
                    __WriteFile(SaveUrls,DefaultFilePath + "_RAW.txt")
            else:
                __WriteFile(SaveUrls, FilePath)

    else:
        print(u"����������ѡ��.�Ƿ���н�������ļ�?[y/n]")
        Fj = raw_input()
        if Fj == 'y' or Fj == '':
            BakFilePath = raw_input("�����뱸���ļ���ַ:")
            try:
                __WriteFile(SaveUrls, BakFilePath)
            except:
                print(u"�ļ�����ʧ��,��д��Ĭ�ϼ�¼�ļ�.LogUrls_bak.txt")
                __WriteFile(SaveUrls, DefaultFilePath + "_BAK.txt")
        else:
            if os.path.exists(FilePath):
                print(u"[!]��д�������ƥ���ļ��Ѵ���,�Ƿ񸲸�?[y/n]")
                Fj = raw_input()
                if Fj == 'y' or Fj == '':
                    __WriteFile(SaveUrls, FilePath, Regex)
                else:
                    __WriteFile(SaveUrls, (DefaultFilePath + "_regex.txt"),Regex)
            else:
                __WriteFile(SaveUrls, FilePath, Regex)
