from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures

def open_browser():
    f = open("data.txt","w+")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-minimized")
    #options.add_argument("--user-data-dir=C:/Users/Lenovo/AppData/Local/Google/Chrome/User Data/Default")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://www.castorama.pl/produkty/wykonczenie.html")
    try:
        category_name = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "category-first-level__title")))
    finally:
        #f.write("<"+category_name.text + ">\n")
        #print("<"+category_name.text + ">")       
        elements = driver.find_elements_by_xpath("//ul[@class='menu-default__list row']/li[@class='menu-default__list--item col-lg-3 col-md-4 col-6']")
        threads = list()
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        for e in elements:
             section_title = e.find_element_by_xpath("div/h4/a").text
             #f.write("`--<"+section_title+ ">\n")
             #print("`--<"+section_title+ ">")
             list_items = e.find_elements_by_xpath("div/ul/li")           
             for l in list_items:
                 item = l.find_element_by_tag_name("a")
                 #f.write("|   `--<" + item.text+ ">\n")
                 #print("|   `--<" + item.text+ ">")
                 #get_products(item.get_attribute("href"),f,item.text)
                 threads.append(executor.submit(get_products,item.get_attribute("href"),f,item.text))                 
                 #x = threading.Thread(target=get_products, args=(item.get_attribute("href"),f,item.text))
                 #print(""+str(progress)+"% done")
             for t in threads:
                 t.result()
                 threads.remove(t)
             #executor.result()
        #not_finished = True
        #while not_finished:
        #    not_finished = False
        #    for t in threads:
        #        if t.isAlive():
        #            not_finished = True
        f.close()
        driver.quit()
def get_products(href, f,section_name):
    #print(href)
    print("Thread starting")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-minimized")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(href)
    #list_products = section[@class='product-price__wrapper product-tail__price']"//section[@class='product-tail products-grid__item']")))
    list_products = driver.find_elements_by_xpath("//section[@class='product-tail products-grid__item']")
    for p in list_products:
        name_product = p.find_element_by_xpath("h3")
        try:
            section_product = p.find_element_by_xpath("section[@class='product-price__wrapper product-tail__price']")
            price_product = section_product.get_attribute("content")
            unit_product = section_product.find_element_by_xpath("div/p/span/span[@class='not-fractioned-price__unit'] | div/p/span/span[@class='conversion-unit']")      
        except:
            print("exception occured at: " + name_product.text)
        #f.write("|   |  `--[" + name_product.text + "][" + price_product +"(" + unit_product.text.strip() +")]\n")
        #print("|   |  `--[" + name_product.text + "][" + price_product +"(" + unit_product.text.strip() +")]")
        f.write("INSERT INTO przedmioty (kategoria, nazwa, cena, ilosc) VALUES ('" + section_name + "','" + name_product.text + "',"  + price_product + ",'" + unit_product.text.strip() + "');\n")
        print("INSERT INTO przedmioty (kategoria, nazwa, cena, ilosc) VALUES ('" + section_name + "','" + name_product.text + "',"  + price_product + ",'" + unit_product.text.strip() + "');")
    driver.quit();
    print("Thread finishing")
open_browser()

