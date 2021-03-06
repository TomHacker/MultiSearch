#coding=utf-8
"""
version 1.0
包含了所有的搜索类.有bing,google,sogou,即刻搜索.360搜索.baidu搜索.
"""
__author__ = 'DM_'

from printers import printGreen, printRed, printPink
import requests
import re
import sys

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'gb18030,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4'
}

SearchStr = "baidu"
Page = 1
SearchUrl = "http://cn.bing.com/search?q=%s&first=%d1&FORM=PERE" % (SearchStr, Page)

class bingSearch():
    """
    bing搜索.每页搜索10个.
    """
    def __init__(self, SearchStr, SearchPages=None,ProxiesEnable=False):
        self.SearchStr = SearchStr
        self.SearchPages = SearchPages
        self.SearchStatus = True
        self.HtmlData = []
        self.Urls = []
        self.ProxiesEnable = False
        if self.ProxiesEnable:
            pass
        else:
            pass

    def GetUrlsByGivenPages(self):
        for Page in xrange(0, self.SearchPages):
            try:
                req = requests.get("http://cn.bing.com/search?q=%s&first=%d1&FORM=PERE" %
                                   (self.SearchStr, Page),
                                   timeout=5,headers=headers)
                percent = int((1.0 * (Page+1) / self.SearchPages) * 100)
                printGreen("[+]Now is Loading Page %d,complete percent:%s." % (Page+1, str(percent) + '%'))
                sys.stdout.write('\r')

                self.HtmlData = req.content
                self.Urls.extend(re.findall(r'<li class="sa_wr">[\s\S]+?<h3><a href="([\s\S]+?)"[\s\S]+?</a></h3>[\s\S]+?</li>', self.HtmlData))
            except requests.RequestException:
                printRed("[-]Time Out. Please Check your connections.")
                break
        sys.stdout.write('\n')

    def GetUrlsBySearchALl(self):

        """
    默认搜索选项(搜索所有的链接).

    """
        SearchPage = 0
        while self.SearchStatus is not None:
            try:
                req = requests.get(
                    "http://cn.bing.com/search?q=%s&first=%d1&FORM=PERE" % (self.SearchStr, SearchPage)
                    , timeout=5, headers=headers)
                self.HtmlData = req.content

                printGreen("[+]Now is Loading Page %d.." % (SearchPage + 1))
                sys.stdout.write('\r')

                self.Urls.extend(re.findall(r'<li class="sa_wr">[\s\S]+?<h3><a href="([\s\S]+?)"[\s\S]+?</a></h3>[\s\S]+?</li>', self.HtmlData))
                self.SearchStatus = re.search(r'下一页', self.HtmlData)
                SearchPage += 1
            except requests.RequestException:
                printRed("[-]Time Out. Please Check your connections.")
                break
        printGreen(u'\n[+]一共查询了{0:d}页.\n'.format(SearchPage))

    def GetUrls(self):
        if self.SearchPages is None:
            self.GetUrlsBySearchALl()
        else:
            self.GetUrlsByGivenPages()
        printPink(u"[+]返回结果一共有%d条." % len(self.Urls))
        printPink(u"[!]去重后结果一共有%d条." % len(set(self.Urls)))


class googleSearch():
    """
    google搜索.每页搜索100个.
    """
    def __init__(self, SearchStr, SearchPages=None):
        self.SearchStr = SearchStr
        self.SearchPages = SearchPages
        self.SearchStatus = True
        self.HtmlData = []
        self.Urls = []

    def GetUrlsByGivenPages(self):
        for Page in xrange(1, self.SearchPages + 1):
            try:
                req = requests.get("http://203.208.46.176/search?q=%s&start=%d00&num=100" %
                                   (self.SearchStr, Page),
                                   timeout=5,headers=headers)
                percent = int((1.0 * Page / self.SearchPages) * 100)
                printGreen("[+]Now is Loading Page %d,complete percent:%s." % (Page, str(percent) + '%'))
                sys.stdout.write('\r')

                self.HtmlData = req.content
                self.Urls.extend(re.findall(r'<li class="g">[\s\S]+?href="([\s\S]+?)"[\s\S]+?</li>', self.HtmlData))
            except requests.RequestException:
                printRed("[-]Time Out. Please Check your connections.")
                break
        sys.stdout.write('\n')

    def GetUrlsBySearchALl(self):

        """
    默认搜索选项(搜索所有的链接).

    """
        SearchPage = 0
        while self.SearchStatus is not None:
            try:
                req = requests.get(#
                                   "http://203.208.46.176/search?q=%s&start=%d00&num=100" % (self.SearchStr, SearchPage)
                    , timeout=5, headers=headers)
                self.HtmlData = req.content

                printGreen("[+]Now is Loading Page %d.." % (SearchPage + 1))
                sys.stdout.write('\r')

                self.Urls.extend(re.findall(r'<li class="g">[\s\S]+?href="([\s\S]+?)"[\s\S]+?</li>', self.HtmlData))
                self.SearchStatus = re.search(r'下一页', self.HtmlData)
                SearchPage += 1
            except requests.RequestException:
                printRed("[-]Time Out. Please Check your connections.")
                break
        printGreen(u'\n[+]一共查询了{0:d}页.\n'.format(SearchPage))

    def GetUrls(self):
        if self.SearchPages is None:
            self.GetUrlsBySearchALl()
        else:
            self.GetUrlsByGivenPages()
        printPink(u"[+]返回结果一共有%d条." % len(self.Urls))
        printPink(u"[!]去重后结果一共有%d条." % len(set(self.Urls)))


class baiduSearch():
    """
    baidu搜索,每页搜索100个.
    """
    def __init__(self, SearchStr, SearchPages=None):
        """

        :param SearchStr:搜索关键词
        :param SearchPages: 是否有指定搜索前几页.
        """
        self.SearchStr = SearchStr
        self.SearchPages = SearchPages
        self.SearchStatus = True
        self.HtmlData = []
        self.Urls = []

    def GetUrlsByGivenPages(self):

        """
    如果给出查询的页面数量 则按给出的查询页面数量进行查询.默认搜索全部链接.

    :return: 返回所给页面的所有的搜索链接.
    """
        PagesNum = 0
        for Page in xrange(1, self.SearchPages + 1):
            try:
                req = requests.get("http://www.baidu.com/s?wd=%s&pn=%d00&ie=utf-8&rn=100" %
                                   (self.SearchStr, Page), timeout=5, headers=headers)
                self.HtmlData = req.content

                percent = int((1.0 * Page / self.SearchPages) * 100)
                printGreen("[+]Now is Loading Page %d,complete percent:%s." % (Page, str(percent) + '%'))
                sys.stdout.write('\r')

                BaiduUrls = re.findall(r'<h3 class="t">[\s\S]*?href="([\s\S]+?)"[\s\S]+?</h3>', self.HtmlData)
                for CacheUrl in BaiduUrls:
                    TryTime = 0
                    RetryTime = 3
                    while RetryTime > TryTime:
                        try:
                            if TryTime > 0:
                                print u"[-]Time Out. RetryTime:%d.." % TryTime
                            RealUrl = requests.head(CacheUrl, allow_redirects=False, timeout=5).headers['location']
                            self.Urls.append(RealUrl)
                            break
                        except requests.exceptions.Timeout:
                            TryTime += 1
                            pass
                PagesNum += 1
            except requests.RequestException:
                print "\n[-]Time Out. Please Check your connections.\n"
                break
        print u"\n[+]Work Done,%d pages worked.\n" % PagesNum

    def GetUrlsBySearchALl(self):

        """
    默认搜索选项(搜索所有搜狗给出的链接).

    :return: 所有的链接.
    """
        SearchPage = 0
        while self.SearchStatus is not None:
            try:
                req = requests.get("http://www.baidu.com/s?wd=%s&pn=%d00&ie=utf-8&rn=100" %
                                   (self.SearchStr, SearchPage),
                                   timeout=5, headers=headers)
                self.HtmlData = req.content

                printGreen("[+]Now is Loading Page %d.." % (SearchPage + 1))
                sys.stdout.write('\r')

                BaiduUrls = re.findall(r'<h3 class="t">[\s\S]*?href="([\s\S]+?)"[\s\S]+?</h3>', self.HtmlData)
                for CacheUrl in BaiduUrls:
                    TryTime = 0
                    RetryTime = 3
                    while RetryTime > TryTime:
                        try:
                            if TryTime > 0:
                                printRed("\n[-]Time out.Retrying.. %d ,Current url: %s.\n" % (TryTime, CacheUrl))
                            RealUrl = requests.head(CacheUrl, allow_redirects=False, timeout=5).headers['location']
                            self.Urls.append(RealUrl)
                            self.SearchStatus = re.search(r'下一页', self.HtmlData)
                            break
                        except requests.exceptions.Timeout:
                            TryTime += 1
                            pass
            except requests.RequestException:
                printRed("[-]Time Out. Please Check your connections.")
                break
            SearchPage += 1
        printGreen(u'\n[+]一共查询了{0:d}页.\n'.format(SearchPage))

    def GetUrls(self):
        """
    根据用户是否给出搜索的页面数量决定搜索的方法.

        """
        if self.SearchPages is None:
            self.GetUrlsBySearchALl()
        else:
            self.GetUrlsByGivenPages()
        printPink(u"[+]返回结果一共有%d条." % len(self.Urls))
        printPink(u"[!]去重后结果一共有%d条." % len(set(self.Urls)))



class so360Search():
    """
    360搜索.每页搜索10个
    """
    def __init__(self, SearchStr, SearchPages=None):
        self.SearchStr = SearchStr
        self.SearchPages = SearchPages
        self.SearchStatus = True
        self.HtmlData = []
        self.Urls = []


    def GetUrlsByGivenPages(self):

        """
    如果给出查询的页面数量 则按给出的查询页面数量进行查询.默认搜索全部链接.

    :return: 返回所给页面的所有的搜索链接.
    """
        for Page in xrange(1, self.SearchPages + 1):
            try:
                req = requests.get("http://www.so.com/s?ie=utf-8&q=%s&pn=%d" %
                                   (self.SearchStr, Page),
                                   timeout=5, headers=headers)
                percent = int((1.0 * Page / self.SearchPages) * 100)
                printGreen("[+]Now is Loading Page %d,complete percent:%s." % (Page, str(percent) + '%'))
                sys.stdout.write('\r')

                self.HtmlData = req.content
                self.Urls.extend(re.findall(r'<h3 class="res-title ">[\s]+?<a href="([\s\S]+?)"', self.HtmlData))
            except requests.RequestException:
                printRed("[-]Time Out. Please Check your connections.")
                break
        sys.stdout.write('\n')

    def GetUrlsBySearchALl(self):

        """
    默认搜索选项(搜索所有360搜索给出的链接).

    :return: 所有的链接.
    """
        SearchPage = 0
        while self.SearchStatus is not None:
            try:
                req = requests.get(
                    "http://www.so.com/s?ie=utf-8&q=%s&pn=%d" % (self.SearchStr, (SearchPage + 1))
                    , timeout=5, headers=headers)
                self.HtmlData = req.content

                printGreen("[+]Now is Loading Page %d.." % (SearchPage + 1))
                sys.stdout.write('\r')

                self.Urls.extend(re.findall(r'<h3 class="res-title ">[\s]+?<a href="([\s\S]+?)"', self.HtmlData))
                self.SearchStatus = re.search('id="snext"', self.HtmlData)
                SearchPage += 1
            except requests.RequestException:
                printRed("[-]Time Out. Please Check your connections.")
                break
        printGreen(u'\n[+]一共查询了{0:d}页.\n'.format(SearchPage))

    def GetUrls(self):
        if self.SearchPages is None:
            self.GetUrlsBySearchALl()
        else:
            self.GetUrlsByGivenPages()
        printPink(u"[+]返回结果一共有%d条." % len(self.Urls))
        printPink(u"[!]去重后结果一共有%d条." % len(set(self.Urls)))


class jikeSearch():
    """
    即刻搜索,每页搜索10个.
    """
    def __init__(self, SearchStr, SearchPages=None):
        self.SearchStr = SearchStr
        self.SearchPages = SearchPages
        self.SearchStatus = True
        self.HtmlData = []
        self.Urls = []

    def GetUrlsByGivenPages(self):
        """

        :return:
        """
        for Page in xrange(1, self.SearchPages + 1):
            try:
                req = requests.get("http://www.jike.com/so?q=%s&page=%d" % (self.SearchStr, Page),
                                   timeout=5, headers=headers)
                percent = int((1.0 * Page / self.SearchPages) * 100)
                printGreen("[+]Now is Loading Page %d,complete percent:%s." % (Page, str(percent) + '%'))
                sys.stdout.write('\r')
                self.HtmlData = req.content
                self.Urls.extend(
                    re.findall(r'_dom_name="\d">[\s\S]+?div class="T1"><a href="([\s\S]+?)"', self.HtmlData))
            except requests.RequestException:
                printRed("[-]Time Out. Please Check your connections.")
                break
        sys.stdout.write('\n')
        return self.Urls

    def GetUrlsBySearchAll(self):
        """
    通过jike搜索获取所有的链接.

        """
        SearchPage = 0
        while self.SearchStatus is not None:
            try:
                req = requests.get("http://www.jike.com/so?q=%s&page=%d" % (self.SearchStr, SearchPage + 1),
                                   timeout=5, headers=headers)
                self.HtmlData = req.content
                printGreen("[+]Now is Loading Page %d.." % (SearchPage + 1))
                sys.stdout.write('\r')
                self.Urls.extend(
                    re.findall(r'_dom_name="\d">[\s\S]+?div class="T1"><a href="([\s\S]+?)"', self.HtmlData))
                self.SearchStatus = re.search(r"下一页", self.HtmlData)
                SearchPage += 1
            except requests.RequestException:
                printRed("[-]Time Out. Please Check your connections.")
                self.SearchStatus = None
                break
        printGreen(u"\n[+]一共通过jike.com获取到了%d页链接. \n" % SearchPage)

    def GetUrls(self):
        if self.SearchPages is None:
            self.GetUrlsBySearchAll()
        else:
            self.GetUrlsByGivenPages()
        printPink(u"[+]返回结果一共有%d条." % len(self.Urls))
        printPink(u"[!]去重后结果一共有%d条." % len(set(self.Urls)))


class sogouSearch():
    """
    搜狗搜索.每页搜索100个.
    """
    def __init__(self, SearchStr, SearchPages=None):
        self.SearchStr = SearchStr
        self.SearchPages = SearchPages
        self.SearchStatus = True
        self.HtmlData = []
        self.Urls = []


    def GetUrlsByGivenPages(self):

        """
    如果给出查询的页面数量 则按给出的查询页面数量进行查询.默认搜索全部链接.

    :return: 返回所给页面的所有的搜索链接.
    """
        for Page in xrange(1, self.SearchPages + 1):
            try:

                req = requests.get("http://www.sogou.com/web?query=%s&page=%d&num=100" %
                                   (self.SearchStr, self.SearchPages),
                                   timeout=5)
                self.HtmlData = req.content

                percent = int((1.0 * Page / self.SearchPages) * 100)
                printGreen("[+]Now is Loading Page %d,complete percent:%s." % (Page, str(percent) + '%'))
                sys.stdout.write('\r')

                self.Urls.extend(re.findall(r'id="uigs_d0_\d{1,2}" href="([\s\S]+?)"', self.HtmlData))

            except requests.RequestException:
                printRed("[-]Time Out. Please Check your connections.")
                break
        sys.stdout.write('\n')

    def GetUrlsBySearchALl(self):

        """
    默认搜索选项(搜索所有搜狗给出的链接).

    :return: 所有的链接.
    """
        SearchPage = 0
        while self.SearchStatus is not None:
            try:
                req = requests.get(
                    "http://www.sogou.com/web?query={0:s}&page={1:d}&num=100".format(self.SearchStr, (SearchPage + 1))
                    , timeout=5)
                printGreen("[+]Now is Loading Page %d.." % (SearchPage + 1))
                sys.stdout.write('\r')
                self.HtmlData = req.content
                self.Urls.extend(re.findall(r'id="uigs_d0_\d{1,2}" href="([\s\S]+?)"', self.HtmlData))
                self.SearchStatus = re.search('sogou_next', self.HtmlData)
                SearchPage += 1
            except requests.RequestException:
                break
        printGreen(u'\n[+]一共查询了{0:d}页.\n'.format(SearchPage))


    def GetUrls(self):
        if self.SearchPages is None:
            self.GetUrlsBySearchALl()
        else:
            self.GetUrlsByGivenPages()
        printPink(u"[+]返回结果一共有%d条." % len(self.Urls))
        printPink(u"[!]去重后结果一共有%d条." % len(set(self.Urls)))
