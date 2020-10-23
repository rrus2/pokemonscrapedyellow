import requests
from bs4 import BeautifulSoup
import csv

def download_pages():
    r = requests.get('https://pokemondb.net/pokedex/game/red-blue-yellow', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'})
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find('div', attrs={'class': 'infocard-list infocard-list-pkmn-lg'})
    linksToFilter = [x['href'] for x in div.find_all('a', attrs={'class': 'ent-name'})]
    links = []
    for link in linksToFilter:
        links.append('https://pokemondb.net' + link)
    return links

def download_links_and_return_dict(pages):
    listToReturn = [['ID', 'Name', 'Types', 'Species', 'Height', 'Weight', 'Abilities']]
    dictToReturn = []
    for page in pages:
        r = requests.get(page, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'})
        soup = BeautifulSoup(r.text, 'html.parser')
        name = soup.find('h1').get_text()
        print(name)
        table = soup.find('table')
        ids = table.find('strong').get_text()
        typesArr = [x.get_text() for x in table.find_all('a', attrs = {'class':'type-icon'})]
        types = ', '.join(typesArr)
        species = table.find_all('tr')[2].find('td').get_text()
        height = table.find_all('tr')[3].find('td').get_text()
        weight = table.find_all('tr')[4].find('td').get_text()
        abilities = [x.get_text() for x in table.find_all('tr')[5].find_all('a')]
        abilitiesStr = ', '.join(abilities)
        l = [ids, name, types, species, height, weight, abilitiesStr]
        listToReturn.append(l)
        d = {
            'ID': ids,
            'Name': name,
            'Types': types,
            'Species': species,
            'Height': height,
            'Weight': weight,
            'Abilities': abilitiesStr
        }
        dictToReturn.append(d)

    return dictToReturn

def make_csv(listOfPokemon):
    with open('pokemon.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        for i in listOfPokemon:
            writer.writerows(i)

def make_dict(listOfDicts):
    print(listOfDicts)
    with open('pokemon2.csv', 'w', encoding='UTF-8') as csvFile:
        fieldnames = ['ID', 'Name', 'Types', 'Species', 'Height', 'Weight', 'Abilities']
        writer = csv.DictWriter(csvFile, fieldnames)
        writer.writeheader()
        for i in listOfDicts:
            writer.writerow(i)

def main():
    pages = download_pages()
    listOfPokemon = download_links_and_return_dict(pages)
    make_dict(listOfPokemon)

if __name__ == '__main__':
    main()