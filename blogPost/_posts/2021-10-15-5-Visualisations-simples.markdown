---
layout: post
title:  "Visualisations simples"
date:   2021-10-15 14:49:00
categories: jekyll update
---

# Question 1

##### <span style="color:grey">Produisez un histogramme ou un BARPLOT  des types de tirs sur toutes les équipes dans une saison de votre choix. Superposez le nombre de buts sur le nombre de tirs. Quel semble être le type de tir le plus dangereux ? Le type de tir le plus courant ? Ajoutez cette figure et cette discussion à votre article de blog.</span>

<br>

### Analyse des types de tirs

[//]: <> Nombre de tires et de buts par type de tires pour la saison 2018

<p align="center">
  <img src="/assets/simpleVisualisation/nombre_de_tire_et_de_but_par_type_de_tire.png" alt="Pourcentage d'arrêts sur le classement des 20 meilleurs gardiens"/>
</p>

<br>

<p align="center">
  <img src="/assets/percentageByShotType.png" alt="Pourcentage d'arrêts sur le classement des 20 meilleurs gardiens"/>
</p>

<br>

>Les tirs les plus courants et de très loin sont les tirs du poignet suivis dans l'ordre : des tirs frappés, des tirs du rever, des tirs pointé, des tirs déviés et enfin des tirs enroulés.
Bien que les tirs du poignet sont les plus fréquent, ce ne sont pas les tirs les plus dangereux. Pour celà il faut regarder le pourcentage de tirs réussi par type de tir. Le grand vainceur est le tir pointé avec presque 20% de réussite, suivi du tir dévié avec presque 18% de réussite.

<br>

---

# Question 2

##### <span style="color:grey">Quelle est la relation entre la distance à laquelle un tir a été effectué et la chance qu'il s'agisse d'un but ? Produisez un graphique pour chaque saison entre 2018-19 et 2020-21 pour répondre à cette question, et ajoutez-le à votre article de blog avec quelques phrases décrivant votre silhouette. Y a-t-il eu beaucoup de changements au cours des trois dernières saisons? Remarque : il existe plusieurs façons de montrer cette relation ! Si votre personnage raconte la bonne histoire, vous obtiendrez tous les points.</span>

<br>

### Histogramme du nombre de but en fonction de la distance du tir

<p align="center">
  <img src="/assets/distanceBut.png" alt="Distance des buts"/>
</p>

Nous pouvons remarquer que la majorité des buts sont marqué grâce à des tirs près de la ligne bleue. Une fois que l'on s'éloigne de cette ligne bleue, le nombre de but marqués chute drastiquement pour remonter petit à petit lorsque l'on se rapproche des cages pour atteindre un nouveau pic. À l'inverse, si l'on s'éloigne des cages on compte très peu de but marqués depuis l'autre côté du terrain. On remarque cependant que la la majorité des buts marqués de l'autre côté du terrain sont tiré depuis la distance la plus grande, quasiment depuis les cages de l'équipe qui marque. (Le goal doit alors certainement profiter de l'effet de surprise pour marquer lui même)

Remarque d'Olivier sur la cohérence de la répartition des tirs : 
> Ouais ca a du sens avec le heatmap
> La case qui a le plus de tirs c’est près de la ligne bleu
> C’est de là d’où tirent les défenseurs

<br>

---

# Question 3

##### <span style="color:grey">Combinez les informations des sections précédentes pour produire un graphique qui montre le pourcentage de buts (# buts / # tirs) en fonction à la fois de la distance par rapport au filet et de la catégorie de types de tirs (vous pouvez choisir une seule saison de votre choix) brièvement Discutez de vos conclusions ; Par exemple, quels pourraient être les types de tirs les plus dangereux ?</span>
