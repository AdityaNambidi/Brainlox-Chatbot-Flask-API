import requests
from bs4 import BeautifulSoup

#This program checks the given brainlox url and collects the url of each course into a list.

url = 'https://brainlox.com/courses/category/technical'
domain = "https://brainlox.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extracting course links
def get_urls():
    courses = []
    for course in soup.find_all('div', class_='single-courses-box'):
        link = course.find('a', class_="d-block image").get('href')
        courses.append(domain + link)
    
    return courses