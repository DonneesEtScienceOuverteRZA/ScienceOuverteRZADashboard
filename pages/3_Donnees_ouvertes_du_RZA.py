import streamlit as st
from PIL import Image
import pandas as pd
from pyDataverse.models import Dataset
from pyDataverse.utils import read_file
from pyDataverse.api import NativeApi
import glob
import re
import ast
import datetime
import plotly.express as px
import plotly.graph_objects as go
import requests
from markdownify import markdownify as md
from Recuperation_dataverses import Recup_dataverses, Recup_contenu_dataverse,Recup_contenu, Recup_contenu_sans_check, Recup_contenu_dryad, Recup_contenu_zenodo,Recup_contenu_gbif, Recup_dataverses_rdg, recuperation_zenodo, recuperation_nakala, Recup_contenu_nakala, recuperation_dryad, recuperation_gbif

######################################################################################################################
########### TITRE DE L'ONGLET ########################################################################################
######################################################################################################################
st.set_page_config(
    page_title="Donnees ouvertes du RZA",
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

colors = ['#FEBB5F','#EFE9AE','#CDEAC0','#A0C6A9', '#FEC3A6','#FE938C','#E8BED3','#90B7CF','#7C9ACC','#9281C0','#FEBB5F','#EFE9AE','#CDEAC0','#A0C6A9', '#FEC3A6','#FE938C','#E8BED3','#90B7CF','#7C9ACC','#9281C0']
graph_title_font = 24
graph_xaxis_ticks_font = 15
graph_xaxis_title_font = 20
graph_yaxis_ticks_font = 15
graph_yaxis_title_font = 20
legend_title_font = 15
legend_font =15
graph_title_color = "gray"
graph_ticks_color = 'gray'

######################################################################################################################
########### PARAMETRES  ##############################################################################################
######################################################################################################################

d = datetime.date.today()

######################################################################################################################
######################## INDORES #####################################################################################
BASE_URL_INDORES="https://data.indores.fr"
API_TOKEN_INDORES="19f0769d-564f-44ac-809b-22853f186960"

######################################################################################################################
######################## RDG #########################################################################################
BASE_URL_RDG="https://entrepot.recherche.data.gouv.fr/"
API_TOKEN_RDG="b02fd46a-2fb0-4ac3-8717-ae70ec35185a"

######################################################################################################################
######################## NAKALA ######################################################################################
url_nakala = "https://api.nakala.fr/search"
headers_nakala = {
  'X-API-KEY': 'c3cac1e9-cecc-a05c-bf8e-2459669a1f31',
  'accept': 'application/json'
}

######################################################################################################################
######################## ZENODO ######################################################################################
url_zenodo = 'https://zenodo.org/api/records/'
zenodo_token = "OMMGEVUcApEKSt4JEkSK7OzpqZQPMvGKAlB2yP2MXG6APstRn2hWpiHfpjaA"
headers_zenodo = {"Content-Type": "application/json"}

######################################################################################################################
########################## DRYAD #####################################################################################
url_dryad = "https://datadryad.org/api/v2/search?"

######################################################################################################################
########################## GBIF ######################################################################################
url_gbif = "https://api.gbif.org/v1/dataset?"
headers_gbif = {'accept': 'application/json'}


liste_ZAs_ = ["Zone atelier territoires uranifères",
              " Zone Atelier Seine",
              " Zone atelier Loire",
              " Zone atelier bassin du Rhône",
              " Zone atelier bassin de la Moselle",
              " Zone atelier Alpes",
              " Zone atelier arc jurassien",
              " Zone atelier Armorique",
              " Zone atelier Plaine et Val de Sèvre",
              " Zone atelier environnementale urbaine",
              " Zone atelier Hwange",
              " Zone atelier Pyrénées Garonne",
              " Zone atelier Brest Iroise",
              " Zone Atelier Antarctique et Terres Australes",
              " Zone Atelier Santé Environnement Camargue",
              " Zone Atelier Argonne"]

liste_ZAs_bis = [['Zone atelier territoires uranifères','36'],
              [' Zone Atelier Seine','37'],
              [' Zone atelier Loire','38'],
              [' Zone atelier bassin du Rhône','39'],
              [' Zone atelier bassin de la Moselle','40'],
              [' Zone atelier Alpes','42'],
              [' Zone atelier arc jurassien','43'],
              [' Zone atelier Armorique','44'],
              [' Zone atelier Plaine et Val de Sèvre','45'],
              [' Zone atelier environnementale urbaine','46'],
              [' Zone atelier Hwange','47'],
              [' Zone atelier Pyrénées Garonne','48'],
              [' Zone atelier Brest Iroise','49'],
              [' Zone Atelier Antarctique et Terres Australes','10295'],
              [' Zone Atelier Santé Environnement Camargue','10296'],
              [' Zone Atelier Argonne','10297']]

######################################################################################################################
########### SELECTION ZA #############################################################################################
######################################################################################################################

all_ZAs= st.sidebar.checkbox("Ensemble du réseau ZA")
if all_ZAs==True :
    Selection_ZA = liste_ZAs_
else:
    Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs_)


######################################################################################################################
########### SELECTION ENTREPOT #######################################################################################
######################################################################################################################
Choix_entrepot = st.sidebar.subheader('Entrepôts')
with st.sidebar:
    if 'catalogues' not in st.session_state:
        st.session_state.catalogues = False
    if 'indores' not in st.session_state:
        st.session_state.indores = False
    if 'rdg' not in st.session_state:
        st.session_state.rdg = False
    if 'nakala' not in st.session_state:
        st.session_state.nakala = False
    if 'zenodo' not in st.session_state:
        st.session_state.zenodo = False
    if 'dryad' not in st.session_state:
        st.session_state.dryad = False
    if 'gbif' not in st.session_state:
        st.session_state.gbif = False

    def handle_checkbox0_change():
        if st.session_state.catalogues:
            st.session_state.indores = False
            st.session_state.rdg = False
            st.session_state.nakala = False
            st.session_state.zenodo = False
            st.session_state.nakala = False
            st.session_state.zenodo = False

    def handle_checkbox1_change():
        if st.session_state.indores:
            st.session_state.catalogues = False
            st.session_state.rdg = False
            st.session_state.nakala = False
            st.session_state.zenodo = False
            st.session_state.nakala = False
            st.session_state.zenodo = False

    def handle_checkbox2_change():
        if st.session_state.rdg:
            st.session_state.catalogues = False
            st.session_state.indores = False
            st.session_state.nakala = False
            st.session_state.zenodo = False
            st.session_state.nakala = False
            st.session_state.zenodo = False
            
    def handle_checkbox3_change():
        if st.session_state.nakala:
            st.session_state.catalogues = False
            st.session_state.indores = False
            st.session_state.rdg = False
            st.session_state.zenodo = False
            st.session_state.dryad = False
            st.session_state.gbif = False

    def handle_checkbox4_change():
        if st.session_state.zenodo:
            st.session_state.catalogues = False
            st.session_state.indores = False
            st.session_state.rdg = False
            st.session_state.nakala = False
            st.session_state.dryad = False
            st.session_state.gbif = False
    
    def handle_checkbox5_change():
        if st.session_state.dryad:
            st.session_state.catalogues = False
            st.session_state.indores = False
            st.session_state.rdg = False
            st.session_state.nakala = False
            st.session_state.gbif = False
            st.session_state.zenodo = False
    
    def handle_checkbox6_change():
        if st.session_state.gbif:
            st.session_state.catalogues = False
            st.session_state.indores = False
            st.session_state.rdg = False
            st.session_state.nakala = False
            st.session_state.dryad = False
            st.session_state.zenodo = False

    choix_groupe_OHM = False
    catalogues = st.checkbox("OUTILS ZA (GEONETWORKS)", key='catalogues', on_change=handle_checkbox0_change)
    indores = st.checkbox("INDORES", key='indores', on_change=handle_checkbox1_change)
    rdg = st.checkbox("RGD", key='rdg', on_change=handle_checkbox2_change)
    nakala = st.checkbox("NAKALA", key='nakala', on_change=handle_checkbox3_change)
    zenodo = st.checkbox("ZENODO", key='zenodo', on_change=handle_checkbox4_change)
    dryad = st.checkbox("DRYAD", key='dryad', on_change=handle_checkbox5_change)
    gbif = st.checkbox("GBIF", key='gbif', on_change=handle_checkbox6_change)

######################################################################################################################
########### TITRE GENERAL ############################################################################################
######################################################################################################################
st.title(":grey[Donnees ouvertes du RZA]")

######################################################################################################################
########## CATALOGUE INDORES #########################################################################################
######################################################################################################################
if catalogues:
    ######################  TITRE CATALOGUES  #######################################
    st.title(":grey[Analyse des dépôts dans les geonetworks]")

    st.success("Selectionner une ou plusieurs zones ateliers (ou l'ensemble du réseau) / CASE A COCHER ou LISTE DEROULANTE")

    # tableau complet de Cat.indores
    df_c = pd.read_csv("pages/data/Cat_InDoRES/infos_MD2/Tableau_complet.csv", index_col=[0])
    df_c.reset_index(drop=True, inplace=True)
    df_c_selected =df_c[df_c['GroupeEtMention'].isin(Selection_ZA)]

    def transfo(input_string):
    # Use ast.literal_eval to safely evaluate the string as a Python expression
        return ast.literal_eval(input_string)

    def transfo_bis(input_string):
        # Use ast.literal_eval to safely evaluate the string as a Python expression
        return input_string.replace(",","").replace("[","").replace("]","").replace("'","").replace("?","").replace("None","").replace("undefined","")

    df_c['Url'] = df_c['Url'].apply(transfo_bis)

    # Ajout d'une colonne booléenne pour la présence d'url => objectif : la filtrer
    for i in range(len(df_c)):
        if df_c.loc[i,'Url']!='':
            df_c.loc[i,'Check_url']=True
        else:
            df_c.loc[i,'Check_url']=False

    # Tableau complet des ressoucres
    df_ress = pd.read_csv("pages/data/Cat_InDoRES/infos_MD2/Tableau_fichiers_ressources.csv", index_col=[0])

    # Tableau ressources avec les éléments du tableau complet => attention, qq fiches sortent du traitement
    df_ress_ = pd.merge(df_c, df_ress, on='Identifiant', how='inner')

    df_ress_checked = df_ress_[(df_ress_['Check_url'] == True) | (df_ress_['Check_BroAndSisters'] == True) | (df_ress_['Check_children'] == True) | (df_ress_['Check_parent'] == True) | (df_ress_['Check_fcats'] == True)]
    df_ress_checked.reset_index(drop=True, inplace=True)

    df_ress_visu_checked =df_ress_checked[df_ress_checked['GroupeEtMention'].isin(Selection_ZA)]
    df_ress_visu_checked.reset_index(drop=True, inplace=True)

    df_ress_visu_checked['Children']=df_ress_visu_checked['Children url (properties)']+df_ress_visu_checked['Urls children']
    df_ress_visu_checked['Parent']=df_ress_visu_checked['Parent url (properties)']+df_ress_visu_checked['Urls brothersAndSisters']
    df_ress_visu_checked['BroAndSisters']=df_ress_visu_checked['brothersAndSisters url (properties)']+df_ress_visu_checked['Urls parents']
    df_ress_visu_checked['Fcats']=df_ress_visu_checked['hasfeaturecats url (properties)']+df_ress_visu_checked['Urls hasfeaturecats']+df_ress_visu_checked['facts url (properties)']

    

    sum_children = df_ress_visu_checked['Nombre_children'].sum()
    sum_parent = df_ress_visu_checked['Nombre_parent'].sum()
    sum_hassources = df_ress_visu_checked['Nombre_hassources'].sum()
    sum_associated = df_ress_visu_checked['Nombre_associated'].sum()
    sum_hasfeaturescats = df_ress_visu_checked['Nombre_hasfeaturescats'].sum()
    sum_fcats = df_ress_visu_checked['Nombre_fcats'].sum()
    sum_services = df_ress_visu_checked['Nombre_services'].sum()
    sum_BroAndSisters = df_ress_visu_checked['Nombre_BroAndSisters'].sum()

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric(label='Brothers And Sisters', value=sum_BroAndSisters)
    with col2:
        st.metric(label='Childrens', value=sum_children)
    with col3:
        st.metric(label='Parents', value=sum_parent)
    with col4:
        st.metric(label="Catalogue d'attributs", value=sum_fcats)

    def split_http(input_string):
        split_urls = []
        i = 0

        while i < len(input_string):
            # Look for the start of the next 'http' or 'https'
            if input_string[i:i+4] == "http":
                # Look for the next 'http' or end of string to get the whole URL
                next_http = input_string.find("http", i + 4)
                if next_http == -1:
                    # If no more 'http' is found, grab the rest of the string
                    split_urls.append(input_string[i:])
                    break
                else:
                    # Append the current URL and move to the next
                    split_urls.append(input_string[i:next_http])
                    i = next_http
            else:
                i += 1

        # Print the list of URLs
        return split_urls
    
    liste_col_transfo = ['Nom du contact','orga du contact']
    for x, col in enumerate(liste_col_transfo):
        df_ress_visu_checked[col] = df_ress_visu_checked[col].apply(transfo)
    liste_col_transfo_bis = ['Children','Parent','Fcats', 'BroAndSisters']
    for x, col in enumerate(liste_col_transfo_bis):
        df_ress_visu_checked[col] = df_ress_visu_checked[col].apply(transfo_bis)

    columns_to_visualize = ['Identifiant','GroupeEtMention','Titre', 'Date','Nom du contact','orga du contact','Url','Children','Parent','Fcats', 'BroAndSisters']
    df_ress_visu_checked_ = df_ress_visu_checked[columns_to_visualize]
    df_ress_visu_checked__ = df_ress_visu_checked_.copy()
    df_ress_visu_checked__['Url'] = df_ress_visu_checked__['Url'].apply(split_http)
    df_ress_visu_checked__['Parent'] = df_ress_visu_checked__['Parent'].apply(split_http)
    df_ress_visu_checked__['Children'] = df_ress_visu_checked__['Children'].apply(split_http)
    df_ress_visu_checked__['BroAndSisters'] = df_ress_visu_checked__['BroAndSisters'].apply(split_http)
    df_ress_visu_checked__['Fcats'] = df_ress_visu_checked__['Fcats'].apply(split_http)

    if len(Selection_ZA)==1:
        col1, col2, col3 = st.columns([0.5,0.2,0.3])
        with col1:
            Sommes_check_selected_df = f"Décomptes sur {Selection_ZA[0]} / {len(df_c_selected)} fiches"
            s_Sommes_check_selected_df  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Sommes_check_selected_df}</p>"
            st.markdown(s_Sommes_check_selected_df ,unsafe_allow_html=True)
        with col2:
            st.metric(label="Nombre de fiches avec une url", value=len(df_ress_visu_checked_))
        with col3:
            datacatalogue_to_get = df_ress_visu_checked_.to_csv(index=False)
            st.download_button(
                label="Téléchargement des données sélectionnées en CSV",
                data=datacatalogue_to_get,
                file_name=f'cat_InDoRES_{Selection_ZA[0]}_{d}.csv',
                mime='text/csv')
    elif len(Selection_ZA)==16:
        col1, col2, col3 = st.columns([0.5,0.2,0.3])
        with col1:
            Sommes_check_selected_df = f"Décomptes sur l'ensemble du réseau / {len(df_c_selected)} fiches"
            s_Sommes_check_selected_df  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Sommes_check_selected_df}</p>"
            st.markdown(s_Sommes_check_selected_df ,unsafe_allow_html=True)
        with col2:
            st.metric(label="Nombre de fiches avec une url", value=len(df_ress_visu_checked_))
        with col3:
            datacatalogue_to_get = df_ress_visu_checked_.to_csv(index=False)
            st.download_button(
                label="Téléchargement des données sélectionnées en CSV",
                data=datacatalogue_to_get,
                file_name=f'cat_InDoRES_AllZAs_{d}.csv',
                mime='text/csv')

    with st.container(border=True):
        for i in range(len(df_ress_visu_checked_)):
            t0 = f"FICHIER #{i+1}"
            s_t0 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t0}</p>"
            st.markdown(s_t0,unsafe_allow_html=True)
            col1,col2 = st.columns(2)
            with col1:
                t0a = 'Titre'
                s_t0a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0a}</p>"
                st.markdown(s_t0a,unsafe_allow_html=True)
                st.markdown(df_ress_visu_checked_.loc[i,'Titre'])
                t0c = 'Date'
                s_t0c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0c}</p>"
                st.markdown(s_t0c,unsafe_allow_html=True)
                st.markdown(df_ress_visu_checked_.loc[i,'Date'])
                t0d = 'Nom du contact'
                s_t0d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0d}</p>"
                st.markdown(s_t0d,unsafe_allow_html=True)
                try:
                    st.markdown(df_ress_visu_checked_.loc[i,'Nom du contact'][0])
                except:
                    pass
                t0h = 'Organisation du contact'
                s_t0h = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0h}</p>"
                st.markdown(s_t0h,unsafe_allow_html=True)
                try:
                    st.markdown(df_ress_visu_checked_.loc[i,'orga du contact'][0])
                except:
                    pass
            with col2:
                if 'http' in df_ress_visu_checked_.loc[i,'Url']:
                    url1_seperated = split_http(df_ress_visu_checked_.loc[i,'Url'])
                    t0e = 'Lien URL'
                    s_t0e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0e}</p>"
                    st.markdown(s_t0e,unsafe_allow_html=True)
                    for j in range(len(url1_seperated)):
                        st.markdown(url1_seperated[j])
                else:
                    url1_seperated = df_ress_visu_checked_.loc[i,'Url']
                    t0e = 'Lien URL'
                    s_t0e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0e}</p>"
                    st.markdown(s_t0e,unsafe_allow_html=True)
                    st.markdown(url1_seperated)

                if 'http' in df_ress_visu_checked_.loc[i,'Parent']:
                    url_parent_seperated = split_http(df_ress_visu_checked_.loc[i,'Parent'])
                    t0f = 'URL Parent'
                    s_t0f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0f}</p>"
                    st.markdown(s_t0f,unsafe_allow_html=True)
                    for k in range(len(url_parent_seperated)):
                        st.markdown(url_parent_seperated[k])
                else:
                    url_parent_seperated = df_ress_visu_checked_.loc[i,'Parent']
                    t0f = 'URL Parent'
                    s_t0f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0f}</p>"
                    st.markdown(s_t0f,unsafe_allow_html=True)
                    st.markdown(df_ress_visu_checked_.loc[i,'Parent'])

                if 'http' in df_ress_visu_checked_.loc[i,'Children']:
                    url_children_seperated = split_http(df_ress_visu_checked_.loc[i,'Children'])
                    t0g = 'URL Children'
                    s_t0g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0g}</p>"
                    st.markdown(s_t0g,unsafe_allow_html=True)
                    for l in range(len(url_children_seperated)):
                        st.markdown(url_children_seperated[l])
                else:
                    url_children_seperated = df_ress_visu_checked_.loc[i,'Children']
                    t0g = 'URL Children'
                    s_t0g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0g}</p>"
                    st.markdown(s_t0g,unsafe_allow_html=True)
                    st.markdown(url_children_seperated)

                url_broAndSisters_seperated = split_http(df_ress_visu_checked_.loc[i,'BroAndSisters'])
                t0i = 'URL Brothers And Sisters'
                s_t0i = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0i}</p>"
                st.markdown(s_t0i,unsafe_allow_html=True)
                for m in range(len(url_broAndSisters_seperated)):
                    st.markdown(url_broAndSisters_seperated[m])

                url_fcats_seperated = split_http(df_ress_visu_checked_.loc[i,'Fcats'])
                t0i = 'URL Attributs'
                s_t0i = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0i}</p>"
                st.markdown(s_t0i,unsafe_allow_html=True)
                for n in range(len(url_fcats_seperated)):
                    st.markdown(url_fcats_seperated[n])
    

    ##########################################################################################
    ########### POUR L'ADMINISTRATEUR ########################################################
    ##########################################################################################

    # Mot de passe pour faire des récupérations automatisées
    admin_pass = 'admin'
    admin_action = st.sidebar.text_input(label="Pour l'administrateur")


    if admin_action == admin_pass:
        # RECUPERATION DES CONTENUS VIA BOUTON ##############################################       
        Recup_globale = st.sidebar.button('recupération des contenus')
        if Recup_globale:
            with st.spinner("La récup globale est en cours"):
                df_ress_visu_checked__.to_csv("pages/data/Cat_InDoRES/Contenu_CatInDoRES_checked.csv")

######################################################################################################################
############ DATA INDORES ############################################################################################
######################################################################################################################
if indores:
    ######################  TITRE INDORES  ##########################################
    st.title(":grey[Analyse des dépôts dans Data.InDoRes]")

    st.success("Selectionner une ou plusieurs zones ateliers (ou l'ensemble du réseau) / CASE A COCHER ou LISTE DEROULANTE")

    #adresse_dataInDoRes = 'https://data.indores.fr/dataverse/dataindores'
    #s_adresse_dataInDoRes = f"<p style='font-size:25px;color:rgb(150,150,150)'>{adresse_dataInDoRes}</p>"
    #st.markdown(s_adresse_dataInDoRes ,unsafe_allow_html=True)

    fichier = f'tableau_dataverses-{d}.csv'

    fi = glob.glob(f"pages/data/Data_InDoRES/tableau_dataverses*.csv")

    visu_sunburst= st.checkbox("Voir l'ensemble des entrepôts existants")

    ##########################################################################################
    ########### VISUALISATIONS ###############################################################
    ##########################################################################################

    df_complet = pd.read_csv("pages/data/Data_InDoRES/Contenu_DataInDoRES2.csv",index_col=[0])

    if all_ZAs:
        with st.container(border=True):
            Nombre_depots = df_complet['Entrepot'].value_counts()
            for i in range(len(liste_ZAs_)):
                if liste_ZAs_[i] in Nombre_depots.index.values:
                    pass
                else:
                    Nombre_depots[liste_ZAs_[i]]=0
            df = pd.DataFrame(Nombre_depots.values,index=Nombre_depots.index.values,columns=['Nombre_dépôts'])
            fig0= go.Figure()
            for i, za in enumerate(df.index.values):
                selec = df.index.values[i:i+1]
                selec_len = df['Nombre_dépôts'].values[i:i+1]
                fig0.add_trace(go.Bar(
                                y=selec,
                                x=selec_len,
                                name=za,
                                orientation = 'h',
                                marker=dict(color=colors[i])
                            ))
            fig0.update_layout(
                                title=dict(
                                        text=f'Nombre de dépôts répertoriées sur Data.InDoRES',
                                        font=dict(size=graph_title_font, family='Arial', color=graph_title_color)
                                        ),
                                yaxis=dict(
                                        tickfont=dict(size=graph_yaxis_ticks_font, family='Arial', color=graph_ticks_color)   
                                        ),
                                        xaxis=dict(
                                            tickfont=dict(size=graph_xaxis_ticks_font, family='Arial', color=graph_ticks_color)   
                                        ),
                                        width=1000,
                                        height=600,
                                        showlegend=False)
            st.plotly_chart(fig0,use_container_width=True)

    if len(Selection_ZA)!=0:
        df_visu = df_complet[df_complet['Entrepot'].isin(Selection_ZA)]
        df_visu.reset_index(inplace=True)
        df_visu.drop(columns='index', inplace=True)
        #st.dataframe(df_visu)

        if len(Selection_ZA)==1:
            col1,col2,col3 = st.columns([0.5,0.2,0.3])
            with col1:
                Visu_depots = f"Données publiées dans la {Selection_ZA[0]}"
                s_Visu_depots  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots}</p>"
                st.markdown(s_Visu_depots ,unsafe_allow_html=True)
            with col2:
                st.metric(label="Nombre de dépôts décomptés", value=len(df_visu))
            with col3:
                dataInDoRES_to_get = df_visu.to_csv(index=False)
                st.download_button(
                        label="Téléchargement des données sélectionnées en CSV",
                        data=dataInDoRES_to_get,
                        file_name=f'data_InDoRES_{Selection_ZA[0]}_{d}.csv',
                        mime='text/csv')
        elif 1<len(Selection_ZA)<16:
            selection_name = ""
            for i in range(len(Selection_ZA)):
                selection_name+=Selection_ZA[i].strip().replace("Zone atelier", "ZA ").replace(" ","")
            col1,col2,col3 = st.columns([0.5,0.2,0.3])
            with col1:
                Visu_depots = f"Données publiées dans les ZA suivantes: {Selection_ZA}"
                s_Visu_depots  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots}</p>"
                st.markdown(s_Visu_depots ,unsafe_allow_html=True)
            with col2:
                st.metric(label="Nombre de dépôts décomptés", value=len(df_visu))
            with col3:
                dataInDoRES_to_get = df_visu.to_csv(index=False)
                st.download_button(
                        label="Téléchargement des données sélectionnées en CSV",
                        data=dataInDoRES_to_get,
                        file_name=f'data_InDoRES_{selection_name}_{d}.csv',
                        mime='text/csv')
        elif len(Selection_ZA)==16:
            selection_name = "All_ZAs"
            col1,col2,col3 = st.columns([0.5,0.2,0.3])
            with col1:
                Visu_depots = f"Données publiées dans l'ensemble du réseau des Zones Ateliers"
                s_Visu_depots  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots}</p>"
                st.markdown(s_Visu_depots ,unsafe_allow_html=True)
            with col2:
                st.metric(label="Nombre de dépôts décomptés", value=len(df_visu))
            with col3:
                dataInDoRES_to_get = df_visu.to_csv(index=False)
                st.download_button(
                        label="Téléchargement des données sélectionnées en CSV",
                        data=dataInDoRES_to_get,
                        file_name=f'data_InDoRES_{selection_name}_{d}.csv',
                        mime='text/csv')
        
        if len(df_visu)!=0:
                for i in range(len(df_visu)):
                    with st.container(border=True):
                        t0 = f"FICHIER #{i+1}"
                        s_t0 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t0}</p>"
                        st.markdown(s_t0,unsafe_allow_html=True)
                        col1,col2, col3 = st.columns([0.6,0.2,0.2])
                        with col1:
                            t0a = 'Titre'
                            s_t0a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0a}</p>"
                            st.markdown(s_t0a,unsafe_allow_html=True)
                            st.markdown(df_visu.loc[i,'Titre'])
                        with col2:
                            t0b = 'Thème'
                            s_t0b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0b}</p>"
                            st.markdown(s_t0b,unsafe_allow_html=True)
                            st.markdown(df_visu.loc[i,'Thème'])
                        with col3:
                            t0c = 'Date'
                            s_t0c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0c}</p>"
                            st.markdown(s_t0c,unsafe_allow_html=True)
                            st.markdown(df_visu.loc[i,'Date de publication'])
                        col1,col2, col3 = st.columns([0.6,0.2,0.2])
                        with col1:
                            t0d = 'Résumé'
                            s_t0d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0d}</p>"
                            st.markdown(s_t0d,unsafe_allow_html=True)
                            st.markdown(df_visu.loc[i,'Résumé'])
                        with col2:
                            t0e = 'Publication URL'
                            s_t0e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0e}</p>"
                            st.markdown(s_t0e,unsafe_allow_html=True)
                            st.markdown(df_visu.loc[i,'Publication URL'])
                        with col3:
                            t0f = 'DOI'
                            s_t0f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0f}</p>"
                            st.markdown(s_t0f,unsafe_allow_html=True)
                            st.markdown(df_visu.loc[i,'Url'])
                        col1,col2, col3 = st.columns([0.6,0.2,0.2])
                        with col1:
                            t0g = 'Auteur'
                            s_t0g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0g}</p>"
                            st.markdown(s_t0g,unsafe_allow_html=True)
                            st.markdown(df_visu.loc[i,'Auteur'])
                        with col2:
                            t0h = 'Organisation'
                            s_t0h = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0h}</p>"
                            st.markdown(s_t0h,unsafe_allow_html=True)
                            st.markdown(df_visu.loc[i,'Organisation'])
                        with col3:
                            t0i = 'Email'
                            s_t0i = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0i}</p>"
                            st.markdown(s_t0i,unsafe_allow_html=True)
                            st.markdown(df_visu.loc[i,'Email'])

    ##########################################################################################
    ########### VISUALISATION SUNBURST #######################################################
    ##########################################################################################

    if len(fi)!=0:
        fich = fi[-1]
        dataverses = pd.read_csv(fich)
        if visu_sunburst:
            fig = px.sunburst(dataverses, path=['niv0','niv1', 'niv2','niv3'], values='val')
            fig.update_layout(
                title=f'Visuel des différents Dataverses dans Data.InDoRes via {fich}',
                width=1000,
                height=1000)
            st.plotly_chart(fig,use_container_width=True)
    else:
        st.write('Il est nécessaire de mettre à jour vos entrepôts')

    ###################### CREATION CONNEXION #######################################

    def connect_to_dataverse(BASE_URL, API_TOKEN):
        try:
            # Create a new API connection
            api = NativeApi(BASE_URL, API_TOKEN)
            resp = api.get_info_version()
            response = resp.json()
            
            # Check connection success
            if response['status']=='OK':
                st.session_state['dataverse_api'] = api
                st.success("Connexion établie avec Data. InDoRES")
            else:
                st.error("Connexion échouée!")
        except Exception as e:
            st.error(f"Connection error: {e}")
        return api
    
    ###################### Indices des dataverses ###################################

    def find_indices(lst, elements):
        indices = []
        for element in elements:
            try:
                indices.append(lst.index(element))
            except ValueError:
                pass  # Element not found in the list
        return indices

    
    ##########################################################################################
    ########### POUR L'ADMINISTRATEUR ########################################################
    ##########################################################################################

    # Mot de passe pour faire des récupérations automatisées
    admin_pass = 'admin'
    admin_action = st.sidebar.text_input(label="Pour l'administrateur")


    if admin_action == admin_pass:

        # MAJ DES ENTREPOTS EXISTANTS #######################################################
        b1 = st.sidebar.button(label=" Mise à jour des entrepôts Dataverses dans Data.InDoRes ")

        if b1==True:
            with st.spinner("Récupération des entrepôts existants"):
                api = connect_to_dataverse(BASE_URL_INDORES,  API_TOKEN_INDORES)
                Recup_dataverses(api,fichier)


        # RECUPERATION DES CONTENUS VIA BOUTON ##############################################       
        Recup_globale = st.sidebar.button('recupération des contenus')
        if Recup_globale:
            ids = find_indices(liste_ZAs_, Selection_ZA)
            with st.spinner("La récup globale est en cours"):
                api = connect_to_dataverse(BASE_URL_INDORES,  API_TOKEN_INDORES)
                liste_columns_df_entrepot=['selection','Entrepot','Store','ID','Url','Date de publication','Titre','Auteur','Organisation',"Email",'Résumé','Thème','Publication URL']
                df_entrepot = pd.DataFrame(columns=liste_columns_df_entrepot)
                for i, za in enumerate(Selection_ZA):
                    s = int(liste_ZAs_bis[ids[i]][1])
                    print(s)
                    df = Recup_contenu_sans_check(api, s, "Data.Indores", za)
                    dfi = pd.concat([df_entrepot,df], axis=0)
                    dfi.reset_index(inplace=True)
                    dfi.drop(columns='index', inplace=True)
                    df_entrepot = dfi
                df_entrepot.to_csv("pages/data/Data_InDoRES/Contenu_DataInDoRES2.csv")

######################################################################################################################
#################### RECHERCHE DATA GOUV #############################################################################
######################################################################################################################
if rdg:

    ######################  TITRES  #######################################
    st.title(":grey[Analyse des dépôts dans Recherche Data Gouv]")

    #adresse_RDG = 'https://entrepot.recherche.data.gouv.fr/dataverse/root?q='
    #s_adresse_RDG = f"<p style='font-size:25px;color:rgb(150,150,150)'>{adresse_RDG}</p>"
    #st.markdown(s_adresse_RDG ,unsafe_allow_html=True)

    ######################  PARAMETRES  ###################################

    fichier = f'tableau_dataverses_rdg-{d}.csv'

    fi = glob.glob(f"pages/data/rechercheDataGouv/tableau_dataverses*.csv")

    if len(fi)!=0:
        fich = fi[-1]
        dataverses = pd.read_csv(fich,index_col=[0])
    else:
        st.write('Il est nécessaire de mettre à jour vos entrepôts')


    ###################### CREATION CONNEXION #############################
    def connect_to_dataverse(BASE_URL, API_TOKEN):
        try:
            # Create a new API connection
            api = NativeApi(BASE_URL, API_TOKEN)
            resp = api.get_info_version()
            response = resp.json()
                
            # Check connection success
            if response['status']=='OK':
                st.session_state['rdg_api'] = api
                st.success("Connexion établie avec Recherche Data Gouv")
            else:
                st.error("Connexion échouée!")
        except Exception as e:
            st.error(f"Connection error: {e}")
        return api

    ##########################################################################################
    ########### VISUALISATION TABLEAU OU SUNBURST ############################################
    ##########################################################################################

    if 'tab' not in st.session_state:
        st.session_state.tab = False
    if 'sun' not in st.session_state:
        st.session_state.sun = False

    def handle_tab_change():
        if st.session_state.tab:
            st.session_state.sun = False
            

    def handle_sunburst_change():
        if st.session_state.sun:
            st.session_state.tab = False

    st.success("Selectionner une ou plusieurs zones ateliers (ou l'ensemble du réseau) / CASE A COCHER ou LISTE DEROULANTE")
    st.success("Vous pouvez aussi voir le contenu d'un entrepôt de votre en choix / COCHER LA CASE CI-DESSOUS A GAUCHE")

    col1,col2 = st.columns(2)
    with col1:
        tab = st.checkbox("Visualiser le contenu entier d'un entrepôt (non filtré)", key='tab', on_change=handle_tab_change)
    with col2:
        sun = st.checkbox("Voir l'ensemble des entrepôts existants", key='sun', on_change=handle_sunburst_change)

    if tab:
        if len(Selection_ZA)!=0:
            dataverses['niv1-niv2']=dataverses['niv1']+' / '+dataverses['niv2']
            Selected_entrepot = st.selectbox('Choisissez votre entrepôt dans la liste', dataverses['niv1-niv2'].values)
            api_rdg = connect_to_dataverse(BASE_URL_RDG,  API_TOKEN_RDG)
            with st.spinner("Analyse en cours"):
                liste_columns_df_entrepot_rdg_selected=['selection','Entrepot','Dataverse','ID','Url','Date de publication','Titre','Auteur','Organisation',"Email",'Résumé','Thème','Publication URL']
                df_entrepot_rdg_selected = pd.DataFrame(columns=liste_columns_df_entrepot_rdg_selected)
                s = int(dataverses['ids_niv2'][dataverses['niv1-niv2']==Selected_entrepot])
                df = Recup_contenu_sans_check(api_rdg, s, Selected_entrepot, Selection_ZA[0])
                dfi = pd.concat([df_entrepot_rdg_selected,df], axis=0)
                dfi.reset_index(inplace=True)
                dfi.drop(columns='index', inplace=True)
                df_entrepot_rdg_selected = dfi
        else:
            dataverses['niv1-niv2']=dataverses['niv1']+' / '+dataverses['niv2']
            Selected_entrepot = st.selectbox('Choisissez votre entrepôt dans la liste', dataverses['niv1-niv2'].values)
            api_rdg = connect_to_dataverse(BASE_URL_RDG,  API_TOKEN_RDG)
            with st.spinner("Analyse en cours"):
                liste_columns_df_entrepot_rdg_selected=['selection','Entrepot','Dataverse','ID','Url','Date de publication','Titre','Auteur','Organisation',"Email",'Résumé','Thème','Publication URL']
                df_entrepot_rdg_selected = pd.DataFrame(columns=liste_columns_df_entrepot_rdg_selected)
                s = int(dataverses['ids_niv2'][dataverses['niv1-niv2']==Selected_entrepot])
                df = Recup_contenu_sans_check(api_rdg, s, Selected_entrepot, 'Aucun filtre')
                dfi = pd.concat([df_entrepot_rdg_selected,df], axis=0)
                dfi.reset_index(inplace=True)
                dfi.drop(columns='index', inplace=True)
                df_entrepot_rdg_selected = dfi


        if len(df_entrepot_rdg_selected)!=0:
            col1,col2,col3 = st.columns([0.5,0.2,0.3])
            with col1:
                Visu_depots_rdg_selected = f"Données publiées dans {Selected_entrepot}"
                s_Visu_depots_rdg_selected  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots_rdg_selected}</p>"
                st.markdown(s_Visu_depots_rdg_selected ,unsafe_allow_html=True)
            with col2:
                st.metric(label="Nombre de dépôts décomptés", value=len(df_entrepot_rdg_selected))
            with col3:
                dataRDG_selected_to_get = df_entrepot_rdg_selected.to_csv(index=False)
                st.download_button(
                        label="Téléchargement des données sélectionnées en CSV",
                        data=dataRDG_selected_to_get,
                        file_name=f'data_RDG_{Selected_entrepot}_{d}.csv',
                           mime='text/csv')


            for i in range(len(df_entrepot_rdg_selected)):
                with st.container(border=True):
                    t0 = f"FICHIER #{i+1}"
                    s_t0 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t0}</p>"
                    st.markdown(s_t0,unsafe_allow_html=True)
                    col1,col2, col3 = st.columns([0.6,0.2,0.2])
                    with col1:
                        t0a = 'Titre'
                        s_t0a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0a}</p>"
                        st.markdown(s_t0a,unsafe_allow_html=True)
                        st.markdown(df_entrepot_rdg_selected.loc[i,'Titre'])
                    with col2:
                        t0b = 'Thème'
                        s_t0b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0b}</p>"
                        st.markdown(s_t0b,unsafe_allow_html=True)
                        st.markdown(df_entrepot_rdg_selected.loc[i,'Thème'])
                    with col3:
                        t0c = 'Date'
                        s_t0c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0c}</p>"
                        st.markdown(s_t0c,unsafe_allow_html=True)
                        st.markdown(df_entrepot_rdg_selected.loc[i,'Date de publication'])
                    col1,col2, col3 = st.columns([0.6,0.2,0.2])
                    with col1:
                        t0d = 'Résumé'
                        s_t0d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0d}</p>"
                        st.markdown(s_t0d,unsafe_allow_html=True)
                        st.markdown(df_entrepot_rdg_selected.loc[i,'Résumé'])
                    with col2:
                        t0e = 'Publication URL'
                        s_t0e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0e}</p>"
                        st.markdown(s_t0e,unsafe_allow_html=True)
                        st.markdown(df_entrepot_rdg_selected.loc[i,'Publication URL'])
                    with col3:
                        t0f = 'DOI'
                        s_t0f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0f}</p>"
                        st.markdown(s_t0f,unsafe_allow_html=True)
                        st.markdown(df_entrepot_rdg_selected.loc[i,'Url'])
                    col1,col2, col3 = st.columns([0.6,0.2,0.2])
                    with col1:
                        t0g = 'Auteur'
                        s_t0g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0g}</p>"
                        st.markdown(s_t0g,unsafe_allow_html=True)
                        st.markdown(df_entrepot_rdg_selected.loc[i,'Auteur'])
                    with col2:
                        t0h = 'Organisation'
                        s_t0h = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0h}</p>"
                        st.markdown(s_t0h,unsafe_allow_html=True)
                        st.markdown(df_entrepot_rdg_selected.loc[i,'Organisation'])
                    with col3:
                        t0i = 'Email'
                        s_t0i = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0i}</p>"
                        st.markdown(s_t0i,unsafe_allow_html=True)
                        st.markdown(df_entrepot_rdg_selected.loc[i,'Email'])
        else:
            col1,col2,col3 = st.columns([0.5,0.2,0.3])
            with col1:
                Visu_depots_rdg_selected = f"Données publiées dans {Selected_entrepot}"
                s_Visu_depots_rdg_selected  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots_rdg_selected}</p>"
                st.markdown(s_Visu_depots_rdg_selected ,unsafe_allow_html=True)
            with col2:
                st.metric(label="Nombre de dépôts décomptés", value=len(df_entrepot_rdg_selected))
            with col3:
                pass

    else:
        ##########################################################################################
        ########### VISUALISATIONS GENERALES ###############################################################
        ##########################################################################################

        df_rdg_complet = pd.read_csv("pages/data/rechercheDataGouv/Contenu_RDG_complet.csv",index_col=[0])

        if all_ZAs:
            with st.container(border=True):
                Nombre_depots = df_rdg_complet['Entrepot'].value_counts()
                for i in range(len(liste_ZAs_)):
                    if liste_ZAs_[i] in Nombre_depots.index.values:
                        pass
                    else:
                        Nombre_depots[liste_ZAs_[i]]=0
                df = pd.DataFrame(Nombre_depots.values,index=Nombre_depots.index.values,columns=['Nombre_dépôts'])
                fig0= go.Figure()
                for i, za in enumerate(df.index.values):
                    selec = df.index.values[i:i+1]
                    selec_len = df['Nombre_dépôts'].values[i:i+1]
                    fig0.add_trace(go.Bar(
                                    y=selec,
                                    x=selec_len,
                                    name=za,
                                    orientation = 'h',
                                    marker=dict(color=colors[i])
                                ))
                fig0.update_layout(
                                    title=dict(
                                            text=f'Nombre de dépôts répertoriées sur RDG',
                                            font=dict(size=graph_title_font, family='Arial', color=graph_title_color)
                                            ),
                                    yaxis=dict(
                                            tickfont=dict(size=graph_yaxis_ticks_font, family='Arial', color=graph_ticks_color)   
                                            ),
                                            xaxis=dict(
                                                tickfont=dict(size=graph_xaxis_ticks_font, family='Arial', color=graph_ticks_color)   
                                            ),
                                            width=1000,
                                            height=600,
                                            showlegend=False)
                st.plotly_chart(fig0,use_container_width=True)

        if len(Selection_ZA)!=0:
            df_rdg_visu = df_rdg_complet[df_rdg_complet['Entrepot'].isin(Selection_ZA)]
            df_rdg_visu.reset_index(inplace=True)
            df_rdg_visu.drop(columns='index', inplace=True)
            #st.dataframe(df_visu)

            if len(Selection_ZA)==1:
                col1,col2,col3 = st.columns([0.5,0.2,0.3])
                with col1:
                    Visu_depots_rdg = f"Données publiées dans la {Selection_ZA[0]}"
                    s_Visu_depots_rdg  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots_rdg}</p>"
                    st.markdown(s_Visu_depots_rdg ,unsafe_allow_html=True)
                with col2:
                    st.metric(label="Nombre de dépôts décomptés", value=len(df_rdg_visu))
                with col3:
                    dataRDG_to_get = df_rdg_visu.to_csv(index=False)
                    st.download_button(
                            label="Téléchargement des données sélectionnées en CSV",
                            data=dataRDG_to_get,
                            file_name=f'data_RDG_{Selection_ZA[0]}_{d}.csv',
                            mime='text/csv')
            elif 1<len(Selection_ZA)<16:
                selection_name = ""
                for i in range(len(Selection_ZA)):
                    selection_name+=Selection_ZA[i].strip().replace("Zone atelier", "ZA ").replace(" ","")
                col1,col2,col3 = st.columns([0.5,0.2,0.3])
                with col1:
                    Visu_depots_rdg = f"Données publiées dans les ZA suivantes: {Selection_ZA}"
                    s_Visu_depots_rdg  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots_rdg}</p>"
                    st.markdown(s_Visu_depots_rdg ,unsafe_allow_html=True)
                with col2:
                    st.metric(label="Nombre de dépôts décomptés", value=len(df_rdg_visu))
                with col3:
                    dataRDG_to_get = df_rdg_visu.to_csv(index=False)
                    st.download_button(
                            label="Téléchargement des données sélectionnées en CSV",
                            data=dataRDG_to_get,
                            file_name=f'data_RDG_{selection_name}_{d}.csv',
                            mime='text/csv')
            elif len(Selection_ZA)==16:
                selection_name = "All_ZAs"
                col1,col2,col3 = st.columns([0.5,0.2,0.3])
                with col1:
                    Visu_depots_rdg = f"Données publiées dans l'ensemble du réseau des Zones Ateliers"
                    s_Visu_depots_rdg  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots_rdg}</p>"
                    st.markdown(s_Visu_depots_rdg ,unsafe_allow_html=True)
                with col2:
                    st.metric(label="Nombre de dépôts décomptés", value=len(df_rdg_visu))
                with col3:
                    dataRDG_to_get = df_rdg_visu.to_csv(index=False)
                    st.download_button(
                            label="Téléchargement des données sélectionnées en CSV",
                            data=dataRDG_to_get,
                            file_name=f'data_RDG_{selection_name}_{d}.csv',
                            mime='text/csv')
            
            if len(df_rdg_visu)!=0:
                    for i in range(len(df_rdg_visu)):
                        with st.container(border=True):
                            t0 = f"FICHIER #{i+1}"
                            s_t0 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t0}</p>"
                            st.markdown(s_t0,unsafe_allow_html=True)
                            col1,col2, col3 = st.columns([0.6,0.2,0.2])
                            with col1:
                                t0a = 'Titre'
                                s_t0a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0a}</p>"
                                st.markdown(s_t0a,unsafe_allow_html=True)
                                st.markdown(df_rdg_visu.loc[i,'Titre'])
                            with col2:
                                t0b = 'Thème'
                                s_t0b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0b}</p>"
                                st.markdown(s_t0b,unsafe_allow_html=True)
                                st.markdown(df_rdg_visu.loc[i,'Thème'])
                            with col3:
                                t0c = 'Date'
                                s_t0c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0c}</p>"
                                st.markdown(s_t0c,unsafe_allow_html=True)
                                st.markdown(df_rdg_visu.loc[i,'Date de publication'])
                            col1,col2, col3 = st.columns([0.6,0.2,0.2])
                            with col1:
                                t0d = 'Résumé'
                                s_t0d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0d}</p>"
                                st.markdown(s_t0d,unsafe_allow_html=True)
                                st.markdown(df_rdg_visu.loc[i,'Résumé'])
                            with col2:
                                t0e = 'Publication URL'
                                s_t0e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0e}</p>"
                                st.markdown(s_t0e,unsafe_allow_html=True)
                                st.markdown(df_rdg_visu.loc[i,'Publication URL'])
                            with col3:
                                t0f = 'DOI'
                                s_t0f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0f}</p>"
                                st.markdown(s_t0f,unsafe_allow_html=True)
                                st.markdown(df_rdg_visu.loc[i,'Url'])
                            col1,col2, col3 = st.columns([0.6,0.2,0.2])
                            with col1:
                                t0g = 'Auteur'
                                s_t0g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0g}</p>"
                                st.markdown(s_t0g,unsafe_allow_html=True)
                                st.markdown(df_rdg_visu.loc[i,'Auteur'])
                            with col2:
                                t0h = 'Organisation'
                                s_t0h = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0h}</p>"
                                st.markdown(s_t0h,unsafe_allow_html=True)
                                st.markdown(df_rdg_visu.loc[i,'Organisation'])
                            with col3:
                                t0i = 'Email'
                                s_t0i = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0i}</p>"
                                st.markdown(s_t0i,unsafe_allow_html=True)
                                st.markdown(df_rdg_visu.loc[i,'Email'])
        else:
            pass    

    if sun:
        fig = px.sunburst(dataverses, path=['niv0','niv1','niv2'], values='val')
        fig.update_layout(
                    title=f'Visuel des différents Dataverses dans RDG via {fich}',
                    width=1000,
                    height=1000)
        st.plotly_chart(fig,use_container_width=True)



    ##########################################################################################
    ########### POUR L'ADMINISTRATEUR ########################################################
    ##########################################################################################
    admin_pass = 'admin'
    admin_action = st.sidebar.text_input(label="Pour l'administrateur")

    if admin_action == admin_pass:

        b1 = st.sidebar.button(label=" Mise à jour des entrepôts Dataverses dans RDG ")

        if b1==True:
            with st.spinner("Récupération des entrepôts existants"):
                api_rdg = connect_to_dataverse(BASE_URL_RDG,  API_TOKEN_RDG)
                Recup_dataverses_rdg(api_rdg,fichier)

    # RECUPERATION DES CONTENUS VIA BOUTON ##########################################       
        Recup_globale = st.sidebar.button('recupération des contenus')
        if Recup_globale:
            with st.spinner("La récup globale est en cours"):
                api_rdg = connect_to_dataverse(BASE_URL_RDG,  API_TOKEN_RDG)
                liste_columns_df_entrepot_rdg=['selection','Entrepot','Store','ID','Url','Date de publication','Titre','Auteur','Organisation',"Email",'Résumé','Thème','Publication URL']
                df_entrepot_rdg = pd.DataFrame(columns=liste_columns_df_entrepot_rdg)
                for i in range(len(dataverses)):
                    print(i)
                    for j in range(len(Selection_ZA)):
                        print(j)
                        try:
                            s = int(dataverses.loc[i,'ids_niv2'])
                            entrepot = dataverses.loc[i,'niv2']
                            df = Recup_contenu(api_rdg, s, entrepot, Selection_ZA[j])
                            dfi = pd.concat([df_entrepot_rdg,df], axis=0)
                            dfi.reset_index(inplace=True)
                            dfi.drop(columns='index', inplace=True)
                            dfi_ = dfi[dfi['Check']==True]
                            df_entrepot_rdg = dfi_
                        except:
                            pass
                        
                df_entrepot_rdg.to_csv("pages/data/rechercheDataGouv/Contenu_RDG_complet.csv")

######################################################################################################################
############################ NAKALA ##################################################################################
######################################################################################################################
if nakala:
    st.title(":grey[Analyse des dépôts dans Nakala]")

    #adresse_nakala = url_nakala
    #s_adresse_nakala = f"<p style='font-size:25px;color:rgb(150,150,150)'>{adresse_nakala}</p>"
    #st.markdown(s_adresse_nakala ,unsafe_allow_html=True)

    st.success("Selectionner une ou plusieurs zones ateliers (ou l'ensemble du réseau) / CASE A COCHER ou LISTE DEROULANTE")

    if len(Selection_ZA)==0:
        df_entrepot_nakala_selected = []
    else:
        with st.spinner("Recherche en cours"):
            liste_columns_df_entrepot_nakala_selected=['Store','Entrepot','ID','Titre','Auteur','Date de publication','Publication Url']
            df_entrepot_nakala_selected = pd.DataFrame(columns=liste_columns_df_entrepot_nakala_selected)
            for i, s in enumerate(Selection_ZA):
                params_nakala = {'q': f'"{s.lower()}"',
                                'size':1000}
                df_nakala = Recup_contenu_nakala(url_nakala,params_nakala, headers_nakala, s)
                dfn = pd.concat([df_entrepot_nakala_selected,df_nakala], axis=0)
                dfn.reset_index(inplace=True)
                dfn.drop(columns='index', inplace=True)
                df_entrepot_nakala_selected = dfn
                df_entrepot_nakala_selected.to_csv()

            #st.dataframe(df_entrepot_nakala_selected)

    
    if len(df_entrepot_nakala_selected)!=0:
        if len(Selection_ZA)==1:
                col1, col2, col3 = st.columns([0.5,0.2,0.3])
                with col1:
                    Sommes_check_selected_df = f"Décomptes sur {Selection_ZA[0]}"
                    s_Sommes_check_selected_df  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Sommes_check_selected_df}</p>"
                    st.markdown(s_Sommes_check_selected_df ,unsafe_allow_html=True)
                with col2:
                    st.metric(label="Nombre de publications trouvées", value=len(df_entrepot_nakala_selected))
                with col3:
                    datanakala_to_get = df_entrepot_nakala_selected.to_csv(index=False)
                    st.download_button(
                        label="Téléchargement des données sélectionnées en CSV",
                        data=datanakala_to_get,
                        file_name=f'data_nakala_{Selection_ZA[0]}_{d}.csv',
                        mime='text/csv')
        elif 1<len(Selection_ZA)<16:
                selection_name = ""
                for i in range(len(Selection_ZA)):
                    selection_name+=Selection_ZA[i].strip().replace("Zone atelier", "ZA ").replace(" ","")
                col1,col2,col3 = st.columns([0.5,0.2,0.3])
                with col1:
                    Visu_depots_nakala = f"Données publiées dans les ZA suivantes: {Selection_ZA}"
                    s_Visu_depots_nakala  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots_nakala}</p>"
                    st.markdown(s_Visu_depots_nakala ,unsafe_allow_html=True)
                with col2:
                    st.metric(label="Nombre de dépôts décomptés", value=len(df_entrepot_nakala_selected))
                with col3:
                    datanakala_to_get = df_entrepot_nakala_selected.to_csv(index=False)
                    st.download_button(
                            label="Téléchargement des données sélectionnées en CSV",
                            data=datanakala_to_get,
                            file_name=f'data_nakala_{selection_name}_{d}.csv',
                            mime='text/csv')            
        elif len(Selection_ZA)==16:
                col1, col2, col3 = st.columns([0.5,0.2,0.3])
                with col1:
                    Sommes_check_selected_df = f"Décomptes sur l'ensemble du réseau"
                    s_Sommes_check_selected_df  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Sommes_check_selected_df}</p>"
                    st.markdown(s_Sommes_check_selected_df ,unsafe_allow_html=True)
                with col2:
                    st.metric(label="Nombre de publications trouvées", value=len(df_entrepot_nakala_selected))
                with col3:
                    datanakala_to_get = df_entrepot_nakala_selected.to_csv(index=False)
                    st.download_button(
                        label="Téléchargement des données sélectionnées en CSV",
                        data=datanakala_to_get,
                        file_name=f'data_nakala_AllZAs_{d}.csv',
                        mime='text/csv')
            
        for i in range(len(df_entrepot_nakala_selected)):
            with st.container(border=True):
                t0 = f"FICHIER #{i+1}"
                s_t0 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t0}</p>"
                st.markdown(s_t0,unsafe_allow_html=True)
                col1,col2 = st.columns([0.6,0.4])
                with col1:
                    t0a = 'Titre'
                    s_t0a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0a}</p>"
                    st.markdown(s_t0a,unsafe_allow_html=True)
                    st.markdown(df_entrepot_nakala_selected.loc[i,'Titre'])
                with col2:
                    t0b = 'Date'
                    s_t0b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0b}</p>"
                    st.markdown(s_t0b,unsafe_allow_html=True)
                    st.markdown(df_entrepot_nakala_selected.loc[i,'Date de publication'])
                col1,col2 = st.columns([0.6,0.4])
                with col1:
                    t0e = 'Auteur'
                    s_t0e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0e}</p>"
                    st.markdown(s_t0e,unsafe_allow_html=True)
                    st.markdown(df_entrepot_nakala_selected.loc[i,'Auteur'])
                with col2:
                    t0d = 'Publication URL'
                    s_t0d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0d}</p>"
                    st.markdown(s_t0d,unsafe_allow_html=True)
                    st.markdown(df_entrepot_nakala_selected.loc[i,'Publication Url'])
                    
                

    ##########################################################################################
    ########### POUR L'ADMINISTRATEUR ########################################################
    ##########################################################################################
    admin_pass = 'admin'
    admin_action = st.sidebar.text_input(label="Pour l'administrateur")

    if admin_action == admin_pass:
        Recup_globale = st.sidebar.button('recupération des contenus')
        if Recup_globale:
            with st.spinner("La récup globale est en cours"):
                liste_columns_df_entrepot_nakala_selected=['Store','Entrepot','ID','Titre','Auteur','Date de publication','Résumé','Publication Url']
                df_entrepot_nakala_selected = pd.DataFrame(columns=liste_columns_df_entrepot_nakala_selected)
                for i, s in enumerate(liste_ZAs_):
                    params_nakala = {'q': f'"{s.lower()}"',
                                        'size':1000}
                    df_nakala = Recup_contenu_nakala(url_nakala,params_nakala, headers_nakala, s)
                    dfn = pd.concat([df_entrepot_nakala_selected,df_nakala], axis=0)
                    dfn.reset_index(inplace=True)
                    dfn.drop(columns='index', inplace=True)
                    df_entrepot_nakala_selected = dfn
                df_entrepot_nakala_selected.to_csv("pages/data/Nakala/Contenu_Nakala_complet.csv")

######################################################################################################################
############################ ZENODO ##################################################################################
######################################################################################################################
if zenodo:
    st.title(":grey[Analyse des dépôts dans Zenodo]")

    st.success("Selectionner une ou plusieurs zones ateliers (ou l'ensemble du réseau) / CASE A COCHER ou LISTE DEROULANTE")

    #adresse_zenodo = url_zenodo
    #s_adresse_zenodo = f"<p style='font-size:25px;color:rgb(150,150,150)'>{adresse_zenodo}</p>"
    #st.markdown(s_adresse_zenodo ,unsafe_allow_html=True)
    if len(Selection_ZA)==0:
        pass
    else:
        with st.spinner("Recherche en cours"):
            liste_columns = ['Store','Entrepot','ID','Titre','Auteur',"Résumé","Date de publication","Publication Url"]
            df_global_zenodo = pd.DataFrame(columns=liste_columns)
            for i, s in enumerate(Selection_ZA):
                params_zenodo = {'q': f'"{s.lower()}"',
                        'access_token': zenodo_token}
                
                df = Recup_contenu_zenodo(url_zenodo,params_zenodo, headers_zenodo, s)
                dfi = pd.concat([df_global_zenodo,df], axis=0)
                dfi.reset_index(inplace=True)
                dfi.drop(columns='index', inplace=True)
                df_global_zenodo = dfi
            df_global_zenodo.sort_values(by='ID', inplace=True, ascending=False)
            df_global_zenodo.reset_index(inplace=True)
            df_global_zenodo.drop(columns='index', inplace=True)

        df_visu_zenodo = df_global_zenodo[df_global_zenodo['Entrepot'].isin(Selection_ZA)]
        df_visu_zenodo.reset_index(inplace=True)
        df_visu_zenodo.drop(columns='index', inplace=True)

        

        if len(df_visu_zenodo)!=0:
            if len(Selection_ZA)==1:
                col1, col2, col3 = st.columns([0.5,0.2,0.3])
                with col1:
                    Sommes_check_selected_df = f"Décomptes sur {Selection_ZA[0]}"
                    s_Sommes_check_selected_df  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Sommes_check_selected_df}</p>"
                    st.markdown(s_Sommes_check_selected_df ,unsafe_allow_html=True)
                with col2:
                    st.metric(label="Nombre de publications trouvées", value=len(df_visu_zenodo))
                with col3:
                    datazenodo_to_get = df_visu_zenodo.to_csv(index=False)
                    st.download_button(
                        label="Téléchargement des données sélectionnées en CSV",
                        data=datazenodo_to_get,
                        file_name=f'data_zenodo_{Selection_ZA[0]}_{d}.csv',
                        mime='text/csv')
        elif 1<len(Selection_ZA)<16:
                selection_name = ""
                for i in range(len(Selection_ZA)):
                    selection_name+=Selection_ZA[i].strip().replace("Zone atelier", "ZA ").replace(" ","")
                col1,col2,col3 = st.columns([0.5,0.2,0.3])
                with col1:
                    Visu_depots_zenodo = f"Données publiées dans les ZA suivantes: {Selection_ZA}"
                    s_Visu_depots_zenodo  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots_zenodo}</p>"
                    st.markdown(s_Visu_depots_zenodo ,unsafe_allow_html=True)
                with col2:
                    st.metric(label="Nombre de dépôts décomptés", value=len(df_visu_zenodo))
                with col3:
                    datazenodo_to_get = df_visu_zenodo.to_csv(index=False)
                    st.download_button(
                            label="Téléchargement des données sélectionnées en CSV",
                            data=datazenodo_to_get,
                            file_name=f'data_zenodo_{selection_name}_{d}.csv',
                            mime='text/csv')    
        elif len(Selection_ZA)==16:
                col1, col2, col3 = st.columns([0.5,0.2,0.3])
                with col1:
                    Sommes_check_selected_df = f"Décomptes sur l'ensemble du réseau"
                    s_Sommes_check_selected_df  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Sommes_check_selected_df}</p>"
                    st.markdown(s_Sommes_check_selected_df ,unsafe_allow_html=True)
                with col2:
                    st.metric(label="Nombre de publications trouvées", value=len(df_visu_zenodo))
                with col3:
                    datazenodo_to_get = df_visu_zenodo.to_csv(index=False)
                    st.download_button(
                        label="Téléchargement des données sélectionnées en CSV",
                        data=datazenodo_to_get,
                        file_name=f'data_zenodo_AllZAs_{d}.csv',
                        mime='text/csv')
            
        for i in range(len(df_visu_zenodo)):
            with st.container(border=True):
                t0 = f"FICHIER #{i+1}"
                s_t0 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t0}</p>"
                st.markdown(s_t0,unsafe_allow_html=True)
                col1,col2 = st.columns([0.8,0.2])
                with col1:
                    t0a = 'Titre'
                    s_t0a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0a}</p>"
                    st.markdown(s_t0a,unsafe_allow_html=True)
                    st.markdown(df_visu_zenodo.loc[i,'Titre'])
                with col2:
                    t0b = 'Date'
                    s_t0b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0b}</p>"
                    st.markdown(s_t0b,unsafe_allow_html=True)
                    st.markdown(df_visu_zenodo.loc[i,'Date de publication'])
                col1,col2 = st.columns([0.8,0.2])
                with col1:
                    t0c = 'Résumé'
                    s_t0c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0c}</p>"
                    st.markdown(s_t0c,unsafe_allow_html=True)
                    st.markdown(md(df_visu_zenodo.loc[i,'Résumé']))
                with col2:
                    t0d = 'Publication URL'
                    s_t0d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0d}</p>"
                    st.markdown(s_t0d,unsafe_allow_html=True)
                    st.markdown(df_visu_zenodo.loc[i,'Publication Url'])
                    t0e = 'Auteur'
                    s_t0e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0e}</p>"
                    st.markdown(s_t0e,unsafe_allow_html=True)
                    st.markdown(df_visu_zenodo.loc[i,'Auteur'])
    
    ##########################################################################################
    ########### POUR L'ADMINISTRATEUR ########################################################
    ##########################################################################################
    admin_pass = 'admin'
    admin_action = st.sidebar.text_input(label="Pour l'administrateur")

    if admin_action == admin_pass:
        Recup_globale = st.sidebar.button('recupération des contenus')
        if Recup_globale:
            with st.spinner("La récup globale est en cours"):
                liste_columns = ['Store','Entrepot','ID','Titre','Auteur',"Résumé","Date de publication","Publication Url"]
                df_global_zenodo = pd.DataFrame(columns=liste_columns)
                for i, s in enumerate(liste_ZAs_):
                    params_zenodo = {'q': f'"{s.lower()}"',
                            'access_token': zenodo_token}
                    
                    df = Recup_contenu_zenodo(url_zenodo,params_zenodo, headers_zenodo, s)
                    dfi = pd.concat([df_global_zenodo,df], axis=0)
                    dfi.reset_index(inplace=True)
                    dfi.drop(columns='index', inplace=True)
                    df_global_zenodo = dfi
                df_global_zenodo.sort_values(by='ID', inplace=True, ascending=False)
                df_global_zenodo.reset_index(inplace=True)
                df_global_zenodo.drop(columns='index', inplace=True)
                df_global_zenodo.to_csv("pages/data/Zenodo/Contenu_ZENODO_complet.csv")

######################################################################################################################
################################# DRYAD ##############################################################################
######################################################################################################################
if dryad:
    st.title(":grey[Analyse des dépôts dans Dryad]")

    st.success("Selectionner une ou plusieurs zones ateliers (ou l'ensemble du réseau) / CASE A COCHER ou LISTE DEROULANTE")
    #adresse_dryad = url_dryad
    #s_adresse_dryad = f"<p style='font-size:25px;color:rgb(150,150,150)'>{adresse_dryad}</p>"
    #st.markdown(s_adresse_dryad ,unsafe_allow_html=True)

    with st.spinner("Recherche en cours"):
        liste_columns_dryad = ['Store','Entrepot','ID','Date de publication','Titre','Auteur prénom 1','Auteur Nom 1',
                            'Organisation 1',"Email 1",'Auteur prénom 2','Auteur Nom 2','Organisation 2',"Email 2",
                            'Auteur prénom 3','Auteur Nom 3','Organisation 3',"Email 3",'Résumé','Thème','Publication URL']
        df_dryad_global = pd.DataFrame(columns=liste_columns_dryad)
        for i in range(len(Selection_ZA)):
            params_dryad = {'q':Selection_ZA[i]}
            Nombre_dryad, df_dryad = Recup_contenu_dryad(url_dryad,params_dryad, Selection_ZA[i])
            dfi = pd.concat([df_dryad_global,df_dryad], axis=0)
            dfi.reset_index(inplace=True)
            dfi.drop(columns='index', inplace=True)
            df_dryad_global = dfi

        df_dryad_global.sort_values(by='Date de publication', inplace=True, ascending=False)
        df_dryad_global.reset_index(inplace=True)
        df_dryad_global.drop(columns='index', inplace=True)
    
    if len(df_dryad_global)!=0:
            if len(Selection_ZA)==1:
                col1, col2, col3 = st.columns([0.5,0.2,0.3])
                with col1:
                    Sommes_check_selected_df = f"Décomptes sur {Selection_ZA[0]}"
                    s_Sommes_check_selected_df  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Sommes_check_selected_df}</p>"
                    st.markdown(s_Sommes_check_selected_df ,unsafe_allow_html=True)
                with col2:
                    st.metric(label="Nombre de publications trouvées", value=len(df_dryad_global))
                with col3:
                    datadryad_to_get = df_dryad_global.to_csv(index=False)
                    st.download_button(
                        label="Téléchargement des données sélectionnées en CSV",
                        data=datadryad_to_get,
                        file_name=f'data_dryad_{Selection_ZA[0]}_{d}.csv',
                        mime='text/csv')
            elif 1<len(Selection_ZA)<16:
                selection_name = ""
                for i in range(len(Selection_ZA)):
                    selection_name+=Selection_ZA[i].strip().replace("Zone atelier", "ZA ").replace(" ","")
                col1,col2,col3 = st.columns([0.5,0.2,0.3])
                with col1:
                    Visu_depots_dryad = f"Données publiées dans les ZA suivantes: {Selection_ZA}"
                    s_Visu_depots_dryad  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots_dryad}</p>"
                    st.markdown(s_Visu_depots_dryad ,unsafe_allow_html=True)
                with col2:
                    st.metric(label="Nombre de dépôts décomptés", value=len(df_dryad_global))
                with col3:
                    datadryad_to_get = df_dryad_global.to_csv(index=False)
                    st.download_button(
                            label="Téléchargement des données sélectionnées en CSV",
                            data=datadryad_to_get,
                            file_name=f'data_dryad_{selection_name}_{d}.csv',
                            mime='text/csv')
            elif len(Selection_ZA)==16:
                col1, col2, col3 = st.columns([0.5,0.2,0.3])
                with col1:
                    Sommes_check_selected_df = f"Décomptes sur l'ensemble du réseau"
                    s_Sommes_check_selected_df  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Sommes_check_selected_df}</p>"
                    st.markdown(s_Sommes_check_selected_df ,unsafe_allow_html=True)
                with col2:
                    st.metric(label="Nombre de publications trouvées", value=len(df_dryad_global))
                with col3:
                    datadryad_to_get = df_dryad_global.to_csv(index=False)
                    st.download_button(
                        label="Téléchargement des données sélectionnées en CSV",
                        data=datadryad_to_get,
                        file_name=f'data_dryad_AllZAs_{d}.csv',
                        mime='text/csv')


    df_visu_dryad = df_dryad_global[df_dryad_global['Entrepot'].isin(Selection_ZA)]
    df_visu_dryad.reset_index(inplace=True)
    df_visu_dryad.drop(columns='index', inplace=True)

    for i in range(len(df_visu_dryad)):
        with st.container(border=True):
                t0 = f"FICHIER #{i+1}"
                s_t0 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t0}</p>"
                st.markdown(s_t0,unsafe_allow_html=True)
                col1,col2, col3 = st.columns([0.6,0.2,0.2])
                with col1:
                    t0a = 'Titre'
                    s_t0a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0a}</p>"
                    st.markdown(s_t0a,unsafe_allow_html=True)
                    st.markdown(df_visu_dryad.loc[i,'Titre'])
                with col2:
                    t0b = 'Thème'
                    s_t0b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0b}</p>"
                    st.markdown(s_t0b,unsafe_allow_html=True)
                    st.markdown(df_visu_dryad.loc[i,'Thème'])
                with col3:
                    t0c = 'Date'
                    s_t0c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0c}</p>"
                    st.markdown(s_t0c,unsafe_allow_html=True)
                    st.markdown(df_visu_dryad.loc[i,'Date de publication'])
                col1,col2 = st.columns([0.6,0.4])
                with col1:
                    t0d = 'Résumé'
                    s_t0d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0d}</p>"
                    st.markdown(s_t0d,unsafe_allow_html=True)
                    st.markdown(df_visu_dryad.loc[i,'Résumé'])
                with col2:
                    t0e = 'Publication URL'
                    s_t0e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0e}</p>"
                    st.markdown(s_t0e,unsafe_allow_html=True)
                    st.markdown(df_visu_dryad.loc[i,'Publication URL'])
                col1,col2, col3 = st.columns([0.5,0.3,0.2])
                with col1:
                    t0g = 'Auteur'
                    s_t0g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0g}</p>"
                    st.markdown(s_t0g,unsafe_allow_html=True)
                with col2:
                    t0h = 'Organisation'
                    s_t0h = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0h}</p>"
                    st.markdown(s_t0h,unsafe_allow_html=True)
                with col3:
                    t0i = 'Email'
                    s_t0i = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0i}</p>"
                    st.markdown(s_t0i,unsafe_allow_html=True)
                for b in range(3):
                    with col1:
                        st.markdown(f"{df_visu_dryad.loc[i,f'Auteur Nom {b+1}']} , {df_visu_dryad.loc[i,f'Auteur prénom {b+1}']}")
                    with col2:
                        st.markdown(df_visu_dryad.loc[i,f'Organisation {b+1}'])
                    with col3:
                        st.markdown(df_visu_dryad.loc[i,f'Email {b+1}'])
    
    ##########################################################################################
    ########### POUR L'ADMINISTRATEUR ########################################################
    ##########################################################################################
    admin_pass = 'admin'
    admin_action = st.sidebar.text_input(label="Pour l'administrateur")

    if admin_action == admin_pass:
        Recup_globale = st.sidebar.button('recupération des contenus')
        if Recup_globale:
            with st.spinner("La récup globale est en cours"):
                liste_columns_dryad = ['Store','Entrepot','ID','Date de publication','Titre','Auteur prénom 1','Auteur Nom 1',
                            'Organisation 1',"Email 1",'Auteur prénom 2','Auteur Nom 2','Organisation 2',"Email 2",
                            'Auteur prénom 3','Auteur Nom 3','Organisation 3',"Email 3",'Résumé','Thème','Publication URL']
                df_dryad_global = pd.DataFrame(columns=liste_columns_dryad)
                for i in range(len(liste_ZAs_)):
                    params_dryad = {'q':liste_ZAs_[i]}
                    Nombre_dryad, df_dryad = Recup_contenu_dryad(url_dryad,params_dryad, liste_ZAs_[i])
                    dfi = pd.concat([df_dryad_global,df_dryad], axis=0)
                    dfi.reset_index(inplace=True)
                    dfi.drop(columns='index', inplace=True)
                    df_dryad_global = dfi

                df_dryad_global.sort_values(by='Date de publication', inplace=True, ascending=False)
                df_dryad_global.reset_index(inplace=True)
                df_dryad_global.drop(columns='index', inplace=True)
                df_dryad_global.to_csv("pages/data/Dryad/Contenu_DRYAD_complet.csv")

######################################################################################################################
############################## GBIF ##################################################################################
######################################################################################################################
if gbif:
    st.title(":grey[Analyse des dépôts dans GBIF]")

    st.success("Selectionner une ou plusieurs zones ateliers (ou l'ensemble du réseau) / CASE A COCHER ou LISTE DEROULANTE")
    #adresse_gbif = url_gbif
    #s_adresse_gbif = f"<p style='font-size:25px;color:rgb(150,150,150)'>{adresse_gbif}</p>"
    #st.markdown(s_adresse_gbif ,unsafe_allow_html=True)

    with st.spinner("Recherche en cours"):
        liste_columns_gbif = ['Store','Entrepot','ID','Date de publication','Titre','Auteur prénom 1','Auteur Nom 1',
                                'Organisation 1',"Email 1",'Résumé','Publication URL']
        df_gbif_global = pd.DataFrame(columns=liste_columns_gbif)
        for i in range(len(Selection_ZA)):
            params_gbif = {'q':Selection_ZA[i],
                            'size':1000}
            df_gbif = Recup_contenu_gbif(url_gbif,params_gbif,headers_gbif,Selection_ZA[i])
            dfi = pd.concat([df_gbif_global,df_gbif], axis=0)
            dfi.reset_index(inplace=True)
            dfi.drop(columns='index', inplace=True)
            df_gbif_global = dfi

        df_gbif_global.sort_values(by='Date de publication', inplace=True, ascending=False)
        df_gbif_global.reset_index(inplace=True)
        df_gbif_global.drop(columns='index', inplace=True)
        df_gbif_global['Date de publication 2'] = pd.to_datetime(df_gbif_global['Date de publication']).dt.strftime('%Y-%m-%d')

    if len(df_gbif_global)!=0:
            if len(Selection_ZA)==1:
                col1, col2, col3 = st.columns([0.5,0.2,0.3])
                with col1:
                    Sommes_check_selected_df = f"Décomptes sur {Selection_ZA[0]}"
                    s_Sommes_check_selected_df  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Sommes_check_selected_df}</p>"
                    st.markdown(s_Sommes_check_selected_df ,unsafe_allow_html=True)
                with col2:
                    st.metric(label="Nombre de publications trouvées", value=len(df_gbif_global))
                with col3:
                    datagbif_to_get = df_gbif_global.to_csv(index=False)
                    st.download_button(
                        label="Téléchargement des données sélectionnées en CSV",
                        data=datagbif_to_get,
                        file_name=f'data_gbif_{Selection_ZA[0]}_{d}.csv',
                        mime='text/csv')
            elif 1<len(Selection_ZA)<16:
                selection_name = ""
                for i in range(len(Selection_ZA)):
                    selection_name+=Selection_ZA[i].strip().replace("Zone atelier", "ZA ").replace(" ","")
                col1,col2,col3 = st.columns([0.5,0.2,0.3])
                with col1:
                    Visu_depots_gbif = f"Données publiées dans les ZA suivantes: {Selection_ZA}"
                    s_Visu_depots_gbif  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots_gbif}</p>"
                    st.markdown(s_Visu_depots_gbif ,unsafe_allow_html=True)
                with col2:
                    st.metric(label="Nombre de dépôts décomptés", value=len(df_gbif_global))
                with col3:
                    datagbif_to_get = df_gbif_global.to_csv(index=False)
                    st.download_button(
                            label="Téléchargement des données sélectionnées en CSV",
                            data=datagbif_to_get,
                            file_name=f'data_gbif_{selection_name}_{d}.csv',
                            mime='text/csv')
            elif len(Selection_ZA)==16:
                col1, col2, col3 = st.columns([0.5,0.2,0.3])
                with col1:
                    Sommes_check_selected_df = f"Décomptes sur l'ensemble du réseau"
                    s_Sommes_check_selected_df  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Sommes_check_selected_df}</p>"
                    st.markdown(s_Sommes_check_selected_df ,unsafe_allow_html=True)
                with col2:
                    st.metric(label="Nombre de publications trouvées", value=len(df_gbif_global))
                with col3:
                    datagbif_to_get = df_gbif_global.to_csv(index=False)
                    st.download_button(
                        label="Téléchargement des données sélectionnées en CSV",
                        data=datagbif_to_get,
                        file_name=f'data_gbif_AllZAs_{d}.csv',
                        mime='text/csv')

    df_visu_gbif = df_gbif_global[df_gbif_global['Entrepot'].isin(Selection_ZA)]
    df_visu_gbif.reset_index(inplace=True)
    df_visu_gbif.drop(columns='index', inplace=True)

    for i in range(len(df_visu_gbif)):
            with st.container(border=True):
                t0 = f"FICHIER #{i+1}"
                s_t0 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t0}</p>"
                st.markdown(s_t0,unsafe_allow_html=True)
                col1,col2 = st.columns([0.8,0.2])
                with col1:
                    t0a = 'Titre'
                    s_t0a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0a}</p>"
                    st.markdown(s_t0a,unsafe_allow_html=True)
                    st.markdown(df_visu_gbif.loc[i,'Titre'])
                with col2:
                    t0c = 'Date'
                    s_t0c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0c}</p>"
                    st.markdown(s_t0c,unsafe_allow_html=True)
                    st.markdown(df_visu_gbif.loc[i,'Date de publication 2'])
                col1,col2 = st.columns([0.6,0.4])
                with col1:
                    t0d = 'Résumé'
                    s_t0d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0d}</p>"
                    st.markdown(s_t0d,unsafe_allow_html=True)
                    st.markdown(md(df_visu_gbif.loc[i,'Résumé']))
                with col2:
                    t0e = 'Publication URL'
                    s_t0e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0e}</p>"
                    st.markdown(s_t0e,unsafe_allow_html=True)
                    st.markdown(df_visu_gbif.loc[i,'Publication URL'])
                col1,col2, col3 = st.columns([0.6,0.2,0.2])
                with col1:
                    t0g = 'Auteur'
                    s_t0g = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0g}</p>"
                    st.markdown(s_t0g,unsafe_allow_html=True)
                with col2:
                    t0h = 'Organisation'
                    s_t0h = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0h}</p>"
                    st.markdown(s_t0h,unsafe_allow_html=True)
                with col3:
                    t0i = 'Email'
                    s_t0i = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0i}</p>"
                    st.markdown(s_t0i,unsafe_allow_html=True)
                for b in range(1):
                    with col1:
                        st.markdown(f"{df_visu_gbif.loc[i,f'Auteur Nom {b+1}']} , {df_visu_gbif.loc[i,f'Auteur prénom {b+1}']}")
                    with col2:
                        st.markdown(df_visu_gbif.loc[i,f'Organisation {b+1}'])
                    with col3:
                        st.markdown(df_visu_gbif.loc[i,f'Email {b+1}'])
    
    ##########################################################################################
    ########### POUR L'ADMINISTRATEUR ########################################################
    ##########################################################################################
    admin_pass = 'admin'
    admin_action = st.sidebar.text_input(label="Pour l'administrateur")

    if admin_action == admin_pass:
        Recup_globale = st.sidebar.button('recupération des contenus')
        if Recup_globale:
            with st.spinner("La récup globale est en cours"):
                liste_columns_gbif = ['Store','Entrepot','ID','Date de publication','Titre','Auteur prénom 1','Auteur Nom 1',
                                'Organisation 1',"Email 1",'Résumé','Publication URL']
                df_gbif_global = pd.DataFrame(columns=liste_columns_gbif)
                for i in range(len(liste_ZAs_)):
                    params_gbif = {'q':liste_ZAs_[i],
                                    'size':1000}
                    df_gbif = Recup_contenu_gbif(url_gbif,params_gbif,headers_gbif,liste_ZAs_[i])
                    dfi = pd.concat([df_gbif_global,df_gbif], axis=0)
                    dfi.reset_index(inplace=True)
                    dfi.drop(columns='index', inplace=True)
                    df_gbif_global = dfi

                df_gbif_global.sort_values(by='Date de publication', inplace=True, ascending=False)
                df_gbif_global.reset_index(inplace=True)
                df_gbif_global.drop(columns='index', inplace=True)
                df_gbif_global['Date de publication 2'] = pd.to_datetime(df_gbif_global['Date de publication']).dt.strftime('%Y-%m-%d')
                df_gbif_global.to_csv("pages/data/Gbif/Contenu_GBIF_complet.csv")