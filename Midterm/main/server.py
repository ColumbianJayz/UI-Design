import json, re
from flask import Flask, render_template, Response, request, jsonify

app = Flask(__name__)

data = {
  "1": {
    "id": "1",
    "title": "Igual Que un Àngel",
    "artist": ["Kali Uchis, Peso Pluma"],
    "image": "https://64.media.tumblr.com/fea2798d3f686690beb34bcec1b4f1b5/a36c9b9125005231-09/s540x810/d03098ddf2be4359e26d15bf41546f929ee13330.gif",
    "year": "2023",
    "genres": ["Latino Urbano", "Pop", "Musica Tropicale", "Dembow"],
    "summary": "\"Igual que un Ángel\" is about love's untainted form. Uchis and Peso whisper of a woman, an enigma not swayed by glitter, who craves only love's purest essence, knowing its power to transform. Though scarred by past heartbreaks, her spirit remains untainted, a testament to resilience. In her, Uchis and Pluma see a celestial being sent to guide us in preserving our hearts through trials and disillusionment."
  },
  "3": {
    "id": "3",
    "title": "TQG",
    "artist": ["Karol G, Shakira"],
    "image": "https://64.media.tumblr.com/5bbb3ea27d777ec450eaa392f089bf4f/08fa49c11c961ab4-62/s1280x1920/5041eca1ee1f3ef1b6f12907b107f12221f1a77f.gifv",
    "year": "2023",
    "genres": ["Reggaeton", "Latino Urbano", "Pop", "Musica Tropical"],
    "summary": "\"TQG\" is an acronym for the phrase \"Te Quedó Grande\"; is a reggaeton track, but it's also considered as a diss. The song's lyrics features \"shots\" directed at their ex-boyfriends, Puerto Rican artist Anuel AA and Spanish footballer Gerard Pique. The song also presents lyrics sung by Shakira about Pique's current girlfriend, Clara Chia."
  },
  "2": {
    "id": "2",
    "title": "Con Altura",
    "artist": ["Rosalía"],
    "image": "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ2djaXl5OTluYTg1ODA2aWx2dDljczAzYzhidHBlOGQ1Z3piZWswNCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/24FIitrXGVRFEv2IX9/giphy.gif",
    "year": "2019",
    "genres": ["Reggaeton", "España", "Pop", "Musica Tropical"],
    "summary":"\"Con Altura\" is a song by Spanish singer Rosalía and Colombian singer J Balvin, featuring Spanish producer el Guincho. Written by Rosalía, Balvin, Aury Mariachi Budda Pineda, el Guincho, Frank Dukes, Teo Halm, and Sky Rompiendo and produced by the last four alongside the Spanish singer, the song was released by Columbia Records on 28 March 2019.[1]"
  },
  "4": {
    "id": "4",
    "title": "Cactus",
    "artist": ["Belinda"],
    "image": "https://www.rollingstone.com/wp-content/uploads/2024/02/belinda-cactus.jpg?w=1581&h=1054&crop=1",
    "year": "2024",
    "genres": ["Regional Mexicano", "Pop", "Corrido"],
    "summary": "\"Cactus\" is a song by Spanish-Mexican singer-songwriter Belinda released as the lead single from her upcoming fifth studio album Indomable. It is her first single in 10 years since \"I Love You... Te Quiero\"."
  },
  "5": {
    "id": "5",
    "title": "CONTIGO",
    "artist": ["Karol G", "Tiësto"],
    "image": "https://www.rollingstone.com/wp-content/uploads/2024/02/Karol-G.png?w=1342&h=846&crop=1",
    "year": "2024",
    "genres": ["Reggaeton", "Colombia", "Pop", "Electronic"],
    "summary": "«Contigo» (estilizado en mayúsculas) es una canción de la cantante colombiana Karol G y el DJ neerlandés Tiësto. Fue lanzado el 14 de febrero de 2024 a través de Bichota Records e Interscope Records."
  },
  "6": {
    "id": "6",
    "title": "Tu no eres para mi",
    "artist": ["Fanny Lu"],
    "image": "https://s3.amazonaws.com/image.blingee.com/images17/content/output/000/000/000/602/511879380_704332.gif?4",
    "year": "2008",
    "genres": ["POP"],
    "summary": "The song was written and produced by Fanny Lu, José Gaviria and Andrés Munera. It includes guitar and accordion solos. The lyrics describe a failing romantic relationship, in which the singer describes how she previously loved her man, but he was dishonest with her. As a result, she decides to break him up, admitting that they are not for each other."
  },
  "7": {
    "id": "7",
    "title": "No Querias Lastimarme",
    "artist": ["Gloria Trevi"],
    "image": "https://j.gifs.com/X6ErAV.gif",
    "year": "2012",
    "genres": ["POP"],
    "summary": "\"La Víctima\" es el segundo sencillo del noveno álbum de estudio De película de la cantautora y actriz mexicana Gloria Trevi.3​ Fue lanzado como sencillo por la empresa discográfica Universal Music Latino oficial el lunes 16 de septiembre de 2013.4​ Se trata de una balada romántica perteneciente a los géneros de pop y pop latino.5​ Compuesta por Gloria junto a su hijo Ángel Gabriel y Marcela de la Garza y producida por Armando Ávila."
  },
  "8": {
    "id": "8",
    "title": "Bellisima",
    "artist": ["Annalisa"],
    "image": "https://64.media.tumblr.com/ec33b56b9fcf00c76155bfdde1fb47a9/791a93382355f2d0-0e/s540x810/93e5a1c344ac5143f14f25b4876f98f373ddb7a7.gifv",
    "year": "2022",
    "genres": ["POP"],
    "summary": "I wrote \"Bellisima\" in August 2021, at a decisive moment in my career, the one when you look in the mirror and decide that once you have cleared all filters you can finally build something completely new. It is a painful tale, a punch in the stomach, but written with self-mockery and a pinch of romantic hysteria. It makes you dance, yes, but with tears. That's exactly how I am"
  },
  "9": {
    "id": "9",
    "title": "Chantaje",
    "artist": ["Shakira, Maluma"],
    "image": "https://66.media.tumblr.com/d19cc628978b28174b33051f261478b5/ef70356b5364821d-03/s400x600/d340549e316f55c0e7b17ced52ff8a14d95668e9.gif",
    "year": "2016",
    "genres": ["Reggaeton", "Latino Urbano"],
    "summary": "\"Chantaje\" Puerto Rican composer and recording artist Kenai had the word \"Chantaje\" in his mind months before the idea of a collaboration with Shakira and Maluma emerged.[3] He stated in an interview that the idea of the song was intended to be his own single.[4] While working on music demos in Colombia with The Rudeboyz, he received a call from the production duo to work on a collaborative single between Shakira and Maluma that was intended to be presented to the artists the next day. They were supposed to offer three different demos to Shakira and Maluma, but ended up working on just one feeling confident enough about its potential. The three worked together on the demo one night in Colombia. The Rudeboyz traveled without Kenai the next day to Barcelona, Spain to meet with Shakira and Maluma to keep working on the song together.[3]"
  },
  "10": {
    "id": "10",
    "title": "Hawaii - Remix",
    "artist": ["Maluma, The Weekend"],
    "image": "https://media1.tenor.com/m/RAOtXuz859IAAAAC/the-weeknd-maluma.gif",
    "year": "2020",
    "genres": ["Reggaeton"],
    "summary": "\"Hawaii\"  is a reggaeton song with pop ballad elements about the protagonist dealing with his ex lover publicly preaching her newfound happiness after their break-up, not convinced by her social media persona."
  }
} # type: ignore





# Routes

@app.route('/')
def welcome():
    first_three_items = {k: data[k] for k in list(data)[:3]}
    return render_template('welcome.html', data=first_three_items)

def highlight_case_insensitive(text, search_query):
    def replace_with_highlight(match):
        return f"<span class='highlight'>{match.group(0)}</span>"  # Use matched text
    
    pattern = re.compile(re.escape(search_query), re.IGNORECASE)
    return pattern.sub(replace_with_highlight, text)


@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    results = []
    for item_id, item in data.items():
        title = item['title']
        artist = ", ".join(item['artist'])  # Assuming 'artist' is a list
        genres = ", ".join(item['genres'])  # Assuming 'genres' is a list
        year = item['year']

        # Check for matches (case-insensitive)
        match_in_title = query in title.lower()
        match_in_artist = any(query in a.lower() for a in item['artist'])
        match_in_genres = any(query in g.lower() for g in item['genres'])
        match_in_year = query in str(year)


        if match_in_title or match_in_artist or match_in_genres or match_in_year:
            highlighted_title = highlight_case_insensitive(title, query)
            highlighted_artist = highlight_case_insensitive(artist, query)
            highlighted_genres = highlight_case_insensitive(genres, query)
            highlighted_year = highlight_case_insensitive(str(year), query)

            results.append({'id': item['id'], 'title': highlighted_title, 'artist': highlighted_artist, 'genres': highlighted_genres, 'year': highlighted_year, 'image': item['image'], 'summary': item['summary']})

    return render_template('search.html', results=results, search_query=query)

@app.route('/view/<id>')
def view(id):
    item = data.get(id)
    if item:
        return render_template('view.html', item=item)
    else:
        return "Item not found", 404

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        
        new_song_data = request.json

     
        new_id = str(max([int(k) for k in data.keys()]) + 1)
        new_song_data['id'] = new_id  

    
        data[new_id] = new_song_data

      
        return jsonify({"message": "Song added successfully", "id": new_id}), 200
    
    return render_template('/add.html')

@app.route('/api/song/<id>', methods=['GET'])
def get_song(id):
    song = data.get(id)
    if song:
        return jsonify(song)
    else:
        return jsonify({"error": "Song not found"}), 404

@app.route('/edit/<id>', methods=['GET'])
def edit_song(id):
    return render_template('edit.html')

@app.route('/update/<id>', methods=['POST'])
def update_song(id):
    updated_song_data = request.json
    if id in data:
        data[id] = updated_song_data
        data[id]['id'] = id 
        return jsonify({"message": "Song updated successfully", "id": id}), 200
    else:
        return jsonify({"error": "Song not found"}), 404
if __name__ == '__main__':
    app.run(debug=True)
