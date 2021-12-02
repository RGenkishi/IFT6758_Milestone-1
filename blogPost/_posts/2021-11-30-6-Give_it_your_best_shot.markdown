---
layout: post
title:  "Donnez-lui votre meilleur coup"
date:   2021-11-30 17:30:03
categories: jekyll update
---


# Question 1

##### <span style="color:grey">Dans votre article de blog, discutez des différentes techniques et méthodes que vous avez essayées. Incluez les quatre mêmes figures que dans la Partie 3 (courbe ROC/AUC, taux de buts par rapport au centile de probabilité, proportion cumulée de buts par rapport au centile de probabilité et courbe de fiabilité). Les mesures quantitatives ne sont nécessaires que pour quelques ensembles d'expériences, vous n'avez donc besoin d'inclure que quelques courbes sur chaque tracé (par exemple, des choses que vous avez trouvées intéressantes ou des modèles qui ont particulièrement bien fonctionné). Assurez-vous d'inclure et de mettre en évidence ce que vous considérez comme votre meilleur modèle «final». Pour les méthodes qui n'ont pas été très efficaces ou intéressantes, vous pouvez simplement les inclure sous forme de brève discussion qualitative.</span>
####  -Les courbes Receiver Operating Characteristic (ROC) et la métrique AUC de la courbe ROC
<p align="center">
  <img src="/assets/Give_it_your_best_shot/question_6_Figure_1.png" alt="ROC_AUC_cureve"/>
</p>

<br>

####  -Les courbes du taux de buts en fonction du centile du modèle de probabilité de tir
<p align="center">
  <img src="/assets/Give_it_your_best_shot/question_6_Figure_2.png" alt="Goal_rate_percentile"/>
</p>

<br>

####  -Les courbes de la proportion cumulée de buts en fonction du centile du modèle de probabilité de tir.
<p align="center">
  <img src="/assets/Give_it_your_best_shot/question_6_Figure_3.png" alt="Goal_cumulative_proportion_percentile"/>
</p>

<br>

####  -Les diagrammes de fiabilité (courbe de calibration)
<p align="center">
  <img src="/assets/Give_it_your_best_shot/question_6_Figure_4.png" alt="calibration_curve"/>
</p>

<br>

Discussion

> afin d'essayer de trouver un meilleur modèle pour prédire les buts espère, nous avons commencé par tester trois classifieurs supplémentaires qui sont: MLP, Decision_tree et votingclassifier qui se base sur la combinaison des deux precedent.sur nos trois classificateur, nous avons procédé à une recherche aléatoire d'hyperparametres entraine avec tous les features extrait lors de la question 4.

> pour l'évaluation de nos models nous avons procédé par validation croisée stratifiée afin de conserver la proportion des classes dans chaque sous-ensemble. nous avons aussi voulu observer la précision de nos models à travers une autre métrique, la F1 score qui est une moyenne harmonique de la précision et du rappel. le score F1 de nos modèles ne dépassait pas les 2%, nous avons donc conclu que ce n'était pas un bon moyen d'évaluer la précision,néanmoins nous l'avons gardé ne serait-ce que pour avoir un autre angle de vu.avec ces configurations de base nos résultats sûrs avec l'AUC étaient de 70% pour l'arbre de décision et de 73% pour le MLP et le votingclassifier .

>dans l'optique d'améliorer nos résultats nous avons cherché un autre moyen de normaliser nos données. Jusque-là nous utilisions le minmaxscale, nous sommes donc passés aux power transforms afin de rendre nos données plus gaussiennes. cela nous a permis d'augmenter légèrement nos résultats, passant à 72% pour l'arbre de décision et à 75% pour le MLP et le votingclassifier. nous avons aussi tenté une réduction de dimensionnalité sur nos données grâce à la PCA et une feuture sélection avec l'algorithme du selectKbest avec le Ch2 comme fonction de score mais cela n'a pas été très concluant. 

>le meilleur modèle que nous avons obtenu est le MLP avec les features de base sur lesquels on a appliqué des power transforms au départ ce dernier était au coude à coude avec le votingclassifier,le diagramme de fiabilité nous a permis de les départager. comme l'illustre la figure ci-dessus, le MLP était le model le mieux calibré.

<br>

---
# Question 2
##### <span style="color:grey">À côté des figures, incluez des liens vers l'entrée d'expérience dans vos projets comet.ml pour lesquels vous avez inclus des métriques quantitatives (environ 3-4).Connectez les modèles aux expériences sur comet.ml (exemple ici) et inscrivez-les avec des balises informatives.</span>

<br>

#### -Le modèle basé sur les arbres de decision est disponible [ici](https://www.comet.ml/genkishi/milestone-2/4db124cb82f648cab4f9e53c62bfc846?experiment-tab=chart&showOutliers=true&smoothing=0&transformY=smoothing&xAxis=wall)
<br>

#### -Le modèle basé sur les réseaux de neurones est disponible [ici](https://www.comet.ml/genkishi/milestone-2/11fed86d708d4988a28d7233ff8f527f?experiment-tab=chart&showOutliers=true&smoothing=0&transformY=smoothing&xAxis=wall)
<br>

#### -Le modèle basé sur le bagging est disponible [ici](https://www.comet.ml/genkishi/milestone-2/e35380f848584d2fa5a7da255ccfbce1?experiment-tab=chart&showOutliers=true&smoothing=0&transformY=smoothing&xAxis=wall)
