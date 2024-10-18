import streamlit as st
import pandas as pd
import datetime
import glob
import requests
import json
import re
import numpy as np
import plotly.express as px
import time
from Recuperation_uuids import scraping_GN, uuids_cleaning, recup_group, uuids_cleaning2
from Traitement_records import transcript_json, recup_fiche2, recup_themes_thesaurus_motsCles, recup_attachements, recup_ressources
from Recuperation_groupes import recup_groupes
import ast

######################################################################################################################
########### TITRE DE L'ONGLET ########################################################################################
######################################################################################################################
st.set_page_config(
    page_title="Contenu du catalogue InDoRES",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Application de suivi des outils de science ouverte du RZA, développé par Jérôme Dutroncy"}
)

######################################################################################################################
########### COULEURS DES PAGES #######################################################################################
######################################################################################################################
st.markdown("""
 <style>
    [data-testid=stSidebar] {
        background-color: rgb(6,51,87,0.2);
    }
    .st-emotion-cache-1dj0hjr {
            color: #a9dba6;
    }
    .st-emotion-cache-1q2d4ya {
            color: #3b979f;
    }
    </style>
""", unsafe_allow_html=True)

######################################################################################################################
########### CHOIX VISUELS ############################################################################################
######################################################################################################################
couleur_subtitles = (250,150,150)
taille_subtitles = "25px"
couleur_subsubtitles = (60,150,160)
taille_subsubtitles = "25px"
couleur_True = (0,200,0)
couleur_False = (200,0,0)
wch_colour_box = (250,250,220)
wch_colour_font = (90,90,90)
fontsize = 70

######################################################################################################################
############ PARAMETRES ##############################################################################################
######################################################################################################################

# Date du jour
d = datetime.date.today()
# url du geonetwork
url = "https://cat.indores.fr/geonetwork/srv/api/records/"

# Accès au geonetwork
headers_json = {"accept":"application/json",
           "X-XSRF-TOKEN": "59734158-1618-4e14-b05e-919d931a384b"}
headers_xml = {"accept":"application/xml",
           "X-XSRF-TOKEN": "59734158-1618-4e14-b05e-919d931a384b"}
headers_text = {"accept":"text/plain",
           "X-XSRF-TOKEN": "59734158-1618-4e14-b05e-919d931a384b"}

# Listes
liste_ZAs = [" Zone atelier Alpes", 
             " Zone atelier arc jurassien", 
             " Zone atelier Loire",
             " Zone atelier Armorique",
             " Zone atelier bassin du Rhône",
             " Zone atelier Brest Iroise", 
             " Zone atelier environnementale urbaine",
             " Zone atelier Pyrénées Garonne", 
             " Zone atelier bassin de la Moselle", 
             " Zone Atelier Seine",
             " Zone atelier Hwange",
             "Zone atelier territoires uranifères",
             " Zone Atelier Antarctique et Terres Australes",
             " Zone Atelier Argonne",
             " Zone Atelier Santé Environnement Camargue",
             " Zone atelier Plaine et Val de Sèvre"]

liste_OHMs = ['OHM Littoral méditerranéen',
              'OHM Oyapock',
              'OHM Pyrénées - haut Vicdessos',
              'OHM Bassin Minier de Provence',
              'OHMi Pima County',
              'OHMi Nunavik',
              'OHMi Téssékéré',
              'OHMi Estarreja',
              'OHM Vallée du Rhône',
              'OHM Pays de Bitche',
              'OHM Littoral Caraïbe',
              'OHM Patagonia',
              'OHM Fessenheim',
              'DRIIHM']

filtre_mention =['zaa ','zone atelier alpes', 'zaa - alpes',
           'zone atelier arc jurassien' , 'zaaj - arc jurassien', 'jura',
           'zaar', 'zone atelier armorique','zaar - armorique',
           'zaeu','Zone atelier environnementale urbaine','zaeu - environnementale urbaine',
           'zabr','Zone atelier bassin du Rhône','zabr - bassin du rhône',
           'zabri','Zone atelier Brest Iroise','zabri - brest iroise',
           'zam','Zone atelier bassin de la moselle', 'zam - moselle',
           'zal','Zone atelier loire','zal - loire',
           'zas','zone atelier seine', 'zas - seine',
           'zone atelier pyrénées garonne', 'zapygar - pyrénées-garonne'
           'zone atelier santé environnement camargue', 'zacam - sante environnement camargue',
           'zone atelier territoires uranifères', 'zatu - territoires uranifères',
           'zone atelier antarctique et terres australes',
           'zone atelier argonne', 'zarg - argonne',
           'zone atelier plaine et val de sèvre', 'zapvs - plaine et val de sèvre',
           'zone atelier hwange', 'zahwg - Hwange',
           'ohmi nunavik', 'ohm oyapock', 'ohm pays de bitche', 'ohm bassin minier de provence', 
           'ohmi téssékéré', 'ohm vallée du rhône','ohmi estarreja','ohm pyrénées - haut vicdessos', 
           'ohm littoral méditerranéen', 'ohmi pima county', 'ohm littoral caraïbe']

dico = {"zaa":" Zone atelier Alpes",
        'zone atelier alpes':" Zone atelier Alpes",
        'zaa - alpes':" Zone atelier Alpes",
        "zaaj":" Zone atelier arc jurassien",
        "zone atelier arc jurassien":" Zone atelier arc jurassien",
        "zaaj - arc jurassien":" Zone atelier arc jurassien",
        "jura":" Zone atelier arc jurassien",
        "zaar":" Zone atelier Armorique",
        "zone atelier armorique":" Zone atelier Armorique",
        "zaar - armorique":" Zone atelier Armorique",
        "zaeu":" Zone atelier environnementale urbaine",
        "zone atelier environnementale urbaine":" Zone atelier environnementale urbaine",
        "zaeu - Environnementale Urbaine":" Zone atelier environnementale urbaine",
        "zabr":" Zone atelier bassin du Rhône",
        "zone atelier bassin du rhône":" Zone atelier bassin du Rhône",
        "zabri":" Zone atelier Brest Iroise",
        'zabri - brest iroise':" Zone atelier Brest Iroise",
        "zas":" Zone Atelier Seine",
        "zone atelier seine":" Zone Atelier Seine",
        "zas - seine":" Zone Atelier Seine",
        "zam":" Zone atelier bassin de la Moselle",
        "zone atelier bassin de la moselle":" Zone atelier bassin de la Moselle",
        "zam - moselle":" Zone atelier bassin de la Moselle",
        "zal":" Zone atelier Loire",
        "zone atelier loire":" Zone atelier Loire",
        "zal - loire":" Zone atelier Loire",
        "zapygar":" Zone atelier Pyrénées Garonne",
        "zone atelier pyrénées garonne":" Zone atelier Pyrénées Garonne",
        "zapygar - pyrénées-garonne":" Zone atelier Pyrénées Garonne",
        "zatu":"Zone atelier territoires uranifères",
        "zone atelier territoires uranifères":"Zone atelier territoires uranifères",
        "zata":" Zone Atelier Antarctique et Terres Australes",
        "zone atelier antarctique et terres australes":" Zone Atelier Antarctique et Terres Australes",
        "zapvs":" Zone atelier Plaine et Val de Sèvre",
        "zone atelier plaine et val de sèvre":" Zone atelier Plaine et Val de Sèvre",
        "zarg":" Zone Atelier Argonne",
        'zarg - argonne':" Zone Atelier Argonne",
        "zone atelier argonne":" Zone Atelier Argonne",
        "zahwg":" Zone atelier Hwange",
        "zone atelier hwange":" Zone atelier Hwange",
        "zacam":" Zone Atelier Santé Environnement Camargue",
        "zone atelier santé environnement camargue":" Zone Atelier Santé Environnement Camargue",
        "OHM Pyrénées - haut Vicdessos":"OHM Pyrénées - haut Vicdessos",
        "ohm pyrénées - haut vicdessos":"OHM Pyrénées - haut Vicdessos",
        "OHM Vallée du Rhône":"OHM Vallée du Rhône",
        "ohm vallée du rhône":"OHM Vallée du Rhône",
        "OHMi Téssékéré":"OHMi Téssékéré",
        "ohmi téssékéré":"OHMi Téssékéré",
        "OHMi Pima County":"OHMi Pima County",
        "ohmi pima county":"OHMi Pima County",
        "OHMi Estarreja":"OHMi Estarreja",
        "ohmi estarreja":"OHMi Estarreja",
        "OHM Littoral méditerranéen":"OHM Littoral méditerranéen",
        "ohm littoral méditerranéen":"OHM Littoral méditerranéen",
        "OHM Bassin Minier de Provence":"OHM Bassin Minier de Provence",
        "ohm bassin minier de provence":"OHM Bassin Minier de Provence",
        "OHM Oyapock":"OHM Oyapock",
        "ohm oyapock":"OHM Oyapock",
        "OHMi Nunavik":"OHMi Nunavik",
        "ohmi nunavik":"OHMi Nunavik",
        "OHM Littoral Caraïbe":"OHM Littoral Caraïbe",
        "ohm littoral caraïbe":"OHM Littoral Caraïbe",
        "OHM Pays de Bitche":"OHM Pays de Bitche",
        "ohm pays de bitche":"OHM Pays de Bitche",
        "OHM Patagonia":"OHM Patagonia",
        "ohm patagonia":"OHM Patagonia",
        "OHM Fessenheim":"OHM Fessenheim",
        "ohm fessenheim":"OHM Fessenheim",
        'Aucun groupe, ni mention':'Aucun groupe, ni mention'}

###############################################################################################
############## RECUPERATION DES IDENTIFIANTS EXISTANTS ########################################

# Besoin de récupérer l'ensemble des identifiants

# On scanne pour savoir si un fichier existe
fi = glob.glob(f"pages/data/Cat_InDoRES/uuids/uuid_cat_InDoRes_clean*.csv")

st.title(':grey[Visualisation des fiches]')

st.success("Si vous le souhaitez, filtrer le réseau ciblé (RZA ou OHM) (par défaut, tout apparait) / CASE A COCHER")
st.success("Si vous le souhaitez, filtrer le groupe (ZA ou OHM) ciblé (par défaut, tout apparait) / LISTE DEROULANTE")

# Si oui, on récupère le dernier enregistré ; si non, on récupère les identifiants à la date donnée
if len(fi)!=0:
    fichier_uuids = fi[-1]
    derniere_date_recup = f"Dernière date de récupération des identifiants: {fichier_uuids[52:-4]}"
    s_derniere_date_recup  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{derniere_date_recup}</p>"
    st.markdown(s_derniere_date_recup ,unsafe_allow_html=True)
    ############################## UUIDS ########################################
    uuids = pd.read_csv(fichier_uuids, index_col=[0])
else:
    with st.spinner("Connexion au GeoNetwork et récupération des identifiants existants"):
        try:
            scraping_GN(d)
            uuids_cleaning2(d)
            st.experimental_rerun()
        except:
            st.write('Il est impossible de récupérer les identifiants')

################### CREATION / LECTURE DF INFOS GROUPES ##########################################

try:
    df_infos = pd.read_csv("pages/data/Cat_InDoRES/infos_MD2/infos_groupes.csv",index_col=[0])
except:
    df_infos = pd.DataFrame(columns=['Identifiant','Groupe'])
    df_infos.to_csv("pages/data/Cat_InDoRES/infos_MD2/infos_groupes.csv")

###############################################################################################
########### POUR L'ADMINISTRATEUR ############################################################
###############################################################################################

# Mot de passe pour faire des récupérations automatisées
admin_pass = 'admin'
admin_action = st.sidebar.text_input(label="Pour l'administrateur")

###############################################################################################
# RECUPERATION DES IDENTIFIANTS VIA BOUTON ####################################################

if admin_action == admin_pass:

    RecupIdentifiants = st.sidebar.button("Récupération des identifiants")
    if RecupIdentifiants:
        with st.spinner("Connexion au GeoNetwork et récupération des identifiants existants"):
            scraping_GN(d)   
            uuids_cleaning2(d)
            st.experimental_rerun()

###############################################################################################
# RECUPERATION DES GROUPES VIA BOUTON #########################################################
    col1, col2 = st.sidebar.columns(2)
    with col1:
        Recup_groupes = st.button('recup groupes')
    with col2:
        maj_groupes = st.button('maj')
    if Recup_groupes:
        with st.spinner("La récup des groupes est en cours"):
            liste_uuids = uuids['uuid_cat_InDoRes'].values
            recup_groupes(liste_uuids)
            #df_group = pd.read_csv("pages/data/Cat_InDoRES/infos_MD2/infos_groupes.csv",index_col=[0])
            #for i in range(len(uuids)):
            #    u = uuids.loc[i,'uuid_cat_InDoRes']
            #    if u in df_group['Identifiant'].values:
            #        pass
            #    else:
            #        try:
            #            g = recup_group(uuid=u)
            #        except:
            #            g = ""

            #        df_group_i = pd.DataFrame({'Identifiant':[u], 'Groupe':[g]})
            #        df_group_ = pd.concat([df_group,df_group_i],axis=0)
            #        df_group_.reset_index(inplace=True)
            #        df_group_.drop(columns='index',inplace=True)
            #        df_group = df_group_
            #df_group.to_csv("pages/data/Cat_InDoRES/infos_MD2/infos_groupes.csv")
    if maj_groupes:
        pass

###############################################################################################
# RECUP GLOBALE ###############################################################################

    Recup_globale = st.sidebar.button('recup globale')
    if Recup_globale:
        with st.spinner("La récup globale est en cours"):
            liste_columns_df = ['Identifiant', 'Langue', 'Jeu de caractères', 'Type', 'Date', 'Nom du standard', 'Version du standard', 'Nom du contact', 'orga du contact',
                            'Position du contact', 'Tel du contact', 'Adresse', 'Code Postal', 'Ville', 'Pays', 'Email du contact', "Systeme de référence",
                            'Longitude ouest', 'Longitude est', 'Latitude sud', 'Latitude nord', 'Titre',
                            'Fiche parent id', 'Résumé', "Date de création", 'Objectif', 'Status', 'Fréquence de maj', 'Autres dates', 'Info supplémentaire',
                            'Limite usage', 'Contrainte usage', 'Contrainte accès', 'Autre contrainte',
                            'Format', 'Url', 'Protocole', 'Online description', 'Online nom',
                            'Niveau', 'Conformité', 'Généalogie', 'Portée','Mention du groupe', 'Thesaurus', 'Thèmes', 'Mots Clés', 'theme_thesaurus_motsCles',
                            'F1', 'F2', 'F3', 'F4', 'A1', 'A2', 'I1', 'I2', 'I3', 'R1', 'R2', 'R3']
            df_global = pd.DataFrame(columns=liste_columns_df)
            for i in range(len(df_infos)):
                print(i)
                identif = df_infos.loc[i,'Identifiant']
                datafri = recup_fiche2(url, identif, headers_json, filtre_mention)
                new_df_global = pd.concat([df_global,datafri], axis=0)
                df_global = new_df_global
                df_global.reset_index(inplace=True)
                df_global.drop(columns='index',inplace=True)

            df_global.to_csv("pages/data/Cat_InDoRES/infos_MD2/Tableau_MD2.csv")

            ############## FUSION DES 2 DF: groupes et variables ############################
            df_all = pd.merge(df_global, df_infos, on='Identifiant', how='inner')
            df_all.to_csv("pages/data/Cat_InDoRES/infos_MD2/Tableau_complet.csv")

#################################################################################################
############## RECUP GLOBALE FICHIERS ATTACHES ###############################################
    Recup_attachements = st.sidebar.button('recup des fichiers attachés')
    if Recup_attachements:
        with st.spinner("La récup des fichiers attachés est en cours"):
            liste_columns_df_attachements = ['Identifiant', 'Noms des fichiers', 'Tailles des fichiers']
            df_global_attachements = pd.DataFrame(columns=liste_columns_df_attachements)
            for i in range(len(df_infos)):
                print(i)
                identif = df_infos.loc[i,'Identifiant']
                try:
                    df_attachementsi = recup_attachements(url, identif, headers_json)
                    new_df_global_attachements = pd.concat([df_global_attachements,df_attachementsi], axis=0)
                    df_global_attachements = new_df_global_attachements
                    df_global_attachements.reset_index(inplace=True)
                    df_global_attachements.drop(columns='index',inplace=True)
                except:
                    pass
            df_global_attachements.to_csv("pages/data/Cat_InDoRES/infos_MD2/Tableau_fichiers_attachements.csv")

#################################################################################################
############## RECUP GLOBALE RESSOURCES ASSOCIEES ###############################################
    Recup_ressources = st.sidebar.button('recup des ressources associées')
    if Recup_ressources:
        with st.spinner("La récup des ressources associées est en cours"):
            liste_columns_df_ressources = ['Identifiant', 'Check_children', 'Check_parent','Check_hassources', 'Check_associated', 'Check_hasfeaturescats', 'Check_fcats', 'Check_services', 'Check_BroAndSisters',
                                   'Nombre_children', 'Nombre_parent', 'Nombre_hassources', 'Nombre_associated', 'Nombre_hasfeaturescats', 'Nombre_fcats', 'Nombre_services', 'Nombre_BroAndSisters',
                                   "Children url (properties)", "Titre children","Résumé children", "Formats children", 'Urls children',
                                   "Parent url (properties)", "Titre parents","Résumé parents", "Formats parents", 'Urls parents',
                                   "hasfeaturecats url (properties)", "Titre hasfeaturecats","Résumé hasfeaturecats", "Formats hasfeaturecats", 'Urls hasfeaturecats',
                                   "facts url (properties)", "Titre facts", 
                                   "brothersAndSisters url (properties)","Titre brothersAndSisters","Résumé brothersAndSisters", "Formats brothersAndSisters", 'Urls brothersAndSisters']
            df_global_ressources = pd.DataFrame(columns=liste_columns_df_ressources)
            for i in range(len(df_infos)):
                print(i)
                identif = df_infos.loc[i,'Identifiant']
                try:
                    df_ressourcesi = recup_ressources(url, identif, headers_json)
                    new_df_global_ressources = pd.concat([df_global_ressources,df_ressourcesi], axis=0)
                    df_global_ressources = new_df_global_ressources
                    df_global_ressources.reset_index(inplace=True)
                    df_global_ressources.drop(columns='index',inplace=True)
                except:
                    pass
            df_global_ressources.to_csv("pages/data/Cat_InDoRES/infos_MD2/Tableau_fichiers_ressources.csv")



######################################################################################################################
########### LECTURE ET TRANSFORMATION DU TABLEAU COMPLET #############################################################
######################################################################################################################

df_complet = pd.read_csv("pages/data/Cat_InDoRES/infos_MD2/Tableau_complet.csv", index_col=[0])
df_complet.fillna("", inplace=True)


def transfo(input_string):
    # Use ast.literal_eval to safely evaluate the string as a Python expression
    return ast.literal_eval(input_string)

def transfo0(input_string):
    # Use ast.literal_eval to safely evaluate the string as a Python expression
    return input_string.replace("' '","','")

def transfo00(input_string):
    # Use ast.literal_eval to safely evaluate the string as a Python expression
    return input_string.replace(":"," ")

# Apply the transformation to the entire column
for i in range(len(df_complet)):
    if df_complet.loc[i,'Autres dates']=="":
        df_complet.loc[i,'Autres dates']="[]"
    if df_complet.loc[i,'Nom du contact']=="":
        df_complet.loc[i,'Nom du contact']="[]"
    if df_complet.loc[i,'orga du contact']=="":
        df_complet.loc[i,'orga du contact']="[]"
    if df_complet.loc[i,'Position du contact']=="":
        df_complet.loc[i,'Position du contact']="[]"
    if df_complet.loc[i,'Tel du contact']=="":
        df_complet.loc[i,'Tel du contact']="[]"
    if df_complet.loc[i,'Adresse']=="":
        df_complet.loc[i,'Adresse']="[]"
    if df_complet.loc[i,'Code Postal']=="":
        df_complet.loc[i,'Code Postal']="[]"
    if df_complet.loc[i,'Ville']=="":
        df_complet.loc[i,'Ville']="[]"
    if df_complet.loc[i,'Pays']=="":
        df_complet.loc[i,'Pays']="[]"
    if df_complet.loc[i,'Systeme de référence']=="":
        df_complet.loc[i,'Systeme de référence']="[]"
    if df_complet.loc[i,'Url']=="":
        df_complet.loc[i,'Url']="[]"
    if df_complet.loc[i,'Protocole']=="":
        df_complet.loc[i,'Protocole']="[]"
    if df_complet.loc[i,'Online description']=="":
        df_complet.loc[i,'Online description']="[]"
    if df_complet.loc[i,'Online nom']=="":
        df_complet.loc[i,'Online nom']="[]"
    if df_complet.loc[i,'Format']=="":
        df_complet.loc[i,'Format']="[]"

liste_col_transfo = ['Nom du contact','Position du contact','orga du contact','Tel du contact','Adresse','Code Postal',
                     'Ville','Pays','Url','Protocole','Online description','Online nom','Format']
for x, col in enumerate(liste_col_transfo):
    df_complet[col] = df_complet[col].apply(transfo0)
    df_complet[col] = df_complet[col].apply(transfo)

df_complet['Autres dates'] = df_complet['Autres dates'].apply(transfo)


for i in range(len(df_complet)):
    if 'AUTO' in df_complet.loc[i,'Systeme de référence']:
        df_complet.loc[i,'Systeme de référence']="['Aucun']"
df_complet['Systeme de référence'] = df_complet['Systeme de référence'].apply(transfo00)
df_complet['Systeme de référence'] = df_complet['Systeme de référence'].apply(transfo0)
df_complet['Systeme de référence'] = df_complet['Systeme de référence'].apply(transfo)


for i in range(len(df_complet)):
    if df_complet.loc[i,'Groupe'] != 'Non trié':
        df_complet.loc[i,'GroupeEtMention']=df_complet.loc[i,'Groupe']
    elif df_complet.loc[i,'Groupe'] == 'Non trié':
        if df_complet.loc[i,'Mention du groupe'] == 'Aucune mention':
            df_complet.loc[i,'GroupeEtMention']='Aucun groupe, ni mention'
        else:
            df_complet.loc[i,'GroupeEtMention']=df_complet.loc[i,'Mention du groupe']

df_complet['GroupeEtMention']=df_complet['GroupeEtMention'].map(dico)
df_complet.to_csv("pages/data/Cat_InDoRES/infos_MD2/Tableau_complet.csv")

#st.dataframe(df_complet)

######################################################################################################################
########### SELECTION ZA #############################################################################################
######################################################################################################################
## Le choix est exclusif ###############################################################################
if 'checkbox1' not in st.session_state:
    st.session_state.checkbox1 = False
if 'checkbox2' not in st.session_state:
    st.session_state.checkbox2 = False

# Function to handle checkbox1 change
def handle_checkbox1_change():
    if st.session_state.checkbox1:
        st.session_state.checkbox2 = False

# Function to handle checkbox2 change
def handle_checkbox2_change():
    if st.session_state.checkbox2:
        st.session_state.checkbox1 = False

st.sidebar.markdown('Sélection en cours')
col1,col2 =st.sidebar.columns(2)
choix_groupe_OHM = False
with col1:
    checkbox1 = st.checkbox("RZA", key='checkbox1', on_change=handle_checkbox1_change)
with col2:
    checkbox2 = st.checkbox("OHM", key='checkbox2', on_change=handle_checkbox2_change)


if checkbox1:
    selection_group = st.sidebar.multiselect('choix du groupe',options=liste_ZAs)
    if len(selection_group)==0:
        selection_group = liste_ZAs 
    selected_uuids = df_complet['Identifiant'][df_complet['GroupeEtMention'].isin(selection_group)]
    selected_uuids_ = selected_uuids.reset_index(drop=True)
    st.sidebar.metric('Nombre de fiches:',len(selected_uuids_))
elif checkbox2:
    selection_group = st.sidebar.multiselect('choix du groupe',options=liste_OHMs)
    if len(selection_group)==0:
        selection_group = liste_OHMs
    selected_uuids = df_complet['Identifiant'][df_complet['GroupeEtMention'].isin(selection_group)]
    selected_uuids_ = selected_uuids.reset_index(drop=True)
    st.sidebar.metric('Nombre de fiches:',len(selected_uuids_))
else:
    selected_uuids_ = df_complet['Identifiant'].values
    st.sidebar.metric('Nombre de fiches:',len(selected_uuids_))


##################################################################################################
######################## VISUALISATIONS ##########################################################
##################################################################################################
if 'count' not in st.session_state:
    st.session_state.count = 0
def increment_counter():
    st.session_state.count += 1
def reset_counter():
    st.session_state.count = 0

if 'Visu_attachments' not in st.session_state:
    st.session_state.Visu_attachments = False
if 'Ressources_associees' not in st.session_state:
    st.session_state.Ressources_associees = False

def handle_button1_change():
    if st.session_state.Visu_attachments:
        st.session_state.Ressources_associees = False

def handle_button2_change():
    if st.session_state.Ressources_associees:
        st.session_state.Visu_attachments = False

with st.container(border=True):
    s1 = "IDENTIFIEUR"
    s_s1 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s1}</p>"
    st.markdown(s_s1,unsafe_allow_html=True)

    if st.session_state.count > len(selected_uuids_):
        st.session_state.count = 0

    id_choisie = selected_uuids_[0]
    col01,col02,col03,col4,col5 = st.columns([0.5,0.1,0.1,0.1,0.2])
    with col01:
        try:
            identifieur = st.selectbox(label='',options=selected_uuids_, index=st.session_state.count)
        except: 
            identifieur = ""
            reset_counter()
    with col02:
        st.markdown('')
        st.markdown('')
        button1 = st.button(':heavy_plus_sign:',on_click=increment_counter)
    with col03:
        st.markdown('')
        st.markdown('')
        button2 =st.button('R',on_click=reset_counter)
    with col4:
        st.metric(label="compteur",value=st.session_state.count)
    with col5:
        Visu_attachments = st.checkbox(label='Fichiers attachés', key='Visu_attachments',on_change=handle_button1_change)
        Ressources_associees = st.checkbox(label='Ressources associées', key='Ressources_associees',on_change=handle_button2_change)

    if st.session_state.count > len(selected_uuids_):
        st.write('Vous êtes au bout!')

###############################################################################################################
######################## VISUALISATIONS ATTACHEMENTS ##########################################################
###############################################################################################################
if Visu_attachments:
    df_attachements = pd.read_csv("pages/data/Cat_InDoRES/infos_MD2/Tableau_fichiers_attachements.csv", index_col=[0])

    Sommes_check_selected_df = f"Décomptes sur la sélection en cours"
    s_Sommes_check_selected_df  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Sommes_check_selected_df}</p>"
    st.markdown(s_Sommes_check_selected_df ,unsafe_allow_html=True)

    df_attachements_visu = df_attachements[df_attachements['Identifiant'].isin(selected_uuids_)]
    df_attachements_visu.reset_index(drop=True, inplace=True)

    
    liste_col_transfo_attachements = ['Noms des fichiers','Tailles des fichiers']
    for x, col in enumerate(liste_col_transfo_attachements):
        df_attachements_visu[col] = df_attachements_visu[col].apply(transfo)

    count_fichiers_selected_df = df_attachements_visu['Noms des fichiers'].apply(len).sum()
    count_tailles_fichiers_selected_df = df_attachements_visu['Tailles des fichiers'].apply(sum).sum()

    col1,col2 = st.columns(2)
    with col1:
        st.metric(label="Nombre de fichiers attachés", value=count_fichiers_selected_df)
    with col2:
        st.metric(label="Taille cumulée de fichiers attachés (Octets)", value=count_tailles_fichiers_selected_df)

    
    Visu_attachements = f"Fiche en cours"
    s_Visu_attachements  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_attachements}</p>"
    st.markdown(s_Visu_attachements ,unsafe_allow_html=True)

    df_attachements_visu_i = df_attachements_visu[df_attachements_visu['Identifiant']==identifieur]
    #st.dataframe(df_attachements_visu_i)
        
    for i in range(len(df_attachements_visu_i['Noms des fichiers'].values[0])):
        with st.container(border=True):
            t0 = f"FICHIER #{i+1}"
            s_t0 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t0}</p>"
            st.markdown(s_t0,unsafe_allow_html=True)
            col1,col2 = st.columns(2)
            with col1:
                t0a = 'Noms'
                s_t0a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0a}</p>"
                st.markdown(s_t0a,unsafe_allow_html=True)
                st.markdown(df_attachements_visu_i['Noms des fichiers'].values[0][i])
            with col2:
                t0b = 'Tailles'
                s_t0b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0b}</p>"
                st.markdown(s_t0b,unsafe_allow_html=True)
                st.markdown(df_attachements_visu_i['Tailles des fichiers'].values[0][i])

    if len(df_attachements_visu_i['Noms des fichiers'].values[0])==0 and len(df_attachements_visu_i['Tailles des fichiers'].values[0])==0:
        st.markdown("Il n'y a pas de fichiers attachés")


    #st.dataframe(df_attachements_visu_i)


###############################################################################################################
######################## VISUALISATIONS RESSOURCES ############################################################
###############################################################################################################
elif Ressources_associees:
    df_ressources = pd.read_csv("pages/data/Cat_InDoRES/infos_MD2/Tableau_fichiers_ressources.csv", index_col=[0])

    df_ressources_visu = df_ressources[df_ressources['Identifiant'].isin(selected_uuids_)]
    df_ressources_visu.reset_index(drop=True, inplace=True)

    #st.dataframe(df_ressources_visu)

    df_ressources_visu_checked = df_ressources_visu[(df_ressources_visu['Check_BroAndSisters'] == True) | (df_ressources_visu['Check_children'] == True) | (df_ressources_visu['Check_parent'] == True) | (df_ressources_visu['Check_fcats'] == True)]
    df_ressources_visu_checked.reset_index(drop=True, inplace=True)
    st.dataframe(df_ressources_visu_checked)

    col1, col2 = st.columns([0.6,0.4])
    with col1:
        Sommes_check_selected_df = f"Décomptes sur la sélection en cours / sur {len(df_ressources_visu_checked)} fiches"
        s_Sommes_check_selected_df  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Sommes_check_selected_df}</p>"
        st.markdown(s_Sommes_check_selected_df ,unsafe_allow_html=True)
    with col2:
        visu_ressources_selected = st.checkbox(label= "Voir les ressources des fiches sélectionnées")

    sum_children = df_ressources_visu['Nombre_children'].sum()
    sum_parent = df_ressources_visu['Nombre_parent'].sum()
    sum_hassources = df_ressources_visu['Nombre_hassources'].sum()
    sum_associated = df_ressources_visu['Nombre_associated'].sum()
    sum_hasfeaturescats = df_ressources_visu['Nombre_hasfeaturescats'].sum()
    sum_fcats = df_ressources_visu['Nombre_fcats'].sum()
    sum_services = df_ressources_visu['Nombre_services'].sum()
    sum_BroAndSisters = df_ressources_visu['Nombre_BroAndSisters'].sum()

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric(label='Brothers And Sisters', value=sum_BroAndSisters)
    with col2:
        st.metric(label='Childrens', value=sum_children)
    with col3:
        st.metric(label='Parents', value=sum_parent)
    with col4:
        st.metric(label="Catalogue d'attributs", value=sum_fcats)

    if visu_ressources_selected:
        pass
    else:

        Visu_ressources = f"Fiche en cours"
        s_Visu_ressources  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_ressources}</p>"
        st.markdown(s_Visu_ressources ,unsafe_allow_html=True)


        df_ressources_visu_i = df_ressources[df_ressources['Identifiant']==identifieur]
        #st.dataframe(df_ressources_visu_i)
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            if len(df_ressources_visu_i)==0:
                st.metric(label='Brothers And Sisters', value=0)
            else:
                st.metric(label='Brothers And Sisters', value=df_ressources_visu_i['Nombre_BroAndSisters'])
        with col2:
            if len(df_ressources_visu_i['Nombre_children'])==0:
                st.metric(label='Childrens', value=0)
            else:
                st.metric(label='Childrens', value=df_ressources_visu_i['Nombre_children'])
        with col3:
            if len(df_ressources_visu_i['Nombre_parent'])==0:
                st.metric(label='Parents', value=0)
            else:
                st.metric(label='Parents', value=df_ressources_visu_i['Nombre_parent'])
        with col4:
            if len(df_ressources_visu_i['Nombre_fcats'])==0:
                st.metric(label="Catalogue d'attributs", value=0)
            else:
                st.metric(label="Catalogue d'attributs", value=df_ressources_visu_i['Nombre_fcats'])

        
        liste_col_transfo_ressources = ['facts url (properties)','Titre facts',
                                            'Children url (properties)','Titre children','Résumé children','Formats children','Urls children',
                                            'Parent url (properties)','Titre parents','Résumé parents','Formats parents','Urls parents',
                                            'brothersAndSisters url (properties)','Titre brothersAndSisters','Résumé brothersAndSisters','Formats brothersAndSisters','Urls brothersAndSisters']
        for x, col in enumerate(liste_col_transfo_ressources):
            df_ressources_visu_i[col] = df_ressources_visu_i[col].apply(transfo)
            
        #st.dataframe(df_ressources_visu_i)
        if len(df_ressources_visu_i)!=0:
                
            if df_ressources_visu_i['Check_BroAndSisters'].values:
                for i in range(len(df_ressources_visu_i['Titre brothersAndSisters'].values[0])):
                    with st.container(border=True):
                        t1 = f"BROTHERS & SISTERS - #{i+1}"
                        s_t1 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t1}</p>"
                        st.markdown(s_t1,unsafe_allow_html=True)
                        col1,col2,col3 =st.columns([0.5,0.3,0.2])
                        with col1:
                            t1a = 'Titre'
                            s_t1a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t1a}</p>"
                            st.markdown(s_t1a,unsafe_allow_html=True)
                            try:
                                st.write(df_ressources_visu_i['Titre brothersAndSisters'].values[0][i])
                            except:
                                pass
                        with col2:
                            t1b = 'Urls'
                            s_t1b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t1b}</p>"
                            st.markdown(s_t1b,unsafe_allow_html=True)
                            try:
                                for j in range(len(df_ressources_visu_i['Urls brothersAndSisters'].values[0][i])):
                                    st.write(df_ressources_visu_i['Urls brothersAndSisters'].values[0][i][j])
                            except:
                                pass
                        with col3:
                            t1c = 'Format'
                            s_t1c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t1c}</p>"
                            st.markdown(s_t1c,unsafe_allow_html=True)
                            try:
                                st.write(df_ressources_visu_i['Formats brothersAndSisters'].values[0][i])
                            except:
                                pass
                    
                        col1,col2 =st.columns(2)
                        with col1:
                            t1d = 'Résumé'
                            s_t1d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t1d}</p>"
                            st.markdown(s_t1d,unsafe_allow_html=True)
                            try:
                                st.markdown(df_ressources_visu_i['Résumé brothersAndSisters'].values[0][i])
                            except:
                                pass
                        with col2:
                            t1e = 'Autres Urls'
                            s_t1e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t1e}</p>"
                            st.markdown(s_t1e,unsafe_allow_html=True)
                            try:
                                st.markdown(df_ressources_visu_i['brothersAndSisters url (properties)'].values[0][i])
                            except:
                                pass

                
            if df_ressources_visu_i['Check_children'].values:
                for i in range(len(df_ressources_visu_i['Titre children'].values[0])):
                    with st.container(border=True):
                        t2 = f"CHILDREN - #{i+1}"
                        s_t2 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t2}</p>"
                        st.markdown(s_t2,unsafe_allow_html=True)
                        col1,col2,col3 =st.columns([0.5,0.3,0.2])
                        with col1:
                            t2a = 'Titre'
                            s_t2a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t2a}</p>"
                            st.markdown(s_t2a,unsafe_allow_html=True)
                            try:
                                st.markdown(df_ressources_visu_i['Titre children'].values[0][i])
                            except:
                                pass
                        with col2:
                            t2d = 'Urls'
                            s_t2d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t2d}</p>"
                            st.markdown(s_t2d,unsafe_allow_html=True)
                            try:
                                st.markdown(df_ressources_visu_i['Urls children'].values[0][i])
                            except:
                                pass
                        with col3:
                            t2c = 'Format'
                            s_t2c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t2c}</p>"
                            st.markdown(s_t2c,unsafe_allow_html=True)
                            try:
                                st.markdown(df_ressources_visu_i['Formats children'].values[0][i])
                            except:
                                pass

                        col1,col2 =st.columns(2)
                        with col1:
                            t2d = 'Résumé'
                            s_t2d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t2d}</p>"
                            st.markdown(s_t2d,unsafe_allow_html=True)
                            try:
                                st.markdown(df_ressources_visu_i['Résumé children'].values[0][i])
                            except:
                                pass
                        with col2:
                            t2e = 'Autres Urls'
                            s_t2e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t2e}</p>"
                            st.markdown(s_t2e,unsafe_allow_html=True)
                            try:
                                st.markdown(df_ressources_visu_i['Children url (properties)'].values[0][i])
                            except:
                                pass

            if df_ressources_visu_i['Check_parent'].values:
                for i in range(len(df_ressources_visu_i['Titre parents'].values[0])):
                    with st.container(border=True):
                        t3 = f"PARENT - #{i+1}"
                        s_t3 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t3}</p>"
                        st.markdown(s_t3,unsafe_allow_html=True)
                        col1,col2,col3 =st.columns([0.5,0.3,0.2])
                        with col1:
                            t3a = 'Titre'
                            s_t3a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t3a}</p>"
                            st.markdown(s_t3a,unsafe_allow_html=True)
                            st.markdown(df_ressources_visu_i['Titre parents'].values[0][i])
                        with col2:
                            t3b = 'Urls'
                            s_t3b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t3b}</p>"
                            st.markdown(s_t3b,unsafe_allow_html=True)
                            try:
                                for j in range(len(df_ressources_visu_i['Urls parents'].values[0][i])):
                                    st.markdown(df_ressources_visu_i['Urls parents'].values[0][i][j])
                            except:
                                pass
                        with col3:
                            t3c = 'Format'
                            s_t3c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t3c}</p>"
                            st.markdown(s_t3c,unsafe_allow_html=True)
                            try:
                                st.markdown(df_ressources_visu_i['Formats parents'].values[0][i])
                            except:
                                pass
                            
                        col1,col2 =st.columns(2)
                        with col1:
                            t3d = 'Résumé'
                            s_t3d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t3d}</p>"
                            st.markdown(s_t3d,unsafe_allow_html=True)
                            try:
                                st.markdown(df_ressources_visu_i['Résumé parents'].values[0][i])
                            except:
                                pass
                        with col2:
                            t3e = 'Autres Urls'
                            s_t3e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t3e}</p>"
                            st.markdown(s_t3e,unsafe_allow_html=True)
                            try:
                                st.markdown(df_ressources_visu_i['Parent url (properties)'].values[0][i])
                            except:
                                pass


                if df_ressources_visu_i['Check_fcats'].values:
                    for i in range(len(df_ressources_visu_i['Titre facts'].values[0])):
                        with st.container(border=True):
                            t4 = f"CATALOGUE D'ATTRIBUTS - #{i+1}"
                            s_t4 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t4}</p>"
                            st.markdown(s_t4,unsafe_allow_html=True)
                            col1, col2 = st.columns(2)
                            with col1:
                                t4a = 'Titre'
                                s_t4a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t4a}</p>"
                                st.markdown(s_t4a,unsafe_allow_html=True)
                                try:
                                    st.markdown(df_ressources_visu_i['Titre facts'].values[0][i])
                                except:
                                    pass
                            with col2:
                                t4b = 'Urls'
                                s_t4b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t4b}</p>"
                                st.markdown(s_t4b,unsafe_allow_html=True)
                                for i in range(len(df_ressources_visu_i['facts url (properties)'].values[0])):
                                    st.markdown(df_ressources_visu_i['facts url (properties)'].values[0][i])
            else:
                st.write("Aucune ressource à visualiser pour cet identifiant")

else:
    with st.container(border=True):
        s4 = "IDENTIFICATION PRINCIPALE"
        s_s4 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s4}</p>"
        st.markdown(s_s4,unsafe_allow_html=True)

        col1,col2 = st.columns(2)
        with col1:
            s4a = 'Titre'
            s_s4a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4a}</p>"
            st.markdown(s_s4a,unsafe_allow_html=True)
            st.markdown(df_complet['Titre'][df_complet['Identifiant']==identifieur].values[0])
        with col2:
            s4a_ = 'Fiche Parent'
            s_s4a_ = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4a_}</p>"
            st.markdown(s_s4a_,unsafe_allow_html=True)
            st.markdown(df_complet['Fiche parent id'][df_complet['Identifiant']==identifieur].values[0])

        s4b = 'Résumé'
        s_s4b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4b}</p>"
        st.markdown(s_s4b,unsafe_allow_html=True)
        st.markdown(df_complet['Résumé'][df_complet['Identifiant']==identifieur].values[0])

        col1,col2,col3 = st.columns(3)
        with col1:
            s4d = 'Purpose'
            s_s4d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4d}</p>"
            st.markdown(s_s4d,unsafe_allow_html=True)
            st.markdown(df_complet['Objectif'][df_complet['Identifiant']==identifieur].values[0])
        with col2:
            s4e = 'Status'
            s_s4e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4e}</p>"
            st.markdown(s_s4e,unsafe_allow_html=True)
            st.markdown(df_complet['Status'][df_complet['Identifiant']==identifieur].values[0])
        with col3:
            s4f = 'Fréquence de maj'
            s_s4f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4f}</p>"
            st.markdown(s_s4f,unsafe_allow_html=True)
            st.markdown(df_complet['Fréquence de maj'][df_complet['Identifiant']==identifieur].values[0])

        col1,col2,col3 =st.columns(3)
        with col1:
            s4c = 'Date (création)'
            s_s4c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4c}</p>"
            st.markdown(s_s4c,unsafe_allow_html=True)
            st.markdown(df_complet['Date de création'][df_complet['Identifiant']==identifieur].values[0])
        with col2:
            try:
                s4g = f"Date ({df_complet['Autres dates'][df_complet['Identifiant']==identifieur].values[0][0][0]})"
                s_s4g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4g}</p>"
                st.markdown(s_s4g,unsafe_allow_html=True)
                st.markdown(df_complet['Autres dates'][df_complet['Identifiant']==identifieur].values[0][0][1])
            except:
                pass
        with col3:
            try:
                s4h = f"Date ({df_complet['Autres dates'][df_complet['Identifiant']==identifieur].values[0][1][0]})"
                s_s4h = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4h}</p>"
                st.markdown(s_s4h,unsafe_allow_html=True)
                st.markdown(df_complet['Autres dates'][df_complet['Identifiant']==identifieur].values[0][1][1])
            except:
                pass
        
        s4i = f'Info Supplémentaire'
        s_s4i = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s4i}</p>"
        st.markdown(s_s4i,unsafe_allow_html=True)
        st.markdown(df_complet['Info supplémentaire'][df_complet['Identifiant']==identifieur].values[0])


    with st.container(border=True):
        s2 = "METADONNEES GENERALES"
        s_s2 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s2}</p>"
        st.markdown(s_s2,unsafe_allow_html=True)

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            s2a = 'Date'
            s_s2a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2a}</p>"
            st.markdown(s_s2a,unsafe_allow_html=True)
            st.markdown(df_complet['Date'][df_complet['Identifiant']==identifieur].values[0])
        with col2:
            s2b = 'Langue'
            s_s2b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2b}</p>"
            st.markdown(s_s2b,unsafe_allow_html=True)
            st.markdown(df_complet['Langue'][df_complet['Identifiant']==identifieur].values[0])
        with col3:
            s2c = 'Jeu de caractères'
            s_s2c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2c}</p>"
            st.markdown(s_s2c,unsafe_allow_html=True)
            st.markdown(df_complet['Jeu de caractères'][df_complet['Identifiant']==identifieur].values[0])
        with col4:
            s2d = 'Type'
            s_s2d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2d}</p>"
            st.markdown(s_s2d,unsafe_allow_html=True)
            st.markdown(df_complet['Type'][df_complet['Identifiant']==identifieur].values[0])

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            s2e = 'Nom du contact'
            s_s2e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2e}</p>"
            st.markdown(s_s2e,unsafe_allow_html=True)
            for x in range(len(df_complet['Nom du contact'][df_complet['Identifiant']==identifieur].values[0])):
                st.markdown(df_complet['Nom du contact'][df_complet['Identifiant']==identifieur].values[0][x])
        with col2:
            s2f = 'Position du contact'
            s_s2f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2f}</p>"
            st.markdown(s_s2f,unsafe_allow_html=True)
            for x in range(len(df_complet['Position du contact'][df_complet['Identifiant']==identifieur].values[0])):
                st.markdown(df_complet['Position du contact'][df_complet['Identifiant']==identifieur].values[0][x])
        with col3:
            s2g = 'Orga du contact'
            s_s2g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2g}</p>"
            st.markdown(s_s2g,unsafe_allow_html=True)
            for x in range(len(df_complet['orga du contact'][df_complet['Identifiant']==identifieur].values[0])):
                st.markdown(df_complet['orga du contact'][df_complet['Identifiant']==identifieur].values[0][x])
        with col4:
            s2h = 'Tel du contact'
            s_s2h = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2h}</p>"
            st.markdown(s_s2h,unsafe_allow_html=True)
            for x in range(len(df_complet['Tel du contact'][df_complet['Identifiant']==identifieur].values[0])):
                st.markdown(df_complet['Tel du contact'][df_complet['Identifiant']==identifieur].values[0][x])

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            s2i = 'Adresse'
            s_s2i = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2i}</p>"
            st.markdown(s_s2i,unsafe_allow_html=True)
            for x in range(len(df_complet['Adresse'][df_complet['Identifiant']==identifieur].values[0])):
                st.markdown(df_complet['Adresse'][df_complet['Identifiant']==identifieur].values[0][x])
        with col2:
            s2j = 'Code Postal'
            s_s2j = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2j}</p>"
            st.markdown(s_s2j,unsafe_allow_html=True)
            for x in range(len(df_complet['Code Postal'][df_complet['Identifiant']==identifieur].values[0])):
                st.markdown(df_complet['Code Postal'][df_complet['Identifiant']==identifieur].values[0][x])
        with col3:
            s2k = 'Ville'
            s_s2k = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2k}</p>"
            st.markdown(s_s2k,unsafe_allow_html=True)
            for x in range(len(df_complet['Ville'][df_complet['Identifiant']==identifieur].values[0])):
                st.markdown(df_complet['Ville'][df_complet['Identifiant']==identifieur].values[0][x])
        with col4:
            s2l = 'Pays'
            s_s2l = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2l}</p>"
            st.markdown(s_s2l,unsafe_allow_html=True)
            for x in range(len(df_complet['Pays'][df_complet['Identifiant']==identifieur].values[0])):
                st.markdown(df_complet['Pays'][df_complet['Identifiant']==identifieur].values[0][x])

        col1,col2,col3 = st.columns([0.25,0.25,0.5])
        with col1:
            s2m = 'Nom du standard'
            s_s2m = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2m}</p>"
            st.markdown(s_s2m,unsafe_allow_html=True)
            st.markdown(df_complet['Nom du standard'][df_complet['Identifiant']==identifieur].values[0])
        with col2:
            s2n = 'Version du standard'
            s_s2n = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2n}</p>"
            st.markdown(s_s2n,unsafe_allow_html=True)
            st.markdown(df_complet['Version du standard'][df_complet['Identifiant']==identifieur].values[0])
        with col3:
            s2o = 'Adresse email du contact'
            s_s2o = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s2o}</p>"
            st.markdown(s_s2o,unsafe_allow_html=True)
            st.markdown(df_complet['Email du contact'][df_complet['Identifiant']==identifieur].values[0])

    with st.container(border=True):
        s3 = "SYSTEME DE REFERENCE & LIMITES GEOGRAPHIQUES"
        s_s3 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s3}</p>"
        st.markdown(s_s3,unsafe_allow_html=True)

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            s3a = 'Systèmes renseignés'
            s_s3a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s3a}</p>"
            st.markdown(s_s3a,unsafe_allow_html=True)
            for x in range(len(df_complet['Systeme de référence'][df_complet['Identifiant']==identifieur].values[0])):
                st.markdown(df_complet['Systeme de référence'][df_complet['Identifiant']==identifieur].values[0][x])
        with col2:
            pass
        with col3:
            pass
        with col4:
            pass

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            s3c = 'Longitude Ouest'
            s_s3c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s3c}</p>"
            st.markdown(s_s3c,unsafe_allow_html=True)
            st.markdown(df_complet['Longitude ouest'][df_complet['Identifiant']==identifieur].values[0])
        with col2:
            s3d = 'Longitude Est'
            s_s3d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s3d}</p>"
            st.markdown(s_s3d,unsafe_allow_html=True)
            st.markdown(df_complet['Longitude est'][df_complet['Identifiant']==identifieur].values[0])
        with col3:
            s3e = 'Latitude Sud'
            s_s3e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s3e}</p>"
            st.markdown(s_s3e,unsafe_allow_html=True)
            st.markdown(df_complet['Latitude sud'][df_complet['Identifiant']==identifieur].values[0])
        with col4:
            s3f = 'Latitude Nord'
            s_s3f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s3f}</p>"
            st.markdown(s_s3f,unsafe_allow_html=True)
            st.markdown(df_complet['Latitude nord'][df_complet['Identifiant']==identifieur].values[0])

    with st.container(border=True):
        theme_thesaurus_motsCles = recup_themes_thesaurus_motsCles(url, identifieur, headers_json)
        s5 = "MOTS CLES"
        s_s5 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s5}</p>"
        st.markdown(s_s5,unsafe_allow_html=True)

        col1,col2,col3 = st.columns(3)
        with col1:
            s5a = f'Thésaurus éventuel'
            s_s5a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s5a}</p>"
            st.markdown(s_s5a,unsafe_allow_html=True)
        with col2:
            s5b = f'Type de mots clés'
            s_s5b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s5b}</p>"
            st.markdown(s_s5b,unsafe_allow_html=True)
        with col3:
            s5c = f'Mots Clés'
            s_s5c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s5c}</p>"
            st.markdown(s_s5c,unsafe_allow_html=True)

        for j in range(len(theme_thesaurus_motsCles)):
            col1,col2,col3 = st.columns(3)
            with col1:
                st.markdown(theme_thesaurus_motsCles[j][2])
            with col2:
                st.markdown(theme_thesaurus_motsCles[j][1])
            with col3:
                for i in range(len(theme_thesaurus_motsCles[j][0])):
                    st.markdown(theme_thesaurus_motsCles[j][0][i])

    with st.container(border=True):
        s6 = "CONTRAINTES"
        s_s6 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s6}</p>"
        st.markdown(s_s6,unsafe_allow_html=True)

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            s6a = "Limite d'Accès"
            s_s6a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s6a}</p>"
            st.markdown(s_s6a,unsafe_allow_html=True)
            st.markdown(df_complet['Contrainte accès'][df_complet['Identifiant']==identifieur].values[0])
        with col2:
            s6b = "Contrainte d'usage"
            s_s6b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s6b}</p>"
            st.markdown(s_s6b,unsafe_allow_html=True)
            st.markdown(df_complet['Contrainte usage'][df_complet['Identifiant']==identifieur].values[0])
        with col3:
            s6c = "Limite d'Usage"
            s_s6c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s6c}</p>"
            st.markdown(s_s6c,unsafe_allow_html=True)
            st.markdown(df_complet['Limite usage'][df_complet['Identifiant']==identifieur].values[0])
        with col4:
            s6d = "Autre contrainte"
            s_s6d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s6d}</p>"
            st.markdown(s_s6d,unsafe_allow_html=True)
            st.markdown(df_complet['Autre contrainte'][df_complet['Identifiant']==identifieur].values[0])

    with st.container(border=True):
        s7 = "DISTRIBUTION"
        s_s7 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s7}</p>"
        st.markdown(s_s7,unsafe_allow_html=True)

        col1,col2 = st.columns([0.7,0.3])
        with col1:
            s7b = "URL"
            s_s7b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7b}</p>"
            st.markdown(s_s7b,unsafe_allow_html=True)
            for x in range(len(df_complet['Url'][df_complet['Identifiant']==identifieur].values[0])):
                st.markdown(df_complet['Url'][df_complet['Identifiant']==identifieur].values[0][x])
        with col2:
            s7c = "Protocole"
            s_s7c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7c}</p>"
            st.markdown(s_s7c,unsafe_allow_html=True)
            for x in range(len(df_complet['Protocole'][df_complet['Identifiant']==identifieur].values[0])):
                st.markdown(df_complet['Protocole'][df_complet['Identifiant']==identifieur].values[0][x])
        
        col1,col2,col3 = st.columns([0.3,0.4,0.3])
        with col1:
            s7d = "Nom de la ressource"
            s_s7d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7d}</p>"
            st.markdown(s_s7d,unsafe_allow_html=True)
            for x in range(len(df_complet['Online nom'][df_complet['Identifiant']==identifieur].values[0])):
                st.markdown(df_complet['Online nom'][df_complet['Identifiant']==identifieur].values[0][x])
        with col2:
            s7e = "Description de la ressource"
            s_s7e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7e}</p>"
            st.markdown(s_s7e,unsafe_allow_html=True)
            for x in range(len(df_complet['Online description'][df_complet['Identifiant']==identifieur].values[0])):
                st.markdown(df_complet['Online description'][df_complet['Identifiant']==identifieur].values[0][x])
        with col3:
            s7a = "Format"
            s_s7a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s7a}</p>"
            st.markdown(s_s7a,unsafe_allow_html=True)
            for x in range(len(df_complet['Format'][df_complet['Identifiant']==identifieur].values[0])):
                st.markdown(df_complet['Format'][df_complet['Identifiant']==identifieur].values[0][x])

    with st.container(border=True):
        s8 = "QUALITE"
        s_s8 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{s8}</p>"
        st.markdown(s_s8,unsafe_allow_html=True)

        col1,col2 = st.columns(2)
        with col1:
            s8a = "Niveau"
            s_s8a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s8a}</p>"
            st.markdown(s_s8a,unsafe_allow_html=True)
            st.markdown(df_complet['Niveau'][df_complet['Identifiant']==identifieur].values[0])

        with col2:
            s8b = "Conformité"
            s_s8b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s8b}</p>"
            st.markdown(s_s8b,unsafe_allow_html=True)
            st.markdown(df_complet['Conformité'][df_complet['Identifiant']==identifieur].values[0])

        col1,col2 = st.columns(2)
        with col1:
            s8c = "Généalogie"
            s_s8c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s8c}</p>"
            st.markdown(s_s8c,unsafe_allow_html=True)
            st.markdown(df_complet['Généalogie'][df_complet['Identifiant']==identifieur].values[0])
        with col2:
            s8d = "Portée"
            s_s8d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{s8d}</p>"
            st.markdown(s_s8d,unsafe_allow_html=True)
            st.markdown(df_complet['Portée'][df_complet['Identifiant']==identifieur].values[0])

##################################################################################################
########## VISUALISATION DU GROUPE ###############################################################

lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'

st.sidebar.markdown('Groupe')

htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                            {wch_colour_box[1]}, 
                                                            {wch_colour_box[2]}, 0.75); 
                                        color: rgb({wch_colour_font[0]}, 
                                                {wch_colour_font[1]}, 
                                                {wch_colour_font[2]}, 0.75); 
                                        font-size: {fontsize}px; 
                                        border-radius: 7px; 
                                        padding-left: 12px; 
                                        padding-top: 10px; 
                                        padding-bottom: 10px; 
                                        line-height:5px;
                                        text-align:center'>
                                        </style><BR><span style='font-size: 25px; 
                                        margin-top: 0;'>{df_complet['Groupe'][df_complet['Identifiant']==identifieur].values[0]}</style></span></p>"""
st.sidebar.markdown(lnk + htmlstr, unsafe_allow_html=True)

lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'

st.sidebar.markdown('Mention')

htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                            {wch_colour_box[1]}, 
                                                            {wch_colour_box[2]}, 0.75); 
                                        color: rgb({wch_colour_font[0]}, 
                                                {wch_colour_font[1]}, 
                                                {wch_colour_font[2]}, 0.75); 
                                        font-size: {fontsize}px; 
                                        border-radius: 7px; 
                                        padding-left: 12px; 
                                        padding-top: 10px; 
                                        padding-bottom: 10px; 
                                        line-height:5px;
                                        text-align:center'>
                                        </style><BR><span style='font-size: 25px; 
                                        margin-top: 0;'>{df_complet['Mention du groupe'][df_complet['Identifiant']==identifieur].values[0]}</style></span></p>"""
st.sidebar.markdown(lnk + htmlstr, unsafe_allow_html=True)