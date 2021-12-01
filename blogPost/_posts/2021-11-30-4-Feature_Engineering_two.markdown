---
layout: post
title:  "Engénierie des caracteristiques 2"
date:   2021-11-30 17:30:05
categories: jekyll update
---

# Question 5

##### <span style="color:grey">Dans votre article de blog, ajoutez une liste de toutes les caractéristiques que vous avez créées pour cette section. Répertoriez chaque caractéristique à la fois par le nom de la colonne dans votre cadre de données ET par une explication simple et lisible par l'humain (c'est-à-dire game_sec : nombre total de secondes écoulées dans le jeu). Si vous avez créé de nouvelles caractéristiques, décrivez brièvement ce qu'elles sont. Ajoutez un lien vers l'expérience qui stocke l'artefact DataFrame filtré pour le jeu spécifié. Notez qu'il ne doit y avoir qu'un seul DataFrame inscrit avec ce nom. Voir l' annexe pour un exemple de ce que nous recherchons.</span>


Liste des caractéristiques:

- "**event_type**" : type de l'événement
- "**shot_type**" : type de tir
- "**game_seconds**" : secondes écoulées dans le jeu
- "**coord_x**" : coordonnée X
- "**coord_y**" : coordonnée Y
- "**distance_from_net**" : distance au filet en pieds
- "**angle_from_net**" : angle de tir en radian (0 : en face du filet)
- "**which_period**" : période de jeu
- "**empty_net**" : True si le filet est vide, False sino

- "**pre_event_type**" : type de l'événement précédent
- "**rebound**" : True si le coup est un rebond (i.e. le coup précédent est un Shot), False sinon.
- "**pre_coord_x**" : coordonnée X de l'événement précédent
- "**pre_coord_y**" : coordonnée Y de l'événement précédent
- "**time_since_last_event**" : temps en seconde écoulé depuis le dernier événement
- "**distance_from_last_event**" : distance en pieds de l'événement par rapport au récédent
- "**change_in_shot_angle**" : diférence absolue entre l'angle de tir précédent et le nouveau. 0 si le coup n'est pas un rebond.
- "**speed**" : vitesse de déplacement en pieds par secondes


#### -Le Dataframe filtré est disponible [ici](https://google.com/404)
