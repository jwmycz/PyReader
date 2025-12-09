from . import *
from utils.tools import *
from lxml import etree
class ReaderRuleHttp(HttpRule):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def get_rule(self):
        if self.rule:
            source=self.rule
            logger.debug(source)
            self.title=source.get('title','').strip()
            self.host=source.get('host','').strip()
            self.query_url=source.get('query_url','').strip()
            self.query_method=source.get('query_method','')
            self.query_params=source.get('query_params','')
            self.query_types=source.get('query_types','Data')
            self.query_charset=source.get('query_charset','')
            self.book_name_xpath=source.get('book_name_xpath','')
            self.book_mainpage_xpath=source.get('book_mainpage_xpath','')
            self.book_author_xpath=source.get('book_author_xpath','')
            self.enable_chapter_page=source.get('enable_chapter_page','')
            self.chapter_page_xpath=source.get('chapter_page_xpath','')
            self.chapter_title_xpath=source.get('chapter_title_xpath','')
            self.chapter_url_xpath=source.get('chapter_url_xpath','')
            self.enable_chapter_next=source.get('enable_chapter_next','')
            self.chapter_next_url_xpath=source.get('chapter_next_url_xpath','')
            self.chapter_next_keyword_xpath=source.get('chapter_next_keyword_xpath','')
            self.chapter_next_keyword=source.get('chapter_next_keyword','')
            self.content_xpath=source.get('content_xpath','')
            self.enable_content_next=source.get('enable_content_next','')
            self.content_next_url_xpath=source.get('content_next_url_xpath','')
            self.content_next_keyword_xpath=source.get('content_next_keyword_xpath','')
            self.content_next_keyword=source.get('content_next_keyword','')
            self.content_filter_type=source.get('content_filter_type','')
            self.content_filter_keyword=source.get('content_filter_keyword','')

    def get_encode(self):
        if self.query_charset==1 or self.query_types==0:
            charset='utf-8'
        elif self.query_charset==2:
            charset='gbk'
        else:
            charset='utf-8'
        return charset
    async def get_title(self, search_name):
        data = None
        keyword = search_name.strip()
        charset = self.get_encode()
        if not is_url(keyword):
            keyword = urllib.parse.quote(keyword,encoding=charset)
        try:
            if self.query_method == "GET":
                url = self.query_url.replace('%s', keyword)
                logger.debug(url)
                data = await self.get(url)
            elif self.query_method == "POST":
                params = self.query_params.replace('%s', keyword)
                logger.debug(params)
                if self.query_types == "Json":
                    data = await self.post(self.query_url, json=params)
                elif self.query_types == "Data":
                    headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
                    data = await self.post(self.query_url, data=params,headers=headers)

                else:
                    logger.warning(f"未处理的 query_charset: {self.query_types}")

            else:
                logger.warning(f"未处理的 query_method: {self.query_method}")

        except Exception as e:
            logger.warning("get_title 请求异常:", e)
            return None

        if not data:
            logger.warning("请求无数据返回")
            return None
        return await self._get_title(data)

    async def _get_title(self, data):
        if data.status_code != 200:
            return None
        charset = self.get_encode()
        data.encoding=charset
        xmls=etree.HTML(data.text)
        logger.debug(data.text)
        book_name_list=xmls.xpath(self.book_name_xpath)
        book_mainpage_list=xmls.xpath(self.book_mainpage_xpath)
        if self.book_author_xpath:
            book_author_list = xmls.xpath(self.book_author_xpath)
        else:
            book_author_list = []

        logger.debug(book_name_list)
        logger.debug(book_mainpage_list)
        logger.debug(book_author_list)
        max_len = max(len(book_name_list), len(book_mainpage_list), len(book_author_list))
        records = []

        for i in range(max_len):
            name = book_name_list[i] if i < len(book_name_list) else ""
            mainpage = book_mainpage_list[i] if i < len(book_mainpage_list) else ""
            author = book_author_list[i] if i < len(book_author_list) else ""

            record = f"{name} | {author} | {mainpage}"
            records.append(record)

        return records

    async def get_change_book(self, data):
        page_list = []
        title_list = []
        url_list = []

        newdata = data.strip().split('|')
        url = self.host.strip() + newdata[2].strip()

        while url:
            try:
                # 异步请求
                response = await self.get(url)

                charset = self.get_encode()
                response.encoding=charset
                text=response.text
                xls = etree.HTML(text)

                # xpath解析
                chapter_pages = xls.xpath(self.chapter_next_url_xpath) or []
                chapter_titles = xls.xpath(self.chapter_title_xpath) or []
                chapter_urls = xls.xpath(self.chapter_url_xpath) or []

                page_list.extend(chapter_pages)
                title_list.extend(chapter_titles)
                url_list.extend(chapter_urls)
                if self.enable_chapter_next != 1:
                    break

                nexturl_list = xls.xpath(self.chapter_next_url_xpath) or []
                keyword_list = xls.xpath(self.chapter_next_keyword_xpath) or []

                if nexturl_list and keyword_list and keyword_list[0] == self.chapter_next_keyword:
                    url = self.host.strip() + nexturl_list[0]
                else:
                    break
            except Exception as e:
                logger.error("获取章节失败:", e)
                break
        return page_list, title_list, url_list

    async def get_content(self,url):
        nowurl=self.host.strip()+url.strip()
        response=await self.get(nowurl)
        charset = self.get_encode()
        response.encoding = charset
        text = response.text
        xls = etree.HTML(text)
        content=xls.xpath(self.content_xpath)
        ct=''
        for i in content:
            ct=ct + i
        return ct