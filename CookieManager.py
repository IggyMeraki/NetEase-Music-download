import time

from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class CookieManager:
    def __init__(self,file_path=None):
        self.file_path = file_path

    @logger.catch
    def login_and_save_cookies(
            self, login_url="https://music.163.com/#"
    ):
        logger.info("启动浏览器中.....")
        try:
            self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        except Exception:
            try:
                self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            except Exception:
                raise Exception(
                    "没有找到浏览器驱动\n"
                    "请直接升级系统到最新的windows系统（专业版\n"
                )
        # self.wait = WebDriverWait(self.driver, 0.5)
        self.driver.get(login_url)
        self.driver.maximize_window()
        time.sleep(1)
        self.driver.refresh()
        time.sleep(1)
        while True:
            try:
                self.driver.find_element(By.CLASS_NAME, "link.s-fc3").click()
                break
            except Exception as _:
                self.driver.refresh()
                time.sleep(1)
        logger.info("浏览器启动, 进行登录.")
        while True:
            try:
                self.driver.find_element(By.CLASS_NAME, "head.f-fl.f-pr")
                break
            except Exception as _:
                pass
        time.sleep(1)
        self.cookies = self.driver.get_cookies()
        self.driver.quit()
        logger.info("登录成功, 浏览器退出.")
        for cookie in self.cookies:
            if cookie.get("name") == "MUSIC_U":
                with open(self.file_path, "w") as f:
                    MUSIC_U = cookie.get("value")
                    f.write("MUSIC_U="+cookie.get("value")+";appver=8.9.75;")
                    break
        return MUSIC_U


if __name__ == '__main__':
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "cookie.txt")
    with open(file_path, 'a'):
        pass
    cm = CookieManager(file_path=file_path)
    cm.login_and_save_cookies()
    print(cm.cookies)