import requests
import os

from requests_html import HTML

THIS_FILE = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(THIS_FILE)
DOWNLOAD_DIR=os.path.join(BASE_DIR,'download')



def url_to_file(*, url: str, save: bool = True, year: str):
    
    #Exists path donwload
    if not os.path.isdir(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        
    #Filename download
    filename = os.path.join(DOWNLOAD_DIR,f'{year}-WorldwideBoxOffice.html')

    request = requests.get(url)
    if request.status_code == 200:
        request_html = request.text
        if save:
            with open(filename, 'w', encoding="utf-8") as file:
                file.write(request_html)
        return request_html
    return None



def parsed_and_extract(*, url: str, year: str):
    
    #Data initial
    table_data=[]

    response_html = url_to_file(url=url, year=year)

    #Request validate date
    if response_html == None:
        return False

    #Selector queryset
    table_class = '.imdb-scroll-table'
    r_html = HTML(html=response_html)
    r_table = r_html.find(table_class)

    #Validate date in a table
    if len(r_table) == 0:
        return False
    
    parsed_table = r_table[0]
    rows = parsed_table.find('tr')

    #Iterator str
    for row in rows[1:]:
        row_data=[]
        cols=row.find('tr')
        for i, col in enumerate(cols):
            row_data.append(col.text)
        table_data.append(row_data)

    return table_data
            


url='https://www.boxofficemojo.com/year/world/2021/'
if __name__ == '__main__':
    x = parsed_and_extract(url=url, year='2021')
    print(x)