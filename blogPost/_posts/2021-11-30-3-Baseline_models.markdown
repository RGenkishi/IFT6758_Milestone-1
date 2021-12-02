---
layout: post
title:  "Modèles de base"
date:   2021-11-30 17:30:06
categories: jekyll update
---

# Question 1

##### <span style="color:grey">Évaluez la précision (c'est-à-dire correctement prédite / totale) de votre modèle sur l'ensemble de validation. Que remarquez-vous ? Regardez les prédictions et discutez de vos découvertes. Quel pourrait être un problème potentiel? Incluez ces discussions dans votre article de blog.</span>

Pour cette question, nous chargeons un Dataset avec 70% des données de 2015 à 2018 réservées à l'entraînement et les 30% restant à la validation.

<p align="center">
    <img src="/assets/Baseline_modeles/accuracy.png" alt="baseline model accuracy"/>
    <img src="/assets/Baseline_modeles/confusion_matrix.png" alt="baseline model confusion atrix"/>
</p>


Analyse

> La précision de notre algorithme est excellentissime avec une accuracyde plus de 90% ! C'est magnifique ! Pas besoin d'aller plus loin...
>
> MAIS que prédit-on ?
> 
> le modèle prédit tous les tires comme n'étant pas des buts.
> Finalement, on ne fait que prédire la classe majoritaire. Un premier problème est que le nombre de "non-buts" est très important face au nombre de buts.



<br>

---

# Question 2-3

##### <span style="color:grey">Entraînez maintenant deux autres classificateurs de régression logistique en utilisant la même configuration que ci-dessus, mais cette fois sur la fonction d'angle, puis à la fois sur la distance et l'angle. Produisez les trois mêmes courbes que celles décrites dans la section précédente pour chaque modèle. Y compris la ligne de base aléatoire, vous devriez avoir un total de 4 lignes sur chaque figure :<br>Régression logistique, entraînée sur la distance uniquement (déjà fait ci-dessus)<br>Régression logistique, entraînée sur l' angle uniquement<br>Régression logistique, entraînée sur la distance et l' angle<br>Ligne de base aléatoire : probabilité prédite est échantillonné à partir d'une distribution uniforme, c'est-à-dire yiU(0,1)<br>Incluez ces quatre figures (chacune avec quatre courbes) dans votre article de blog. En quelques phrases, discutez de votre interprétation de ces résultats.</span>

Courbes ROC et métrique AUC

<p align="center">
  <img src="/assets/Baseline_modeles/Figure_1.png" alt="ROC curve and AUC metrics"/>
</p>


Analyse
>la courbe ROC et la métrique AUCqui est l'air sous la courbe ROC permettent d'évaluer la capacité d'un modèle et effectuer de bonne prédictions, ainsi un modèle parfait tendrait à se placer dans le coin supérieur gauche de la courbe ROC avec un fort taux de vrai positif et un faible taux de faux positifs

> le modèle basé sur la distance est le moins bon de tous les modèles, mais meilleur que le modèle aléatoire, avec un taux de faux positif plus important aux début de la courbe mais qui s'améliore le long du reste. Selon moi cela pourrais être dû aux valeurs aberrantes tels que les tires effectuées depuis la zone de défense de l'équipe qui attaque.

> Les modèles basés sur l'angle et sur la combinaison de l'angle et de la distance ont des performances confondues. Globalement, ces modèles performent mieux que celui basé sur la distance
> En effet, Pour un même taux de faux positif, le taux de vrai positif est plus important.

> Compte tenu du fait que ces deux modèles performent
 de la même façon, nous pouvons conclure que non seulement l'angle est une meilleure caractéristique mais en plus la distance n'apporte pas une information cruciale pour la prédiction.

<br>

Taux de buts (#buts / (#non_buts + #buts)) en fonction du centile du modèle de probabilité de tir

<p align="center">
  <img src="/assets/Baseline_modeles/Figure_2.png" alt="Goal_rate_percentile"/>
</p>


Analyse

> En toute logique, un classifieur
 aléatoire prédit le même pourcentage de but pour chaque centile. C'est confirmé par notre tracé.
 
>De manière générale pour les modèles de logistique régression, les courbes sont croissantes et convergent vers vers le 100ieme
 centile. Cela s'explique par le fait que plus un tire est susceptible d'être un but, plus la probabilité que lui attribue le modèle est elevée,ainsi plus la probabilité est élevée plus il y a de but

> Encore une fois, les modèles basés sur l'angle seul et sur la combinaison angle-distance performent
 de la même manière et beaucoup mieux car leur croissance est plus harmonieuse.

<br>


Proportion cumulée de buts (pas de tirs) en fonction du centile du modèle de probabilité de tir

<p align="center">
  <img src="/assets/Baseline_modeles/Figure_3.png" alt="Goal_cumulative_proportion_percentile"/>
</p>


Analyse

> Cette courbe est assez similaire a la courbe ROC.\
> En effet, on a affiché le taux de positif prédit / nombre total de positif réel. Cette valeur est proportionnelle au taux de vrai positif.
> Du point de vue des centiles, plus le centile baisse, plus la proportion de faux positif dans l'ensemble pris en compte augmente.
> Les deux axes sont donc proportionnels au taux de vrai positif et au taux de faux positif. L'échelle étant la même, les courbes sont semblables.

<br>


Les diagrammes de fiabilité (courbe de calibration)

<p align="center">
    <img src="/assets/Baseline_modeles/Figure_4.png" alt="calibration_curve" />
    <img src="/assets/Baseline_modeles/Figure_4_zoom.png" alt="calibration_curve_zoom" />
</p>
 

Analyse

> Vu l'étendue des probabilités retournée par nos différents modèles, il est difficile de statuer sur ce graphique.\
> Notons cependant que les courbes de qualibration de nos modèles ne sont pas confondu avec la courbe optimale et penchent plus du côté de la courbe du classifieur aléatoire.



<br>

---
# Question 4
##### <span style="color:grey">À côté des figures, incluez des liens vers les trois entrées d'expérience dans vos projets comet.ml qui ont produit ces trois modèles. Enregistrez les trois modèles dans les trois expériences sur comet.ml (exemple ici) et inscrivez-les avec des balises informatives, car vous en aurez besoin pour la section finale.</span>

<br>

#### -Le modèle entrainé avec les distances est disponible [ici](https://www.comet.ml/genkishi/milestone-2/0baf66b30afe41df8afe49c02e8da4e1?experiment-tab=chart&showOutliers=true&smoothing=0&transformY=smoothing&xAxis=wall)
<br>

#### -Le modèle entrainé avec les angles est disponible [ici](https://www.comet.ml/genkishi/milestone-2/ee33cb808231438dbccd8ff6348650a6?experiment-tab=chart&showOutliers=true&smoothing=0&transformY=smoothing&xAxis=wall)
<br>

#### -Le modèle entrainé avec les distances et les angles est disponible [ici](https://www.comet.ml/genkishi/milestone-2/750e55985bd24586a5df9de4af2bbaa6?experiment-tab=chart&showOutliers=true&smoothing=0&transformY=smoothing&xAxis=wall)
