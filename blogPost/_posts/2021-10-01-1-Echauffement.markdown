---
layout: post
title:  "Échauffement"
date:   2021-10-01 11:27:11
categories: jekyll update
---

# Question 1

##### <span style="color:grey">Triez les gardiens de but par leur pourcentage d'arrêts (« VS % »), qui est le rapport de leurs tirs sauvés sur le nombre total de tirs auxquels ils ont fait face. Quels problèmes remarquez-vous en utilisant cette métrique pour classer les gardiens de but ? Que pourrait-on faire pour y faire face ? Ajoutez cette discussion à votre article de blog (pas encore besoin de cadre de données ou de tracé). <br>Remarque : Vous n'avez pas besoin de créer une nouvelle métrique sophistiquée ici. Si vous le souhaitez, vous pouvez effectuer un contrôle de cohérence par rapport à la [page Web officielle des statistiques de la LNH](http://www.nhl.com/stats/goalies?reportType=season&seasonFrom=20172018&seasonTo=20172018 "page Web officielle des statistiques de la LNH"). Vous n'avez pas non plus besoin de reproduire un classement particulier sur la page de la LNH ; si votre approche est raisonnable, vous obtiendrez toutes les notes.</span>

Trions les goals en fonction de leur SV%

[//]: <>  Trie des goal en fonction de leurs SV%

<p align="center">
  <img src="/assets/echauffement/trie_des_goal_en_fonction_du_sv.png" alt="Pourcentage d'arrêts sur le classement des 20 meilleurs gardiens"/>
</p>

<br>

> Quelques problèmes apparaîssent puisque qu'en classant les goals comme nous l'avons fait, on se rend compte que ceux en tete de classement n'ont pas beaucoup de matchs à leurs actifs (un seul en l'occurence pour les trois premiers).Ensuite la majorité d'entre eux n'ont remporté aucun match , il serait donc paradoxal qu'ils soient les meilleurs.
> Il serait interessant de considérer leurs classement en fonction de leurs parties gagnées et de leurs SV%

<br>

---

# Question 2

##### <span style="color:grey">Filtrez les gardiens en utilisant l'approche proposée ci-dessus et produisez un graphique à barres avec les noms des joueurs sur l'axe des y et enregistrer le pourcentage ('SV%') sur l'axe des x. Vous pouvez garder les 20 meilleurs gardiens. Incluez ce chiffre dans votre article de blog; assurez-vous que tous les axes sont étiquetés et que le titre est approprié.</span>

Trions les goals en fonction de leur victoires puis de leur SV%
 nous obtenons le graphique suivant :

<br>

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
