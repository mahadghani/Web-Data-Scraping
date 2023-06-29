from bs4 import BeautifulSoup
import requests
import creds
from listL import *
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

priceList = List()

def findPacific(x,y):
    with requests.Session() as session:
        session.post('https://pacific.tireweb.com/', data=creds.pacificPayload)

        payload = {
            'DESTURL': '../Retail/UniOrder.asp',
            'ACTION': 'ADDITEM',
            'ShowBuyPrice': 'True',
            'ViewOnly': 'False',
            'SnowTires': 'False',
            'ShowWarehouses': 'False',
            'MULTIPLE': 'YES',
            'TYRESIZE': x

        }
        response = session.post('https://pacific.tireweb.com/SizeFinderReturn.asp', data=payload)
        soup = BeautifulSoup(response.content, 'html.parser')
        id = soup.find('input', {'name': 'TyreID'}).get('value')
        
        newPayload = {
            'DESTURL': '../Retail/UniOrder.asp',
            'ACTION': 'ADDITEM',
            'ShowBuyPrice': 'True',
            'ViewOnly': 'False',
            'SnowTires': 'False',
            'ShowWarehouses': 'False',
            'MULTIPLE': 'YES',
            'Tian_TYRESIZE': x,
            'TyreID': id
        }

        newResponse = session.post('https://pacific.tireweb.com/Retail/UniOrder.asp', data=newPayload)
        html = BeautifulSoup(newResponse.content, 'html.parser')
        arrayText = html.findAll('script')[6].text


        # titles of inventory
        start = arrayText.find("var AHead3 = new Array(")
        end = arrayText.find("var AHead4")
        desired_string = arrayText[start:end].replace('var AHead3 = new Array(','').replace(');', '').replace("'", "")
        NAMEarray = desired_string.split(",")
        
        # prices of inventory
        start = arrayText.find("var AHead4 = new Array(")
        end = arrayText.find("var AHead5")
        desired_string = arrayText[start:end].replace('var AHead4 = new Array(','').replace(');', '').replace("'", "")
        PRICEarray = desired_string.split(",")

        # number 1 of inventory
        start = arrayText.find("var AHead5 = new Array(")
        end = arrayText.find("var AHead6")
        desired_string = arrayText[start:end].replace('var AHead5 = new Array(','').replace(');', '').replace("'", "")
        inventoryArray1 = desired_string.split(",")

        # number 2 of inventory
        start = arrayText.find("var AHead6 = new Array(")
        end = arrayText.find("var AHead7")
        desired_string = arrayText[start:end].replace('var AHead6 = new Array(','').replace(');', '').replace("'", "")
        inventoryArray2 = desired_string.split(",")

        # number 3 of inventory
        start = arrayText.find("var AHead7 = new Array(")
        end = arrayText.find("var AHead8")
        desired_string = arrayText[start:end].replace('var AHead7 = new Array(','').replace(');', '').replace("'", "")
        inventoryArray3 = desired_string.split(",")

        # number 4 of inventory
        start = arrayText.find("var AHead8 = new Array(")
        end = arrayText.find("var AHead9")
        desired_string = arrayText[start:end].replace('var AHead8 = new Array(','').replace(');', '').replace("'", "")
        inventoryArray4 = desired_string.split(",")

        index = 0
        length = len(NAMEarray) - 1
        while index < length:
            
            arr1 = inventoryArray1[index].split("QtyAvail>")
            inv1 = arr1[1].replace('</div>', '').replace('+','')

            arr1 = inventoryArray2[index].split("QtyAvail>")
            inv2 = arr1[1].replace('</div>', '').replace('+','')

            arr1 = inventoryArray3[index].split("QtyAvail>")
            inv3 = arr1[1].replace('</div>', '').replace('+','')

            arr1 = inventoryArray4[index].split("QtyAvail>")
            inv4 = arr1[1].replace('</div>', '').replace('+','')

            stock = int(inv1) + int(inv2) + int(inv3) + int(inv4)

            if (stock >= y):
                priceList.insert(float(PRICEarray[index].replace('$','')), NAMEarray[index], stock, 'Pacific') 
            
            index = index + 1


def findAvaun(x,y):
    with requests.Session() as session:
        session.post('https://wholesale.avaun.com/login.php?action=process', data=creds.avaunPayload)
        r = session.get('https://wholesale.avaun.com/advanced_search_result.php?keywords=' + x)
        soup = BeautifulSoup(r.content, 'html.parser')

        ads = soup.find_all('li', class_ = 'listingContainer product-col')
        
        for index in ads:
            stock = index.find_all('div', class_ = 'col-md-12')[1].find('div', class_ = 'row').find_all('div', class_ = 'adddesc')[-1].find_all('b')[-1].text.replace("+", "")
            if stock != '0' and int(stock) >= y:
                price = index.find('span', class_ = 'price-text').text.replace("$", "")
                title = index.find('a', class_ = 'productTitleInProductGrid').text

                priceList.insert(float(price), title, stock, 'Avaun')


def findNorthWest(x,y):
    with requests.Session() as session:
        login = "https://accounts.nwr4tires.com/Identity/Account/Login"
        r = session.post(login, creds.northWestPayload)
        print(r.status_code)

def findTireHub(x,y):
    with requests.Session() as session:
        session.post('https://now.tirehub.com/customer/account/loginPost/', data=creds.tireHubPayload)
        s = 'https://now.tirehub.com/tiresearch/result/?q=' + x
        r = session.get(s)
        print(r.text)


def findTireCO(x,y):
    driver = webdriver.Chrome()
    driver.get("https://shoptireco.com/customer/account/login/")
    driver.find_element(By.ID, "email").send_keys(creds.tireCOPayload['login[username]'])
    driver.find_element(By.ID, "pass").send_keys(creds.tireCOPayload['login[password]'])
    driver.find_element(By.ID, "send2").click()

    driver.get("https://shoptireco.com/catalogsearch/result/index/?=&product_list_order=price_low_to_high&q=" + x)
    r = driver.page_source
    driver.close()
    soup = BeautifulSoup(r, 'html.parser')
    
    outter = soup.find_all('li', class_ = 'item product product-item')
    for z in outter:
        stock = 0
        stockOutter = z.find('div', class_ = 'product-item-info').find('div', class_ = 'bottom-wrap').find('div', class_ = 'attributes').find('ul', class_ = 'items availability').find_all('li')
        for index in stockOutter:
            stock = stock + int(index.find('span').text.replace("+", ""))

        if stock >= y:
            title = z.find('a', class_ = 'product-item-link').text
            price = z.find('span', class_ = 'price').text.replace("$", "")
            priceList.insert(float(price), title, stock, 'TireCO')


def findNTW(x,y):
    with requests.Session() as session:
        session.post('https://order.ntw.com/ntwtips/login_action.cfm', data=creds.ntwPayload)
        pricePayload = {
            'doWhat': 'searchProductSAPMetro',
            'size1': x,
            'size2': '',
            'brandfilter': '',
            'linefilter': '',
            'includeOOS': 'false',
            'productType': 'TIRE',
            'speedRating': '',
            'searchTabType': 'size',
        }
        responce = session.post('https://order.ntw.com/ntwtips/distribution/do.cfm', data=pricePayload)
        
        json_obj = json.loads(responce.text)
        # Convert the JSON object to a pretty-printed string
        #pretty_json_str = json.dumps(json_obj, indent=4)

        # Print the pretty-printed string
        #print(pretty_json_str)
        
        for tire in json_obj['items']:
            availList = tire['slaBuckets']
            stock = 0
            for num in availList:
                stock = stock + int(num['Quantity'])
            if (stock >= y):
                title = tire['productDescription']
                cost = tire['price']['cost']
                priceList.insert(float(cost), title, stock, 'NTW')



def findATD(x,y):
    with requests.Session() as session:
        session.post('https://atdonline.com/j_spring_security_check', creds.atdPayload)
        r = session.get('https://atdonline.com/search/global?gbbSearchFlag=&N=10895&Ntk=Search.atdonline_global&Ntt=' + x)
        soup = BeautifulSoup(r.content, 'html.parser')
        print(soup)

def findPrice(x, y):
    #findAvaun(x,y)             #DONE
    findPacific(x,y)            #DONE
    #findNTW(x,y)                #DONE    
    #findNorthWest(x,y)         #UNDER PROGRESS
    #findTireHub(x,y)            #UNDER PROGRESS
    #findTireCO(x,y)             #DONE       
    #findATD(x,y)               #UNDER PROGRESS

    priceList.listprint()

###################   MAIN     ###################
if __name__ == '__main__':
    
    print('Enter tire size')
    x = input('> ')
    print('Enter quantity')
    y = input('> ')
    start_time = time.time()
    findPrice(x, int(y))
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('\n\n\nElapsed time:', elapsed_time)
