
import requests
import streamlit as st

headers_xml = {"accept":"application/xml",
           "X-XSRF-TOKEN": "59734158-1618-4e14-b05e-919d931a384b"}
headers_json = {"accept":"application/json",
           "X-XSRF-TOKEN": "59734158-1618-4e14-b05e-919d931a384b"}
identifieur = 'ead8e65d-d41c-4507-8102-dc6619ac06b6'
url = "https://cat.indores.fr/geonetwork/srv/api/records/"
url_ = url + identifieur

resp2 = requests.get(url_,headers=headers_xml)
print(resp2)
if resp2.status_code == 200:
    xml_content = resp2.text
    print(xml_content)
    try:
        print('ok')
        with open(f"{identifieur}.json", 'w') as file:
            file.write(xml_content)
    except:
        pass


st.markdown("""
 <style>
    [data-testid=stSidebar] {
        background-color: rgb(6,51,87,0.2);
    }
    .st-emotion-cache-1dj0hjr {
            color: #3b979f;
    }
    .st-emotion-cache-1rtdyuf {
            color: #3b979f;
    }
    .st-emotion-cache-6tkfeg {
            color: #3b979f;
    }
    .st-emotion-cache-1q2d4ya {
            color: #3b979f;
    }
    </style>
""", unsafe_allow_html=True)


"Sur l'ensemble des pages des entrepôts:"
        
"- Choix de visualiser pour l'ensemble du RZA ou pour des ZA sélectionnées (Noms complets des ZA)"
"- Possibilité de visualiser l'ensemble des sous entrepôts ou collections existantes sur ces entrepôts:"
"           (un choix apparait quand la case de l'entrepôt choisi est cochée)"
"- Suite à la selection de la ZA choisie, il est proposé un tableau avec les enregistrements retrouvés"
"(Attention, la recherche est faite sur le mot-clé 'Nom de la ZA', il y a potentiellement des erreurs)"



"Sur les pages dédiées au géocatalogue:"
"- Choix de visualiser pour l'ensemble du RZA ou pour des ZA sélectionnées (les noms des groupes associés)"
"           (ce choix a été rendu possible aussi pour les OHM ayant leur sous-portail)"
"- Choix de filtrer avec une date de début de l'analyse"
"       (pour ne regarder que la dernière année, ou les dernières années par exemple)"

"Visualisation du contenu général de Cat.InDoRES:"
"- Répartition des fiches: Nombres de fiches comptabilisées dans chaque sous-portail par l'application"
"       (attention ZAM: incapacité temporaire à récupérer les fiches sur cette application)"
"       (attention ZAPygar: nombre de fiches inférieur à celui que l'on trouve sur le géocatalogue)"
"       (le choix de filtrage des dates est indisponible pour cette visualisation)"
"- Evolution temporelle: il est proposé un compte semestriel des fiches publiées"
"- Répartition spatiale: une visualisation des localisations"
"       (attention, toutes les fiches ne sont pas complétées sur ce champ)"
"       (attention, pour les ohms, il faut dézoomer pour voir les points ;)"
"- Autres champs: "
"   - Langues: un graphique 'camembert' sur la répartition respective entre français et anglais"
"   - Standards: un graphique 'camembert' sur la répartition respective entre standards "
"       (Voir les fiches qui ont un schéma différent du schéma ISO)"
"   - Formats utilisés: visualisation en barres horizontales des formats les plus utilisés"
"       (attention: les noms de formats renseignés ont dû être nettoyés pour que des catégories claires apparaissent)"
"       (choix de ne montrer que les 10 plus importants)"
"   - Organisations: visualisation en barres horizontales des organisations les plus mentionnées"
"       (attention: les noms renseignés d'organisations ont dû être nettoyés)"
"       (choix de ne montrer que les 15 plus importants)"
"   - Organisations: visualisation en barres horizontales des contacts les plus mentionnées"
"       (attention: les noms renseignés d'auteurs ont dû être nettoyés)"
"       (choix de ne montrer que les 15 plus importants)"
"   - Droits: un graphique 'camembert' sur la répartition respective entre contraintes renseignées"
"- Descriptions:"
"   - Il s'agit d'une analyse des thésaurus et mots-clés."
"   - la répartition entre usage ou non de thésaurus et présentée à gauche"
"   - Dès lors qu'un thésaurus est utilisé, le décompte des thésaurus employés est présenté à droite"
"       (choix de montrer les 18 thésaurus les plus employés ohm et RZA confondus)"
"   - Deux histogrammes présentent l'occurence du nombre de mots-clés renseignés"
"   - Enfin, les occurences mot-clé par mot-clé sont proposées"
"- Matrice FAIR:"
"   - Une matrice FAIR propose une vision générale de l'état de remplissage des fiches de métadonnées."
"   - En noir: c'est OK"
"   - En blanc: ce n'est pas OK"


FAIR_principes = Image.open("pages/data/Images/Principes_FAIR.png")
st.image(FAIR_principes, width=1000)

st.title(':grey[Rappel des référents "Données" du RZA]')

st.markdown('Jérôme Dutroncy, LTSER-FR Réseau des Zones Ateliers jerome.dutroncy@univ-smb.fr')

st.markdown('Cécile Pignol , Zone Atelier Alpes - cecile.pignol@univ-smb.fr')

st.markdown('A venir, Zone Atelier Arc Jurassien - ')

st.markdown('Françoise Le Moal ,  Zone Atelier Armorique - francoise.le-moal@univ-rennes1.fr')

st.markdown('Anne Clemens , Zone Atelier Bassin du Rhône - anne.clemens@graie.org')

st.markdown('A venir,  Zone Atelier Brest Iroise - ')

st.markdown('Isabelle Charpentier , Zone Atelier Environnementale Urbaine - icharpentier@unistra.fr')

st.markdown('Simon Chamaillé , Zone Atelier Hwange - simon.chamaille@cefe.cnrs.fr')

st.markdown('Annaelle Simonneau ,  Zone Atelier Loire - anaelle.simonneau@univ-orleans.fr')

st.markdown('Emmanuelle Montarges  , Zone Atelier Bassin de la Moselle - emmanuelle.montarges@univ-lorraine.fr')

st.markdown('Wilfired Heintz , Zone Atelier Pyrénées Garonne - wilfried.heintz@inrae.fr')

st.markdown('Marie Silvestre , Zone Atelier Seine - marie.silvestre@sorbonne-universite.fr')

st.markdown('David Sarramia , Zone Atelier Territoires Uranifères - david.sarramia@clermont.in2p3.fr')

st.markdown('Iris Barjhoux , Zone Atelier Environnementale Rurale - iris.barjhoux@univ-reims.fr')

st.markdown('Jean-Claude Raynal  , Zone Atelier Santé Environnement Camargue - jean-claude.raynal@cnrs.fr')


#################################################################################################################
######### SEANOE ################################################################################################
"""from sickle import Sickle

# SEANOE's OAI-PMH endpoint URL
oai_url = "https://www.seanoe.org/oai/OAIHandler"

# Initialize Sickle with the SEANOE OAI-PMH endpoint
sickle = Sickle(oai_url)

# Example request: List metadata formats
def list_metadata_formats():
    formats = sickle.ListMetadataFormats()
    for metadata_format in formats:
        print(metadata_format)

# Example request: List records
def list_records(metadata_prefix='oai_dc', from_date=None, until_date=None):
    records = sickle.ListRecords(metadataPrefix=metadata_prefix, from_=from_date, until=until_date)
    for record in records:
        print(record.metadata)

# Example request: Get record by ID
def get_record(identifier, metadata_prefix='oai_dc'):
    record = sickle.GetRecord(identifier=identifier, metadataPrefix=metadata_prefix)
    print(record.metadata)

# Run an example function
list_metadata_formats()

# Optionally, list records between dates or get a specific record
# list_records(from_date="2022-01-01", until_date="2022-12-31")
get_record(90452)  # Replace with actual identifier   """