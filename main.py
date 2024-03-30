import re
import time
import requests
import webbrowser
from tqdm import tqdm
from openai import OpenAI
from docx import Document
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def set_target():
    x = input("\nIf you enter a date, the year and month are defaulted to this month of this year.\nAnd if you enter a month and date, the year are defaulted to this year.\n\nAcceptable formats:YYYY_MM_DD / YYYY-MM-DD / YYYYMMDD:  ")
    x = x.strip().replace('-', '').replace('_', '')
    if len(x) == 2: 
        x = datetime.today().strftime('%Y%m') + x 
    elif len(x) == 4: 
        x = datetime.today().strftime('%Y') + x
    date_obj = datetime.strptime(x, '%Y%m%d')
    #date = date_obj.strftime('%Y-%m-%d')
    print("Target Date: ", date_obj,"\n")
    return date_obj


def gpt_conclusion(set_date=None):

    if set_date is not None:
        today = set_date.strftime('%Y-%m-%d')
        yesterday = (set_date - timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        today = datetime.today().strftime('%Y-%m-%d')
        yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    base_url = f'https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=&terms-0-field=title&classification-computer_science=y&classification-physics_archives=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date={yesterday}&date-to_date={today}&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first&start='
    
    all_papers = []
    paper_count = 0 
    start = 0
    while True:
        url = base_url + str(start)
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            papers = soup.find_all('li', class_='arxiv-result')
            
            for paper in papers:
                title = paper.find('p', class_='title is-5 mathjax').get_text(strip=True)
                authors = paper.find('p', class_='authors').get_text(strip=True)
                abstract = paper.find('p', class_='abstract mathjax').get_text(strip=True)
                comment_tag = paper.find('p', class_='comments is-size-7')
                comment = comment_tag.get_text(strip=True) if comment_tag else None
                paper_info = f"Title: {title}\nAuthors: {authors}\nAbstract: {abstract}\nComment: {comment}\n"
                if paper_count>5:
                    break
                
                all_papers.append([paper_info])
                
                paper_count += 1
            
            total_results = soup.find('h1', class_='title is-clearfix').get_text(strip=True)
            total = int(re.search(r'Showing \d+–\d+ of (\d+) results', total_results).group(1))

            if start + 200 < total:
                start += 200
            else:
                break
        else:
            print("Failed to fetch data from arXiv.")
            break
    
    gpt_output = ""
    id=1
    client = OpenAI(api_key = "Your gpt api key") #
    for paper_group in tqdm(all_papers):
        time.sleep(1.1)
        gpt_input = f'幫我統整以下1篇論文，編號第{id}，格式如下:[編號]\n[英文標題]\n[中文標題]\n[所有作者(以逗點隔開)]\n[你統整的內容(條列式)]\n[同行審查(有被收錄請標註如CVPR2024，沒有則照comment裡原文貼上，若沒有comment則特別標記comment: 無)]\n[分隔線(==========)]: \n'+str(paper_group)
        id+=1
        
        gpt_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user", "content": gpt_input}]
        )
        
        gpt_output += gpt_response.choices[0].message.content+ "\n\n"
        
    output_filename = "./gpt_output/gpt_output.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(gpt_output)

    print(f"\nGPT output saved to {output_filename}")

    doc = Document()
    doc.add_paragraph(gpt_output)
    doc.save("./gpt_output/gpt_output.docx")
    print("GPT output saved to gpt_output.docx\n")

    return 

def open_arxiv(date=None):

    if date is not None:
        yesterday = (date - timedelta(days=1)).strftime('%Y-%m-%d')
        date_str = date.strftime('%Y-%m-%d')
    else:
        date = datetime.today()
        yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        date_str = date.strftime('%Y-%m-%d')

    url = f"https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=&terms-0-field=title&classification-computer_science=y&classification-physics_archives=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date={yesterday}&date-to_date={date_str}&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first"

    info = webbrowser.open(url)
    if info:
        print("\nOpen website successfully.\n")
    else:
        print("\nError with opening browser.\n")

def main():

    print("===================================================================================")
    print("This program accesses information from the arXiv website, which is owned by Cornell\nUniversity (Educational Corporation; NEW YORK, USA).\n\nAll papers are owned by their respective authors.")
    print("\nThis program is solely for the purpose of web scraping and does not engage in any \ncopyright infringement.\n\nProgram Version: 1.3.1")
    print("===================================================================================\n")
    target_date = datetime.today()
    while True:
        
        selection = input("Press 1~5 to select a function:(press 0 to terminate executing this program)\n1. Setting target date.\n2. Open today's arXiv website(CS field).\n3. Open target date's arXiv website(CS field).\n4. Let GPT conclusion today's paper.\n5. Let GPT conclusion target_date's paper.\nYour Choice: ")
        if selection == "0":
            return 
        elif selection == "1":
            target_date = set_target()
        elif selection == "2":
            open_arxiv()
        elif selection == "3":
            open_arxiv(date = target_date)
        elif selection == "4":
            gpt_conclusion()
        elif selection =="5":
            gpt_conclusion(set_date = target_date)
        else:
            print("Invalid input. Please enter a number between 1 and 3, or 0 to exit.")

if __name__ == '__main__':
    main()
