from bs4 import BeautifulSoup
import requests
import smtplib

def scrape():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"}

    url = "https://www.imdb.com/chart/top"
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    movies_list = soup.find("tbody", {"class": "lister-list"}).findAll("tr")

    movie_bundle = []
    for movie in movies_list:
        movie_name = movie.find("td", {"class": "titleColumn"}).find("a").get_text()
        rating = movie.find("td", {"class": "ratingColumn imdbRating"}).get_text()
        released_on = movie.find("td", {"class": "titleColumn"}).find("span").get_text()
        movie_bundle.append([movie_name.strip(), rating.strip(), released_on.strip()])
    
    return movie_bundle

def send_mail(formatted_list):
    # Add the sender email as string.
    sender = ''
    # Add the receiver email as string or list if you need to send to multiple emails
    receiver = ''
    # Add the credentials as string
    password = ''
    subject = 'Top Movies From IMDB'

    body = f'''
Hey, There !
These are the top rated movies scraped from the official IMDB site. Enjoy Sent via Python SMTP!

{formatted_list}
'''
    
    message = f'Subject: {subject}\n\n{body}'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(sender, password)
    server.sendmail(sender, receiver, message.encode("utf8"))
    server.quit()

def format_movies(bundle):
    count = 1
    movie_list = ""
    for movie in bundle:
        movie_list += f'{count}.    {movie[0]}{movie[2]} | Rating: {movie[1]} \n\n'
        count +=1
    return movie_list

send_mail(format_movies(scrape()))
