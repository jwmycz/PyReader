对reader的规则进行了扩充和一些小修改

{
    "book_sources": [
        {
            "title": "平凡文学",    //网站名，可重复
            "host": "http://www.pksge.la",  //网站主页，不可重复
            "query_url": "http://www.pksge.la/modules/article/search.php",  //搜索链接
            "query_method": "POST",    //搜索链接类型'POST','GET'
            "query_params": "searchkey=%s&searchtype=articlename",  //搜索参数
            "query_charset": 1,   //使用编码格式，默认UTF-8,为1时为UTF-8，为2时为GBK
            "query_types":	"Data",  //搜索发送参数类型，'Data','Json',两种
            "book_name_xpath": "//div[@class=\"tutuiTitle\"]/h2/a/@title",  //搜索后小说名XPATH
            "book_mainpage_xpath": "//div[@class=\"tutuiTitle\"]/h2/a/@href",  //搜索后小说链接XPATH
            "book_author_xpath": "//div[@class=\"tutuiTitle\"]/h3[1]/text()", //搜索后小说作者XPATH
            "enable_chapter_page": 0,  //未适配
            "chapter_page_xpath": "", //未适配
            "chapter_title_xpath": "//div[@class='zhangjiekaishi']/ul/li/a/text()",  //目录标题XPATH
            "chapter_url_xpath": "//div[@class='zhangjiekaishi']/ul/li/a/@href",  //目录链接XPATH
            "enable_chapter_next": 0,  //目录是否开启下一页
            "chapter_next_url_xpath": "",  //下一页目录链接XPATH
            "chapter_next_keyword_xpath": "",  //下一页名字XPATH
            "chapter_next_keyword": "",  //下一页名字，与下一页名字XPATH对比
            "content_xpath": "//*[@id=\"booktext\"]/text()",  //章节内容XPATH
            "enable_content_next": 0,  //章节内容是否有下一页
            "content_search_url_bool": true,   //章节内容是否复用小说链接进行拼接
            "content_next_url_xpath": "",  //章节内容下一页XPATH
            "content_next_keyword_xpath": "",  //章节内容下一页名字XPATH
            "content_next_keyword": "",  //章节内容下一页名字，与章节内容下一页名字XPATH对比
            "content_filter_type": 0,  //无文本过滤0，关键字过滤1，正则过滤未匹配
            "content_filter_keyword": ""
        }
    ]
}