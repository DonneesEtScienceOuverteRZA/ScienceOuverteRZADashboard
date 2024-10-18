import streamlit as st
from PIL import Image
from Publications import afficher_publications_hal
import pandas as pd
import datetime

######################################################################################################################
########### TITRE DE L'ONGLET ########################################################################################
######################################################################################################################
st.set_page_config(
    page_title="Publications du RZA sur HAL",
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

######################################################################################################################
########### PARAMETRES #####################################################################################################
######################################################################################################################
d = datetime.date.today().year

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

###############################################################################################
########### POUR L'ADMINISTRATEUR ############################################################
###############################################################################################

# Mot de passe pour faire des récupérations automatisées
admin_pass = 'admin'
admin_action = st.sidebar.text_input(label="Pour l'administrateur")

if admin_action == admin_pass:

    RecupPublications = st.sidebar.button("Récupération des publications")
    if RecupPublications:
        with st.spinner("Connexion à HAL pour récupérer l'ensemble des publications"):
                liste_columns_hal = ['Store','Entrepot','Ids','Titre et auteurs','Uri','Type','Type de document', 'Date de production']
                df_global_hal_admin = pd.DataFrame(columns=liste_columns_hal)
                for i, s in enumerate(liste_ZAs_):
                        url_type = f'http://api.archives-ouvertes.fr/search/?q=text:"{s.lower().strip()}"&rows=1500&wt=json&fq=producedDateY_i:[2000 TO {d}]&sort=docid asc&fl=docid,label_s,uri_s,submitType_s,docType_s, producedDateY_i'
                        df = afficher_publications_hal(url_type, s)
                        dfi = pd.concat([df_global_hal_admin,df], axis=0)
                        dfi.reset_index(inplace=True)
                        dfi.drop(columns='index', inplace=True)
                        df_global_hal_admin = dfi
                df_global_hal_admin.sort_values(by='Ids', inplace=True, ascending=False)
                df_global_hal_admin.reset_index(inplace=True)
                df_global_hal_admin.drop(columns='index', inplace=True)
                df_global_hal_admin.to_csv("pages/data/Hal/Contenu_HAL_complet.csv")

######################################################################################################################
########### SELECTION ZA #############################################################################################
######################################################################################################################

all_ZAs= st.sidebar.checkbox("Ensemble du réseau ZA")
if all_ZAs==True :
    Selection_ZA = liste_ZAs_
else:
    Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs_)

######################################################################################################################
########### SELECTION ANNEE ##########################################################################################
######################################################################################################################
col1,col2 = st.sidebar.columns(2)
with col1:
        start_year = st.text_input(label='Année de début')
        if start_year=='':
               start_year=d
with col2:
       st.write('')
       annee_unique = st.checkbox(label='année unique')

if annee_unique:
        end_year = start_year
else:
        end_year = d

######################################################################################################################
########### VISUALISATION ##########################################################################################
######################################################################################################################
st.title(":grey[Extraction des publications sur HAL]")

st.success("Selectionner une ou plusieurs zones ateliers (ou l'ensemble du réseau) / CASE A COCHER ou LISTE DEROULANTE")
st.success("Selectionner une année de début de recherche (par défaut: année en cours) / TAPER ANNEE + ENTREE ")

with st.spinner("Recherche en cours"):
        liste_columns_hal = ['Store','Entrepot','Ids','Titre et auteurs','Uri','Type','Type de document', 'Date de production']
        df_global_hal = pd.DataFrame(columns=liste_columns_hal)
        for i, s in enumerate(Selection_ZA):
                url_type = f'http://api.archives-ouvertes.fr/search/?q=text:"{s.lower().strip()}"&rows=1500&wt=json&fq=producedDateY_i:[{start_year} TO {end_year}]&sort=docid asc&fl=docid,label_s,uri_s,submitType_s,docType_s, producedDateY_i'
                df = afficher_publications_hal(url_type, s)
                dfi = pd.concat([df_global_hal,df], axis=0)
                dfi.reset_index(inplace=True)
                dfi.drop(columns='index', inplace=True)
                df_global_hal = dfi
        df_global_hal.sort_values(by='Ids', inplace=True, ascending=False)
        df_global_hal.reset_index(inplace=True)
        df_global_hal.drop(columns='index', inplace=True)

if len(df_global_hal)==0:
     pass
else:
        col1, col2 = st.columns(2)
        with col1:
                st.metric(label="Nombre de publications trouvées", value=len(df_global_hal))

        with col2:
                if all_ZAs:
                        selection_name = "All_ZAs"
                else:
                        selection_name = ""
                        for i in range(len(Selection_ZA)):
                                selection_name+=Selection_ZA[i].strip().replace("Zone atelier", "ZA ").replace(" ","")

                data_to_get = df.to_csv(index=False)
                st.write("")
                # Download button
                st.download_button(
                        label="Téléchargement des données sélectionnées en CSV",
                        data=data_to_get,
                        file_name=f'data_HAL_{selection_name}_from_{start_year}_to_{end_year}.csv',
                        mime='text/csv')

        for i in range(len(df_global_hal)):
                with st.container(border=True):
                        t0 = f"#{i+1}"
                        s_t0 = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t0}</p>"
                        st.markdown(s_t0,unsafe_allow_html=True)
                        col1,col2 = st.columns([0.7, 0.3])
                        with col1:
                                t0a = 'Auteurs et Titre'
                                s_t0a = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0a}</p>"
                                st.markdown(s_t0a,unsafe_allow_html=True)
                                st.markdown(df_global_hal.loc[i,'Titre et auteurs'])
                        with col2:
                                t0b = 'Uri'
                                s_t0b = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0b}</p>"
                                st.markdown(s_t0b,unsafe_allow_html=True)
                                st.markdown(df_global_hal.loc[i,'Uri'])

                        col1,col2,col3,col4 = st.columns(4)
                        with col1:
                                t0c = 'Type'
                                s_t0c = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0c}</p>"
                                st.markdown(s_t0c,unsafe_allow_html=True)
                                st.markdown(df_global_hal.loc[i,'Type'])
                        with col2:
                                t0d = 'Doc'
                                s_t0d = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0d}</p>"
                                st.markdown(s_t0d,unsafe_allow_html=True)
                                st.markdown(df_global_hal.loc[i,'Type de document'])
                        with col3:
                                t0e = 'Id'
                                s_t0e = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0e}</p>"
                                st.markdown(s_t0e,unsafe_allow_html=True)
                                st.markdown(df_global_hal.loc[i,'Ids'])
                        with col4:
                                t0f = 'Date de production'
                                s_t0f = f"<p style='font-size:{taille_subsubtitles};color:rgb{couleur_subsubtitles}'>{t0f}</p>"
                                st.markdown(s_t0f,unsafe_allow_html=True)
                                st.markdown(df_global_hal.loc[i,'Date de production'])