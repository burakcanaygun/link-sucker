import requests
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, InvalidSessionIdException
import pandas as pd
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument('--no-sandbox')
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 '
    'Safari/537.36')
options.add_argument('--disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument('--profile-directory=Default')
options.add_argument('--incognito')
options.add_argument('--disable-plugins-discovery')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('prefs', {'intl.accept_languages': '{locale}'.format(locale="en-EN")})
capabilities = DesiredCapabilities.CHROME
driver = webdriver.Chrome(options=options, executable_path='./chromedriver.exe', desired_capabilities=capabilities)

print(driver.execute_script("return navigator.userAgent;"))
url = 'https://yandex.com/search/'
titles = []
all_links = []
first_page = 1


def link_sucker(user_search_input, user_last_page):
    try:
        for page in range(1, int(user_last_page) + 1):
            driver.get(url + "?text=" + str(user_search_input) + "&p=" + str(page))
            contents = driver.find_elements_by_css_selector('.link.link_theme_normal.organic__url')
            # it's just try to catch title
            r = requests.get(url + "?text=" + str(user_search_input) + "&p=" + str(page))
            source = BeautifulSoup(r.content, "lxml")
            # and try to magical things
            if source.title.text == "Oops!":
                print("Yandex Know You! Bypass this captcha")
                print(time.sleep(20))
            else:
                titles.append(source.title.text)
                if len(all_links) > 0:
                    all_links.clear()
                for content in contents:
                    query_string = content.get_attribute("href")
                    # remove query
                    print(query_string)
                    clean_links = query_string[:query_string.find('?', 0)]
                    # append urls
                    all_links.append(clean_links)

                    """
                        If the links are not working properly, do this:
                        remove clean_links
                        and change all_links.append(clean_links) to
                        all.links.append(query_string)
                    """
                # loop for title
            for title in titles:
                pd.DataFrame({title: all_links}).to_csv(str(user_search_input) + '.csv', mode='a', index=False,
                                                        header=title)
            driver.close()  # don't forget to close driver or it will be blow up but who's care?
    except (TimeoutException, InvalidSessionIdException):
        print("Probably you're banned")
        driver.quit()
