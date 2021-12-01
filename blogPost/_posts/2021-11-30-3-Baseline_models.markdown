---
layout: post
title:  "Modèles de base"
date:   2021-11-30 11:20:00
categories: jekyll update
---

# Question 1

##### <span style="color:grey">À l'aide de votre ensemble de données (rappelez-vous, ne touchez pas à l'ensemble de test !), créez une division d'entraînement et de validation comme bon vous semble.utilisant seulement la de fonctiondistance,formationun Logistic Regressisur classifieur avec les paramètres complètement par défaut.Évaluez la précision (c'est-à-dire correctement prédite / totale) de votre modèle sur l'ensemble de validation. Que remarquez-vous ? Regardez les prédictions et discutez de vos découvertes. Quel pourrait être un problème potentiel? Incluez ces discussions dans votre article de blog.</span>

<br>

---
# Question 2-3

##### <span style="color:grey">Incluez ces quatre figures (chacune avec quatre courbes) dans votre article de blog. En quelques phrases, discutez de votre interprétation de ces résultats.</span>
####  -Les courbes Receiver Operating Characteristic (ROC) et la métrique AUC de la courbe ROC
<p align="center">
  <img src="/assets/Baseline_modeles/Figure_1.png" alt="ROC_AUC_cureve"/>
</p>

<br>

####  -Les courbes du taux de buts en fonction du centile du modèle de probabilité de tir
<p align="center">
  <img src="/assets/Baseline_modeles/Figure_2.png" alt="Goal_rate_percentile"/>
</p>

<br>

####  -Les courbes de la proportion cumulée de buts en fonction du centile du modèle de probabilité de tir.
<p align="center">
  <img src="/assets/Baseline_modeles/Figure_3.png" alt="Goal_cumulative_proportion_percentile"/>
</p>

<br>

####  -Les diagrammes de fiabilité (courbe de calibration)
<p align="center">
  <img src="/assets/Baseline_modeles/Figure_4.png" alt="calibration_curve"/>
</p>

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