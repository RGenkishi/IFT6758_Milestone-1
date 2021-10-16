---
layout: post
title:  "Acquisition de données"
date:   2021-10-01 11:27:11
categories: jekyll update
---

# Question 1

##### <span style="color:grey">Rédigez un bref tutoriel sur la façon dont votre équipe a téléchargé l'ensemble de données. Imaginez :) que vous cherchiez un guide sur la façon de télécharger les données play-by-play ; votre guide devrait vous faire dire "Parfait - c'est exactement ce que je cherchais!". Cela peut être aussi simple que de copier votre fonction et un exemple d'utilisation, et d'écrire une ou deux phrases la décrivant.</span>

L’API qui permet d’accéder aux données des parties de la LNH est assez facile d’utilisation. L’url de l’API a le format suivant : https://statsapi.web.nhl.com/api/v1/game/ID/feed/live où ID représente l’identifiant unique de la partie.
L’identifiant de la partie est séparé en trois parties. L’année de la saison, le type de partie (01 pour la pré-saison, 02 pour la saison régulière, et 03 pour les séries éliminatoires), et l’identifiant de la partie comme tel. 

Pour la saison régulière, l’identifiant de la partie est un nombre à 4 chiffres, de 0001 à 1271 (puisqu’il y a 1271 parties dans une saison régulière depuis la saison 2016-2017). Ainsi, pour prendre un exemple, la quatrième partie de la saison régulière de 2016-2017 aurait l’identifiant 2017020004.

Les choses se compliquent un peu pour l’identifiant de partie des séries éliminatoires. Les séries éliminatoires voient s’affronter 16 équipes et se déroule en 4 tours. Chaque tour (round) les équipes s’affronter dans un 4 de 7. La première à remporter 4 parties (game) l’emporte. Lors du premier tour, il y a 8 affrontements (matchup) entre 2 équipes, puis 4 au tour suivant, puis 2 et finalement 1. L’identifiant d’une partie en série éliminatoire est aussi un nombre de 4 chiffre. Le premier chiffre est un 0, le second est le numéro du tour, le troisième le numéro de l’affrontement, puis le dernier est le numéro de partie. Ainsi, pour prendre un exemple, le troisième match du deuxième affrontement du premier tour des séries éliminatoire de la saison 2016-2017 aurait l’identifiant 2017030123.

En python, on peut faire des requêtes à un API grâce à la librairie `requests` et sa méthode `get()`. En passant l’url de la requête en paramètre, on recevra les données sous format json. Voici le code que l’on peut utiliser pour aller chercher toutes les données des parties pour une année en saison réguliere.

```
game_data = {}
max_game = 1271
season_type = "02"
for i in range(1, (max_game+1)):
    gameId = str(year) + season_type + str(i).zfill(4)
    response = requests.get(url=(self.api_url + gameId +"/feed/live"))
    game_data["regular" + gameId] = response.json()
    time.sleep(0.1)
```

Il est recommandé une faire un time.sleep() d’au moins un dixième de seconde entre chaque requête afin de ne pas surchargé l’API et risquer de se faire bannir.

Pour aller chercher les données pour les séries éliminatoires, on peut utiliser le code suivant :

```
game_data = {}
first_digit = 0
season_type = "03"

for round in range(1, 5):
    for matchup in range(1, ((8 // (2 ** (round - 1))) + 1)):
        for game in range(1, 8):
            game_id = str(year) + season_type + str(first_digit) + str(round) + str(matchup) + str(game)
            url = (self.api_url + game_id + "/feed/live")
            print(url)
            response = requests.get(url=(self.api_url + game_id + "/feed/live"))
            if (response.status_code == 404):
                time.sleep(0.1)
                break
            game_data["playoff" + game_id] = response.json()
            time.sleep(0.1)
```

