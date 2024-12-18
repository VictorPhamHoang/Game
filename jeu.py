import sqlite3
import time

conn = sqlite3.connect('bd.sqlite')
curseur = conn.cursor()

### Définitions des fonctions

#ajoute un petit délai pour l'affichage de texte, on remplacera print() par cette fonction
def print_delay(ch):
    time.sleep(0.1)
    print(ch)


#afficher le nom du jeu
def demarrage():
    print_delay("\n\n\n")
    print_delay("****************************")
    print_delay("* - Restaurant Simulator - *")
    print_delay("****************************\n\n")


#fonction qui demande le pseudo du joueur, puis vérifie si le pseudo est dans la table Joueur, si non : le rajoute avec le nom du joueur en +
def verif_pseudo(pseudo):
    curseur.execute("SELECT pseudo_joueur FROM joueur")
    liste_pseudo = curseur.fetchall()
    print_delay("")

    #si le pseudo renseigné est dans la BD on lui affiche toutes les parties qu'il a crée et on lui demande s'il veut continuer une partie en cours ou en recommencer une
    if ((pseudo,) in liste_pseudo):
        #récupération liste des parties du joueurs
        curseur.execute("SELECT id_entreprise, score, mois_en_cours, nom_entreprise FROM entreprise where pseudo_joueur = ?", (pseudo,))
        liste = curseur.fetchall()

        #il se peut que l'on ait créée un compte mais pas créer de partie
        #dans ce cas, on crée une partie automatiquement dans le 'if'
        if liste == []:
            return creation_partie(pseudo)

        #affiche la liste des parties d'un joueur
        else:  
            liste_affi = []
            print_delay("Il semble que vous ayez déjà un compte, voici la liste de vos parties:") 
            for k in range (len(liste)):
                if liste[k][2] < 4:
                    print_delay("partie numéro "+ str(k) + ": [nom du restaurant: " + str(liste[k][3]) + ", statut: en cours, mois: " + str(liste[k][2]) + "/4]")
                else:
                    print_delay("partie numéro "+ str(k) + ": [nom du restaurant " + str(liste[k][3]) + ", statut: terminé, score: " + str(liste[k][1]) + "]")

        #demande si l'utilisateur veux continuer une partie ou en recommencer une
        print_delay("\nChoisissez si vous voulez continuer une partie ou en recommencer une ('continuer'/'recommencer'):")
        print("-> ", end = "")
        choix = ""

        #vérifie que l'utilisateur a bien écrit 'continuer' ou 'recommencer'
        while (choix != "continuer") and (choix != "recommencer"):
            choix = input()

            #si l'utilisateur veut continuer alors il doit renseigné le numéro de partie (qui etait affiché dans la liste des parties créées)
            if choix == "continuer":
                print_delay("Ecrivez le numéro de la partie que vous voulez continuer ou afficher les scores d'une partie au statut 'terminé':")
                print("-> ", end = "")
                n = int(input())

                #vérifie que le numéro de partie renseigné est bien valide
                if 0 <= int(n) and int(n) < len(liste):
                    id_entrepr = liste[n][0]
                    return id_entrepr
                else:
                    while not(0 <= int(n) and int(n) < len(liste)):
                        print_delay("erreur : écrivez un numéro de partie valide (les numéros de partie se trouvent au dessus)")
                        print("-> ", end="")
                        n = int(input())
                    id_entrepr = liste[n][0]
                    return id_entrepr
                
            #si l'utilisateur veut recommencer, alors on créée une nouvelle partie
            elif choix == "recommencer":
                return creation_partie(pseudo)
            print_delay("erreur: veuillez choisir entre 'continuer' et 'recommencer' ")
            print("-> ", end="")

    #sinon on créer un nouveau joueur dans la table Joueur ayant pour ID le pseudo qu'il a renseigné
    #puis on créer une nouvelle partie avec creation_partie() définie au préalable
    else:
        print_delay("Votre pseudo n'est pas répertorié donc il semble que vous soyez nouveau, nous allons vous créer un compte qui aura pour identifiant votre pseudo ['" + str(pseudo) + "'] (il ne faut pas l'oublier!).")
        print_delay("Avant de commencer la partie, pouvons-nous connaître votre nom ? : ")
        print("nom-> ", end = "")
        nom = input()
        print_delay("\n")
        creation_compte(pseudo, nom)
        return creation_partie(pseudo)


#créer un compte si l'utilisateur utilise un pseudo (lorsqu'on lui demande un pseudo) qui n'est pas dans la BD
def creation_compte(pseudo, nom_joueur):
    curseur.execute("INSERT INTO joueur VALUES (?, ?)", (pseudo, nom_joueur))
    conn.commit()


#créer une nouvelle partie (nouvelle ligne d'une entreprise dans la table Entreprise) en lui expliquant le but du jeu et en lui demandant le nom du restaurant
def creation_partie(pseudo):
    curseur.execute("SELECT nom_joueur FROM joueur WHERE pseudo_joueur = ?", (pseudo,))
    nom_joueur = curseur.fetchall()

    #but du jeu et demande nom du restaurant
    print_delay("Bonjour " + str(nom_joueur[0][0]) + ", bienvenue dans Restaurant Simulator !" )
    print_delay("Vous êtes sur le point d'ouvrir votre restaurant.")
    print_delay("Le jeu se déroulera en 4 tours, votre but sera de rembourser un prêt tout en ayant le meilleur avis des clients.")
    print_delay("A chaque tour vous devrez faire un choix en fonction du niveau des ressources (inflation, coût des ressources...)")
    print_delay("Tout d'abord, quel nom voulez-vous donner à votre restaurant ?")
    print_delay("Insérez un nom de restaurant :")
    print("-> ", end ="")
    nom_restaurant = input()
    print_delay("\n")

    #insère le restaurant dans la BD ayant pour ID (27 si c'est la 27e partie créée par exemple)
    curseur.execute("SELECT id_entreprise FROM entreprise") #récupère l'ID de la dernière partie créée
    resultats = curseur.fetchall()
    id_restaurant = len(resultats) + 1
    curseur.execute("INSERT INTO entreprise (id_entreprise, pseudo_joueur, nom_entreprise, mois_en_cours) VALUES (?, ?, ?, ?)", (id_restaurant, pseudo, nom_restaurant, 1))
    conn.commit()

    return(id_restaurant)


#permet de recupérer le mois en cours d'une partie afin de faire jouer l'utilisateur jusqu'à que le mois dépasse 4 mois
def recup_sauvegarde_mois(id_entreprise):
    curseur.execute("SELECT mois_en_cours FROM entreprise WHERE id_entreprise = ?", (id_entreprise,))
    resultats = curseur.fetchall()
    return(resultats[0][0])


#vérifie si l'utilisateur écrit 'ok' dans une fonction input()
#cette fonction sera utilisée à la fin de chaque tour(mois) afin que cela sauvegarde la partie et que la partie passe au tour(mois) suivant
def ok(numero_mois):
    print("Ecrivez 'ok' afin de sauvegarder le mois " + str(numero_mois) + " et passer au mois suivant:")
    print("'ok'-> ", end = "")
    input_user = input()
    while input_user != "ok":
        print("Veuillez réessayer en écrivant 'ok':")
        print("ok-> ", end="")
        input_user = input()
    print("\npartie sauvegardé!")

#vérifie si l'utilisateur écrit bien un nombre entier ou flottant
def input_int_or_float():
    print_delay("Ecrivez un nombre :")
    print("-> €", end = "")
    number = input()
    condition = True
    if "." in number:
        try:
            float_test = float(number)
            if float_test > 0:
                    condition = False
        except ValueError:
            condition = True
    else:
        try:
            int_test = int(number) 
            if int_test > 0:
                    condition = False
        except ValueError:
            condition = True
    
    while condition:
        print_delay("Veuillez écrire un nombre valide, pensez à mettre un point au lieu d'une virgule :")
        print("-> €", end = "")
        number = input()
        if "." in number:
            try:
                float_test = float(number)
                if float_test > 0:
                    condition = False
            except ValueError:
                condition = True
        else:
            try:
                int_test = int(number) 
                if int_test > 0:
                    condition = False
            except ValueError:
                condition = True

    return number

#fonction qui prend en paramètre le mois, puis en fonction de celui-ci, exécute la fonction appropriée en fonction du numéro du mois
def jeu(mois, pseudo, id_entreprise):
    if mois == 1:
        jeu_mois_1(id_entreprise, mois)

    elif mois == 2:
        jeu_mois_2(id_entreprise, mois)

    elif mois == 3:
        jeu_mois_3(id_entreprise, mois)

    elif mois == 4:
        jeu_mois_4(id_entreprise, mois)

    elif mois == 5:
        jeu_mois_5(id_entreprise, mois)


#jeu du mois 1
def jeu_mois_1(id_entreprise, mois):
    print_delay("\n\n\n*****************")
    print_delay("Début du 1er mois")
    print_delay("*****************")
    print_delay("""Récaputilatif : 
        Il vous manquez 1150€ pour ouvrir votre restaurant et vous les avez emprunté à la banque à taux d'intérêt 0,
        que vous allez devoir rembourser au bout des 4 mois.
        Le loyer est de 2000€/mois,
        l'énergie est de 200€/mois
        vous avez 1 salarié que vous payez 2500€/mois, 
        vos dépenses personnelles s'élèvent à 1500€/mois,
        le prix de la matière première pour UN plat est de 5€ """)
    print_delay("Sachant qu'il y aura environ 24 clients par jour.")
    print_delay("Vous allez devoir fixer le prix d'un plat, attention: un prix élevé peu baisser votre la note des clients mais augmentra votre bénéfice!")
    print_delay("Quel prix voulez-vous fixer pour UN plat ce mois-ci ? (en euro et écrire un point à la place d'une virgule, exemple: 12.5):")
    prix = float(input_int_or_float())

    print_delay("\n--Fin du 1er mois--")
    
    curseur.execute("SELECT prix_matieres_prem, prix_loyer, salaire, depenses_persos, energie FROM ressources WHERE id_ressource == 1")
    liste = curseur.fetchall()
    nb_clients = 24

    #bénéfice = prix*nb_clients*30 - (loyer + energie + depenses_persos + salaire + prix_mat_prem*nb_clients*30)
    benefice = round(prix*nb_clients*30 - (liste[0][1] + liste[0][4] + liste[0][3] + liste[0][2] + liste[0][0]*nb_clients*30), 1)

    #note en fonction du prix en utilisant les règles de note_mois_1()
    note = round(note_mois_1(prix), 2)
    print_delay("Vous avez fait un bénéfice de " + str(benefice) +"€ ce mois-ci, et avez obtenu une moyenne de " + str(note) +" étoiles sur Tripadvisor ce premier mois.")

    ok(mois)

    #mise à jour dans la bd : du mois, du benefice total et de la note moyenne totale du restaurant
    curseur.execute("UPDATE entreprise SET mois_en_cours = 2 WHERE id_entreprise = ?", (id_entreprise,))
    conn.commit()
    curseur.execute("UPDATE entreprise SET note_totale = ?, benefice_total = ? WHERE id_entreprise = ?", (note, benefice, id_entreprise))
    conn.commit()

#etoiles en fonction du prix du plat pour le mois 1
def note_mois_1(prix):
    if 18 <= prix:
        return 0
    elif 17 <= prix and prix < 18:
        return 1
    elif 16 <= prix and prix < 17:
        return 2
    elif 15 <= prix and prix < 16:
        return 3
    elif 14 <= prix and prix < 15:
        return 4
    elif prix < 14:
        return 5
        
#jeu du mois 2
def jeu_mois_2(id_entreprise, mois):
    print_delay("\n\n")
    print_delay("****************")
    print_delay("Début du 2e mois")
    print_delay("****************\n")
    print_delay("Il y a eu une inflation de 10" + "%" + " sur la matière première et il y aura environ 18 clients par jour à cause de l'inflation.")
    print_delay("Quel nouveau prix voulez vous fixer pour UN plat ce mois-ci ?")
    prix = float(input_int_or_float())

    print_delay("\n--Fin du 2e mois--")

    curseur.execute("SELECT prix_matieres_prem, prix_loyer, salaire, depenses_persos, energie FROM ressources WHERE id_ressource == 2")
    liste = curseur.fetchall()

    nb_clients = 18

    #bénéfice = prix*nb_clients*30 - (loyer + energie + depenses_persos + salaire + prix_mat_prem*nb_clients)
    benefice = round(prix*nb_clients*30 - (liste[0][1] + liste[0][4] + liste[0][3] + liste[0][2] + liste[0][0]*nb_clients*30), 1)
    #note en fonction du prix en utilisant les règles de note_mois_2_3()
    note = round(note_mois_2_3(prix), 2)
    
    curseur.execute("SELECT note_totale FROM entreprise WHERE id_entreprise = ?", (id_entreprise,))
    note_bd = curseur.fetchall()
    #calcule la nouvelle note en prenant en compte les mois précédents
    nouvelle_note = round((note_bd[0][0] + note)/mois, 2)
    
    curseur.execute("SELECT benefice_total FROM entreprise WHERE id_entreprise = ?", (id_entreprise,))
    benefice_bd = curseur.fetchall()
    #calcule le benefice total en prenant en compte les mois précédents
    nouveau_benefice = benefice_bd[0][0] + benefice

    #affiche les résultats du mois et globaux
    print_delay("Ce mois-ci, vous avez fait un bénéfice de " + str(benefice) +"€ et obtenu une note moyenne de " + str(note) +" étoiles sur Tripadvisor.")
    print_delay("Durant ces 2 mois, votre bénéfice total est donc de: " + str(nouveau_benefice) + "€ et votre note moyenne totale est passée à : " + str(nouvelle_note) + " étoiles")

    ok(mois)


    #mise à jour dans la bd
    curseur.execute("UPDATE entreprise SET mois_en_cours = 3 WHERE id_entreprise = ?", (id_entreprise,))
    conn.commit()
    curseur.execute("UPDATE entreprise SET note_totale = ?, benefice_total = ? WHERE id_entreprise = ?", (nouvelle_note, nouveau_benefice, id_entreprise))
    conn.commit()


#jeu du mois 3
def jeu_mois_3(id_entreprise, mois):
    print_delay("\n\n")
    print_delay("****************")
    print_delay("Début du 3e mois")
    print_delay("****************\n")
    print_delay("Il y a eu une augmentation de l'énergie de 200€ et il y aura encore environ 18 clients par jour ce mois-ci")
    print_delay("Quel nouveau prix voulez vous fixer pour UN plat ce mois-ci ?")
    prix = float(input_int_or_float())

    print_delay("\n--Fin du 3e mois--")

    curseur.execute("SELECT prix_matieres_prem, prix_loyer, salaire, depenses_persos, energie FROM ressources WHERE id_ressource == 3")
    liste = curseur.fetchall()

    nb_clients = 18

    #bénéfice = prix*nb_clients*30 - (loyer + energie + depenses_persos + salaire + prix_mat_prem*nb_clients)
    benefice = round(prix*nb_clients*30 - (liste[0][1] + liste[0][4] + liste[0][3] + liste[0][2] + liste[0][0]*nb_clients*30), 1)
    #note en fonction du prix en utilisant les règles de note_mois_2_3()
    note = round(note_mois_2_3(prix), 2)
    
    curseur.execute("SELECT note_totale FROM entreprise WHERE id_entreprise = ?", (id_entreprise,))
    note_bd = curseur.fetchall()
    #calcule la nouvelle note en prenant en compte les mois précédents
    nouvelle_note = round((2*note_bd[0][0] + note)/mois, 2)

    curseur.execute("SELECT benefice_total FROM entreprise WHERE id_entreprise = ?", (id_entreprise,))
    benefice_bd = curseur.fetchall()
    #calcule le benefice total en prenant en compte les mois précédents
    nouveau_benefice = benefice_bd[0][0] + benefice

    #affiche les résultats du mois et globaux
    print_delay("Ce mois-ci, vous avez fait un bénéfice de " + str(benefice) +"€ et obtenu une note moyenne de " + str(note) +" étoiles sur Tripadvisor.")
    print_delay("Durant ces 3 mois, votre bénéfice total est donc de: " + str(nouveau_benefice) + "€ et votre note moyenne totale est passée à: " + str(nouvelle_note) + " étoiles")

    ok(mois)

    #mise à jour dans la bd
    curseur.execute("UPDATE entreprise SET mois_en_cours = 4 WHERE id_entreprise = ?", (id_entreprise,))
    conn.commit()
    curseur.execute("UPDATE entreprise SET note_totale = ?, benefice_total = ? WHERE id_entreprise = ?", (nouvelle_note, nouveau_benefice, id_entreprise))
    conn.commit()


#etoiles en fonction du prix du plat pour le mois 2 et 3
def note_mois_2_3(prix):
    if 19 <= prix:
        return 0
    elif 18 <= prix and prix < 19:
        return 1
    elif 17 <= prix and prix < 18:
        return 2
    elif 16 <= prix and prix < 17:
        return 3
    elif 15 <= prix and prix < 16:
        return 4
    elif prix < 15:
        return 5

#jeu du mois 4
#c'est le dernier mois, donc après ce tour le jeu est fini, ainsi on affiche les résultats du joueurs (bénéfice, note et score)
#puis le mois du restaurant passe à 5 par convention (5 <=> partie finie <=> affichage des résultats)
def jeu_mois_4(id_entreprise, mois):
    print_delay("\n\n")
    print_delay("**************************")
    print_delay("Début du 4e (dernier) mois")
    print_delay("**************************\n")
    print_delay("""Un restaurant concurrent arrive dans la ville, celui-ci fixe son prix d'un plat à 16€
            de ce fait, votre restaurant fixe aussi le prix d'un plat à 16€ et donc la note totale de votre restaurant ne changera pas ce mois-ci.
            Cependant, vous avez le choix de licencier votre salarié ou non,
            si vous le licenciez: vous êtes seul et vous ne pouvez qu'accepter 14 clients par jour,
            sinon: le nombre de clients moyen par jour est toujours de 18.""")
    print_delay("Voulez-vous donc licencier votre salarié ? (oui/non) ?")
    print("-> ", end= "")
    choix = input()

    #vérifie si l'utilisateur écrit bien 'oui' ou 'non' (on aurait pu définir une fonction comme pour ok() mais on ne va l'utiliser qu'une fois)
    while choix != "oui" and choix != "non":
        print_delay("Veuillez écrire 'oui' ou 'non':")
        print("-> ", end="")
        choix = input()

    curseur.execute("SELECT prix_matieres_prem, prix_loyer, salaire, depenses_persos, energie FROM ressources WHERE id_ressource == 3")
    liste = curseur.fetchall()
    prix = 16
 
    if choix == "oui":
        nb_clients = 14
        benefice = round(prix*nb_clients*30 - (liste[0][1] + liste[0][4] + liste[0][3] + liste[0][0]*nb_clients*30), 1)
        print_delay("Vous avez fait un bénéfice de " + str(benefice) + "€ ce mois-ci")

    else:
        nb_clients = 18
        benefice = round(prix*nb_clients*30 - (liste[0][1] + liste[0][4] + liste[0][3] + liste[0][2] + liste[0][0]*nb_clients*30), 1)
        print_delay("\nVous avez fait un bénéfice de " + str(benefice) + "€ ce mois-ci") 

    print_delay("\n--Fin du 4e (dernier) mois--")

    curseur.execute("SELECT prix_matieres_prem, prix_loyer, salaire, depenses_persos, energie FROM ressources WHERE id_ressource == 3")
    liste = curseur.fetchall()

    curseur.execute("SELECT benefice_total FROM entreprise WHERE id_entreprise = ?", (id_entreprise,))
    benefice_bd = curseur.fetchall()
    nouveau_benefice = benefice_bd[0][0] + benefice

    #mise à jour dans la bd
    curseur.execute("UPDATE entreprise SET mois_en_cours = 5 WHERE id_entreprise = ?", (id_entreprise,))
    conn.commit()
    curseur.execute("UPDATE entreprise SET benefice_total = ? WHERE id_entreprise = ?", (nouveau_benefice, id_entreprise))
    conn.commit()

#fin de partie, affiche le score de la partie
def jeu_mois_5(id_entreprise, mois):
    print_delay("\nVous avez terminé la partie.\n")

    curseur.execute("SELECT benefice_total FROM entreprise WHERE id_entreprise = ?", (id_entreprise,))
    benefice_bd = curseur.fetchall()
    curseur.execute("SELECT note_totale FROM entreprise WHERE id_entreprise = ?", (id_entreprise,))
    note_bd = curseur.fetchall()

    print_delay("Votre bénéfice total durant ces 4 mois est de: " + str(benefice_bd[0][0]) + "€.")
    if benefice_bd[0][0] > 10000:
        print_delay("Bravo vous avez fait les bons choix et avez réussi à rembourser votre prêt!")
        score = int(round((benefice_bd[0][0] + note_bd[0][0]*10),0))

    else:
        print_delay("Malheureusement vous n'avez pas fait les bons choix et donc vous n'avez pas réussi à rembourser votre prêt de 1150€ en 4 mois)")
        score = int(round((0 + note_bd[0][0]*10),0))

    curseur.execute("SELECT note_totale FROM entreprise WHERE id_entreprise = ?", (id_entreprise,))
    note_bd = curseur.fetchall()
    print_delay("Et la note totale sur ces 4 mois de votre restaurant est de : " + str(note_bd[0][0]) + " étoiles sur Tripadvisor!")
    print_delay("Le score de votre partie est calculée en fonction de: si vous avez remboursé votre près, le bénéfice et de la note des clients.")

    
    print_delay("\nVous avez donc obtenu le score de : " + str(score) + "\n")
    
    curseur.execute("UPDATE entreprise SET score = ? WHERE id_entreprise = ?", (score, id_entreprise,))
    conn.commit()

###########################################

### Code exécuté

demarrage()
print_delay("Veuillez taper votre pseudo afin de vous connecter/créer un compte (exemple: alexandre123): ")
print("-> ", end="")
pseudo = input()

id_entreprise = verif_pseudo(pseudo) #exécute la vérification de pseudo puis recupère l'id de l'entreprise jouée (une nouvelle ou une ancienne en cours)
mois = recup_sauvegarde_mois(id_entreprise) #récupère le dernier mois joué par l'utilisateur afin qu'il reprenne sa partie là où il s'était arrêté.

#si c'est une nouvelle partie, ou une partie en cours : on rentre dans la bouche
#sinon c'est une partie terminée on exécute jeu_mois_5() qui affiche le score de la partie terminée
while(mois < 5):
    jeu(mois, pseudo, id_entreprise) #exécute le jeu en fonction du mois en cours du restaurant
    mois = recup_sauvegarde_mois(id_entreprise) #récupère le nouveau mois

#après la boucle, le mois est définie à 5: c'est la fin de la partie
#la fonction affiche le score de la partie
jeu_mois_5(id_entreprise, mois)

print_delay("Vous pouvez quitter le terminal")

curseur.close()
conn.close()