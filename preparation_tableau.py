import pandas as pd
from datetime import datetime
import numpy as np
import re

def prepa_date(tableau, rule="6ME"):
    tableau_date = tableau.copy()
    tableau_date.set_index('Date', inplace=True)
    tableau_date_resampled = tableau_date.resample(rule=rule).size()
    liste_dates = tableau_date_resampled.index.values
    liste_comptes = tableau_date_resampled.values
    df_date = pd.DataFrame([liste_dates,liste_comptes], index=['Date','Compte_resampled']).T
    df_date['Date'] = pd.to_datetime(df_date['Date'], format='mixed', utc=True)
    return df_date

def year(tableau):
    tableau_year = tableau.copy()
    tableau_year['Date'] = pd.to_datetime(tableau_year['Date'], format='mixed', utc=True)
    tableau_year.sort_values(by="Date", inplace=True)
    tableau_year.reset_index(inplace=True)
    tableau_year.drop(columns='index',inplace=True)
    for i in range(len(tableau_year)):
        try:
            y = datetime.date(tableau_year.loc[i,'Date']).year
            if y==1:
                y=np.NaN
        except:
            y = np.NAN
        tableau_year.loc[i,'Year']= y
    return tableau_year

def coordonnees(tableau):
    tableau_coord = tableau.copy()
    tableau_coord['lat']=(tableau_coord['Latitude sud']+tableau_coord['Latitude nord'])/2
    tableau_coord['long']=(tableau_coord['Longitude ouest']+tableau_coord['Longitude est'])/2
    return tableau_coord

def remove_duplicate_patterns(text,pattern):
        occurrences = list(re.finditer(pattern, text))
    
        if not occurrences:
            return text  

        for match in occurrences[1:]:
            text = text[:match.start()] + text[match.end():]
        
        return text

def traitement_langues(tableau):
    tableau_ = tableau.copy()

    for i in range(len(tableau_)):
            if tableau_.loc[i,'Langue']=="['en' 'fr']":
                tableau_.loc[i,'Langue']="eng & fre"
            elif tableau_.loc[i,'Langue']=="en":
                tableau_.loc[i,'Langue']="eng"
            elif tableau_.loc[i,'Langue']=="ang":
                tableau_.loc[i,'Langue']="eng"
            elif tableau_.loc[i,'Langue']=="['fr']":
                tableau_.loc[i,'Langue']="fre"
    
    return tableau_

def traitement_standards(tableau):
    tableau_ = tableau.copy()

    for i in range(len(tableau_)):
            if tableau_.loc[i,'Nom du standard']=="ISO 19115:2003 Geographic information - Metadata":
                tableau_.loc[i,'Nom du standard']="ISO 19115:2003/19139"
            elif tableau_.loc[i,'Nom du standard']=="ISO 19115-2 Geographic Information - Metadata Part 2 Extensions for imagery and gridded data":
                tableau_.loc[i,'Nom du standard']="ISO 19115-2 Extensions for imagery and gridded data"
            elif tableau_.loc[i,'Nom du standard']=="ISO 19115/19139":
                tableau_.loc[i,'Nom du standard']="ISO 19115:2003/19139"
            elif tableau_.loc[i,'Nom du standard']=="http://www.isotc211.org/2005/gco":
                tableau_.loc[i,'Nom du standard']="ISO 19136:2005"
            elif tableau_.loc[i,'Nom du standard']=="https://cat.indores.fr/geonetwork/xml/schemas/dublin-core/schema.xsd":
                tableau_.loc[i,'Nom du standard']="ISO 15836 (Dublin Core)"
            elif tableau_.loc[i,'Nom du standard']=="Cendrine":
                tableau_.loc[i,'Nom du standard']="ISO 15836 (Dublin Core)"
            elif tableau_.loc[i,'Nom du standard']=="patricia cicille":
                tableau_.loc[i,'Nom du standard']="ISO 15836 (Dublin Core)"
            elif tableau_.loc[i,'Nom du standard']=="07170":
                tableau_.loc[i,'Nom du standard']="ISO 15836 (Dublin Core)"
            elif tableau_.loc[i,'Nom du standard']=="23, rue Jean Baldassini":
                tableau_.loc[i,'Nom du standard']="ISO 15836 (Dublin Core)"
            elif tableau_.loc[i,'Nom du standard']=="UK GEMINI":
                tableau_.loc[i,'Nom du standard']="ISO 15836 (Dublin Core)"
            elif tableau_.loc[i,'Nom du standard']=="Chenouf Sarra":
                tableau_.loc[i,'Nom du standard']="ISO 15836 (Dublin Core)"
            elif tableau_.loc[i,'Nom du standard']=="ISO 19115-3 ISO 19115-3":
                tableau_.loc[i,'Nom du standard']="ISO 19115-3"
            elif tableau_.loc[i,'Nom du standard']=="ISO19139":
                tableau_.loc[i,'Nom du standard']="ISO 19115:2003/19139"
    
    return tableau_

def traitement_droits(tableau):
    tableau_ = tableau.copy()
    tableau_['Contrainte usage'] = tableau_['Contrainte usage'].fillna('Non renseigné')

    for i in range(len(tableau_)):
        if 'available' in str(tableau_.loc[i,'Contrainte usage']):
                tableau_.loc[i,'Contrainte usage']="available"
        elif 'restricted' in str(tableau_.loc[i,'Contrainte usage']):
                tableau_.loc[i,'Contrainte usage']="restricted"
        elif 'other' in str(tableau_.loc[i,'Contrainte usage']):
                tableau_.loc[i,'Contrainte usage']="other restrictions"
    
    return tableau_

def traitement_formats(tableau):
    tableau_ = tableau.copy()
    for i in range(len(tableau_)):
        try:
            tableau_.loc[i,'Format']=tableau_.loc[i,'Format'][2:-2]
        except:
            pass
        if tableau_.loc[i,'Format']=='':
            tableau_.loc[i,'Format']="non renseigné"
        elif tableau_.loc[i,'Format']=="Pas de logiciel associé à la donnée":
            tableau_.loc[i,'Format']="non renseigné"
        elif tableau_.loc[i,'Format']=="modèle de simulation du Grand Lyon":
            tableau_.loc[i,'Format']="non renseigné"
        elif tableau_.loc[i,'Format']=="Vigilance":
            tableau_.loc[i,'Format']="non renseigné"
        elif tableau_.loc[i,'Format']=="inapplicable":
            tableau_.loc[i,'Format']="non renseigné"
        elif tableau_.loc[i,'Format']=="application/pdf":
            tableau_.loc[i,'Format']="PDF"
        elif tableau_.loc[i,'Format']=="application/x-shapefile":
            tableau_.loc[i,'Format']="ESRI Shapefile"
        elif tableau_.loc[i,'Format']=="esri Shapefile":
            tableau_.loc[i,'Format']="ESRI Shapefile"
        elif tableau_.loc[i,'Format']=="Esri Shapefile":
            tableau_.loc[i,'Format']="ESRI Shapefile"
        elif tableau_.loc[i,'Format']=="SHP":
            tableau_.loc[i,'Format']="ESRI Shapefile"
        elif tableau_.loc[i,'Format']=="GeoTiff":
            tableau_.loc[i,'Format']="GeoTIFF"
        elif tableau_.loc[i,'Format']=="GEOTIFF":
            tableau_.loc[i,'Format']="GeoTIFF"
        elif tableau_.loc[i,'Format']=="TIFF":
            tableau_.loc[i,'Format']="GeoTIFF"
        elif tableau_.loc[i,'Format']=="TIF":
            tableau_.loc[i,'Format']="GeoTIFF"
        elif tableau_.loc[i,'Format']=="shape":
            tableau_.loc[i,'Format']="ESRI Shapefile"
        elif tableau_.loc[i,'Format']=="EXCEL":
            tableau_.loc[i,'Format']="XLS"
        elif tableau_.loc[i,'Format']=="application/vnd.ms-excel":
            tableau_.loc[i,'Format']="XLS"
        elif tableau_.loc[i,'Format']=="application/vnd.ms-excel' 'text/csv":
            tableau_.loc[i,'Format']="XLS"
        elif 'excel' in str(tableau_.loc[i,'Format']):
            tableau_.loc[i,'Format']="XLS"
        elif 'CSV' in str(tableau_.loc[i,'Format']):
            tableau_.loc[i,'Format']="CSV"
        elif tableau_.loc[i,'Format']=="application/pdf' 'application/vnd.ms-excel":
            tableau_.loc[i,'Format']="PDF"
        elif tableau_.loc[i,'Format']=="Jpeg2000":
            tableau_.loc[i,'Format']="JPEG"
        elif tableau_.loc[i,'Format']=="IRB, TIF, JPEG, BMP":
            tableau_.loc[i,'Format']="JPEG"
        elif tableau_.loc[i,'Format']=="Mammouth":
            tableau_.loc[i,'Format']="non renseigné"
        elif tableau_.loc[i,'Format']=="text/csv":
            tableau_.loc[i,'Format']="TXT"
        elif tableau_.loc[i,'Format']=="GDB":
            tableau_.loc[i,'Format']="ESRI Shapefile"
        elif tableau_.loc[i,'Format']=="vecteur' 'table postgis":
            tableau_.loc[i,'Format']="Vecteur"
        elif tableau_.loc[i,'Format']=="ESRI shapefile":
            tableau_.loc[i,'Format']="ESRI Shapefile"
        elif tableau_.loc[i,'Format']=="ESRI Shapefile (shp)":
            tableau_.loc[i,'Format']="ESRI Shapefile"
        elif tableau_.loc[i,'Format']=="Shapefile (.shp)":
            tableau_.loc[i,'Format']="ESRI Shapefile"
        elif tableau_.loc[i,'Format']=="TIF, GDB":
            tableau_.loc[i,'Format']="ESRI Shapefile"
        elif tableau_.loc[i,'Format']=="TIF, JPG, GDB":
            tableau_.loc[i,'Format']="ESRI Shapefile"
        elif tableau_.loc[i,'Format']=="JPG":
            tableau_.loc[i,'Format']="JPEG"
        elif tableau_.loc[i,'Format']=="xlsx":
            tableau_.loc[i,'Format']="XLS"
        elif tableau_.loc[i,'Format']=="Texte":
            tableau_.loc[i,'Format']="TXT"

    return tableau_

def traitement_orgas(tableau):
    tableau_ = tableau.copy()
    for i in range(len(tableau_)):
        try:
            tableau_.loc[i,'orga du contact']=tableau_.loc[i,'orga du contact'][2:-2].lower()
        except:
            pass
        if tableau_.loc[i,'orga du contact']=='':
            tableau_.loc[i,'orga du contact']='Non renseigné'
        elif tableau_.loc[i,'orga du contact']=='letg umr 6554 cnrs':
            tableau_.loc[i,'orga du contact']='UMR 6554 LETG CNRS'
        elif tableau_.loc[i,'orga du contact']=='umr6554 letg cnrs':
            tableau_.loc[i,'orga du contact']='UMR 6554 LETG CNRS'
        elif tableau_.loc[i,'orga du contact']=='letg-rennes costelletg-rennes umr 6554 cnrs université de rennes 2':
            tableau_.loc[i,'orga du contact']='UMR 6554 LETG CNRS'
        elif tableau_.loc[i,'orga du contact']=='letg rennes umr 6554 cnrs université de rennes 2':
            tableau_.loc[i,'orga du contact']='UMR 6554 LETG CNRS'
        elif tableau_.loc[i,'orga du contact']=='sorbonne université - metis':
            tableau_.loc[i,'orga du contact']='UMR 7619 metis sorbonne université'
        elif tableau_.loc[i,'orga du contact']=='sorbonne université - umr 7619 metis':
            tableau_.loc[i,'orga du contact']='UMR 7619 metis sorbonne université'
        elif tableau_.loc[i,'orga du contact']=='upmc - umr 7619 metis':
            tableau_.loc[i,'orga du contact']='UMR 7619 metis sorbonne université'
        elif tableau_.loc[i,'orga du contact']=='sorbonne université - métis':
            tableau_.loc[i,'orga du contact']='UMR 7619 metis sorbonne université'
        elif tableau_.loc[i,'orga du contact']=='upsorbonne université - umr 7619 metis':
            tableau_.loc[i,'orga du contact']='UMR 7619 metis sorbonne université'
        elif tableau_.loc[i,'orga du contact']=='cnrs - eccorev (fr3098)':
            tableau_.loc[i,'orga du contact']='UMR 3098 CNRS ECCOREV'
        elif tableau_.loc[i,'orga du contact']=='cnrs - eccorev (fr3098) - ohm bassin minier de provence':
            tableau_.loc[i,'orga du contact']='UMR 3098 CNRS ECCOREV'
        elif tableau_.loc[i,'orga du contact']=='letg-rennes costel':
            tableau_.loc[i,'orga du contact']='UMR 6554 LETG CNRS'
        elif tableau_.loc[i,'orga du contact']=='ietr umr cnrs 6164 / letg-rennes umr 6554 cnrs université de rennes 2':
            tableau_.loc[i,'orga du contact']='UMR 6554 LETG CNRS'
        elif tableau_.loc[i,'orga du contact']=='letg':
            tableau_.loc[i,'orga du contact']='UMR 6554 LETG CNRS'
        elif tableau_.loc[i,'orga du contact']=='letg-rennes umr 6554 cnrs université de rennes 2' :
            tableau_.loc[i,'orga du contact']='UMR 6554 LETG CNRS'            
        elif tableau_.loc[i,'orga du contact']=="umr 1069 sas inrae - l'institut agro rennes-angers":
            tableau_.loc[i,'orga du contact']='UMR 1069 INRA - agrocampus ouest'
        elif tableau_.loc[i,'orga du contact']=='ens de lyon - umr 5600 evs' :
            tableau_.loc[i,'orga du contact']='UMR5600 EVS - ENS de lyon'
        elif tableau_.loc[i,'orga du contact']=='evs umr 5600 cnrs université de lyon' :
            tableau_.loc[i,'orga du contact']='UMR 5600 EVS - ENS de lyon'
        elif tableau_.loc[i,'orga du contact']=='ecole des mines de saint-etienne- umr 5600 evs' :
            tableau_.loc[i,'orga du contact']='UMR 5600 EVS - ENS de lyon'
        elif tableau_.loc[i,'orga du contact']=='umr 5600' :
            tableau_.loc[i,'orga du contact']='UMR 5600 EVS - ENS de lyon'
        elif tableau_.loc[i,'orga du contact']=='umr 5600 evs - ens de lyon' :
            tableau_.loc[i,'orga du contact']='UMR 5600 EVS - ENS de lyon'    
        elif tableau_.loc[i,'orga du contact']=='cnrs leca' :
            tableau_.loc[i,'orga du contact']='leca' 
        elif 'umr 6553' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 6553 ECOBIO'
        elif '3189' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='IRL 3189 ESS'
        elif 'pag' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='Non renseigné'
        elif 'cerege' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='CEREGE Geoscience Environnement'
        elif 'letg' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 6554 LETG CNRS'
        elif '5126' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 5126 Etudes spatiales biosphère'
        elif '5245' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 5245 CNRS ECOLAB'
        elif 'lorraine' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='Université de Lorraine'
        elif '7300' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 7300 espace cnrs'
        elif 'pnra' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='Parc Naturel Regional Armorique'
        elif 'iuem' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMS 3113 IUEM'
        elif 'umr6554' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 6554 LETG CNRS'
        elif '5602' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 5602 GEODE'
        elif '7619' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 7619 metis sorbonne université'
        elif '5288' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 5288 Laboratoire AMIS'
        elif 'inrae' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='INRAE'
        elif 'letg 6554' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 6554 LETG CNRS'
        elif 'ums3113' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMS 3113 IUEM'
        elif 'umr6539' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 6539 CNRS LEMAR'
        elif 'umr6538' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 6538 CNRS LGO'
        elif 'indigeo' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='INDIGEO'
        elif 'umr 1069' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 1069 INRA - agrocampus ouest'
        elif 'umr 6118' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 6118 CNRS Geosciences Rennes'
        elif 'umr 6554' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 6554 LETG CNRS'
        elif 'umr 5023' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 5023 - LEHNA'
        elif 'chrono-environnement' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 6249 laboratoire chrono-environnement'
        elif 'mines saint-etienne' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='MINES Saint-Etienne - centre spin'
        elif tableau_.loc[i,'orga du contact']=='ecobio umr 6553 cnrs université de rennes 1' :
            tableau_.loc[i,'orga du contact']='UMR 6553 ECOBIO'
        elif tableau_.loc[i,'orga du contact']=='ecobio umr 6553 cnrs université de rennes' :
            tableau_.loc[i,'orga du contact']='UMR 6553 ECOBIO'
        elif tableau_.loc[i,'orga du contact']=='umr 6553 cnrs ecobio' :
            tableau_.loc[i,'orga du contact']='UMR 6553 ECOBIO'
        elif tableau_.loc[i,'orga du contact']=='umr 6553 ecobio' :
            tableau_.loc[i,'orga du contact']='UMR 6553 ECOBIO'
        elif tableau_.loc[i,'orga du contact']=='umr ecobio 6553 cnrs université de rennes 1' :
            tableau_.loc[i,'orga du contact']='UMR 6553 ECOBIO'
        elif tableau_.loc[i,'orga du contact']=="ecobio umr 6553 cnrs université de rennes 1'  'ecobio umr 6553 cnrs université de rennes 1" :
            tableau_.loc[i,'orga du contact']='UMR 6553 ECOBIO'
        elif 'umr 7362' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 7362 CNRS UNISTRA'
        elif tableau_.loc[i,'orga du contact']=='bagap umr 0980' :
            tableau_.loc[i,'orga du contact']='UMR 0980 bagap INRAE agrocampus'
        elif tableau_.loc[i,'orga du contact']=='inrae bagap' :
            tableau_.loc[i,'orga du contact']='UMR 0980 bagap INRAE agrocampus'
        elif tableau_.loc[i,'orga du contact']=='bagap umr 0980 inrae agrocampus ouest esa' :
            tableau_.loc[i,'orga du contact']='UMR 0980 bagap INRAE agrocampus'
        elif tableau_.loc[i,'orga du contact']=='mines saint-etienne - centre spin - peg' :
            tableau_.loc[i,'orga du contact']='MINES Saint-Etienne - centre spin'
        elif tableau_.loc[i,'orga du contact']=='mines saint-etienne' :
            tableau_.loc[i,'orga du contact']='MINES Saint-Etienne - centre spin'
        elif tableau_.loc[i,'orga du contact']=='mines saint-etienne - centre spin - gse' :
            tableau_.loc[i,'orga du contact']='MINES Saint-Etienne - centre spin'
        elif tableau_.loc[i,'orga du contact']=='irstea grenoble - ur dtm' :
            tableau_.loc[i,'orga du contact']='IRSTEA'
        elif tableau_.loc[i,'orga du contact']=='irstea lyon-villeurbanne' :
            tableau_.loc[i,'orga du contact']='IRSTEA'
        elif 'irstea' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']="IRSTEA"
        elif '{unité de recherche}' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']="Non renseigné"
        elif 'ofb dras santéagri' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']="Non renseigné"
        elif 'ecobio 6553' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 6553 ECOBIO'
        elif 'umr 6566' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 6566 CNRS CREAAH'
        elif 'bagap' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 0980 bagap INRAE agrocampus'
        elif 'sad-paysage' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 0980 bagap INRAE agrocampus'
        elif 'ums3343' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMS 3343 OSUR'
        elif 'leca' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']="Laboratoire LECA"
        elif 'edytem' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']="UMR 5204 Edytem"
        elif 'asters' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='ASTERS CEN 74'
        elif 'pacte' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='Laboratoire PACTE'
        elif 'grenoble-alpes' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='Université Grenoble Alpes'
        elif 'chasseurs du doubs' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='FDC du Doubs'
        elif 'umr 6049' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 6049 Laboratoire THEMA'
        elif 'umr 6282' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='UMR 6282 Biogéosciences'
        elif 'dryad' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='Non renseigné'
        elif 'zenodo' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='Non renseigné'
        elif 'fredon' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='FREDON Bourgogne FC'
        elif 'centre hospitalier régional universitaire de besançon' in str(tableau_.loc[i,'orga du contact']):
            tableau_.loc[i,'orga du contact']='CHRU de Besançon'
        elif tableau_.loc[i,'orga du contact']=='leca':
            tableau_.loc[i,'orga du contact']="Laboratoire LECA"
        elif tableau_.loc[i,'orga du contact']=='espace umr 7300 cnrs uma' :
            tableau_.loc[i,'orga du contact']='UMR 7300 espace cnrs'
        elif tableau_.loc[i,'orga du contact']=='espace umr 7300 cnrs au' :
            tableau_.loc[i,'orga du contact']='UMR 7300 espace cnrs'
        elif tableau_.loc[i,'orga du contact']=='umr espace 7300' :
            tableau_.loc[i,'orga du contact']='UMR 7300 espace cnrs'
        elif tableau_.loc[i,'orga du contact']=='inra' :
            tableau_.loc[i,'orga du contact']='UMR1069 INRA - agrocampus ouest'
        elif tableau_.loc[i,'orga du contact']=='zaa-ltser' :
            tableau_.loc[i,'orga du contact']='zaa'
        elif tableau_.loc[i,'orga du contact']=="direction régionale de l’environnement de l’aménagement et du logement d'auvergne-rhône-alpes (dreal auvergne-rhône-alpes)" :
            tableau_.loc[i,'orga du contact']='DREAL'
        elif tableau_.loc[i,'orga du contact']=="asters - cen 74" :
            tableau_.loc[i,'orga du contact']='ASTERS CEN 74'
        elif tableau_.loc[i,'orga du contact']=="laboratoire chrono-environnement (umr 6249)" :
            tableau_.loc[i,'orga du contact']='UMR 6249 laboratoire chrono-environnement'
        elif tableau_.loc[i,'orga du contact']=="umr 5023 - lehna" :
            tableau_.loc[i,'orga du contact']='UMR 5023 - LEHNA'
        elif tableau_.loc[i,'orga du contact']=="agence de l'eau" :
            tableau_.loc[i,'orga du contact']="Agence de l'Eau"

    return tableau_

def traitement_contacts(tableau):
    tableau_ = tableau.copy()

    def transfo_contact(x):
        return [item.strip() for item in x.split(';')]

    for i in range(len(tableau_)):
        try:
            tableau_.loc[i,'Nom du contact']=tableau_.loc[i,'Nom du contact'][2:-2].lower().replace("' '",";")
        except:
            pass
        if tableau_.loc[i,'Nom du contact']=='':
            tableau_.loc[i,'Nom du contact']='Non renseigné'
        elif tableau_.loc[i,'Nom du contact']=='pierre stéphan':
            tableau_.loc[i,'Nom du contact']='pierre, stéphan'
        elif tableau_.loc[i,'Nom du contact']=='pierre stephan':
            tableau_.loc[i,'Nom du contact']='pierre, stéphan'
        elif 'bray' in str(tableau_.loc[i,'Nom du contact']):
            tableau_.loc[i,'Nom du contact']='bray frédéric'
        elif 'renaud' in str(tableau_.loc[i,'Nom du contact']):
            tableau_.loc[i,'Nom du contact']='renaud julien'
        elif 'nabucet' in str(tableau_.loc[i,'Nom du contact']):
            tableau_.loc[i,'Nom du contact']='nabucet jean'
        elif 'moal' in str(tableau_.loc[i,'Nom du contact']):
            tableau_.loc[i,'Nom du contact']='le moal françoise'
        elif 'mony' in str(tableau_.loc[i,'Nom du contact']):
            tableau_.loc[i,'Nom du contact']='mony cendrine'
        elif 'aviron' in str(tableau_.loc[i,'Nom du contact']):
            tableau_.loc[i,'Nom du contact']='aviron stephanie'
        elif 'eschbach' in str(tableau_.loc[i,'Nom du contact']):
            tableau_.loc[i,'Nom du contact']='eschbach david'

    tableau_['Nom du contact'] = tableau_['Nom du contact'].apply(str)
    tableau_['Nom du contact'] = tableau_['Nom du contact'].apply(transfo_contact)
    return tableau_

def traitement_thesaurus(tableau):
    tableau_ = tableau.copy()
    tableau_.reset_index(inplace=True)
    tableau_.drop(columns='index',inplace=True)
    for i in range(len(tableau_)):
        tableau_.loc[i,'Thesaurus']=tableau_.loc[i,'Thesaurus'][1:-1]
        if len(tableau_.loc[i,'Thesaurus'])==0:
            tableau_.loc[i,'Thesaurus_usage']="NON"
        else:
            tableau_.loc[i,'Thesaurus_usage']="OUI"

    tableau_oui = tableau_[tableau_['Thesaurus_usage']=='OUI']
    tableau_oui.reset_index(inplace=True)
    tableau_oui.drop(columns='index',inplace=True)
    tableau_non = tableau_[tableau_['Thesaurus_usage']=='NON']
    tableau_non.reset_index(inplace=True)
    tableau_non.drop(columns='index',inplace=True)

    def transfo(x):
        return [item.strip().strip("'") for item in x.split(',')]

    tableau_oui['Thesaurus_listed'] = tableau_oui['Thesaurus'].apply(transfo)
    tableau_oui['Thesaurus_listed_len'] = tableau_oui['Thesaurus_listed'].apply(lambda x:len(x))

    elements_to_remove = {'version 1.0', 'version 2.4'}
    tableau_oui['Thesaurus_listed'] = tableau_oui['Thesaurus_listed'].apply(lambda lst: [x for x in lst if x not in elements_to_remove])
    pattern = 'GEMET - INSPIRE themes'
    pattern2 = 'Continents countries sea regions of the world'
    pattern3 = 'Régions administratives de France'
    replace_dict = {'INSPIRE themes': pattern,
                    'GEMET':pattern,
                    'Registre de thème INSPIRE':pattern,
                    'GEMET inspire themes - version 1.0':pattern,
                    'GEMET Thesaurus version 1.0':pattern,
                    'INSPIRE':pattern,
                    'inspire':pattern,
                    'Gemet':pattern,
                    'Continents':pattern2,
                    'countries':pattern2,
                    'sea regions of the world':pattern2,
                    'sea regions of the world.':pattern2,
                    'Region':pattern3}
    tableau_oui['Thesaurus_listed'] = tableau_oui['Thesaurus_listed'].apply(lambda lst: [replace_dict.get(x, x) for x in lst])
    tableau_oui['Thesaurus_listed'] = tableau_oui['Thesaurus_listed'].apply(set)
    tableau_oui['Thesaurus_listed'] = tableau_oui['Thesaurus_listed'].apply(list)

    return tableau_ ,tableau_oui, tableau_non

def traitement_mots_cles(tableau):
    tableau_ = tableau.copy()
    tableau_.reset_index(inplace=True)
    tableau_.drop(columns='index',inplace=True)
    for i in range(len(tableau_)):
        tableau_.loc[i,'Mots Clés']=tableau_.loc[i,'Mots Clés'][1:-1]
        tableau_.loc[i,'Mots Clés']=tableau_.loc[i,'Mots Clés'].replace(';',',')

    def transfo(x):
        return [item.strip().strip("'") for item in x.split(',')]
    
    tableau_['Mots_clés_listed'] = tableau_['Mots Clés'].apply(transfo)
    tableau_['Mots_clés_listed_len'] = tableau_['Mots_clés_listed'].apply(lambda x:len(x))

    return tableau_