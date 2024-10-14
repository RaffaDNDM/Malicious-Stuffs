#######################
# @author: RaffaDNDM
# @date:   2022-09-10
#######################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
#path = 'D:\Programs\ChromeDriver\chromedriver.exe'

class Whatsapp:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def __enter__(self):
        self.driver.get('https://web.whatsapp.com')
        input('Press ENTER when you insert QRcode')
        return self

    def send_msg(self):
        try:
            while True:
                print('\n___________________________________________')
                receiver = input('Receiver: ')
                msg = input('Msg: ')
                num_rep = int(input('Num repetitions:'))

                if num_rep < 1:
                    print('[ERROR] At least 1 repetition')
                    exit(1)

                search_box = self.driver.find_element_by_xpath("//*[@id='side']/div[1]/div/label/div/div[2]")
                search_box.send_keys(receiver)
                search_box.send_keys(Keys.ENTER)

                for i in range(num_rep):
                    msg_box = self.driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")
                    msg_box.send_keys(msg)
                    msg_box.send_keys(Keys.ENTER)

        except KeyboardInterrupt:
            print('\n___________________________________________', end='\n\n')
            pass
            

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


def main():
    with Whatsapp() as whats_sender:
        whats_sender.send_msg()

if __name__=='__main__':
    main()