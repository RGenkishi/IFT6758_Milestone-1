docker run --env COMET_API_KEY=$COMET_API_KEY --publish 8080:8080 serving
# La variable d'environnement est passée ici pour pouvoir run le container avec une autre API KEY que celle
# de la machine où le container a été build