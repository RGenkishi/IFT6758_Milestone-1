---
layout: post
title:  "Ranger les données"
date:   2021-10-15 14:41:00
categories: jekyll update
---

# Question 1

##### <span style="color:grey">Dans votre article de blog, incluez un petit extrait de votre cadre de données final (par exemple, en utilisant head(10)). Vous pouvez simplement inclure une capture d'écran plutôt que de vous battre pour que les tableaux soient soigneusement formatés en HTML/markdown.</span>

<br> 

####  Tableau des 20 premiers éléments de la saison 2019 rangés selon les indications


|    | matchId    | event | period | teamId | teamName | teamLink | teamTriCode | coordX | coordY | shooterName | goalieName | strength | shotSecondaryType     |
|----|------------|-------|--------|--------|----------|----------|-------------|--------|--------|-------------|------------|----------|-----------------------|
| 0  | 2019020001 | Goal | 00:25 | 9  | Ottawa Senators     | /api/v1/teams/9  | OTT | 85.0  | -1.0  | Brady Tkachuk    | Frederik Andersen | Even | Tip-In     |
| 1  | 2019020001 | Shot | 01:31 | 10 | Toronto Maple Leafs | /api/v1/teams/10 | TOR | -32.0 | -2.0  | Morgan Rielly    | Craig Anderson    | None | Snap Shot  |
| 2  | 2019020001 | Shot | 03:23 | 9  | Ottawa Senators     | /api/v1/teams/9  | OTT | 63.0  | -6.0  | Dylan DeMelo     | Frederik Andersen | None | Snap Shot  |
| 3  | 2019020001 | Shot | 03:56 | 10 | Toronto Maple Leafs | /api/v1/teams/10 | TOR | -59.0 | -20.0 | Morgan Rielly    | Craig Anderson    | None | Wrist Shot |
| 4  | 2019020001 | Shot | 04:47 | 10 | Toronto Maple Leafs | /api/v1/teams/10 | TOR | -42.0 | -29.0 | Tyson Barrie     | Craig Anderson    | None | Slap Shot  |
| 5  | 2019020001 | Shot | 04:53 | 10 | Toronto Maple Leafs | /api/v1/teams/10 | TOR | -52.0 | -7.0  | Tyson Barrie     |   Craig Anderson  | None | Slap Shot  |
| 6  | 2019020001 | Shot | 05:31 | 10 | Toronto Maple Leafs | /api/v1/teams/10 | TOR | -38.0 | 38.0  | Cody Ceci        | Craig Anderson    | None | Wrist Shot |
| 7  | 2019020001 | Shot | 05:52 | 10 | Toronto Maple Leafs | /api/v1/teams/10 | TOR | -76.0 | -14.0 | Andreas Johnsson | Craig Anderson    | None | Wrist Shot |
| 8  | 2019020001 | Shot | 06:02 | 10 | Toronto Maple Leafs | /api/v1/teams/10 | TOR | -63.0 | -31.0 | Mitchell Marner  | Craig Anderson    | None | Slap Shot  |
| 9  | 2019020001 | Shot | 07:11 | 10 | Toronto Maple Leafs | /api/v1/teams/10 | TOR | -78.0 | 13.0  | William Nylander | Craig Anderson    | None | Tip-In     |
| 10 | 2019020001 | Shot | 07:30 | 10 | Toronto Maple Leafs | /api/v1/teams/10 | TOR | -32.0 | 34.0  | Tyson Barrie     | Craig Anderson    | None | Wrist Shot |
| 11 | 2019020001 | Shot | 07:39 | 10 | Toronto Maple Leafs | /api/v1/teams/10 | TOR | -80.0 | -4.0  | William Nylander | Craig Anderson    | None | Wrist Shot |
| 12 | 2019020001 | Shot | 07:59 | 9  | Ottawa Senators     | /api/v1/teams/9  | OTT | 78.0  | -5.0  | Colin White      | Frederik Andersen | None | Snap Shot  |
| 13 | 2019020001 | Shot | 08:05 | 9  | Ottawa Senators     | /api/v1/teams/9  | OTT | 47.0  | 23.0  | Thomas Chabot    | Frederik Andersen | None | Snap Shot  |
| 14 | 2019020001 | Shot | 08:15 | 10 | Toronto Maple Leafs | /api/v1/teams/10 | TOR | -64.0 | 24.0  | Auston Matthews  |  Craig Anderson   | None | Wrist Shot |
| 15 | 2019020001 | Shot | 09:08 | 9  | Ottawa Senators     | /api/v1/teams/9  | OTT | 83.0  | -4.0  | Anthony Duclair  | Frederik Andersen | None | Backhand   |
| 16 | 2019020001 | Shot | 10:06 | 9  | Ottawa Senators     | /api/v1/teams/9  | OTT | 67.0  | -20.0 | Tyler Ennis      | Frederik Andersen | None | Snap Shot  |
| 17 | 2019020001 | Shot | 10:12 | 9  | Ottawa Senators     | /api/v1/teams/9  | OTT | 47.0  | -36.0 | Nikita Zaitsev   | Frederik Andersen | None | Slap Shot  |
| 18 | 2019020001 | Shot | 12:22 | 9  | Ottawa Senators     | /api/v1/teams/9  | OTT | 56.0  | 28.0  | Anthony Duclair  | Frederik Andersen | None | Wrist Shot |
| 19 | 2019020001 | Shot | 12:58 | 10 | Toronto Maple Leafs | /api/v1/teams/10 | TOR | -45.0 | -41.0 | Morgan Rielly    | Craig Anderson    | None | Wrist Shot |
|....| .......... | .... | ..... | ...| ................... | ................ | ... | ......| ..... | ................ | ................. | .....| .......... | 



<br>

---

# Question 2

##### <span style="color:grey">Vous remarquerez que le champ de « force » (c.-à-d. égal, avantage numérique, en désavantage numérique) n'existe que pour les buts, pas pour les tirs. De plus, il n'inclut pas la force réelle des joueurs sur la glace (c'est-à-dire 5 contre 4, ou 5 contre 3, etc.). Discutez de la façon dont vous pourriez ajouter les informations sur la force réelle (c'est-à-dire 5 contre 4, etc.) aux tirs et aux buts, compte tenu des autres types d'événements (au-delà des tirs et des buts) et des fonctionnalités disponibles. Vous n'avez pas besoin de l'implémenter pour ce jalon.</span>



<br>

---

# Question 3

##### <span style="color:grey">En quelques phrases, discutez de certaines fonctionnalités supplémentaires que vous pourriez envisager de créer à partir des données disponibles dans cet ensemble de données. Nous ne cherchons pas de réponses particulières, mais si vous avez besoin d'inspiration, un tir ou un but pourrait-il être classé comme un rebond ou un tir dans le rush?</span>

