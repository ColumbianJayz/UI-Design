import json
from flask import Flask, render_template, Response, request, jsonify

app = Flask(__name__)

data = {
  "1": {
    "id": "1",
    "title": "Igual Que un Àngel",
    "artist": ["Kali Uchis, Peso Pluma"],
    "image": "https://i.scdn.co/image/ab67616d0000b273b968625b03ec59b30b48e9c3",
    "year": "2023",
    "genres": ["Latino Urbano", "Pop", "Musica Tropicale", "Dembow"],
    "similar song ids": ["2", "3", "10"],
    "summary": "\"Igual que un Ángel\" is about love's untainted form. Uchis and Peso whisper of a woman, an enigma not swayed by glitter, who craves only love's purest essence, knowing its power to transform. Though scarred by past heartbreaks, her spirit remains untainted, a testament to resilience. In her, Uchis and Pluma see a celestial being sent to guide us in preserving our hearts through trials and disillusionment."
  },
  "2": {
    "id": "2",
    "title": "TQG",
    "artist": ["Karol G, Shakira"],
    "image": "https://remezcla.com/wp-content/uploads/2023/02/508c2b7b-df27-52fb-f955-94a2ec9e04a1-1424x1068.jpeg",
    "year": "2023",
    "genres": ["Reggaeton", "Latino Urbano", "Pop", "Musica Tropical"],
    "similar song ids": ["3", "10"],
    "summary": "\"TQG\" is an acronym for the phrase \"Te Quedó Grande\"; is a reggaeton track, but it's also considered as a diss. The song's lyrics features \"shots\" directed at their ex-boyfriends, Puerto Rican artist Anuel AA and Spanish footballer Gerard Pique. The song also presents lyrics sung by Shakira about Pique's current girlfriend, Clara Chia."
  },
  "3": {
    "id": "3",
    "title": "Columbia",
    "artist": ["Quevedo"],
    "image": "https://m.media-amazon.com/images/I/51WvqboN5sL._UXNaN_FMjpg_QL85_.jpg",
    "year": "2023",
    "genres": ["Reggaeton", "España", "Pop", "Musica Tropical"],
    "similar song ids": ["2", "3", "10"],
    "summary": "«Columbia» es una canción del cantante español Quevedo. Es el primer trabajo en solitario desde el lanzamiento de su primer álbum Donde quiero estar."
  },
  "4": {
    "id": "4",
    "title": "Cactus",
    "artist": ["Belinda"],
    "image": "https://www.rollingstone.com/wp-content/uploads/2024/02/belinda-cactus.jpg?w=1581&h=1054&crop=1",
    "year": "2024",
    "genres": ["Regional Mexicano", "Pop", "Corrido"],
    "similar song ids": ["4"],
    "summary": "\"Cactus\" is a song by Spanish-Mexican singer-songwriter Belinda released as the lead single from her upcoming fifth studio album Indomable. It is her first single in 10 years since \"I Love You... Te Quiero\"."
  },
  "5": {
    "id": "5",
    "title": "CONTIGO",
    "artist": ["Karol G", "Tiësto"],
    "image": "https://www.rollingstone.com/wp-content/uploads/2024/02/Karol-G.png?w=1342&h=846&crop=1",
    "year": "2024",
    "genres": ["Reggaeton", "Colombia", "Pop", "Electronic"],
    "similar song ids": ["2", "3", "6"],
    "summary": "«Contigo» (estilizado en mayúsculas) es una canción de la cantante colombiana Karol G y el DJ neerlandés Tiësto. Fue lanzado el 14 de febrero de 2024 a través de Bichota Records e Interscope Records."
  },
  "6": {
    "id": "6",
    "title": "LALA",
    "artist": ["Myke Towers"],
    "image": "https://remezcla.com/wp-content/uploads/2023/02/508c2b7b-df27-52fb-f955-94a2ec9e04a1-1424x1068.jpeg",
    "year": "2023",
    "genres": ["Reggaeton"],
    "similar song ids": ["2", "3", "10"],
    "summary": "The \"sing-song\", described as \"fun in [its] own right\",[1] talks about different motions of a flirt, examining feelings of affection and jealousy.[2] Although the meaning behind the chorus has not been explained, it is widely believed to be ambiguous. Majority of users picking up the track on TikTok are shown making a tongue movement.[3] Following a surge in popularity on TikTok in late June 2023, the song went on to chart in the top 5 of multiple countries on Spotify,[4] becoming Towers' highest charting song on several streaming platforms to date.[5]"
  },
  "7": {
    "id": "7",
    "title": "La Victima",
    "artist": ["Xavi"],
    "image": "https://remezcla.com/wp-content/uploads/2023/02/508c2b7b-df27-52fb-f955-94a2ec9e04a1-1424x1068.jpeg",
    "year": "2023",
    "genres": ["Regional Mexicano"],
    "similar song ids": ["4"],
    "summary": "\"La Víctima\" is a song by American singer-songwriter Xavi, which was released as a single on August 17, 2023, through Interscope. The song achieved virality through TikTok,[1] which lead to becoming the singer's breakthrough single, debuting at number 91 on the Billboard Hot 100 and peaking at number 46.[2][3] Prior to the release of \"La Diabla\", which would be the singer's second breakthrough single, \"La Víctima\" was the singer's highest charting song to date."
  },
  "8": {
    "id": "8",
    "title": "La Diabla",
    "artist": ["Xavi"],
    "image": "https://i.scdn.co/image/ab67616d0000b273b968625b03ec59b30b48e9c3",
    "year": "2023",
    "genres": ["Regional Mexicano"],
    "similar song ids": ["4"],
    "summary": "\"La Diabla\" is a song by American singer-songwriter Xavi, which was released as a single on November 8, 2023, through Interscope. The song achieved virality through TikTok, which lead to becoming the singer's second breakthrough single, peaking at number 32 on the Billboard Hot 100."
  },
  "9": {
    "id": "9",
    "title": "Pa Que Guaye",
    "artist": ["Natti Natasha, Karol G"],
    "image": "https://i.scdn.co/image/ab67616d0000b273b968625b03ec59b30b48e9c3",
    "year": "2023",
    "genres": ["Reggaeton", "Latino Urbano"],
    "similar song ids": ["2", "3", "10"],
    "summary": "\"Pa' Que Guaye\" is a song by Dominican singer Natti Natasha and Colombian singer Karol G. It was released on March 10, 2023, as the third single from Natasha's upcoming third studio album."
  },
  "10": {
    "id": "10",
    "title": "Ella Quiere Beber",
    "artist": ["Anuel AA, Romeo Santos"],
    "image": "https://i.scdn.co/image/ab67616d0000b273b968625b03ec59b30b48e9c3",
    "year": "2023",
    "genres": ["Reggaeton", "Latino Urbano", "Bachata"],
    "similar song ids": ["2", "3", "6"],
    "summary": "\"Ella Quiere Beber\" is a song by Puerto Rican rapper Anuel AA featuring American singer Romeo Santos. It was released on October 12, 2023, as the lead single from Anuel AA's second studio album. The song combines elements of reggaeton and bachata, and its lyrics revolve around a woman who wants to forget her ex by going out to drink and party."
  }
} # type: ignore





# Routes

@app.route('/')
def welcome():
    first_three_items = {k: data[k] for k in list(data)[:3]}
    return render_template('welcome.html', data=first_three_items)
@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    if not query:
        return render_template('welcome.html', data={}, search_query=query, message="No results found. Please enter a valid search")

    results = []
    for item_id, item in data.items():
      
        if query in item['title'].lower():
            results.append(item)
            continue 

        
        if any(query in artist.lower() for artist in item.get('artist', [])):
            results.append(item)
            continue 

       
        if any(query in genre.lower() for genre in item.get('genres', [])):
            results.append(item)
            continue 

    if not results:
        message = "No results found"
    else:
        message = f"Found it! Displaying results below for \"{query}\""
    return render_template('search.html', results=results, search_query=query, message=message)

@app.route('/view/<id>')
def view(id):
    item = data.get(id)
    if item:
        return render_template('view.html', item=item)
    else:
        return "Item not found", 404


if __name__ == '__main__':
    app.run(debug=True)
