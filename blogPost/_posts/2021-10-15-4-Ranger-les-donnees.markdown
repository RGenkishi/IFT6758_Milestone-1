---
layout: post
title:  "Ranger les données"
date:   2021-10-15 14:41:00
categories: jekyll update
---

# Question 1

##### <span style="color:grey">Dans votre article de blog, incluez un petit extrait de votre cadre de données final (par exemple, en utilisant head(10)). Vous pouvez simplement inclure une capture d'écran plutôt que de vous battre pour que les tableaux soient soigneusement formatés en HTML/markdown.</span>

<br> 

####  Tableau des 10 premiers éléments de la saison 2019 rangés selon les indications


|   | game_id           | game_time            | date_year | date_month | date_day | period_time | which_period | period_type | event_type | is_goal | shot_type  | strength | team_id | team_name           | team_link        | team_tri_code | shooter_name     | goalie_name       | rink_side | coord_x | coord_y |
|---|-------------------|----------------------|-----------|------------|----------|-------------|--------------|-------------|------------|---------|------------|----------|---------|---------------------|------------------|---------------|------------------|-------------------|-----------|---------|---------|
| 0 | regular2019020001 | 2019-10-02T23:15:32Z | 2019      | 10         | 2        | 00:25       | 1            | REGULAR     | Goal       | True    | Tip-In     | Even     | 9       | Ottawa Senators     | /api/v1/teams/9  | OTT           | Brady Tkachuk    | Frederik Andersen | left      | 85.0    | -1.0    |
| 1 | regular2019020001 | 2019-10-02T23:18:23Z | 2019      | 10         | 2        | 01:31       | 1            | REGULAR     | Shot       | False   | Snap Shot  |          | 10      | Toronto Maple Leafs | /api/v1/teams/10 | TOR           | Morgan Rielly    | Craig Anderson    | right     | -32.0   | -2.0    |
| 2 | regular2019020001 | 2019-10-02T23:20:45Z | 2019      | 10         | 2        | 03:23       | 1            | REGULAR     | Shot       | False   | Snap Shot  |          | 9       | Ottawa Senators     | /api/v1/teams/9  | OTT           | Dylan DeMelo     | Frederik Andersen | left      | 63.0    | -6.0    |
| 3 | regular2019020001 | 2019-10-02T23:21:17Z | 2019      | 10         | 2        | 03:56       | 1            | REGULAR     | Shot       | False   | Wrist Shot |          | 10      | Toronto Maple Leafs | /api/v1/teams/10 | TOR           | Morgan Rielly    | Craig Anderson    | right     | -59.0   | -20.0   |
| 4 | regular2019020001 | 2019-10-02T23:22:36Z | 2019      | 10         | 2        | 04:47       | 1            | REGULAR     | Shot       | False   | Slap Shot  |          | 10      | Toronto Maple Leafs | /api/v1/teams/10 | TOR           | Tyson Barrie     | Craig Anderson    | right     | -42.0   | -29.0   |
| 5 | regular2019020001 | 2019-10-02T23:22:41Z | 2019      | 10         | 2        | 04:53       | 1            | REGULAR     | Shot       | False   | Slap Shot  |          | 10      | Toronto Maple Leafs | /api/v1/teams/10 | TOR           | Tyson Barrie     | Craig Anderson    | right     | -52.0   | -7.0    |
| 6 | regular2019020001 | 2019-10-02T23:23:19Z | 2019      | 10         | 2        | 05:31       | 1            | REGULAR     | Shot       | False   | Wrist Shot |          | 10      | Toronto Maple Leafs | /api/v1/teams/10 | TOR           | Cody Ceci        | Craig Anderson    | right     | -38.0   | 38.0    |
| 7 | regular2019020001 | 2019-10-02T23:23:40Z | 2019      | 10         | 2        | 05:52       | 1            | REGULAR     | Shot       | False   | Wrist Shot |          | 10      | Toronto Maple Leafs | /api/v1/teams/10 | TOR           | Andreas Johnsson | Craig Anderson    | right     | -76.0   | -14.0   |
| 8 | regular2019020001 | 2019-10-02T23:24:37Z | 2019      | 10         | 2        | 06:02       | 1            | REGULAR     | Shot       | False   | Slap Shot  |          | 10      | Toronto Maple Leafs | /api/v1/teams/10 | TOR           | Mitchell Marner  | Craig Anderson    | right     | -63.0   | -31.0   |
| 9 | regular2019020001 | 2019-10-02T23:26:14Z | 2019      | 10         | 2        | 07:11       | 1            | REGULAR     | Shot       | False   | Tip-In     |          | 10      | Toronto Maple Leafs | /api/v1/teams/10 | TOR           | William Nylander | Craig Anderson    | right     | -78.0   | 13.0    |
| ...| ... | ... | ... |...| ... | ... | ... |...| ... | ... | ... |...| ... | ... | ... |...| ... | ... | ... |...| ... | 


<br>

---

# Question 2

##### <span style="color:grey">Vous remarquerez que le champ de « force » (c.-à-d. égal, avantage numérique, en désavantage numérique) n'existe que pour les buts, pas pour les tirs. De plus, il n'inclut pas la force réelle des joueurs sur la glace (c'est-à-dire 5 contre 4, ou 5 contre 3, etc.). Discutez de la façon dont vous pourriez ajouter les informations sur la force réelle (c'est-à-dire 5 contre 4, etc.) aux tirs et aux buts, compte tenu des autres types d'événements (au-delà des tirs et des buts) et des fonctionnalités disponibles. Vous n'avez pas besoin de l'implémenter pour ce jalon. 
</span>
<br>

Comment obtenir une information plus précise sur la force réelle des joueurs sur la glace ?

>Pour chaque game, dans le json retourné par l'API, dans gameData/Players, on a accès à la liste des joueurs >participants. Il est égallement possible de récupéré l'équipe pour chaque joueur avec la clé 'currentTeam' qui existe pour chacune des personnes participant au match.
>A partir de ces données, on peut compter le nombre de joueurs qui apparaissent dans les événements pour chaque équipe jusqu'a ce qu'un but soit marqué. On estime alors le nombre de joueur présent dans chaque équipe. Cependant on ne sait pas vraiment quand réinitilialiser les compte des joueurs.
>
>Une meilleure méthode consisterai à considérer qu'il y a 6 joueurs par équipe sur la glace au début du match. Puis, lors d'un but, on compte le nombre de pénalités mineure par équipe dans les 2 minutes qui précèdent le goal.
>On fait de même pour les pénalités majeure survenues dans les 5 minutes avant le but et pour les Inconduite dans les 10 minutes. Pour chaque équipe, on compte un nombre maximum de pénalité de 2 puiqu'une équipe ne peut avoir moins de 4 joueurs sur la glace.
>Ainsi, si l'équipe A a eu deux pénalités, et l'équipe B une seule, alors l'équipe A a encore 4 joueurs sur la glace et l'équipe B en a 5. Si le but est de l'équipe A, elle a donc marqué un but à 4 contre 5.


<br>


# Question 3

##### <span style="color:grey">En quelques phrases, discutez de certaines fonctionnalités supplémentaires que vous pourriez envisager de créer à partir des données disponibles dans cet ensemble de données. Nous ne cherchons pas de réponses particulières, mais si vous avez besoin d'inspiration, un tir ou un but pourrait-il être classé comme un rebond ou un tir dans le rush?</span>
<br>

