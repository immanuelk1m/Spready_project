from selenium import webdriver
import pandas as pd
import re
import telegram
import time
import schedule


telgm_token = "Telegram Token"
bot = telegram.Bot(token = telgm_token)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('./chromedriver' ,options=options)




def bunjang_item_db(item, page_count = 4):
    print(item, " Search start")
    name_list = []
    price_list = []
    link_list = []
    date_list = []
    
    for page in range(page_count) :
        url = "https://m.bunjang.co.kr/search/products?order=score&page="+str(page+1)+"&q="+ item 
        driver.get(url)
        driver.implicitly_wait(10)
        
        for i in range(1,100):
            if i % 10 == 0:
                print(i)

            try :
                date = driver.find_element('xpath','//*[@id="root"]/div/div/div[4]/div/div[4]/div/div['+str(i)+']/a/div[2]/div[2]/div[2]').text
                if date.find('주') != -1 or date.find('달') != -1 :
                    break
                
                name = driver.find_element('xpath','//*[@id="root"]/div/div/div[4]/div/div[4]/div/div['+str(i)+']/a/div[2]/div[1]').text
                price = driver.find_element('xpath','//*[@id="root"]/div/div/div[4]/div/div[4]/div/div['+str(i)+']/a/div[2]/div[2]/div[1]').text
                link = driver.find_element('xpath', '//*[@id="root"]/div/div/div[4]/div/div[4]/div/div['+str(i)+']/a').get_attribute('href')
                
                
                price = price.replace(',', '')
                price = price.replace('원', '')
                
                name_list.append(name)
                price_list.append(int(price))
                link_list.append(link)
                date_list.append(date)
                
            except:
                print("error")
                break
    	
    item_db = pd.DataFrame([ x for x in zip(name_list,price_list,link_list,date_list)])
    item_db.columns = ['name', 'price','link','date']
    
    return item_db

    

def remove_outlier(df, price_range):
    print("Remove Outlier")

    # 금지어 제거
    ban_word = ['word1','word2]
    # ex) '케이스','매입','파손','B급','삽니다','교신','삽','구매','교환','사요'
                
    for w in ban_word :
    	df = df[~df['name'].str.contains(w)]
    
    # 가격 이상치 제거
    
    low = price_range[0]
    high = price_range[1]
    condition = (df['price'] >= low) & (df['price'] <= high)
    df = df[condition]
    
    return df




def telegram_send() :
    
    item_price_dict = {
        'IPHONE' : [200000,300000],
  
    }
    
    
    for item in item_price_dict.keys() :
        used_db = bunjang_item_db(item)
        used_db = remove_outlier(used_db, item_price_dict[item])
        msg = item + "\n\n\n"

        for r in range(used_db.shape[0]) :
            msg = msg + str(used_db['name'].iloc[r]) + " \n\n" + str(used_db['price'].iloc[r]) + "  \n\n" +  str(used_db['link'].iloc[r]) + "  \n\n" +  str(used_db['date'].iloc[r]) + "\n\n --------------------------------------------------------- \n"

        bot.sendMessage(chat_id = "Telegram Chat ID", text=msg)

    

schedule.every(8).hours.do(telegram_send) # 8시간마다 실행
 

while True:
    schedule.run_pending()
    time.sleep(1)
