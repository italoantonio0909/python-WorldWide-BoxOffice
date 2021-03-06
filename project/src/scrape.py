import requests
import os
import datetime
import sys

from requests_html import HTML

import pandas

THIS_FILE = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(THIS_FILE)
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'download')
CSV_DIR=os.path.join(BASE_DIR,'data')



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
    header_row=rows[0]
    header_cols=header_row.find('th')
    header_names=[e.text for e in header_cols]

    #Iterator str
    for row in rows[1:]:
        row_data=[]
        cols=row.find('td')
        for i, col in enumerate(cols):
            row_data.append(col.text)
        table_data.append(row_data)
    
    #Exists path data
    if not os.path.isdir(CSV_DIR):
        os.makedirs(CSV_DIR)

    csv_filename=os.path.join(CSV_DIR,f'{year}-WorldwideBoxOffice.csv')
    df=pandas.DataFrame(table_data, columns=header_names)
    df.to_csv(csv_filename, index=False)

    return True



def run(*, start_year: str=None, years_ago:int=1):
    if start_year == None:
        now = datetime.datetime.now()
        start_year = now.year

    for e in range(0, years_ago + 1):
        url = f'https://www.boxofficemojo.com/year/world/{start_year}/'
        parsed_and_extract(url=url,year=start_year)
        start_year-=1
        


if __name__ == '__main__':
    try:
        start = int(sys.argv[1])
    except:
        start = None
    try:
        count = int(sys.argv[2])
    except:
        count = 0
    run(start_year=start, years_ago=count)
