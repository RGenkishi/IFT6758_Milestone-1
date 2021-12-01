---
layout: post
title:  "Modèles de base"
date:   2021-11-29 11:27:11
categories: jekyll update
---

# Question 1

##### <span style="color:grey">Évaluez la précision (c'est-à-dire correctement prédite / totale) de votre modèle sur l'ensemble de validation. Que remarquez-vous ? Regardez les prédictions et discutez de vos découvertes. Quel pourrait être un problème potentiel? Incluez ces discussions dans votre article de blog.</span>

Pour cette question, nous chargeons un Dataset avec 80% des données de 2015 à 2018 réservées à l'entraînement et les 20% restant à la validation.
Les données de 2019 sont reservée à l'ensemble de test du Dataset.

<p align="center">
  <img src="/assets/milestone_2/Q3/accuracy.png" alt="Nombre de tirs regroupés par distance"/>
</p>


Analyse

> La précision de notre algorithme est excellentissime avec une accuracy de plus de 90% ! C'est magnifique ! Pas besoin d'aller plus loin..
> 
> MAIS que prédit-on ?
>
> La table des prédictions est remplie de 0 avec 62222 "non buts" contre 0 buts.
> Le nombre total de prédiction est également 62222.
> Juste pour être sûr, on compte le nombre de prédiction exacte : 56350.
> Et quel est le nombre de "non but" : 56350.
> 
> Finalement, on ne fait que prédire la classe majoritaire. Un premier problème est que le nombre de "non buts" est très important face au nombre de buts.
> Par ailleurs, il se peut que les features à notre disposition ne soient pas suffisante pour faire la différence.
 







<br>

---

# Question 2

##### <span style="color:grey">Entraînez maintenant deux autres classificateurs de régression logistique en utilisant la même configuration que ci-dessus, mais cette fois sur la fonction d'angle, puis à la fois sur la distance et l'angle. Produisez les trois mêmes courbes que celles décrites dans la section précédente pour chaque modèle. Y compris la ligne de base aléatoire, vous devriez avoir un total de 4 lignes sur chaque figure :<br>Régression logistique, entraînée sur la distance uniquement (déjà fait ci-dessus)<br>Régression logistique, entraînée sur l' angle uniquement<br>Régression logistique, entraînée sur la distance et l' angle<br>Ligne de base aléatoire : probabilité prédite est échantillonné à partir d'une distribution uniforme, c'est-à-dire yiU(0,1)<br>Incluez ces quatre figures (chacune avec quatre courbes) dans votre article de blog. En quelques phrases, discutez de votre interprétation de ces résultats.</span>

Courbes ROC et métrique AUC

<p align="center">
  <img src="/assets/milestone_2/Q3/courbe_ROC_Q3.png" alt="Nombre de tirs regroupés par distance"/>
</p>


Analyse

> Le meilleur tends à se placer dans le coin supérieur gauche de la courbe ROC avec un fort taux de vrai positif et un faible taux de faux positifs 
> 
> Avec la Regression Logistique basée sur l'angle de tir, un faible taux de faux positifs entraîne également un faible taux de vrai positifs.
> Lorsque le taux de faux positif dépasse environ 50%, le taux de vrai positif passe enfin la barre des 50%.
> Cet estimateur est donc moins bon que l'estimateur aléatoire sur la moitié de la courbe ROC et meilleur sur l'autre moitiée.\
> On est loin de l'estimateur idéal.
> 
> Les modèles basés sur la distance et sur la combinaison de l'angle et de la distance ont des performances confondues. Globalement, ces modèles performent mieux que l'aléatoire.
> En effet, leurs courbes sont placée au dessus de la première bisectrice. Pour un même taux de faux positif, le taux de vrai positif est plus important.
> 
> Compte tenu du fait que ces deux modèles performent de la même façon, nous pouvons conclure que la mesure de l'angle n'apporte pas une information cruciale pour la prédiction.

<br>


Taux de buts (#buts / (#non_buts + #buts)) en fonction du centile du modèle de probabilité de tir

<p align="center">
  <img src="/assets/milestone_2/Q3/courbe_goal_rate_Q3.png" alt="Nombre de tirs regroupés par distance"/>
</p>


Analyse

> En toute logique, un classifieur aléatoire prédit le même pourcentage de but pour chaque centile. C'est confirmé par notre tracé.
> 
> Pour le classifieur basé sur l'angle uniquement, le taux de but est plus important que 
> 