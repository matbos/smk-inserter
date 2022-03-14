import csv
from math import e
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import FirefoxDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from EntryData import EntryData


def read_file(path):
    entries = []
    with open(path, encoding='utf-8') as csv_file:
        next(csv_file)  # skips the header
        file_reader = csv.reader(csv_file)
        for row in file_reader:
            entries.append(EntryData(row))
    return entries


def open_smk():
    chrome_options = Options()
    chrome_options.add_argument("accept-language=pl-PL")
    chrome_options.add_argument("--lang='pl'")
    chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'pl,pl_PL'})
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get("https://smk.ezdrowie.gov.pl/")

    return driver


def open_smk_firefox():
    driver = webdriver.Firefox()
    driver.get("https://smk.ezdrowie.gov.pl/")
    driver.maximize_window()
    return driver


def process():
    entries = read_file("neuro-TK-poprawione.csv")
    driver = open_smk_firefox()
    # driver = open_smk()    
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/form/button").click()

    wait = WebDriverWait(driver=driver, timeout=60)    
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div[1]/form/div[1]/div/input")))
    
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/form/div[1]/div/input").send_keys('malgorzata.mechel@gmail.com')
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/form/div[2]/div/input").send_keys('Lgw3DY*MKN')
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/form/button").click()
    
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[4]/div/table/tbody/tr/td[2]/div/div/div/div/div/fieldset/table/tbody/tr/td/div/table[1]/tbody[1]/tr[3]/td[7]/div/button")))
    driver.find_element(By.XPATH, "/html/body/div[3]/div[4]/div/table/tbody/tr/td[2]/div/div/div/div/div/fieldset/table/tbody/tr/td/div/table[1]/tbody[1]/tr[3]/td[7]/div/button").click()

    driver.find_element(By.XPATH, "/html/body/div[3]/div[4]/div/table/tbody/tr/td[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td[1]/button").click()
    # wait?
    element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[4]/div/table/tbody/tr/td[2]/div/div/div/div/div/table/tbody/tr/td[2]/div/fieldset/table/tbody/tr/td/div/table[1]/tbody[1]/tr[2]")))    
    
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[4]/div/table/tbody/tr/td[2]/div/div/div/div/div/table/tbody/tr/td[2]/div/fieldset/table/tbody/tr/td/div/table[1]/tbody[1]/tr[2]/td[1]/div")))    
    driver.find_element(By.XPATH, "/html/body/div[3]/div[4]/div/table/tbody/tr/td[2]/div/div/div/div/div/table/tbody/tr/td[2]/div/fieldset/table/tbody/tr/td/div/table[1]/tbody[1]/tr[2]/td[1]/div").click()

    driver.find_element(By.XPATH, "/html/body/div[3]/div[4]/div/table/tbody/tr/td[2]/div/div/div/div/div/table/tbody/tr/td[2]/div/fieldset/table/tbody/tr/td/div/div/div/table/tbody/tr/td/table/tbody/tr/td[2]/button").click()
    
    button = driver.find_element(By.XPATH, '//*[@id="509"]')
    driver.execute_script("arguments[0].scrollIntoView();",button)
    # driver.execute_script("arguments[0].click();", button)
    # ActionChains(driver).move_to_element(button).click(button).perform()
    # button.click()
    
    
    #wait?
    element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[4]/div/table/tbody/tr/td[2]/div/div/div/div/div/div[2]/fieldset/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div/div/div/button")))        

    driver.find_element(By.XPATH, "/html/body/div[3]/div[4]/div/table/tbody/tr/td[2]/div/div/div/div/div/div[2]/fieldset/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div/div/div/button").click()


    input_button_xpath = input('podaj XPath przycisku dodawania: ')
    # buttons suffix
    input_button_suffix = "table[1]/tbody/tr/td[1]/button"
    if not input_button_xpath.endswith(input_button_suffix):
        print("Niepoprawny XPath!")
        exit(-1)
    prefix_xpath = input_button_xpath[:-len(input_button_suffix)]

    i = 0
    input(""+i.__str__()+" z "+len(entries).__str__()+" Start?!")
    for entry in entries:
        i+=1
        add_button = driver.find_element(By.XPATH, input_button_xpath)
        add_button.click()
        date = driver.find_element(By.XPATH, prefix_xpath+"div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[2]/div/input")
        date.send_keys(entry.date)
        year = Select(driver.find_element(By.XPATH, prefix_xpath + "div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[4]/div/select"))
        year.select_by_visible_text(str(entry.year))
        code = Select(driver.find_element(By.XPATH, prefix_xpath + "div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[5]/div/select"))
        code.select_by_index(entry.procedure_code)
        operator = driver.find_element(By.XPATH, prefix_xpath + "div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[6]/div/input")
        operator.send_keys(entry.operator)
        
        gender = Select(driver.find_element(By.XPATH, prefix_xpath + "div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[10]/div/select"))
        gender.select_by_visible_text(entry.gender)

        # execution_place_control_parent = driver.find_element(By.XPATH, prefix_xpath + "div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[7]/div")
        # execution_place_control_parent.click()

        # 
        # execution_place_control = driver.find_element(By.XPATH, prefix_xpath + "div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[7]/div/select")
        # execution_place = Select(execution_place_control)
        # execution_place_option = driver.find_element(By.XPATH, prefix_xpath + "div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[7]/div/select/option[2]")
        # execution_place_option.click()
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, prefix_xpath + "div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[7]/div/select//options[contains(.,'Zakład Diagnostyki Obrazowej - Sosnowiecki Szpital Miejski Sp. z o.o.')]")))
        # execution_place.options[1]
        # execution_place.select_by_visible_text('Zakład Diagnostyki Obrazowej - Sosnowiecki Szpital Miejski Sp. z o.o.')
        # execution_place.deselect_all()
        # execution_place._setSelected(execution_place.options[entry.execution_place])
        # driver.execute_script('document.evaluate("/html/body/div[3]/div[4]/div/table/tbody/tr/td[2]/div/div/div/div/div/div[2]/fieldset/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div/div/table/tbody/tr/td/div/div/table/tbody/tr[8]/td/div/table/tbody/tr[1]/td/div/div/div/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td/div/div/div/table/tbody/tr/td/div/div/div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[7]/div/select/option[2]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;')
        # driver.execute_script('$x(/html/body/div[3]/div[4]/div/table/tbody/tr/td[2]/div/div/div/div/div/div[2]/fieldset/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div/div/table/tbody/tr/td/div/div/table/tbody/tr[8]/td/div/table/tbody/tr[1]/td/div/div/div/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td/div/div/div/table/tbody/tr/td/div/div/div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[7]/div/select/option[2])')
        # driver.execute_script('jQuery(document.evaluate("/html/body/div[3]/div[4]/div/table/tbody/tr/td[2]/div/div/div/div/div/div[2]/fieldset/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div/div/table/tbody/tr/td/div/div/table/tbody/tr[8]/td/div/table/tbody/tr[1]/td/div/div/div/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td/div/div/div/table/tbody/tr/td/div/div/div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[7]/div/select/option[2]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue).attr("selected","selected").change();')
        # driver.execute_script('jQuery(document.evaluate("/html/body/div[3]/div[4]/div/table/tbody/tr/td[2]/div/div/div/div/div/div[2]/fieldset/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div/div/table/tbody/tr/td/div/div/table/tbody/tr[8]/td/div/table/tbody/tr[1]/td/div/div/div/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td/div/div/div/table/tbody/tr/td/div/div/div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[7]/div/select/option[2]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue).val("Zakład Diagnostyki Obrazowej - Sosnowiecki Szpital Miejski Sp. z o.o.")')
        
        # execution_place.select_by_index(entry.execution_place)

        # internship_place_control_parent = driver.find_element(By.XPATH, prefix_xpath + "div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[8]/div")
        # internship_place_control_parent.click()
        # driver.execute_script('jQuery(document.evaluate("/html/body/div[3]/div[4]/div/table/tbody/tr/td[2]/div/div/div/div/div/div[2]/fieldset/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div/div/table/tbody/tr/td/div/div/table/tbody/tr[8]/td/div/table/tbody/tr[1]/td/div/div/div/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td/div/div/div/table/tbody/tr/td/div/div/div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[8]/div/select/option[7]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue).attr("selected","selected").change();')
        # driver.execute_script('jQuery(document.evaluate("/html/body/div[3]/div[4]/div/table/tbody/tr/td[2]/div/div/div/div/div/div[2]/fieldset/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div/div/table/tbody/tr/td/div/div/table/tbody/tr[8]/td/div/table/tbody/tr[1]/td/div/div/div/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td/div/div/div/table/tbody/tr/td/div/div/div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[8]/div/select/option[7]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue).val("Staż kierunkowy w zakresie neuroradiologii, diagnostyki obrazowej głowy i szyi oraz w stomatologii").change()')
        # ActionChains(driver).move_to_element_with_offset(internship_place_control_parent, 0, 0).click(internship_place_control_parent).perform()
        
        # internship_place = Select(driver.find_element(By.XPATH, prefix_xpath + "div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[8]/div/select"))
        # internship_place.select_by_index(entry.internship_place)
        # internship_place.select_by_visible_text("Staż kierunkowy w zakresie neuroradiologii, diagnostyki obrazowej głowy i szyi oraz w stomatologii")
        
        initials = driver.find_element(By.XPATH, prefix_xpath + "div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[9]/div/input")
        initials.send_keys(entry.initials)
        
        if entry.assist:
            assist = driver.find_element(By.XPATH,prefix_xpath + "div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[11]/div/input")
            assist.send_keys(entry.assist)
        if entry.procedure_group:
            procedure_group = driver.find_element(By.XPATH, prefix_xpath + "div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[12]/div/input")
            procedure_group.send_keys(entry.procedure_group)
        if(i%50==0):
            input(""+i.__str__()+" z "+len(entries).__str__()+" Dalej!")

    input("Potwierdź")
    # Save!
    driver.find_element(By.ID, "30060").click()
    input("Potwierdź zapisanie")
    driver.close()


if __name__ == '__main__':
    process()

