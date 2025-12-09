from urllib.parse import quote
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
            self.content_filter_type=source.get('content_filter_type',0)
            self.content_filter_keyword=source.get('content_filter_keyword','')
            self.content_search_url_bool=source.get('content_search_url_bool',False)

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
            keyword = quote(keyword,encoding=charset)
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

    # async def get_change_book(self, data):
    #     title_list = []
    #     url_list = []
    #
    #     newdata = data.strip().split('|')
    #     raw_url = newdata[2].strip()
    #     url = raw_url if raw_url.startswith("http") else self.host.strip() + raw_url
    #     self.searchurl=url
    #     visited = set()  # 防死循环
    #     while url:
    #         if url in visited:
    #             logger.warning(f"重复页面检测到, 停止抓取: {url}")
    #             break
    #         visited.add(url)
    #
    #         try:
    #             response = await self.get(url)
    #             # print(response.text)
    #             charset = self.get_encode()
    #             if charset:
    #                 response.encoding = charset
    #             xls = etree.HTML(response.text)
    #             print(response.text)
    #             # 解析标题和链接
    #             print(self.chapter_title_xpath)
    #             print(self.chapter_url_xpath)
    #             titles = [t for t in xls.xpath(self.chapter_title_xpath) or []]
    #             urls = [u for u in xls.xpath(self.chapter_url_xpath) or []]
    #             print(urls)
    #             print(titles)
    #             # 对齐长度，防止错位
    #             min_len = min(len(titles), len(urls))
    #             title_list.extend(titles[:min_len])
    #             url_list.extend(urls[:min_len])
    #
    #
    #             if self.enable_chapter_next != 1:
    #                 break
    #
    #             # 下一页处理
    #             nexturl_list = xls.xpath(self.chapter_next_url_xpath) or []
    #             keyword_list = xls.xpath(self.chapter_next_keyword_xpath) or []
    #
    #             if not nexturl_list or not keyword_list:
    #                 break
    #
    #             # 符合关键字才继续
    #             if keyword_list[0].strip() == self.chapter_next_keyword:
    #                 next_url = nexturl_list[0].strip()
    #                 url = next_url if next_url.startswith("http") else self.host.strip() + next_url
    #             else:
    #                 break
    #
    #         except Exception as e:
    #             logger.error(f"章节抓取失败: {e}")
    #             break
    #
    #     return title_list, url_list
    def normalize_url(self, u: str):
        u = u.strip()
        # 去掉末尾多余的斜杠
        if u.endswith("/"):
            u = u[:-1]
        return u

    async def get_change_book(self, data):
        title_list = []
        url_list = []

        raw_url = data.strip().split('|')[2].strip()
        url = raw_url if raw_url.startswith("http") else self.host.strip() + raw_url
        # url = self.normalize_url(url)
        self.searchurl = url
        print(url)
        visited = set()

        while True:
            if url in visited:
                logger.warning(f"重复页面检测到，停止抓取: {url}")
                break
            visited.add(url)

            try:
                print(f'列表{url}')
                response = await self.get(url)
                charset = self.get_encode()
                if charset:
                    response.encoding = charset
                xls = etree.HTML(response.text)
                print(response.text)
                titles = xls.xpath(self.chapter_title_xpath) or []
                print(titles)
                urls = xls.xpath(self.chapter_url_xpath) or []
                print(urls)
                min_len = min(len(titles), len(urls))
                title_list.extend(titles[:min_len])
                url_list.extend(urls[:min_len])

                if self.enable_chapter_next != 1:
                    break

                # 优先分页 XPath
                nexturl_list = []
                if self.enable_chapter_page == 1:
                    nexturl_list = xls.xpath(self.chapter_page_xpath) or []
                    logger.debug(f"page mode:{nexturl_list}")

                if nexturl_list:
                    next_url = nexturl_list[0].strip()
                else:
                    nexturl_list = xls.xpath(self.chapter_next_url_xpath) or []
                    keyword_list = xls.xpath(self.chapter_next_keyword_xpath) or []

                    # logger.debug(f"next mode:{nexturl_list} {keyword_list}")

                    if not nexturl_list or not keyword_list:
                        break

                    if keyword_list[0].strip() != self.chapter_next_keyword:
                        break

                    next_url = nexturl_list[0].strip()

                new_url = next_url if next_url.startswith("http") else self.host.strip() + next_url
                new_url = self.normalize_url(new_url)

                # 如果 URL 未变化则退出防死循环
                if new_url == url:
                    logger.warning(f"下一页地址未变化，终止抓取: {new_url}")
                    break

                url = new_url

            except Exception as e:
                logger.error(f"章节抓取失败: {e}")
                break

        return title_list, url_list

    async def get_content(self, url):
        contents = []
        if self.content_search_url_bool==True:
            url =self.searchurl+url.strip()
        if not url.startswith("http"):
            url = self.host.strip() + url.strip()
        print(url)
        while url:
            try:
                response = await self.get(url)
                charset = self.get_encode()
                response.encoding = charset
                text = response.text
                print(text)
                xls = etree.HTML(text)

                # 获取正文，并清洗空格与 HTML 垃圾标签
                content_list = xls.xpath(self.content_xpath) or []
                cleaned = [
                    ''.join(item).strip().replace('\u3000', '').replace('\xa0', '')
                    for item in content_list
                ]
                print(cleaned)
                contents.extend(cleaned)

                # 如果不支持翻页，退出
                if self.enable_content_next != 1:
                    break

                # 下一页提取
                next_url_list = xls.xpath(self.content_next_url_xpath) or []
                keyword_list = xls.xpath(self.content_next_keyword_xpath) or []

                # 校验安全性
                if not next_url_list or not keyword_list:
                    break

                if keyword_list[0] == self.content_next_keyword:
                    next_url = next_url_list[0].strip()
                    if not next_url.startswith("http"):
                        next_url = self.host.strip() + next_url
                    url = next_url
                else:
                    break
            except Exception as e:
                print("内容提取失败:", e)
                break

        # 快速拼接字符串，提高性能
        final_text = "\n\n".join(contents)
        if self.content_filter_type==1:
            final_text=final_text.replace(self.content_filter_keyword, " ")
        return final_text
