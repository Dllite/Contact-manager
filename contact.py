import csv
import tkinter as tk
from tkinter import filedialog

def ajouter_contact():
    while True:
        nom = input("Entrez le nom du contact : ")
        numero = input("Entrez le numéro de téléphone du contact : ")
        
        if not nom.replace(" ", "").isalpha():
            print("Le nom ne doit contenir que des lettres et des espaces.")
            continue  
        if not numero.isdigit():
            print("Le numéro de téléphone ne doit contenir que des chiffres.")
            continue  
        with open('contacts.dat', 'a') as fichier:
            fichier.write(f"Nom: {nom}, Numéro: {numero}\n")
            
        print("Contact ajouté avec succès!")
        break  


def afficher_contacts():
    print("\nListe des contacts :")
    contacts = []
    try:
        with open('contacts.dat', 'r') as fichier:
            for ligne in fichier:
                Nom, Numero = ligne.strip().split(", ")
                print(ligne.strip())
                contacts.append({"Nom": Nom.split(": ")[1], "Numero": Numero.split(": ")[1]})
                #print(contacts)
    except FileNotFoundError:
        print("Le fichier n'existe pas encore. Ajoutez un contact pour le créer.")

def charger_contacts():
    contacts = []
    try:
        with open('contacts.dat', 'r') as fichier:
            for ligne in fichier:
                nom, numero = ligne.strip().split(", ")
                contacts.append({"nom": nom.split(": ")[1], "numero": numero.split(": ")[1]})
    except FileNotFoundError:
        print("Le fichier n'existe pas encore. Ajoutez un contact pour le créer.")
    return contacts

def modifier_contact(contacts):
    for i, contact in enumerate(contacts):
        print(f"{i+1}. Nom: {contact['nom']}, Numéro: {contact['numero']}")
    
    choix = int(input("Entrez le numéro du contact à modifier : ")) - 1
    if 0 <= choix < len(contacts):
        nouveau_nom = input("Entrez le nouveau nom (laissez vide pour ne pas changer) : ")
        nouveau_numero = input("Entrez le nouveau numéro (laissez vide pour ne pas changer) : ")
        
        if nouveau_nom:
            contacts[choix]['nom'] = nouveau_nom
        if nouveau_numero:
            contacts[choix]['numero'] = nouveau_numero
        print("Contact modifié avec succès!")
    else:
        print("Choix invalide.")

def sauvegarder_contacts(contacts):
    with open('contacts.dat', 'w') as fichier:
        for contact in contacts:
            fichier.write(f"Nom: {contact['nom']}, Numéro: {contact['numero']}\n")

def generer_csv_contacts(contacts):
    nom_fichier = input("Entrez le nom du fichier CSV à générer (sans extension) : ")
    nom_fichier += ".csv"

    try:
        with open(nom_fichier, 'w', encoding='utf-8') as fichier_csv:
            # Écriture de du fichier CSV
            fichier_csv.write("Nom,Numéro\n")

            # Écriture des données des contacts
            for contact in contacts:
                fichier_csv.write(f"{contact['nom']},{contact['numero']}\n")

        print(f"Liste des contacts générée avec succès dans '{nom_fichier}'.")
    except IOError:
        print("Erreur lors de la génération du fichier CSV.")
def parcourir_machine():
    root = tk.Tk()
    root.withdraw()

    # Affiche la boîte de dialogue de sélection de fichier
    nom_fichier = filedialog.askopenfilename(title="Sélectionnez un fichier CSV", filetypes=[("Fichiers CSV", "*.csv")])

    if nom_fichier:
        print(f"Fichier sélectionné : {nom_fichier}")
        importer_csv_contacts(nom_fichier)  # Appel la fonction d'importation en passant le chemin du fichier
    else:
        print("Aucun fichier sélectionné.")

def importer_csv_contacts(nom_fichier):
    try:
        contacts = []  # Créer une nouvelle liste pour stocker les contacts importés
        
        with open(nom_fichier, 'r', encoding='utf-8') as fichier_csv:
            lecteur_csv = csv.reader(fichier_csv)
            next(lecteur_csv)  # Ignorer la première ligne (en-tête)

            for ligne in lecteur_csv:
                nom, numero = ligne
                contacts.append({'nom': nom, 'numero': numero})  # Ajouter chaque contact à la liste

        print(f"Contacts importés avec succès depuis '{nom_fichier}'.")
        return contacts  # Retourner la liste des contacts importés
    except FileNotFoundError:
        print("Le fichier CSV spécifié n'existe pas.")
        return [] 
    except IOError:
        print("Erreur lors de la lecture du fichier CSV.")
        return [] 

def menu():
    contacts = charger_contacts()
    while True:
        choix = input("\nQue souhaitez-vous faire ?\n1. Ajouter un contact\n2. Afficher les contacts\n3. Générer la liste des contacts au format CSV\n4. Importer une liste de contacts depuis un fichier CSV\n5. Modifier un contact\n6. Quitter\nChoix : ")
        
        if choix == '1':
            ajouter_contact()
            contacts = charger_contacts() 
        elif choix == '2':
            afficher_contacts()
        elif choix == '3':
            generer_csv_contacts(contacts)
        elif choix == '4':
            parcourir_machine()
        elif choix == '5':
            modifier_contact(contacts)
            sauvegarder_contacts(contacts)
        elif choix == '6':
            sauvegarder_contacts(contacts)
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    menu()
