---
layout: post
title:  "Modèles avancés"
date:   2021-10-15 14:52:00
categories: jekyll update
---

**Les quatres figures se trouvent à la toute fin de la page.**
# Question 1

L'entrainement du modèle de base a été effectué en séparant les données des saisons régulière de 2015 à 2018 en deux ensembles. L'ensemble de validation contient 70% des données et l'ensemble test 30%. Les tests qui permettent d'évaluer la performance du modèle ont été fait sur ce dernier ensemble. Avec une mesure AUC de 0.72, on voit que le modèle entraîné avec XGBoost performe un peu mieux que le modèle entraîné grâce à une régression logistique qui avait atteint un pointage de 0.70. Comme pour la régression logistique, nous pouvons voir sur le diagramme de fiabilités que notre modèle surestime la probabilité qu'un tir soit un but. En effet, dans les deux cas, la courbe de calibration est relativement sous la droite pointillé (qui ndique ce que produirait un modèle parfaitement calibré). Les courbres de pourcentages cumulés de buts et de taux de but sont relativement similaires. En conclusion, le modèle XGBoost performe un peu mieux si l'on se fit à la mesure AUC, mais la différence n'est pas très impressionnante.

# Question 2
Pour le règlages des hyperparamètres, nous avons effectué une recherche sur grille avec validation croisé sur trois hyperparamètres. Voici le code qui générait la grille dans laquelle la recherche était faite :
```
gridsearch_parameters = [
    (scale_pos_weight, max_depth, min_child_weight)
    for scale_pos_weight in range(1,8,2)
    for max_depth in range(4,9)
    for min_child_weight in range(4,9)
]
```

`scale_pos_weight` est un hyperparamètre qui a pour rôle de corriger le biais de notre modèle lorsque les deux classes sont débalancés, comme c'est notre cas. En effet, seulement 10% des tirs sont des buts, il y a donc 9 fois plus de tirs que de buts. Les deux autres hyperparamètres, `max_depth` et `min_child_weight` permettent de trouver un équilbre entre le biais et la variance de notre modèle. Nous nous sommes inspiré de cet [article de blog](https://blog.cambridgespark.com/hyperparameter-tuning-in-xgboost-4ff9100a3b2f) pour trouver ces deux hyperparamètres. Pour chaque ensemble d'hyperparamètres, nous avons effectué une validation croisée sur nos données d'entraînement. Les valeurs qui ont donné les meilleurs résultats étaient :
`scale_pos_weight = 5`,
`max_depth = 6`,
`min_child_weight = 4`. \\
Par la suite, nous avons entrainé notre modèle avec ces hyperparamètres en faisant encore une division 70-30. Notre modèle a légèrement mieux performé que notre modèle de base XGBoost, passant d'une mesure AUC de 0.72 à 0.75. On peut aussi voir sur la courbe de proportion cumulée de buts que la courbe de ce modèle (Hyper_tune_XGBoost) monte légèrement plus rapidement que les autres courbes. Cela signifie qu'il y a un plus grand pourcentage de buts parmis les tirs auxquels notre modèle attribue une haute probabilité.
On peut trouver l'entré comet du modèle [ici](https://www.comet.ml/genkishi/milestone-2/6d557b5daa31414fb40929db0a5d0e3f?experiment-tab=chart&showOutliers=true&smoothing=0&transformY=smoothing&xAxis=wall). La première courbe correspond à la mesure AUC lors de la recherche sur grille des hyperparamètres optimaux.

# Question 3
Nous avons testé deux techniques de sélection des caractéristiques fournis par `sklearn`, soit `mutual_info_classif` et `SelectFromModel`. Ces deux techniques ont été vus dans le cours et appartiennent à deux catégories de techniques de sélection de caractéristique. La première par filtrage, et la seconde par recherche (wrapper methods).
Pour les hyperparamètres, nous avons simplement réutilisés ceux de la précédente question. \\
Pour faire nos tests, nous nous sommes pris de la manière suivante. Nous avons utilisé une des deux techniques de sélection de caractéristique, puis nous avons pris les meilleures caractéristiques selon chachune de ces deux techniques. Nous avons ensuite testé notre modèle avec les `k` meilleures caractéristiques. D'abord la meilleure, puis les deux meilleurs, puis les trois meilleurs, etc. \\
Ce qu'on peut voir c'est que la performance des modèles (évaluée grâce à la mesure AUC) plafonne relativement rapidement au fur et à mesure que l'on ajoute des caractéristiques. \\
Voici donc les résultats des 10 premières itérations pour `mutual_info_classif`.
```
0               1  0.507168
0               2  0.695008
0               3  0.714263
0               4  0.714950
0               5  0.714801
0               6  0.716310
0               7  0.720398
0               8  0.724755
0               9  0.725246
0              10  0.725606
```
Et pour `SelectFromModel`
```
 kbest_features       auc
0               1  0.658371
0               2  0.715486
0               3  0.715095
0               4  0.715705
0               5  0.719339
0               6  0.720572
0               7  0.723954
0               8  0.726061
0               9  0.728071
0              10  0.729421
```

On voit que dans les deux cas, les gains de performance stagnent assez rapidement. Après 3 caractéristiques, les gains sont marginaux. Il ne vaut pas nécessairement la peine d'ajouter des caractéristiques passé ce seuil si l'objectif est de sauver de l'espace mémoire et améliorer la performance de l'entraînement. Voici donc les trois meilleurs caractéristiques selon `mutual_info_classif`:

```
rebound_1
angle_from_net
distance_from_net
```
Puis selon `SelectFromModel`:
```
coord_x 
coord_y 
distance_from_net
```

Étant donné que les résultats du deuxième ensemble étaient légèrement meilleurs, nous les avons sélectionné ces trois derniers. \\
Vous trouverez [ici](https://www.comet.ml/genkishi/milestone-2/40f1a1cd0a5b4d1c94ca9a0c2b250c89?experiment-tab=chart&showOutliers=true&smoothing=0&transformY=smoothing&xAxis=step) la page comet du modèle.

 \\
 \\
Les diagrammes de fiabilité (courbe de calibration)
<p align="center">
  <img src="/assets/question_5/XGBoost_HT_calibration.png" alt="Calibration"/>
</p>
 \\
 \\
Proportion cumulée de buts (pas de tirs) en fonction du centile du modèle de probabilité de tir
<p align="center">
  <img src="/assets/question_5/XGBoost_HT_goal_cumul.png" alt="Goal cumul"/>
</p>
 \\
 \\
Taux de buts (#buts / (#non_buts + #buts)) en fonction du centile du modèle de probabilité de tir
<p align="center">
  <img src="/assets/question_5/XGBoost_HT_rate_curve.png" alt="rate curve6"/>
</p>
 \\
 \\
Courbes ROC et métrique AUC
<p align="center">
  <img src="/assets/question_5/XGBoost_HT_roc_curve.png" alt="roc_curve"/>
</p>
