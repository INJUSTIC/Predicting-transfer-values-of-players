import requests
from bs4 import BeautifulSoup
import pandas as pd
from cleaningFBREF import clean_player_name
from datetime import datetime
import dataframeSaver


def get_player_links():

    top_league_links = ['https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1/plus/?saison_id=2022',
                        'https://www.transfermarkt.co.uk/laliga/startseite/wettbewerb/ES1/plus/?saison_id=2022',
                        'https://www.transfermarkt.co.uk/serie-a/startseite/wettbewerb/IT1/plus/?saison_id=2022',
                        'https://www.transfermarkt.co.uk/bundesliga/startseite/wettbewerb/L1/plus/?saison_id=2022',
                        'https://www.transfermarkt.co.uk/ligue-1/startseite/wettbewerb/FR1/plus/?saison_id=2022']

    teams = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
    site = 'https://www.transfermarkt.co.uk'
    for top_league_link in top_league_links:

        pageTree = requests.get(top_league_link, headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
        links = pageSoup.select(
            ".responsive-table tbody tr td:nth-of-type(2) a")
        for link in links:
            team = link["href"]
            if team != '#' and team[-4:] == '2022':
                teams.append(site + team)
    players = []
    for team in teams:
        pageTree = requests.get(team, headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
        links = pageSoup.select(
            '.responsive-table tbody tr td:nth-of-type(2) a')
        for i in range(len(links)):
            if links[i]["href"] == '#':
                players.append(site + links[i+1]["href"])
                i += 2

    return players


def scrapTransfermarkt(player_links):
    nameList = []
    heightList = []
    ageList = []
    nationalityList = []
    footList = []
    positionList = []
    currClubList = []
    contrExpList = []
    currValueList = []
    for page in player_links:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
        pageTree = requests.get(page, headers=headers)
        soup = BeautifulSoup(pageTree.content, 'html.parser')
        # Extracting Full name
        name = soup.find('tm-compare-player')['player-full-name']

        # Extracting height
        temp = soup.find('span', text='Height:')
        if temp:
            height = temp.find_next_sibling('span').text.strip().split('\xa0')[
                0].replace(',', '.')
        else:
            continue

        # Extracting Age
        temp = soup.find('span', text='Age:')
        if temp:
            age = temp.find_next_sibling('span').text.strip()
        else:
            continue

        # Extracting nationality
        temp = soup.find('span', text='Citizenship:')
        if temp:
            nationality = temp.find_next('span').text.strip().split('\xa0')[0]
        else:
            continue

        temp = soup.find('span', text='Foot:')
        if temp:
            foot = temp.find_next_sibling('span').text.strip()
        else:
            continue

        # Extracting Position
        temp = soup.find('span', text='Position:')
        if temp:
            position = temp.find_next_sibling('span').text.strip()
        else:
            continue

        # Extracting Current club
        temp = soup.select_one(
            '.info-table__content--bold.info-table__content--flex a[title]')
        if temp:
            current_club = temp.text
        else:
            continue

        # Extracting Current value
        temp = soup.find(
            'div', class_='tm-player-market-value-development__current-value')
        if temp:
            current_value = temp.get_text(strip=True)
        else:
            continue

        if current_value[-1] == 'm':
            current_value = int(float(current_value[1:-1])*1000000)
        elif current_value[-1] == 'k':
            current_value = int(float(current_value[1:-1])*1000)
        elif current_value == '-':
            current_value = 0
        else:
            current_value = int(float(current_value[1:-1]))

        temp = soup.find('span', text='Contract expires:')
        if temp:
            contract_expire_year_str = temp.find_next_sibling(
                'span').text.strip()
        else:
            continue

        if contract_expire_year_str == '-':
            contract_expire_year = 0
        else:
            contract_expire_year = datetime.strptime(
                contract_expire_year_str, "%b %d, %Y").date().year - datetime.now().year

        nameList.append(name)
        ageList.append(age)
        footList.append(foot)
        positionList.append(position)
        currClubList.append(current_club)
        currValueList.append(current_value)
        contrExpList.append(contract_expire_year)
        nationalityList.append(nationality)
        heightList.append(height)

    df = pd.DataFrame({"Player": nameList, "Club": currClubList, "Position": positionList, "Age": ageList, "Nationality": nationalityList,
                      "Current value in euro": currValueList, "Contract expire date": contrExpList, "Foot": footList, "Height": heightList})
    df = clean_player_name(df)

    dataframeSaver.saveDataframe(df, 'transfermarkt.xlsx')
