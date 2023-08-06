from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

#participants = [["lim", "ecal"],["pig","jhk"],["pig2","jhk2"],["pig3","jhk3"],["pig4","jhk4"],["pig5","jhk5"]]
#username = "geoandchill_test"
#password = "/s3FDyKEai"
#tournament_name = "test_tournamentaaannnnaa"
#stage_bool = False
#format = "Double Elimination"
#time_s = "2023/02/11 5:00 PM"

def create_bracket(participants,username,password,tournament_name,stage_bool,format,time_s):
    # comment out headless if you want to see what its doing
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("--ignore-certificate-errors")

    # START
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
    driver.get("https://challonge.com/")

    # i did loads of sleeps cuz i dont know how to do it properly and wanted to give it time
    # could probably do wait for or something
    time.sleep(1)

    # gets rid of the cookie window so it doesnt interfere with anything else
    cookie_reject = driver.find_element(By.XPATH, '//*[@id="onetrust-reject-all-handler"]').click()
    # find login button and click it
    login_button = driver.find_element(By.XPATH, '//html/body/div[1]/nav/div[3]/div/div[2]/a')
    driver.execute_script("arguments[0].click();", login_button)

    time.sleep(1)

    # enter user and pass
    username_box = driver.find_element(By.XPATH, '//*[@id="user_session_username_or_email"]')
    password_box = driver.find_element(By.XPATH, '//*[@id="user_session_password"]')
    username_box.send_keys(username)
    password_box.send_keys(password)
    driver.find_element(By.XPATH, "//html/body/div[1]/div[2]/div/div[2]/form/div[4]/input").click()

    time.sleep(1)

    # opens up the dropdown to the create tournament button
    create_button = driver.find_element(By.XPATH, '//html/body/div[1]/div/div/div/div[2]/div/button/span')
    driver.execute_script("arguments[0].click();", create_button)
    tourney_button = driver.find_element(By.XPATH, '//html/body/div[1]/div/div/div/div[2]/div/ul/li[1]/a/strong')
    driver.execute_script("arguments[0].click();", tourney_button)

    time.sleep(1)

    # tournament settings
    tourney_name = driver.find_element(By.XPATH, '//*[@id="tournament_name"]')
    tourney_name.send_keys(tournament_name)
    game_name = driver.find_element(By.XPATH, '//html/body/div[2]/div[2]/form/fieldset[2]/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div/div/input')
    game_name.send_keys("geoguessr")

    if stage_bool == True:
        stage_type = driver.find_element(By.XPATH, '//html/body/div[2]/div[2]/form/fieldset[2]/div/div[2]/div[2]/div/label[2]/span[1]').click()
    
    if format == "Double Elimination":
        double_elim = driver.find_element(By.XPATH, '//*[@id="tournament_tournament_type"]/option[text()="Double Elimination"]').click()
    elif format == "Round Robin":
        round_robin = driver.find_element(By.XPATH, '//*[@id="tournament_tournament_type"]/option[text()="Round Robin"]').click()
    elif format == "Swiss":
        swiss = driver.find_element(By.XPATH, '//*[@id="tournament_tournament_type"]/option[text()="Swiss"]').click()

    start_time = driver.find_element(By.XPATH, '//*[@id="tournament_start_at"]')
    start_time.send_keys(time_s)
    enable_predictions = driver.find_element(By.XPATH, '//*[@id="accept_predictions"]').click()
    confirm = driver.find_element(By.XPATH, '//html/body/div[2]/div[2]/form/div/div/input[2]').click()

    time.sleep(1)

    # bit scuffed with the sleeps but this bit is important so it actually inputs the names
    url = driver.current_url
    add_participants = driver.find_element(By.XPATH, '//html/body/div[4]/div[3]/div[3]/div[1]/div/div/a').click()
    time.sleep(1)
    add_bulk = driver.find_element(By.XPATH, '//html/body/div[4]/div[3]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/a').click()
    time.sleep(1)
    bulk_field = driver.find_element(By.XPATH, '//html/body/div[4]/div[3]/div/div[2]/div[2]/div/div[2]/div/form[2]/fieldset/div/div[1]/textarea')
    time.sleep(1)
    for team in participants:
        joint_team = team[0]
        for person in team:
            if person == team[0]:
                pass
            else:
                joint_team += (" + " + person)
        bulk_field.send_keys(joint_team + "\n")
    confirm_bulk = driver.find_element(By.XPATH, '//html/body/div[4]/div[3]/div/div[2]/div[2]/div/div[2]/div/form[2]/fieldset/div/div[2]/input').click()

    time.sleep(1)

    return(url)

#create_bracket(participants,username,password,tournament_name,stage_bool,format,time_s)