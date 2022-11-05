import time
import requests
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.alert import Alert

id = 'kakao id'
pw = 'kakao pw'
nick_name = 'blog nick name'

w = "가 나 다 라"

comment = "hello~"

# 셀레니움 설정

options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument('--no-sandbox')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('--disable-dev-shm-usage')
options.add_argument("disable-gpu")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

# 속도 향상을 위한 옵션 해제
driver = webdriver.Chrome(executable_path='./chromedriver',options=options)

w_list = []

for i in w:
  if i != ' ':
    w_list.append(i)
w_list = set(w_list)

# 무한루프
for t in range(1000000):

  #################################### 단어 선정 파트 ####################################

  # 랜덤 단어 20개 선정
  word_list = random.sample(w_list, 20)
  print(word_list)

  # 단어 순서대로 반복
  for k_num, k in enumerate(word_list):
    cant = 0  # 댓글 못 단 횟수
    cnt = 0  # 댓글 단 횟수

    #################################### 로그인 파트 ####################################

    # 티스토리 로그인 페이지 접속
    driver.get(
      'https://accounts.kakao.com/login?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fis_popup%3Dfalse%26ka%3Dsdk%252F1.43.0%2520os%252Fjavascript%2520sdk_type%252Fjavascript%2520lang%252Fko-KR%2520device%252FWin32%2520origin%252Fhttps%25253A%25252F%25252Fwww.tistory.com%26auth_tran_id%3Dhyynik61tmn3e6ddd834b023f24221217e370daed18l9pov2iz%26response_type%3Dcode%26state%3DaHR0cDovL3d3dy50aXN0b3J5LmNvbS9t%26redirect_uri%3Dhttps%253A%252F%252Fwww.tistory.com%252Fauth%252Fkakao%252Fredirect%26through_account%3Dtrue%26client_id%3D3e6ddd834b023f24221217e370daed18&talk_login=hidden'
    )
    driver.implicitly_wait(10)  # 페이지 로딩 대기
    time.sleep(4)
    # 로그인 과정
    try:  # 아이디 비밀번호 입력 -> 로그인 버튼 클릭
      time.sleep(2)
      username = driver.find_element('xpath', '//*[@id="input-loginKey"]')
      username.send_keys(id)

      driver.implicitly_wait(10)  # 페이지 로딩 대기
      time.sleep(2)

      password = driver.find_element('xpath', '//*[@id="input-password"]')
      password.send_keys(pw)

      password = driver.find_element(
        'xpath',
        '//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click()
    except Exception:  # 로그인 실패 시 재시도
      time.sleep(2)
      username = driver.find_element('xpath', '//*[@id="id_email_2"]')
      username.send_keys(id)

      driver.implicitly_wait(10)  # 페이지 로딩 대기
      time.sleep(2)

      password = driver.find_element('xpath', '//*[@id="id_password_3"]')
      password.send_keys(pw)

      password = driver.find_element(
        'xpath', '//*[@id="login-form"]/fieldset/div[8]/button[1]').click()

      # 시간 지연
    time.sleep(3)

    #################################### 블로그 주소 스크래핑 파트 ####################################
    site_list = []

    for i in range(5):  # 해당 키워드 5page 스크랩핑
      print('page ', i + 1, 'scraping start')

      driver.get('https://www.tistory.com/m/search/' + k + '/' + str(i + 1) +
                 '/date')  # 키워드 검색 목록 접속
      driver.implicitly_wait(10)  # 페이지 로딩 대기

      for p_g in range(10):
        try:  # 각 page마다 주소 크롤링
          p = driver.find_element(
            'xpath', '//*[@id="mArticle"]/div/ul/li[' + str(p_g + 1) + ']/a')
          site_list.append(p.get_attribute('href'))
        except:
          print('pass')
          continue

    n_site_list = []

    for t in site_list:  # page주소 모바일로 변환
      index = t.find(".com/")
      n_t = t[:index + 5] + 'm/' + t[index + 5:]
      n_site_list.append(n_t)

#################################### 댓글 달기 파트 ####################################

    for s in n_site_list:  # page 수 * 10 반복
      try:
        time.sleep(2)
        driver.get(s + '/comments')
        driver.implicitly_wait(10)
        time.sleep(1)
        da = Alert(driver)

        user_list = []
        print('site   : ', s)
        try:
          guide = driver.find_element(
            'xpath', '//*[@id="mainContent"]/div[1]/div[1]/p[2]').text

          if guide == "로그인 댓글만 허용한 블로그입니다." or guide == "댓글 작성이 불가능한 글입니다.":  # 로그인 필요해 댓글 못 다는 경우
            print(guide)
            continue  # 루프 다시 돌리기

          else:  # 댓글이 하나도 안 달린 경우
            print('case : no comment')
            try:
              driver.find_element(
                'xpath', '//*[@id="mainContent"]/div[2]/div/div/div/input'
              ).click()  # 댓글 입력 창 클릭
              driver.find_element(
                'xpath',
                '//*[@id="mainContent"]/div[2]/form/fieldset/div[2]/div/textarea'
              ).send_keys(comment)  # 댓글 입력
              driver.find_element(
                'xpath',
                '//*[@id="mainContent"]/div[2]/form/fieldset/div[3]/button'
              ).click()  # 완료 버튼 클릭
              driver.implicitly_wait(10)
              cnt = cnt + 1
            except:
              da.accept()
              cnt = cnt - 1
              print("forbiden")
              continue

        except:  # 댓글이 달려 있는 경우 -> 내 댓글 검사
          print('case : comments')
          for c in range(2):  # 이미 내가 댓글을 달았는지 확인
            try:
              xp = '//*[@id="mainContent"]/div[1]/ul/li[' + str(
                c + 1) + ']/div/div[1]/div[2]/div/a/strong'
              t = driver.find_element('xpath', str(xp)).text  # 댓글쓴이 추출
              user_list.append(t)  # 댓글쓴이 리스트에 추가
            except:
              pass

          if (nick_name in user_list) == False:  # 댓글 안 달렸으면
            try:
              driver.find_element(
                'xpath', '//*[@id="mainContent"]/div[2]/div/div/div/input'
              ).click()  # 댓글 입력 창 클릭
              driver.find_element(
                'xpath',
                '//*[@id="mainContent"]/div[2]/form/fieldset/div[2]/div/textarea'
              ).send_keys(comment)  # 댓글 입력
              driver.find_element(
                'xpath',
                '//*[@id="mainContent"]/div[2]/form/fieldset/div[3]/button'
              ).click()  # 완료 버튼 클릭
              driver.implicitly_wait(10)
              cnt = cnt + 1
            except:
              da.accept()
              cnt = cnt - 1
              print("forbiden")
              continue
          else:
            print('my comment already exist')
            continue
      except:
        continue
      print(k_num + 1, 'st - key : ', k, "    ",
            round(cnt / len(n_site_list), 3) * 100, '%')
