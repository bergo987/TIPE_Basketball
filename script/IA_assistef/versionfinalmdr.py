import cv2

# Charger la vidéo
cap = cv2.VideoCapture('/Users/hugo/Documents/Cours/Prepa/TIPE/TIPE_Baskettball/script/IA_assistef/match.mp4')

# Initialiser le détecteur de cascade Haar pour la détection de cercles (paniers)
basket_cascade = cv2.CascadeClassifier('haarcascade_basketball.xml')

while cap.isOpened():
    # Lire une image de la vidéo
    ret, frame = cap.read()

    if ret:
        # Convertir l'image en niveaux de gris
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Détecter les cercles (paniers)
        baskets = basket_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        # Dessiner des rectangles autour des cercles détectés
        for (x, y, w, h) in baskets:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Basket", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Afficher l'image avec les cercles détectés
        cv2.imshow('frame', frame)

        # Attendre l'appui sur la touche 'q' pour quitter la boucle
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

# Libérer la capture vidéo et détruire toutes les fenêtres d'affichage
cap.release()
cv2.destroyAllWindows()
