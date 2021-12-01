---
layout: post
title:  "Ingénierie des caractéristiques"
date:   2021-11-30 17:30:07
categories: jekyll update
---

# Question 1

##### <span style="color:grey">Créez et comprennent les figures suivants dans votre blogpost et brièvement discutez vos observations (quelques phrases): <br>Un histogramme de nombre de tirs (buts et non-buts séparés), regroupées (binned) par distance<br>Un histogramme de nombre de tirs (buts et non-buts séparés), binned par angle <br>Un histogramme 2D où un axe est la distance et l'autre est l'angle. Vous n'avez pas besoin de séparer les buts et les non-buts.</span>

##### <span style="color:grey">Créez et incluez les figures suivantes dans votre billet de blog et discutez brièvement de vos observations (quelques phrases).</span>

####  histogramme du nombre de tirs regroupées par distance
<p align="center">
  <img src="/assets/Feature_Engineering/question_1_1_a.png" alt="Shot_binned_by_distance"/>
</p>

Analyse

> Comme nous l'avions déjà remarqué lors du milestone 1, le nombre de tirs conduisant à un but est minoritaire.
> Pour tous les tirs, la distance de tir la plus populaire est de presque 75 pieds, soit au niveau de la ligne bleue. En s'éloignant de la ligne bleue en s'écartant du filet, le nombre de tentative décroit de façon exponentielle.\
> En se rapprochant du filet, le nombre de tentatives décroit plus doucement jusqu'à une distance de 25 pieds. Les tentatives à une distance inférieure à 25 pieds sont très minoritaire, notamment pour les buts. cela est surement du à la présence de la défense de l'equipe adverse \
> Certaines tentatives sont effectuées entre 125 et 175 pieds mais très peu d'entre elles conduisent effectivement à des buts.

<br>

####   histogramme du nombre de tirs regroupées par angle
<p align="center">
  <img src="/assets/Feature_Engineering/question_1_1_b.png" alt="Shot_binned_by_angle"/>
</p>


<br>

<p align="center">
  <img src="/assets/milestone_2/Q2/nb_shot_by_angle.png" alt="Nombre de tirs regroupés par distance"/>
</p>


Analyse
> pour les angles nous avont considéré deux cas: discriminer les angles de part et d'autre du filet ou pas. nous avont pu constater que les interpretations sont assez similaires ainsi pour plus de simpliciter nous ne feront pas de discrimination d'angle dans la suite de ce devoir.
 
> Nous pouvont constater que la majorité des tirs se font avec un angle compris entre 0 et 1 radian (0 et 57 degrés) par rapport à la normale au filet (i.e. La droite passant par les 2 filets).
> En résumé, Les tirs qui ont le plus de succès sont ceux tentés bien en face du filet et les joueurs le savent : c'est leur angle de tir favori.


<br>

---
# Question 2

####  Un histogramme 2D où un axe est la distance et l'autre est l'angle

<p align="center">
  <img src="/assets/Feature_Engineering/question_1_1_c.png" alt="2D_histogram"/>
</p>


Analyse

> On retrouve les informations que nous avons déjà vu. Compte tenu du nombre important de points, il est difficile de se rendre compte visuellement de la densité pour chaque zone du graphique. Pour nous aider, on s'appuie sur les histogrammes du graphique.
>
> On retrouve l'idée que les tirs à une distance inférieure à 25 pieds sont très peu nombreux. (voir histogramme).
> Les tirs à une distance de 75 pieds sont les plus nombreux et sont préférables pour marquer.
>
> Meme observation pour les angles,les tires qui ont le plus de chance de se solder par un but sont ceux en face du fillet


<br>

---

# Question 2

##### <span style="color:grey">Maintenant, créez deux autres figures reliant le taux de but, c'est-à-dire #buts / (#pad_de_buts + #buts), à la distance et le taux de but à l'angle du tir. Incluez ces figures dans votre article de blog et discutez brièvement de vos observations.</span>

Taux de buts en fonction de la distance et de l'angle

<p align="center">
  <img src="/assets/milestone_2/Q2/goal_rate_by_distance.png" alt="Nombre de tirs regroupés par distance" style="display:inline-block; width:50%; float:left;"/>
  <img src="/assets/milestone_2/Q2/goal_rate_by_angle.png" alt="Nombre de tirs regroupés par distance" style="display:inline-block; width:50%; float:right;"/>
</p>


Analyse

> Du point de vue de la distance, le plus fort taux de but correspond à une distance de 57 à 76 pieds.
> On peut donc recommander de tirer au niveau de la ligne bleue.
> Si très peu de tir sont tenté depuis la zone de défense de l'equipe qui ataque, il semble que le taux de réussite soit également important. Nous remettrons celà en question dans la section suivante.
>
> Du point de vue de l'angle de tir, le taux de réussite est le plus élevé pour les tirs en face du filet.
> Il semble que les tir avec un angle extrème d'environ 3 radian (presque 180 degrés) ont égalment un bon taux de réussite. Il se peut que ces tirs en particuliers s'appuyent sur le rebond du palais sur un adversaire ou sur le goal pour le faire entrer dans le filet.





<br>

---

# Question 3

##### <span style="color:grey">Créez un autre histogramme, cette fois de buts uniquement, classés par distance, et séparez les événements nets vides et non vides. Incluez ce chiffre dans votre article de blog et discutez de vos observations. Pouvez-vous trouver des événements qui ont des caractéristiques incorrectes (par exemple, de mauvaises coordonnées x/y) ? Si oui, prouvez qu'un événement a des caractéristiques incorrectes.</span>

Nombre de buts en fonction de l'état du filet

<p align="center">
  <img src="/assets/Feature_Engineering/question_1_3_a.png" alt="Goal_by_empty_net_or_not"/>
</p>
<br>


Analyse

> On peut remarquer un certain nombre de buts marqués entre 150 et 175 pieds, soit dans la zone de défense.
>
>
