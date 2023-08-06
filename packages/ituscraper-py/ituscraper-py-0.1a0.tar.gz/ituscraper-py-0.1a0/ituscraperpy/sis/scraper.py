from bs4 import BeautifulSoup
import requests
from .classes import Course

COURSE_SCHEDULES_MAIN_URL = "https://www.sis.itu.edu.tr/EN/student/course-schedules/course-schedules.php"
COURSE_SCHEDULES_LEVEL_PARAMETER = "?seviye="
COURSE_SCHEDULES_CODE_PARAMETER = "&derskodu="
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

class CourseScraper():
    def __init__(self, level: str = "LS", main_url: str = COURSE_SCHEDULES_MAIN_URL,
                 headers: dict = HEADERS):
        self.level = level
        if (self.level not in ["LS", "LU"]):
            raise ValueError("Level must be either LS or LU")
        self.main_url = main_url
        self.headers = headers
        self.course_codes = None

    def get_course_codes(self):
        __page = requests.get(self.main_url + COURSE_SCHEDULES_LEVEL_PARAMETER + self.level,
                              headers=self.headers)
        if __page.status_code != 200:
            raise ValueError("Error code: {}.".format(__page.status_code))

        __soup = BeautifulSoup(__page.content, "lxml")
        __codes = __soup.find("select", attrs={"name": "derskodu"}).findAll("option")
        if (len(__codes) < 2):
            raise ValueError("No course codes found.")
        __codes = [c.text.strip() for c in __codes]
        __codes.pop(0)
        self.course_codes = __codes
        return self.course_codes

    def get_course_classes(self, code: str) -> list:
        __course_page_url = self.main_url + COURSE_SCHEDULES_LEVEL_PARAMETER \
                          + self.level + COURSE_SCHEDULES_CODE_PARAMETER \
                          + code

        __page = requests.get(__course_page_url)
        if __page.status_code != 200:
            raise ValueError("Error code: {}.".format(__page.status_code))


        __soup = BeautifulSoup(__page.content, "lxml")
        __classes_raw = __soup \
            .find("table",
                  attrs={"class": "table "
                                  "table-bordered "
                                  "table-striped "
                                  "table-hover "
                                  "table-responsive"}).findAll("tr")
        if (len(__classes_raw) < 3):
            raise ValueError("No classes found.")
        __classes_raw.pop(0)
        __classes_raw.pop(0)

        __classes = []
        for row in __classes_raw:
            columns = row.findAll("td")
            if(len(columns) != 15):
                raise ValueError("Invalid number of columns.")
            __classes.append(
                Course(*[c.text for c in columns])
            )

        return __classes


