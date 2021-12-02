---
layout: post
title:  " Évaluer sur l'ensemble de test"
date:   2021-11-30 10:30:02
categories: jekyll update
---

# Question 1 (la saison régulière)

Plusieurs choses intéressante émanent de ce test sur les données d'une nouvelle saison (qui n'ont pas été utilisées pour entraîner le modèle). Nous nous concentrerons ici sur la comparaison du modèle XGBoost et MLP. Dans les deux cas, les modèles performent moins biens que sur les données d'entraînement. On passe en effet, pour la mesure AUC, de 0.75 à 0.72 pour MLP, et de 0.75 à 0.73 pour XGBoost. Chose étrange, MLP semble être très bien calibré pour les probabilités prédites entre 0.0 et 0.75, mais il devient extrêmement mauvais par la suite. Cela semble signifier qu'il se met à donner des très haute probabilités à des tirs qui ne sont pas de buts. XGBoost n'a pas ce problème. En effet, ces prédictions semblent d'améliorer lorsque les probabilités qu'il attribue à un tir sont hautes. Pour ce qui est de la régression linéaire, on voit que ses performances ne changent à peu près pas (on reste à 0.70 d'AUC). Ce modèle est moins performant mais il ne perd pas en perfomance lorsqu'il rencontre de nouvelles données

\\
 \\
Les diagrammes de fiabilité (courbe de calibration)
<p align="center">
  <img src="/assets/question_7/regular_calibration.png" alt="Calibration"/>
</p>
 \\
 \\
Proportion cumulée de buts (pas de tirs) en fonction du centile du modèle de probabilité de tir
<p align="center">
  <img src="/assets/question_7/regular_goal_cumul.png" alt="Goal cumul"/>
</p>
 \\
 \\
Taux de buts (#buts / (#non_buts + #buts)) en fonction du centile du modèle de probabilité de tir
<p align="center">
  <img src="/assets/question_7/regular_rate_curve.png" alt="rate curve6"/>
</p>
 \\
 \\
Courbes ROC et métrique AUC
<p align="center">
  <img src="/assets/question_7/regular_roc_curve.png" alt="roc_curve"/>
</p>


# Question 2 (les séries éliminatoires)

Ce qu'on peut remarquer, pour les séries éliminatoires, c'est la totale déconfiture de MLP. On doit pouvoir en conclure que ce modèle souffre d'un surapprentissage sur les données des saisons régulières. XGBoost s'en sort, quant à lui, assez bien en passant à un AUC de 0.72. Chose intéressante est la stabilité des modèles de régression logistique. On doit pouvoir en conclure que les caractéristiques sur lesquels sont entraînés ces modèles sont relativement fiables, peu importe si l'on se trouve en séries éliminatoire ou en saison régulière.
\\
 \\
Les diagrammes de fiabilité (courbe de calibration)
<p align="center">
  <img src="/assets/question_7/playoff_calibration.png" alt="Calibration"/>
</p>
 \\
 \\
Proportion cumulée de buts (pas de tirs) en fonction du centile du modèle de probabilité de tir
<p align="center">
  <img src="/assets/question_7/playoff_goal_cumul.png" alt="Goal cumul"/>
</p>
 \\
 \\
Taux de buts (#buts / (#non_buts + #buts)) en fonction du centile du modèle de probabilité de tir
<p align="center">
  <img src="/assets/question_7/playoff_rate_curve.png" alt="rate curve6"/>
</p>
 \\
 \\
Courbes ROC et métrique AUC
<p align="center">
  <img src="/assets/question_7/playoff_roc_curve.png" alt="roc_curve"/>
</p>