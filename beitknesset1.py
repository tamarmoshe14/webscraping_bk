import requests
from lxml import html
import xlsxwriter
from time import sleep

page_num = 0
list_main_url = []
for i in range(84):
    main_url = 'https://reformjudaism.org/urj-congregations?congregation=&distance_address_field=&distance_num_miles=5.0&worship_services=All&community=All&urj_camp_affiliations=All&page={}'.format(page_num)
    page_num += 1
    list_main_url.append(main_url)
#now i have a list of all pages

page_count = 1
all_links=[]

bkmaillist = xlsxwriter.Workbook("bkmaillist.xlsx")
outsheet = bkmaillist.add_worksheet()

for page in list_main_url:
    print (page_count, len(list_main_url))
    resp = requests.get(page, headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0"})
    tree = html.fromstring(html = resp.text)
    links_of_page = tree.xpath('//div/div/h3[@class="field-content mb-3"]/a/@href')
    for link in links_of_page:
      all_links.append("https://reformjudaism.org"+link)

emails=[]
phones=[]
names=[]
addresses_1=[]
addresses_2 = []
page_num = 1
for bkpage in all_links:
    print (page_num)
    resp2 = requests.get(bkpage, headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0"})
    tree = html.fromstring(html = resp2.text)
    try:
        email = tree.xpath('//div[@class="col-md-6"]/div/p[@title="email"]/a/@href')[0]
    except:
        email = "no email"
    emails.append(email)
    try:
        phone = tree.xpath('//div[@class="col-md-6"]/div/p[@title="phone"]/a/@href')[0]
    except:
        phone = "no phone"
    phones.append(phone)
    try:
        name = tree.xpath('//div[@class="container py-4"]/div/div/h1/text()')[0]
    except:
        name = "no name"
    names.append(name)
    try:
        address_1 = tree.xpath('//div[@class="container py-4"]/div/div/div/div/div[@class="address"]/p[1]/text()')[0]
    except:
        address_1 = "no address"
    addresses_1.append(address_1)
    try:
        address_2 = tree.xpath('//div[@class="container py-4"]/div/div/div/div/div[@class="address"]/p[2]/text()')[0]
    except:
        address_2 = "no address"
    addresses_2.append(address_2)
    
    page_num +=1



mail_print_count = 1
phone_print_count = 1
name_print_count = 1
address_1_print_count = 1
address_2_print_count = 1

for email in emails:
    print (mail_print_count, len(emails))   
    outsheet.write(mail_print_count, 0, email)
    mail_print_count +=1

for phone in phones:    
    outsheet.write(phone_print_count, 1, phone)
    print (phone_print_count, len(emails))   
    phone_print_count +=1

for name in names:    
    outsheet.write(name_print_count, 2, name)
    print (name_print_count, len(emails))   
    name_print_count +=1

for address_1 in addresses_1:    
    outsheet.write(address_1_print_count, 3, address_1)
    print (address_1_print_count, len(emails))   
    address_1_print_count +=1
    
for address_2 in addresses_2:    
    outsheet.write(address_2_print_count, 4, address_2)
    print (address_2_print_count, len(emails))   
    address_2_print_count +=1


bkmaillist.close()


