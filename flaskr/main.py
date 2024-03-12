from flask import Flask, render_template, request
import calendar
import requests
from bs4 import BeautifulSoup
import datetime
import re


app = Flask(__name__)

def scrape_data(team_name):
    if team_name == ' ':
        return []
        
    res = requests.get('https://www.nmjp.net/football/')
    soup = BeautifulSoup(res.text, 'html.parser')
    
    tag_objs = soup.find_all('tr')
    
    my_list = []
    for tag_obj in tag_objs:
        text = tag_obj.get_text()
        if team_name in text:
            if '延期' not in text:
                text_list = text.split(' ')
                sprited_list = [word for word in text_list if word.strip()]
                my_list.append(sprited_list)
    return my_list

@app.route('/')
def index():
    now = datetime.datetime.now()
    year = request.args.get('year', now.year, type=int)
    month = request.args.get('month', now.month, type=int)
    cal = calendar.monthcalendar(year, month)
    
    #team_name = ''  # ここにユーザーが入力したチーム名を入れるようにする
    team_name = request.args.get('team_name', None)
    if team_name is None:
        team_name = ' '

    team_list = []
    scraped_list = []
    team_list.append(team_name)
    for team in team_list:
        scraped_data = scrape_data(team)
        scraped_list.append(scraped_data)
    
    
    date_list = []
    for date in scraped_data:
        result = re.sub(r"\D", "", date[0])
        date_list.append(int(result))
    
    return render_template('index.html', cal=cal, year=year, month=month, scraped_data=scraped_data, date_list=date_list, team_name=team_name, team_list=team_list)

if __name__ == '__main__':
    app.run(debug=True)
