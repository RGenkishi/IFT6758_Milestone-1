---
layout: post
title:  "Donnez-lui votre meilleur coup"
date:   2021-11-30 11:30:00
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

---
# Question 2
##### <span style="color:grey">À côté des figures, incluez des liens vers l'entrée d'expérience dans vos projets comet.ml pour lesquels vous avez inclus des métriques quantitatives (environ 3-4).Connectez les modèles aux expériences sur comet.ml (exemple ici) et inscrivez-les avec des balises informatives.</span>

<br>

#### -Le modèle basé sur les arbres de decision est disponible [ici](https://www.comet.ml/genkishi/milestone-2/4db124cb82f648cab4f9e53c62bfc846?experiment-tab=chart&showOutliers=true&smoothing=0&transformY=smoothing&xAxis=wall)
<br>

#### -Le modèle basé sur les réseaux de neurones est disponible [ici](https://www.comet.ml/genkishi/milestone-2/11fed86d708d4988a28d7233ff8f527f?experiment-tab=chart&showOutliers=true&smoothing=0&transformY=smoothing&xAxis=wall)
<br>

#### -Le modèle basé sur le bagging est disponible [ici](https://www.comet.ml/genkishi/milestone-2/e35380f848584d2fa5a7da255ccfbce1?experiment-tab=chart&showOutliers=true&smoothing=0&transformY=smoothing&xAxis=wall)


