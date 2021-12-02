from scrapy import Request, Spider
from scrapy.http import HtmlResponse
from wiki_mipt.items import MiptLecturer


class LecturersSpider(Spider):
    name = "lecturers"

    def start_requests(self):
        urls = [
            "http://wikimipt.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D1%80%D0%B5%D0%BF%D0%BE%D0%B4%D0%B0%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D0%B8_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83",
        ]
        for url in urls:
            yield Request(url=url, callback=self.parse_lecturers_list)

    def parse_lecturers_list(self, response: HtmlResponse):
        """Собираем ссылки на лекторов и делаем реквесты по ним.
        Так же ищем следующую страницу, если она существует - переходим.
        """
        lecturers_xpath = "//div[@class='mw-category-group']/ul/li/a/@href"
        lecturers = response.xpath(lecturers_xpath).getall()
        for lecturer_url in lecturers:
            lecturer_url = response.urljoin(lecturer_url)
            yield Request(url=lecturer_url, callback=self.parse_lecturer_data)

        next_page = response.xpath('//div[@id="mw-pages"]/a[2]/@href').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield Request(url=next_page_url, callback=self.parse_lecturers_list)

    def parse_lecturer_data(self, response: HtmlResponse):
        """Просто парсим данные"""
        profile = MiptLecturer()

        profile["full_name"] = response.xpath("//h1[@id='firstHeading']/text()").get()

        birth_xpath = "//th[contains(text(),'Дата рождения')]/../td/text()"
        profile["birth_day"] = response.xpath(birth_xpath).get()

        teach_place_xpath = "//th[contains(text(),'Работает')]/../td/ul/li/a/text()"
        profile["teach_place"] = response.xpath(teach_place_xpath).get()

        degree_xpath = "//th[contains(text(),'Учёная степень')]/../td/text()"
        profile["degree"] = response.xpath(degree_xpath).get()

        knowledge_xpath = "//td[contains(text(),'Знания')]/../td/div/span/text()"
        profile["knowledge"] = response.xpath(knowledge_xpath).get()

        teaching_xpath = (
            "//td[contains(text(),'Умение преподавать')]/../td/div/span/text()"
        )
        profile["teaching_skill"] = response.xpath(teaching_xpath).get()

        commication_xpath = "//td[contains(text(),'В общении')]/../td/div/span/text()"
        profile["commication_skill"] = response.xpath(commication_xpath).get()

        easy_xpath = "//td[contains(text(),'«Халявность»')]/../td/div/span/text()"
        profile["easy_exam"] = response.xpath(easy_xpath).get()

        overall_xpath = "//td[contains(text(),'Общая оценка')]/../td/div/span/text()"
        profile["overall_score"] = response.xpath(overall_xpath).get()

        yield profile
