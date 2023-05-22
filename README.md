# TIPE_Baskettball
**Repo contenant tout le nécessaire à mon TIPE**

Le but du tipe est de proposer un systeme permettant de compter les points d'un match de basket grâce à une prise vidéo en directe 
    et de pouvoir en même temps enregister une vidéo avec le systeme de tracking et une sans. 

Pour le moment on traque une balle grace à sa couleur, il faut implementer le suivie par forme afin
    de faire les deux en même temps.

Il faut faire attention à la version d'opencv d'installer, il faut la version 4.5.4.60

Problématique : 
    Comment liberer de la mêmoire humaine ?

**Ce qui reste à implémenter :**
* suivie de la balle par la forme 
* suivie des joueurs (leurs placements) et si ils ont la balles
* suivie des points 
* suivie des joueurs (leurs statistique)
* mini map ?? 

Listes des sites utiles pour le TIPE
- https://github.com/ry-werth/nba-automation
- https://pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
- https://colorpicker.me/#d21313
- https://piofthings.net/blog/opencv-baby-steps-4-building-a-hsv-calibrator
- https://github.com/abhisavaliya/hsv_calibration/
- https://www.devopsschool.com/blog/what-is-opennn-and-how-it-works-an-overview-and-its-use-cases/


# À Checker : 
Nous initialisons ensuite un détecteur de cascade Haar pour détecter les cercles (paniers) à partir du fichier XML "haarcascade_basketball.xml".

Kalman filter : https://www.educba.com/opencv-kalman-filter/
et le github
# Motivation

## Comptage de point automatisé/informatisé

Le comptage des points est un élément central du basketball, mais parfois à cause du manque de bénévoles des joueurs doivent s’en charger, les pénalisants ainsi.C’est pour cela que j’ai décidé de me pencher sur un comptage de points automatisé, facilement modifiable, grâce à une caméra. 

La conception de ce système s’inscrit directement dans le thème de l’année, de par son importance dans le jeu, et par son utilisation possible lors des entrainement du basketball. 


### *Problématique :*  
La tenue des scores étant essentielle au basketball, il est important de trouver un moyen fiable et peu chère d’assister les bénévoles dans la prise en compte des paniers, et de par la même occasion fournir aux équipes des statistique non apporté par les statistiques de la fédération.


## Sceance du 15/05
reprise depuis les vacances, plusieurs tentatives avec un filtre de kalman, 
"script/IA_assistef/video_balltracker.py" le script fonctionne, il faut maintenant le modifier pour avoir le suivie d'une seule balle

## Scéance du 22/05 
Début de la mcot, la vidéo tourne à present en boucle (problème de freezze resolue avec une double boucle while)
liste des problemes inatendus : reflet des balles sur un beau sol
but : 
* ligne horizontal pour la detection du panier ( decouper  en 6 zone pour un panier a droite un panier à gauche) 