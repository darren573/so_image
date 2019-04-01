from scrapy import Request, FormRequest
import scrapy


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['example.webscraping.com']
    start_urls = ['http://example.webscraping.com/user/profile']

    def parse(self, response):
        # 解析登录后下载的页面，此例中为用户个人信息页面
        keys = response.css('table label::text').re('(.+):')  # 主要包括名字，姓氏，邮箱等字段
        values = response.css('table td.w2p_fw::text').extract()  # 主要包括名字，姓氏，邮箱等字段的内容
        # keys = response.css('table label::text').re('(.+):')
        # values = response.css('table td.w2p_fw::text').extract()
        # 组成字典
        yield dict(zip(keys, values))

    # ----------------------------登录---------------------------------
    # 登录页面的url
    login_url = 'http://example.webscraping.com/user/login'

    def start_requests(self):
        yield Request(self.login_url, callback=self.login)

    def login(self, response):
        # 登录页面的解析函数，构造FormRequest对象提交表单
        fd = {'email': '1415754221@qq.com', 'password': 'darren573'}
        yield FormRequest.from_response(response, formdata=fd, callback=self.parse_login)

    def parse_login(self, response):
        # 登录成功后，继续爬取start_urls 中的页面
        if '欢迎shengen ' in response.text:
            yield from super().start_requests()  # Python 3语法
