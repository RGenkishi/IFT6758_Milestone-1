---
layout: post
title:  "Échauffement"
date:   2021-10-01 11:27:11
categories: jekyll update
---

# Question 1

##### <span style="color:grey">Triez les gardiens de but par leur pourcentage d'arrêts (« VS % »), qui est le rapport de leurs tirs sauvés sur le nombre total de tirs auxquels ils ont fait face. Quels problèmes remarquez-vous en utilisant cette métrique pour classer les gardiens de but ? Que pourrait-on faire pour y faire face ? Ajoutez cette discussion à votre article de blog (pas encore besoin de cadre de données ou de tracé). <br>Remarque : Vous n'avez pas besoin de créer une nouvelle métrique sophistiquée ici. Si vous le souhaitez, vous pouvez effectuer un contrôle de cohérence par rapport à la [page Web officielle des statistiques de la LNH](http://www.nhl.com/stats/goalies?reportType=season&seasonFrom=20172018&seasonTo=20172018 "page Web officielle des statistiques de la LNH"). Vous n'avez pas non plus besoin de reproduire un classement particulier sur la page de la LNH ; si votre approche est raisonnable, vous obtiendrez toutes les notes.</span>

Trions les goals en fonction de leur SV%

```python
import pandas as pd
from ift6758.data import get_player_stats

df = get_player_stats(2018, 'goalies')

pd.set_option("max_rows", None)  # Affiche toute les lignes

df["SV%"] = pd.to_numeric(df["SV%"], errors='coerce').fillna(0)  # formate la colonne %SV en numérique et remplis les NaN par des 0
sortedGoalie = df.sort_values(by="SV%", ascending=False)

print(sortedGoalie[["Player", "W", "SV%"]])
```


|  | Player | W | SV% |
|---|---|---|---|
| 85 | Dustin Tokarski | 0 | 1.000 |
| 11 | Jack Campbell | 0 | 1.000 |
| 63 | Alex Nedeljkovic | 0 | 1.000 |
| 29 | Kristers Gudlevskis | 0 | 1.000 |
| 26 | Jon Gillies | 1 | 0.964 |
| 51 | Charlie Lindgren | 2 | 0.949 |
| 81 | Alex Stalock | 1 | 0.944 |
| 9 | Sergei Bobrovsky | 41 | 0.931 |
| 17 | Aaron Dell | 11 | 0.931 |
| 33 | Magnus Hellberg | 1 | 0.929 |
| 82 | Anthony Stolarz | 2 | 0.928 |
| 10 | Laurent Brossoit | 4 | 0.928 |
| 36 | Jimmy Howard | 10 | 0.927 |
| 8 | Antoine Bibeau | 1 | 0.927 |
| 3 | Craig Anderson | 25 | 0.926 |
| 28 | Philipp Grubauer | 13 | 0.926 |
| 35 | Braden Holtby | 42 | 0.925 |
| 25 | John Gibson | 25 | 0.924 |
| 16 | Scott Darling | 18 | 0.924 |
| 70 | Carey Price | 37 | 0.923 |
| 20 | Devan Dubnyk | 40 | 0.923 |
| ...| ... | ... | ... |


> Nous avons ici volontairement affiché le nombre de victoire des goals en plus de leur SV%.
> Un problème apparaît puisque qu'en classant les goals comme nous l'avons fait, nous ne prennons pas en compte leur nombre de victoire et des goals sans aucune victoire se plaçent en tête de liste.


<br>

---

# Question 2

##### <span style="color:grey">Filtrez les gardiens en utilisant l'approche proposée ci-dessus et produisez un graphique à barres avec les noms des joueurs sur l'axe des y et enregistrer le pourcentage ('SV%') sur l'axe des x. Vous pouvez garder les 20 meilleurs gardiens. Incluez ce chiffre dans votre article de blog; assurez-vous que tous les axes sont étiquetés et que le titre est approprié.</span>
<br>

Trions les goals en fonction de leur victoires puis de leur SV%

```python
df["W"] = pd.to_numeric(df["W"], errors='coerce')
reSortedGoalie = df.sort_values(by=["W", "SV%"], ascending=False)

print(reSortedGoalie[["Player", "W", "SV%"]])
```

|  | Player | W | SV% |
|---|---|---|---|
| 35 | Braden Holtby | 42 | 0.925 |
| 84 | Cam Talbot | 42 | 0.919 |
| 9 | Sergei Bobrovsky | 41 | 0.931 |
| 20 | Devan Dubnyk | 40 | 0.923 |
| 70 | Carey Price | 37 | 0.923 |
| 73 | Tuukka Rask | 37 | 0.915 |
| 41 | Martin Jones | 35 | 0.912 |
| 2 | Frederik Andersen | 33 | 0.918 |
| 0 | Jake Allen | 33 | 0.915 |
| 62 | Matt Murray | 32 | 0.923 |
| 15 | Corey Crawford | 32 | 0.918 |
| 75 | Pekka Rinne | 31 | 0.918 |
| 52 | Henrik Lundqvist | 31 | 0.910 |
| 92 | Peter Budaj | 30 | 0.915 |
| 27 | Thomas Greiss | 26 | 0.913 |
| 21 | Brian Elliott | 26 | 0.910 |
| 56 | Steve Mason | 26 | 0.908 |
| 34 | Connor Hellebuyck | 26 | 0.907 |
| 89 | Cam Ward | 26 | 0.905 |
| 3 | Craig Anderson | 25 | 0.926 |
| ...| ... | ... | ... |

#### Graphique

[//]: <>  Graphique des pourcentage d'arrêts sur le classement des 20 meilleurs gardiens

<p align="center">
  <img src="/assets/echauffement/pourcentage_d'arrets_sur_le_classement_des_20_meilleurs_gardiens.png" alt="Pourcentage d'arrêts sur le classement des 20 meilleurs gardiens"/>
</p>


<br>

---

# Question 3

##### <span style="color:grey">Le pourcentage d'économies n'est évidemment pas une fonctionnalité très complète. Discutez des autres caractéristiques qui pourraient être utiles pour déterminer la performance d'un gardien de but. Vous n'avez pas besoin de mettre en œuvre quoi que ce soit à moins que vous ne le vouliez vraiment, tout ce qui est requis est un court paragraphe de discussion.</span>
<br>


Comment améliorer notre classement ?

> Une première amélioration de notre classement consisterait à prendre en compte le nombre de match joué. Plus de poids pourrait être accordé aux performances des goals qui démontré leurs compétences sur un nombre de match important. Les performances des goals n'ayant fait qu'un match ou deux peuvent relever de la chance et sont moins significative.
>
> Le nombre d'attaques subies par un goal pourrait égamelent être pris en compte. Pour deux goals avec le même SV%, celui ayant subi le plus d'attaques gagnerait des places dans le classement.
