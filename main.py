#importation des modules
from tkinter import *
from random import *
_PhotoImageTk = PhotoImage

def PhotoImage(file) :
	"Charge une image ; Tk >= 8.6 lit les PNG, sinon repli sur Pillow"
	try :
		return _PhotoImageTk(file=file)
	except TclError :
		from PIL import Image, ImageTk
		return ImageTk.PhotoImage(Image.open(file).convert("RGBA"))

#fonctions

##################################################
def init() :
	"Écran d'accueil de l'application"
	global DISPLAY
	DISPLAY = "loading"
	can.delete(ALL) #effacer le canvas
	images_autres() #importation des autres images du jeu
	can.create_image(640, 360, image=DICO_IMG_AUTRES["stade"]) #image de fond
	can.create_image(640, 160, image=DICO_IMG_AUTRES["logo"]) #image logo du jeu
	can.create_text(640, 625, text="Chargement...", fill="#FFFFFF", font=("Arial","20","bold")) #texte "Chargement"
	fen.after(100, loading) #commencer le chargement
##################################################

##################################################
def loading() :
	"Chargement du jeu"
	images_types() #importation des images du type de pokémon
	images_pokemons() #importations des images des pokémons
	images_cadres() #importation des images des cadres autour de chaque pokémon
	images_num_gen() #importation des images des numéros de génération dans le pokédex
	read_types() #lecture et création de tableau de types (combat)
	read_infos() #création de la liste 2D concernant les infos de chaque pokemon
	fen.after(100, pre_pokedex) #afficher le pokédex une fois le chargement terminé
##################################################

##################################################
def pre_pokedex() :
	"Avant l'affichage du pokédex"
	global DISPLAY
	#bar : barre au dessus de navigation entre les générations (canvas)
	DISPLAY = "pokedex"
	
	bar.place(x=0,y=0) #placement de la barre
	bar.create_image(640, 25, image=DICO_IMG_AUTRES["bar"]) #image de fond de la barre

	bar.create_image(150, 25, image=DICO_IMG_AUTRES["battle"]) #image du bouton combat
	bar.create_image(1080, 25, image=DICO_IMG_AUTRES["deck"]) #image du bouton combat
	bar.create_image(1230, 25, image=DICO_IMG_AUTRES["exit"]) #image du bouton combat
	#images des boutons générations
	for n in range(8) :
		if n == GEN :
			bar.create_image(TUPLE_CX_GEN[n], 25, image=LISTE_IMG_NUM_GEN[n+8])
		else :
			bar.create_image(TUPLE_CX_GEN[n], 25, image=LISTE_IMG_NUM_GEN[n])

	pokedex() #affiche les pokémons
##################################################

##################################################
def pokedex() :
	"Affichage des pokemons en possession"
	global SCROLL
	can.delete(ALL) #efface le canvas
	can.create_image(0, 0, image=DICO_IMG_AUTRES["fond"], anchor="nw") #image de fond
	SX = TUPLE_NB_GEN[GEN]//6
	if SX == TUPLE_NB_GEN[GEN]/6 :
		SX -= 1
	can.create_rectangle(1260, 50+SCROLL*(670/SX), 1280, 50+(SCROLL+1)*(670/SX), fill="#FFFFFF", width=0)

	#pour chaque pokemon affiché (8)
	for n in range(18) :
		x, y = TUPLE_CXY_POKEDEX[n][0], TUPLE_CXY_POKEDEX[n][1]
		n += 6*SCROLL + TUPLE_MAX_GEN[GEN]
		#si le pokemon est dans la liste et dans la génération affichée
		if TUPLE_MAX_GEN[GEN] <= n < TUPLE_MAX_GEN[GEN+1] and n < 890 :
			if TABLE_INFOS[n][6] == "1" :
				# can.create_image(x+20, y+135, image=DICO_IMG_AUTRES["plus"])
				pokemon(n, x, y) #affichage du pokémon et de ses caractéristiques
			else :
				can.create_image(x, y, image=DICO_IMG_AUTRES["cadre_vide"]) #affichage d'un cadre vide
##################################################

##################################################
def display_deck() :
	global DECK, DISPLAY
	DISPLAY = "deck"
	can.delete(ALL)
	can.create_image(640, 360, image=DICO_IMG_AUTRES["fond"]) #image de fond
	DECK = [] #liste vide
	FICHIER = open("fichiers/deck.txt")
	for LIGNE in FICHIER :
		DECK.append(int(LIGNE)) #ajouter les 6 pokémons du deck
	FICHIER.close
	for n in range(6) :
		pokemon(DECK[n]-1, TUPLE_CXY_POKEDEX[n+6][0], TUPLE_CXY_POKEDEX[n+6][1])
	can.create_image(TUPLE_CXY_POKEDEX[MODIF+6][0], TUPLE_CXY_POKEDEX[MODIF+6][1]+25, image=DICO_IMG_AUTRES["arrow"])
##################################################

##################################################
def pre_battle() :
	"Combat"
	global DISPLAY, DECK, SCORE, STEP_ADV, STEP_PLR, SCORE_F
	#DECK : deck du combat : 4 pokémons adverses + 4 pokémons du joueur (liste)
	#SCORE : score du combat (entier)
	#STEP_ADV : avancement du combat (entier)
	DISPLAY = "pre_battle"
	SCORE = 0
	STEP_ADV = 6
	STEP_PLR = 6
	SCORE_F = 0

	bar.place(x=0, y=-200) #enlever la barre
	can.delete(ALL) #effacer le canvas
	can.create_image(640, 360, image=DICO_IMG_AUTRES["fond_battle"]) #image de fond

	DECK = [] #liste vide
	for n in range(6) :
		DECK.append(randint(1,890)) #ajouter 4 pokémons random
	FICHIER = open("fichiers/deck.txt")
	for LIGNE in FICHIER :
		DECK.append(int(LIGNE)) #ajouter les 4 pokémons du deck
	FICHIER.close
	
	for n in range(12) :
		x, y = TUPLE_CXY_BATTLE[n][0], TUPLE_CXY_BATTLE[n][1]
		pokemon(DECK[n]-1, x, y) #affiche les pokémons du deck
##################################################

##################################################
def battle() :
	global DISPLAY, ADV
	DISPLAY = "battle"
	can.delete(ALL) #effacer le canvas
	can.create_image(640, 360, image=DICO_IMG_AUTRES["fond_battle"]) #image de fond

	for n in range(6) :
		x, y = TUPLE_CXY_BATTLE[n+6][0], TUPLE_CXY_BATTLE[n+6][1]
		if DECK[n+6] != -1 :
			pokemon(DECK[n+6]-1, x, y) #affiche les pokémons du deck

	ADV = 6 - STEP_ADV
	pokemon(DECK[ADV]-1, 640, 150) #affiche les pokémons du deck

	can.create_text(220, 40, text="POINTS FAIBLES", fill="#FFFFFF", font=("Arial", 20, "bold"))
	can.create_text(1060, 40, text="POINTS FORTS", fill="#FFFFFF", font=("Arial", 20, "bold"))

	LISTE_TYPE_ADV = []
	LISTE_FAIBLE = []
	LISTE_FORT = []

	for k in range(2) :
		for n in range(18) :
			if TUPLE_TYPES[n] == type((DECK[ADV]-1))[k] :
				LISTE_TYPE_ADV.append(n)
	for k in range(2) :
		for n in range(18) :
			if TABLE_TYPES[n][LISTE_TYPE_ADV[k]] == "-1" :
				LISTE_FORT.append(n)
			elif TABLE_TYPES[n][LISTE_TYPE_ADV[k]] == "1" :
				LISTE_FAIBLE.append(n)

	LISTE_FAIBLE = list(set(LISTE_FAIBLE))
	LISTE_FORT = list(set(LISTE_FORT))

	for n in LISTE_FAIBLE :
		for k in LISTE_FORT :
			if n == k :
				LISTE_FORT.remove(k)
				LISTE_FAIBLE.remove(n)

	y = 75
	for n in LISTE_FAIBLE :
		can.create_image(220, y, image=DICO_IMG_TYPES[TUPLE_TYPES[n]]) #logo du premier type
		y += 25
	y = 75
	for n in LISTE_FORT :
		can.create_image(1060, y, image=DICO_IMG_TYPES[TUPLE_TYPES[n]]) #logo du premier type
		y += 25
##################################################

##################################################
def duel(PLR) :
	"Duel entre 2 pokémons dans un combat"
	global SCORE, DECK, STEP_ADV, STEP_PLR, DISPLAY, SCORE_F
	#SAVE : sauvegarde du score avant sa mise à jour pour savoir qui a gagné le duel
	DISPLAY = "duel"
	LISTE_NUM = [DECK[PLR], DECK[ADV]]

	#types des pokémons concernés par le duel
	LISTE_TYPES = []
	for n in range(2) :
		LISTE_TYPES += type(LISTE_NUM[n]-1)
	for n in range(4) :
		for i in range(18) :
			if TUPLE_TYPES[i] == LISTE_TYPES[n] :
				LISTE_TYPES[n] = i

	#coordonnées des pokémons concernés par le duel
	xj, yj = TUPLE_CXY_BATTLE[PLR][0], TUPLE_CXY_BATTLE[PLR][1]
	# xa, ya = TUPLE_CXY_BATTLE[ADV][0], TUPLE_CXY_BATTLE[ADV][1]

	#mettre à jour le score en fonction des types des pokémons du duel
	SAVE = SCORE
	for n in range(2) :
		SCORE += int(TABLE_TYPES[LISTE_TYPES[n]][LISTE_TYPES[n+2]])

	#afficher un symbole gagné ou perdu selon le duel de pokémons
	if SAVE < SCORE : #gagne
		can.create_image(640, 150, image=DICO_IMG_AUTRES["perdu"])
		# can.create_image(xj, yj, image=DICO_IMG_AUTRES["gagne"])
		SCORE_F += 1
		DECK[ADV] = -1
		STEP_ADV -= 1
	elif SAVE > SCORE : #perdu
		# can.create_image(640, 150, image=DICO_IMG_AUTRES["gagne"])
		can.create_image(xj, yj, image=DICO_IMG_AUTRES["perdu"])
		SCORE_F -= 1
		DECK[PLR] = -1
		STEP_PLR -= 1
	else : #égalité
		can.create_image(640, 150, image=DICO_IMG_AUTRES["perdu"])
		can.create_image(xj, yj, image=DICO_IMG_AUTRES["perdu"])
		DECK[ADV], DECK[PLR] = -1, -1
		STEP_ADV -= 1
		STEP_PLR -= 1

	# DECK[ADV], DECK[PLR] = -1, -1 #montrer que ces pokémons ont déjà joué
	# STEP_ADV -= 1 #enlever 1 à l'avancement du combat

	if STEP_ADV == 0 or STEP_PLR == 0 :
		fen.after(1000, fin_battle) #écran de fin de combat si celui-ci est terminé
##################################################

##################################################
def fin_battle() :
	"Fin du combat"
	global DISPLAY, IMG_OEUF, OEUF_RARE, SCORE_F
	DISPLAY = "fin_battle"
	can.delete(ALL) #effacer le canvas
	can.create_image(0, 0, image=DICO_IMG_AUTRES["fond"], anchor="nw") #image de fond
	#vérification du nombre de pokémons possédés
	NB_UNLOCK = 0
	for n in range(890) :
		if TABLE_INFOS[n][6] == "1" :
			NB_UNLOCK += 1
	#perdu : pas de gain
	
	if NB_UNLOCK == 890 :
		can.create_text(640, 360, text="VOUS AVEZ TOUS LES POKÉMONS !", font=("Arial",50,"bold"), fill="#FFFFFF")
		SCORE_F = -1
	elif STEP_PLR == 0 and STEP_ADV != 0 :
		can.create_text(640, 360, text="PERDU !", font=("Arial",50,"bold"), fill="#FFFFFF")
	#égalité ou gagné : oeuf gagné
	else :
		RANDOM = randint(1,20)
		if RANDOM == 1 :
			OEUF_RARE = "ultra-chimère"
		elif 2 <= RANDOM < 3 :
			OEUF_RARE = "fabuleux"
		elif 4 <= RANDOM < 7 :
			OEUF_RARE = "légendaire"
		else :
			OEUF_RARE = ""
		IMG_OEUF = PhotoImage(file="images/oeuf_"+OEUF_RARE+".png")
		can.create_image(640, 420, image=IMG_OEUF)
		can.create_text(640, 80, text="Oeuf de Pokémon "+OEUF_RARE+" !", font=("Arial",30,"bold"), fill="#FFFFFF")
##################################################

##################################################
def oeuf_open() :
	"Gains d'oeufs"
	global DISPLAY, TABLE_INFOS
	DISPLAY = "oeuf_open"
	can.delete(ALL) #effacer le canvas
	can.create_image(0, 0, image=DICO_IMG_AUTRES["fond"], anchor="nw") #image de fond
	POKEMON_GAIN = randint(0,889)
	try :
		while TABLE_INFOS[POKEMON_GAIN][4].lower() != OEUF_RARE or TABLE_INFOS[POKEMON_GAIN][6] == "1" :
			POKEMON_GAIN = randint(0,889)
	except :
		while TABLE_INFOS[POKEMON_GAIN][6] == "1" :
			POKEMON_GAIN = randint(0,889)
	pokemon(POKEMON_GAIN, 640, 360)

	TABLE_INFOS[POKEMON_GAIN][6] = 1
	with open("fichiers/infos.txt", "w") as FICHIER :
		DICO_CARACTERES = {"â":"Ã¢", "é":"Ã©", "è":"Ã¨", "É":"Ã‰", "♀":"â™€", "♂":"â™", "ï":"Ã¯", "È":"Ãˆ", "Ê":"Ãª", "ç":"Ã§", "ô":"Ã´"} #caratères à transformer en utf-8

		for n in range(890) :
			for k in range(7) :
				TABLE_INFOS[n][k] = str(TABLE_INFOS[n][k])
			ligne = ";".join(TABLE_INFOS[n])
			for av, ap in DICO_CARACTERES.items() :
				ligne = ligne.replace(av, ap)
			FICHIER.write(ligne)
			FICHIER.write("\n")
##################################################

##################################################
def images_types() :
	"Importation des images du type de pokemon"
	global DICO_IMG_TYPES
	#DICO_IMG_TYPES : Données des images importées de chaque type (dictionnaire)
	DICO_IMG_TYPES = {} #dictionnaire vide
	#pour le nombre de types (18)
	for n in range(18) :
		DICO_IMG_TYPES[TUPLE_TYPES[n]] = PhotoImage(file="types/"+TUPLE_TYPES[n].lower()+".png") #ajoute l'image dans le dictionnaire au même rang que le type concerné
##################################################

##################################################
def images_pokemons() :
	global TABLE_IMG_POKEMONS
	"Importation des images des pokemons"
	#TABLE_IMG_POKEMONS : Données des images importées de chaque pokémon (liste 2D)
	TABLE_IMG_POKEMONS = [] #liste vide
	#pour le nombre de pokémons (890)
	for n in range(890) :
		n = "0"*(3-len(str(n+1))) + str(n+1) #place des 0 au début du nombre pour avoir une chaine de 3 caractères
		TABLE_IMG_POKEMONS.append(PhotoImage(file="pokemons/"+n+".png")) #ajoute l'image importée dans la liste
##################################################

##################################################
def images_cadres() :
	"Importation des images du cadre autour des pokemons"
	global DICO_IMG_CADRES
	#DICO_IMG_CADRES : Données des images importées de chaque cadre de pokémon (dictionnaire)
	DICO_IMG_CADRES = {} #dictionnaire vide
	#pour le nombre de cadres (4)
	for n in range(4) :
		DICO_IMG_CADRES[TUPLE_RARETES[n]] = PhotoImage(file="images/cadre_"+TUPLE_RARETES[n]+".png") #ajoute l'image dans le dictionnaire au même rang que la rareté concernée
##################################################

##################################################
def images_num_gen() :
	global LISTE_IMG_NUM_GEN
	"Importation des images des pokemons"
	#TABLE_IMG_NUM_GEN : Données des images importées de chaque numéro de génération (liste 2D)
	LISTE_IMG_NUM_GEN = [] #liste vide
	for k in ("", "_select") : #ajouter les images de sélection après
		#pour le nombre de générations (7)
		for n in range(8) :
			LISTE_IMG_NUM_GEN.append(PhotoImage(file="images/num"+str(n+1)+k+".png")) #ajoute l'image importée dans la liste
##################################################

##################################################
def images_autres() :
	global DICO_IMG_AUTRES
	"Importation des autres images du jeu"
	#DICO_IMG_AUTRES : Données des images importées (dictionnaire)
	DICO_IMG_AUTRES = {} #dictionnaire vide
	#pour le nombre d'images (8)
	for n in TUPLE_IMG_AUTRES :
		DICO_IMG_AUTRES[n] = PhotoImage(file="images/"+n+".png") #ajoute l'image dans le dictionnaire
##################################################

##################################################
def read_infos() :
	"Lire le tableau d'infos au format .txt et le transformer en liste 2D"
	global TABLE_INFOS
	#TABLE_INFOS : tableau de données sur les pokémons (liste 2D)
	#DICO_UNLOCK : nombre de pokémons débloqués par rareté (dictionnaire)
	#FICHIER : fichier ouvert (liste 2D)
	#LIGNE : chaque ligne du fichier "FICHIER" (chaine de caractères)
	#DICO_CARACTERES : caractères mal encodés à remplacer (dictionnaire)
	#AV : caractère à remplacer pour Avant (chaine de caractères)
	#AP : caractère remplacé pour Après (chaine de caractères)
	
	TABLE_INFOS = [] #liste vide
	with open("fichiers/infos.txt") as FICHIER :
		#pour chaque ligne du fichier
		for LIGNE in FICHIER :
			DICO_CARACTERES = {"Ã©":"é", "Ã¨":"è", "Ã‰":"É", "â™€":"♀", "â™":"♂", "Ã¯":"ï", "'ï»¿":"", "ï»¿":"", "Ãˆ":"È", "Ãª":"Ê", "Ã¢":"â", "Ã§":"ç", "Ã´":"ô"} #caratères à transformer en utf-8
			#pour chaque élément du dictionnaire
			for AV, AP in DICO_CARACTERES.items() :
				LIGNE = LIGNE.replace(AV, AP) #remplacer les caractères affichés non normalement
			TABLE_INFOS.append(LIGNE.replace("\n","").split(";")) #transformer la ligne en liste (séparateur ";")
##################################################

##################################################
def read_types() :
	"Lire le tableau de types au format .txt et le transformer en liste 2D"
	global TABLE_TYPES
	#TABLE_TYPES : Informations sur les types qui l'emportent (liste 2D)
	#FICHIER : fichier ouvert (liste 2D)
	#LIGNE : chaque ligne du fichier "FICHIER" (chaine de caractères)
	TABLE_TYPES = [] #liste vide
	FICHIER = open("fichiers/type.txt") #ouvrir le fichier
	#pour chaque ligne du fichier
	for LIGNE in FICHIER :
		TABLE_TYPES.append(LIGNE.replace("\n","").split(";")) #transformer la ligne en liste (séparateur ";")
	FICHIER.close() #fermer le fichier
##################################################

##################################################
def pokemon(NUM, x, y) :
	"Afficher un pokémon avec ses caractéristiques"
	#NUM : Numéro du pokémon (de 0 à 890)
	#x, y : coordonnées de l'image
	#TYPE : type du pokémon
	can.create_image(x, y, image=DICO_IMG_CADRES[TABLE_INFOS[NUM][4]]) #image du cadre autour
	can.create_image(x, y, image=TABLE_IMG_POKEMONS[NUM]) #image du pokemon
	can.create_text(x, y+125, text=TABLE_INFOS[NUM][1].upper(), fill="#FFFFFF", font=("Arial",15, "bold")) #nom du pokemon
	can.create_text(x+75, y+95, text=TABLE_INFOS[NUM][0], fill="#FFFFFF", font=("Arial",25,"bold"), anchor="e") #numéro du pokemon
	
	#nombre de types du pokémon (1 ou 2 selon la présence du "/" dans l'élément de la liste)
	TYPE = type(NUM)
	# can.create_image(x-32, y+85, image=DICO_IMG_TYPES[TYPE[0]]) #logo du premier type
	if TYPE[0] != TYPE[1] : #pour 2 types
		can.create_image(x-32, y+85, image=DICO_IMG_TYPES[TYPE[0]]) #logo du premier type
		can.create_image(x-32, y+105, image=DICO_IMG_TYPES[TYPE[1]]) #logo du deuxième type
	else :
		can.create_image(x-32, y+95, image=DICO_IMG_TYPES[TYPE[0]]) #logo du premier type
##################################################

##################################################
def type(NUM) :
	"Trouver le(s) type(s) d'un pokémon"
	#SLASH : position du "/" dans la case du tableau (séparer les 2 types)
	LISTE = [] #liste vide
	if "/" in TABLE_INFOS[NUM][2] :
		slash = TABLE_INFOS[NUM][2].find("/")
		LISTE.append(TABLE_INFOS[NUM][2][0:slash])
		LISTE.append(TABLE_INFOS[NUM][2][slash+1:len(TABLE_INFOS[NUM][2])])
	else :
		for n in range(2) :
			LISTE.append(TABLE_INFOS[NUM][2])
	return LISTE
##################################################

##################################################
def clic(evt) :
	"Actions à faire quand le clic droit est pressé"
	global GEN, SCROLL, TABLE_INFOS, MODIF
	#pokedex
	if DISPLAY == "pokedex" :
		#pour chaque bouton de génération
		for n in range(8) :
			if TUPLE_CX_GEN[n]-50 < evt.x < TUPLE_CX_GEN[n]+50 and 0 < evt.y < 50 :
				GEN = n #changer la génération (de 0 à 7)
				SCROLL = 0 #remettre le scroll à 0
				pre_pokedex() #remettre à jour l'affichage
		if 25 < evt.x < 275 and 0 < evt.y < 50 :
			fen.after(10, pre_battle) #lancer le combat
		if 1005 < evt.x < 1155 and 0 < evt.y < 50 :
			fen.after(100, display_deck)
		if 1205 < evt.x < 1255 and 0 < evt.y < 50 :
			fen.destroy()
		for n in range(18) :
			if TUPLE_CXY_POKEDEX[n][0]-75 < evt.x < TUPLE_CXY_POKEDEX[n][0]+75 and TUPLE_CXY_POKEDEX[n][1]-75 < evt.y < TUPLE_CXY_POKEDEX[n][1]+75 :
				try :
					if TABLE_INFOS[6*SCROLL + TUPLE_MAX_GEN[GEN] + n][6] == "1" and TUPLE_MAX_GEN[GEN] < (6*SCROLL + TUPLE_MAX_GEN[GEN] + n + 1) <= TUPLE_MAX_GEN[GEN+1] :
						LISTE = [] #liste vide
						FICHIER = open("fichiers/deck.txt")
						for LIGNE in FICHIER :
							LISTE.append(int(LIGNE)) #ajouter les 4 pokémons du deck
						FICHIER.close
						LISTE[MODIF] = 6*SCROLL + TUPLE_MAX_GEN[GEN] + n + 1
						FICHIER = open("fichiers/deck.txt", "w")
						for LIGNE in LISTE :
							FICHIER.write(str(LIGNE))
							FICHIER.write("\n")
						FICHIER.close()
				except :
					pass
					
	#préparation du combat
	if DISPLAY == "pre_battle" :
		fen.after(100, battle)
	#combat
	if DISPLAY == "battle" :
		#pour chaque pokémon du joueur
		for n in range(6) :
			if TUPLE_CXY_BATTLE[n+6][0]-100 < evt.x < TUPLE_CXY_BATTLE[n+6][0]+100 and TUPLE_CXY_BATTLE[n+6][1]-100 < evt.y < TUPLE_CXY_BATTLE[n+6][1]+100 :
				if DECK[n+6] != -1 :
					fen.after(100, duel(n+6)) #lance un duel pour le nième pokémon du joueur
	if DISPLAY == "duel" and STEP_ADV != 0 and STEP_PLR != 0 :
		fen.after(1000, battle)
	#fin de combat
	if DISPLAY == "fin_battle" :
		if SCORE_F <= 0 :
			pre_pokedex() #revenir au pokédex
		else :
			fen.after(100, oeuf_open) #ouverture d'oeuf
	#ouverture d'oeuf
	if DISPLAY == "oeuf_open" :
		read_infos() #remettre à jour les données pour ajouter le nouveau pokémon
		fen.after(100, pre_pokedex) #revenir au pokédex
	if DISPLAY == "deck" :
		if evt.y < 50 :
			fen.after(100, pre_pokedex)
		else :
			for n in range(6) :
				if TUPLE_CXY_POKEDEX[n+6][0]-75 < evt.x < TUPLE_CXY_POKEDEX[n+6][0]+75 :
					MODIF = n
			display_deck()
##################################################

##################################################
def scroll_action(evt) :
	"Actions à faire quand le scroll est déclenché"
	global SCROLL
	#pokedex
	if DISPLAY == "pokedex" :
		#monter
		if evt.delta > 0 and SCROLL > 0 :
			SCROLL -= 1
		#descendre
		elif evt.delta < 0 and SCROLL < TUPLE_NB_GEN[GEN]/6 - 2 :
			SCROLL += 1
		pokedex() #remettre à jour l'affichage
##################################################

#création de la fenêtre
fen = Tk()
fen.geometry("1280x720")
fen.title("Pokémon Générations")

#création du canvas
can = Canvas(fen, width=1280, height=720, bg="#00AAEE", highlightthickness=0)
can.place(x=0,y=0)
bar = Canvas(fen, width=1280, height=50, bg="#003040", highlightthickness=0) #création de la barre

#variables
DISPLAY = "loading" #état de la fenêtre (utile pour les clics détectés)
SCROLL = 0 #état de scroll dans le pokedex
GEN = 0 #génération affichée dans le pokédex
MODIF = 0 #pokémon modifié du deck

#tuples
TUPLE_TYPES = ("ACIER", "COMBAT", "DRAGON", "EAU", "ÉLECTRIK", "FÉE", "FEU", "GLACE", "INSECTE", "NORMAL", "PLANTE", "POISON", "ROCHE", "PSY", "SPECTRE", "SOL", "TÉNÈBRES", "VOL") #tous les types
TUPLE_RARETES = ("", "légendaire", "fabuleux", "ultra-chimère")
TUPLE_IMG_AUTRES = ("fond", "battle", "cadre_vide", "fond_battle", "perdu", "gagne", "stade", "logo", "bar", "deck", "exit", "arrow", "plus")
TUPLE_MAX_GEN = (0, 151, 251, 386, 493, 649, 721, 809, 890) #maximums de chaque génération
TUPLE_NB_GEN = (151, 100, 135, 107, 156, 72, 88, 81) #nombre de pokémons dans chaque génération
TUPLE_CX_GEN = (349, 435, 521, 607, 693, 779, 865, 951) #coordonnées x des images de générations dans le pokédex
TUPLE_CXY_POKEDEX = ((140,130), (340,130), (540,130), (740,130), (940,130), (1140,130), (140,350), (340,350), (540,350),
					 (740,350), (940,350), (1140,350), (140,570), (340,570), (540,570), (740,570), (940,570), (1140,570)) #coordonnées x et y des pokémons affichés dans le pokédex
TUPLE_CXY_BATTLE = ((140,180), (340,180), (540,180), (740,180), (940,180), (1140,180), (140,520), (340,520), (540,520), (740,520), (940,520), (1140,520)) #coordonnées x et y des pokémons affichés en combat
DICO_MAX_RARE = {"":728, "légendaire":49, "fabuleux":21, "ultra-chimère":11, "total":890}

#fonctions principales
init() #lancement de l'application
fen.bind_all("<ButtonPress-1>", clic) #détection du clic droit enfoncé
can.bind("<MouseWheel>", scroll_action) #détection de la molette
fen.resizable(width=False, height=False) #empêcher le redimensionnement de la fenêtre
fen.mainloop() #afficher la fenêtre en continu jusqu'à l'arrêt du programme