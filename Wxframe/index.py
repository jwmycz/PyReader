from LogRecord.record import logger
from rules import write_reader_rules,read_reader_rules
from HttpRule.ReaderRuleHttp import ReaderRuleHttp
import threading
import asyncio
from . import *
from utils.AWord import aword


# 统一一个后台事件循环
loop = asyncio.new_event_loop()
threading.Thread(target=loop.run_forever, daemon=True).start()

def run_async(coro):
    asyncio.run_coroutine_threadsafe(coro, loop)
class MainFrame(MyFrame1):
    def __init__(self,parent):
        super().__init__(parent)

        self.timer = wx.Timer(self)
        self.timer.Start(60000)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)

        # 启动线程刷新
        self.start_update_thread()

        # 初始化参数
        self.book_sources=None
        self.rules=None
        self.req=None
        self.page_list=None
        self.title_list=None
        self.url_list=None

    def start_update_thread(self):
        t = threading.Thread(target=self.update_label_thread, daemon=True)
        t.start()

    def update_label_thread(self):
        """后台线程执行耗时任务"""
        new_text = aword()  # 耗时操作放后台
        wx.CallAfter(self.update_label_ui, new_text)

    def update_label_ui(self, text):
        """主线程更新控件"""
        self.m_staticText1.SetLabel(text)
        self.Layout()
        self.Refresh()

    def on_timer(self, event):
        self.start_update_thread()

    def on_close(self, event):
        if self.timer.IsRunning():
            self.timer.Stop()
        self.Destroy()



    def Selereader(self, event):
        dialog = wx.FileDialog(
            self,
            message="选择 Reader 源文件",
            wildcard="源文件 (*.json;*.txt)|*.json;*.txt|所有文件 (*.*)|*.*",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )

        if dialog.ShowModal() == wx.ID_OK:
            filepath = dialog.GetPath()
            logger.debug(f"选择文件:{filepath}")
            with open(filepath,'r',encoding='utf-8') as f:
                reads=f.read()
            write_reader_rules(reads)
        dialog.Destroy()


    def load_reader( self, event ):
        book_sources=read_reader_rules()
        self.book_sources=book_sources
        alltitle=[]
        if book_sources:
            for source in book_sources:
                logger.debug(source)
                title=source.get('title','')
                alltitle.append(title)
                # host=source.get('host','')
                # query_url=source.get('query_url','')
                # query_method=source.get('query_method','')
                # query_params=source.get('query_params','')
                # query_charset=source.get('query_charset','')
                # book_name_xpath=source.get('book_name_xpath','')
                # book_mainpage_xpath=source.get('book_mainpage_xpath','')
                # book_author_xpath=source.get('book_author_xpath','')
                # enable_chapter_page=source.get('enable_chapter_page','')
                # chapter_page_xpath=source.get('chapter_page_xpath','')
                # chapter_title_xpath=source.get('chapter_title_xpath','')
                # chapter_url_xpath=source.get('chapter_url_xpath','')
                # enable_chapter_next=source.get('enable_chapter_next','')
                # chapter_next_url_xpath=source.get('chapter_next_url_xpath','')
                # chapter_next_keyword_xpath=source.get('chapter_next_keyword_xpath','')
                # chapter_next_keyword=source.get('chapter_next_keyword','')
                # content_xpath=source.get('content_xpath','')
                # enable_content_next=source.get('enable_content_next','')
                # content_next_url_xpath=source.get('content_next_url_xpath','')
                # content_next_keyword_xpath=source.get('content_next_keyword_xpath','')
                # content_next_keyword=source.get('content_next_keyword','')
                # content_filter_type=source.get('content_filter_type','')
                # content_filter_keyword=source.get('content_filter_keyword','')
            logger.debug(alltitle)
            self.m_comboBox1.Set(alltitle)

    def change_rule(self, event):
        search_keyword = self.m_comboBox1.GetValue()
        for source in self.book_sources:
            if search_keyword in source.get('title',''):
                self.rules = source


    def Search(self, event):
        wx.CallAfter(self.m_comboBox2.Set, [])
        search_name = self.m_textCtrl1.GetValue().strip()
        if not search_name:
            return
        run_async(self._Search(search_name))
        # asyncio.create_task(self._Search(search_name))

    async def _Search(self, search_name):
        req = ReaderRuleHttp(rule=self.rules)
        self.req=req
        req.get_rule()
        try:
            result = await req.get_title(search_name)
        except Exception as e:
            logger.error(e)
            result = []
        if result:
            wx.CallAfter(self.m_comboBox2.Set, result)


    def change_book(self, event):
        wx.CallAfter(self.m_listBox1.Set, [])
        data=self.m_comboBox2.GetValue()
        logger.debug(f'选择书籍--》{data}')
        if not data:
            return
        run_async(self._get_change_book(data))

    async def _get_change_book(self, data):
        try:
            page_list, title_list, url_list = await self.req.get_change_book(data)

        except Exception as e:
            logger.error(e)
            page_list, title_list, url_list = []
        self.page_list=page_list
        self.title_list=title_list
        self.url_list=url_list
        if title_list:
            wx.CallAfter(self.m_listBox1.Set, title_list)

    def get_content(self, event):
        wx.CallAfter(self.m_textCtrl2.SetValue, '')
        idx = self.m_listBox1.GetSelection()
        if idx == wx.NOT_FOUND:
            wx.MessageBox("请先选择一个章节！", "提示", wx.OK | wx.ICON_INFORMATION)
            return
        url_name = self.url_list[idx]
        if not url_name:
            return
        run_async(self._get_content(url_name))

    async def _get_content(self, url_name):
        try:
            content= await self.req.get_content(url_name)
        except Exception as e:
            logger.error(e)
            content= ''
        wx.CallAfter(self.m_textCtrl2.SetValue, content)