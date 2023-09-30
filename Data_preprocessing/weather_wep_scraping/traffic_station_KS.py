import re
from bs4 import BeautifulSoup as bs
import requests
import csv

url = 'https://kcpd.kcg.gov.tw/cp.aspx?n=693052840FE00C08&s=D36FF802DE9B88C4'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}


response = requests.get(url, headers=headers)
html_code = response.text

soup = bs(html_code, 'lxml')

pattern = r"q=([\d.]+),([\d.]+)"

links = soup.select('div.page_map04>table>tbody>tr>td>a')

csv_file = open('data.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Title', 'Latitude', 'Longitude'])

for a in links:
    alt = a.find('img').get('alt')
    map_url = a['href']
    match = re.search(pattern, map_url)

    if match:
        latitude = match.group(1)
        longitude = match.group(2)
        # print("Title:", alt)
        # print("Latitude:", latitude)
        # print("Longitude:", longitude)
        csv_writer.writerow([alt, latitude, longitude])
