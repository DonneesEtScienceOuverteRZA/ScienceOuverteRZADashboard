import pandas as pd
import numpy as np
import re
from pyDataverse.models import Dataset, Dataverse
from pyDataverse.utils import read_file
from pyDataverse.api import NativeApi
import json
import requests
import streamlit as st
from markdownify import markdownify as md


##################################################################################################################
############################################### ZENODO ###########################################################
##################################################################################################################
def recuperation_zenodo(url_zenodo,params_zenodo, headers_zenodo):
    results = []
    r = requests.get(url_zenodo,
                    params=params_zenodo,
                    headers=headers_zenodo)
    
    if r.status_code==200:
        resp_zenodo = r.json()['hits']['hits']

    """while True:
        resp_zenodo = requests.get(url_zenodo,
                    params=params_zenodo,
                    headers=headers_zenodo)
        data = resp_zenodo.json()

        # If there are no results, break the loop
        if not data['hits']['hits']:
            break

        # Add current page's results to the total results
        results.extend(data['hits']['hits'])

        # Increment the page number to get the next set of results
        params_zenodo['page'] += 1

    print(f"Total results retrieved: {len(results)}")"""
            
    return resp_zenodo

##################################################################################################################
######### RECUPERATION ZENODO ####################################################################################
def Recup_contenu_zenodo(url_zenodo,params_zenodo, headers_zenodo, entrepot):
    entrepot_selected = []
    store_z = []
    identifieurs = []
    titre = []
    auteur = []
    resume = []
    datesPublication = []
    publication_url = []
    try:
        contenu_zenodo = recuperation_zenodo(url_zenodo,params_zenodo, headers_zenodo)
        #st.write(contenu_zenodo)
        for i in range(len(contenu_zenodo)):
                try:
                    identifieurs.append(contenu_zenodo[i]['id'])
                except:
                    identifieurs.append("")
                try:
                    titre.append(contenu_zenodo[i]['title'])
                except:
                    titre.append("")
                try:
                    auteur.append(contenu_zenodo[i]['metadata']['creators'][0]['name'])
                except:
                    auteur.append("")
                try:
                    resume.append(contenu_zenodo[i]['metadata']['description'])
                except:
                    resume.append("")
                try:
                    datesPublication.append(contenu_zenodo[i]['metadata']['publication_date'])
                except:
                    datesPublication.append("")
                try:
                    publication_url.append(contenu_zenodo[i]['metadata']['doi'])
                except:
                    publication_url.append("")
                entrepot_selected.append(entrepot)
                store_z.append('Zenodo')
        
    except:
        pass
    reponse_df = pd.DataFrame({'Store':store_z,
                               'Entrepot':entrepot_selected,
                               'ID':identifieurs,
                                'Titre':titre,
                                'Auteur':auteur,
                                "Résumé":resume,
                                "Date de publication":datesPublication,
                                "Publication Url": publication_url})
    return reponse_df

##################################################################################################################
################################################# NAKALA #########################################################
##################################################################################################################
def recuperation_nakala(url_nakala,params_nakala, headers_nakala):
    
    r = requests.get(url_nakala,
                    params=params_nakala,
                    headers=headers_nakala)
    
    return r.json()['datas']


def Recup_contenu_nakala(url_nakala,params_nakala, headers_nakala, entrepot_data):
    entrepot_selected = []
    store_n = []
    identifieurs = []
    titre = []
    auteur = []
    datesPublication = []
    publication_url = []
    try:
        contenu_nakala = recuperation_nakala(url_nakala,params_nakala, headers_nakala)
        #st.write(contenu_nakala)
        for i in range(len(contenu_nakala)):
            try:
                identifieurs.append(contenu_nakala[i]['identifier'])
            except:
                identifieurs.append("")
            try:
                datesPublication.append(contenu_nakala[i]['creDate'])
            except:
                datesPublication.append("")
            try:
                titre.append(contenu_nakala[i]['metas'][0]['value'])
            except:
                titre.append("")
            try:
                auteur.append(contenu_nakala[i]['rights'][0]['name'])
            except:
                auteur.append("")
            try:
                publication_url.append(contenu_nakala[i]['uri'])
            except:
                publication_url.append("")
            entrepot_selected.append(entrepot_data)
            store_n.append('Nakala')
    
    except:
        pass
    reponse_df = pd.DataFrame({'Store':store_n,
                               'Entrepot':entrepot_selected,
                               'ID':identifieurs,
                                'Titre':titre,
                                'Auteur':auteur,
                                'Date de publication':datesPublication,
                                'Publication Url':publication_url})

    return reponse_df


#################################################################################################################
################################################## DRYAD ########################################################
#################################################################################################################
def recuperation_dryad(url_dryad,params_dryad):
    r = requests.get(url_dryad,
                    params=params_dryad)
    
    return r.json()

##################################################################################################################
######### RECUPERATION DRYAD #####################################################################################
def Recup_contenu_dryad(url_dryad,params_dryad,entrepot):
    entrepot_selected = []
    identifieurs = []
    store_dryad = []
    titre = []
    auteur_prenom1 = []
    auteur_nom1 = []
    auteur_affiliation1 = []
    auteur_email1 = []
    auteur_prenom2 = []
    auteur_nom2 = []
    auteur_affiliation2 = []
    auteur_email2 = []
    auteur_prenom3 = []
    auteur_nom3 = []
    auteur_affiliation3 = []
    auteur_email3 = []
    resume = []
    datesPublication = []
    auteur_affiliation1 = []
    auteur_email1 = []
    subject = []
    publication_url = []
    try:
        contenu_dryad = recuperation_dryad(url_dryad,params_dryad)
        #st.write(contenu_dryad)
        Nombre_dryad = contenu_dryad['count']
        if Nombre_dryad !=0:
            for i in range(Nombre_dryad):
                try:
                    identifieurs.append(contenu_dryad['_embedded']['stash:datasets'][i]['identifier'])
                except:
                    identifieurs.append("")
                try:
                    titre.append(contenu_dryad['_embedded']['stash:datasets'][i]['title'])
                except:
                    titre.append("")
                try:
                    resume.append(md(contenu_dryad['_embedded']['stash:datasets'][i]['abstract']))
                except:
                    resume.append("")
                try:
                    datesPublication.append(contenu_dryad['_embedded']['stash:datasets'][i]['publicationDate'])
                except:
                    datesPublication.append("")
                try:
                    publication_url.append(contenu_dryad['_embedded']['stash:datasets'][i]['sharingLink'])
                except:
                    publication_url.append("")
                try:
                    subject.append(contenu_dryad['_embedded']['stash:datasets'][i]['fieldOfScience'])
                except:
                    subject.append("")
                try:
                    auteur_prenom1.append(contenu_dryad['_embedded']['stash:datasets'][i]['authors'][0]['firstName'])
                except:
                    auteur_prenom1.append("")
                try: 
                    auteur_nom1.append(contenu_dryad['_embedded']['stash:datasets'][i]['authors'][0]['lastName'])
                except:
                    auteur_nom1.append("")
                try:
                    auteur_affiliation1.append(contenu_dryad['_embedded']['stash:datasets'][i]['authors'][0]['affiliation'])
                except:
                    auteur_affiliation1.append("")
                try:
                    auteur_email1.append(contenu_dryad['_embedded']['stash:datasets'][i]['authors'][0]['email'])
                except:
                    auteur_email1.append("")   
                try:
                    auteur_prenom2.append(contenu_dryad['_embedded']['stash:datasets'][i]['authors'][1]['firstName'])
                except:
                    auteur_prenom2.append("")
                try:    
                    auteur_nom2.append(contenu_dryad['_embedded']['stash:datasets'][i]['authors'][1]['lastName'])
                except:
                    auteur_nom2.append("")
                try:
                    auteur_affiliation2.append(contenu_dryad['_embedded']['stash:datasets'][i]['authors'][1]['affiliation'])
                except:
                    auteur_affiliation2.append("")
                try:
                    auteur_email2.append(contenu_dryad['_embedded']['stash:datasets'][i]['authors'][1]['email'])
                except:
                    auteur_email2.append("")
                try:
                    auteur_prenom3.append(contenu_dryad['_embedded']['stash:datasets'][i]['authors'][2]['firstName'])
                except:
                    auteur_prenom3.append("")
                try:
                    auteur_nom3.append(contenu_dryad['_embedded']['stash:datasets'][i]['authors'][2]['lastName'])
                except:
                    auteur_nom3.append("")
                try:
                    auteur_affiliation3.append(contenu_dryad['_embedded']['stash:datasets'][i]['authors'][2]['affiliation'])
                except:
                    auteur_affiliation3.append("")
                try:
                    auteur_email3.append(contenu_dryad['_embedded']['stash:datasets'][i]['authors'][2]['email'])
                except:
                    auteur_email3.append("")
                entrepot_selected.append(entrepot)
                store_dryad.append('Dryad')
    except:
        pass

    df_dryad = pd.DataFrame({'Store':store_dryad,
                             'Entrepot':entrepot_selected,
                             'ID':identifieurs,
                            'Date de publication':datesPublication,
                            'Titre':titre,
                            'Auteur prénom 1':auteur_prenom1,
                            'Auteur Nom 1':auteur_nom1,
                            'Organisation 1':auteur_affiliation1,
                            "Email 1":auteur_email1,
                            'Auteur prénom 2':auteur_prenom2,
                            'Auteur Nom 2':auteur_nom2,
                            'Organisation 2':auteur_affiliation2,
                            "Email 2":auteur_email2,
                            'Auteur prénom 3':auteur_prenom3,
                            'Auteur Nom 3':auteur_nom3,
                            'Organisation 3':auteur_affiliation3,
                            "Email 3":auteur_email3,
                            'Résumé':resume,
                            'Thème':subject,
                            'Publication URL':publication_url
                                })
    return Nombre_dryad, df_dryad

#################################################################################################################
#################################################### GBIF #######################################################
#################################################################################################################
def recuperation_gbif(url_gbif,params_gbif, headers_gbif):
    
    r = requests.get(url_gbif,
                    params=params_gbif,
                    headers=headers_gbif)
    
    return r.json()

##################################################################################################################
######### RECUPERATION GBIF ######################################################################################
def Recup_contenu_gbif(url_gbif,params_gbif,headers_gbif,entrepot):
    entrepot_selected = []
    identifieurs = []
    store_gbif = []
    titre = []
    auteur_prenom1 = []
    auteur_nom1 = []
    auteur_affiliation1 = []
    auteur_email1 = []
    resume = []
    datesPublication = []
    publication_url = []
    try:
        contenu_gbif = recuperation_gbif(url_gbif,params_gbif, headers_gbif)
        Nombre_gbif = contenu_gbif['count']
        if Nombre_gbif !=0:
            for i in range(Nombre_gbif):
                try:
                    identifieurs.append(contenu_gbif['results'][i]['doi'])
                except:
                    identifieurs.append("")
                try:
                    titre.append(contenu_gbif['results'][i]['title'])
                except:
                    titre.append("")
                try:
                    resume.append(contenu_gbif['results'][i]['description'])
                except:
                    resume.append("")
                try:
                    auteur_prenom1.append(contenu_gbif['results'][i]['contacts'][0]['firstName'])
                except:
                    auteur_prenom1.append("")
                try:
                    auteur_nom1.append(contenu_gbif['results'][i]['contacts'][0]['lastName'])
                except:
                    auteur_nom1.append("")
                try:
                    auteur_affiliation1.append(contenu_gbif['results'][i]['contacts'][0]['organization'])
                except:
                    auteur_affiliation1.append("")
                try:
                    auteur_email1.append(contenu_gbif['results'][i]['contacts'][0]['email'][0])
                except:
                    auteur_email1.append("")
                try:
                    if contenu_gbif['results'][i]['identifiers'][1]['type']=='URL':
                        publication_url.append(contenu_gbif['results'][i]['identifiers'][1]['identifier'])
                    elif contenu_gbif['results'][i]['identifiers'][0]['type']=='URL':
                        publication_url.append(contenu_gbif['results'][i]['identifiers'][0]['identifier'])
                    elif contenu_gbif['results'][i]['identifiers'][2]['type']=='URL':
                        publication_url.append(contenu_gbif['results'][i]['identifiers'][2]['identifier'])
                    else:
                        publication_url.append("")
                except:
                    publication_url.append("")
                try:
                    datesPublication.append(contenu_gbif['results'][i]['pubDate'])
                except:
                    datesPublication.append("")
                entrepot_selected.append(entrepot)
                store_gbif.append('GBIF')
    except:
        pass
    df_gbif = pd.DataFrame({'Store':store_gbif,
                            'Entrepot':entrepot_selected,
                             'ID':identifieurs,
                            'Date de publication':datesPublication,
                            'Titre':titre,
                            'Auteur prénom 1':auteur_prenom1,
                            'Auteur Nom 1':auteur_nom1,
                            'Organisation 1':auteur_affiliation1,
                            "Email 1":auteur_email1,
                            'Résumé':resume,
                            'Publication URL':publication_url
                                })
    return df_gbif


##################################################################################################################
######### FILTRATION DES CONTENUS ################################################################################
def search_in_json(data, search_string):
    if isinstance(data, dict):
        # If data is a dictionary, search in values recursively
        for key, value in data.items():
            if search_string in key.lower() or search_in_json(value, search_string):
                return True
    elif isinstance(data, list):
        # If data is a list, search in each item recursively
        for item in data:
            if search_in_json(item, search_string):
                return True
    elif isinstance(data, str):
        # If data is a string, check if search_string is in it
        if search_string in data.lower():
            return True
    return False


##################################################################################################################
######### RECUPERATION CONTENU DATAVERSE #########################################################################
def Recup_contenu_dataverse(api,s):
    datav = api.get_dataverse_contents(s)
    datav_contenu = datav.json()
    return datav_contenu

##################################################################################################################
######### RECUPERATION CONTENU DATASET ###########################################################################
def Recup_contenu_dataset(api,persistenteUrl):
    dataset = api.get_dataset(persistenteUrl)
    dataset_contenu = dataset.json()
    return dataset_contenu

##################################################################################################################
######### RECUP GLOBAL DATAVERSE #################################################################################
def Recup_contenu(api,s, entrepot_data, entrepot):
    identifieurs = []
    persistentUrls = []
    datesPublication = []
    selections = []
    entrepot_selected = []
    entrepot_dataverses = []
    titre = []
    auteur = []
    auteur_affiliation = []
    auteur_email = []
    resume = []
    subject = []
    publication_url = []
    checks = []
    try:
        datav_contenu = Recup_contenu_dataverse(api,s)
        if len(datav_contenu['data'])==0:
            pass
        else:
            for j in range(len(datav_contenu['data'])):
                test_type = datav_contenu["data"][j]['type']
                if test_type =="dataverse":
                    s2 = datav_contenu["data"][j]['id']
                    sousdatav_contenu = Recup_contenu_dataverse(api,s2)
                    for k in range(len(sousdatav_contenu['data'])):
                        try:
                            identifieur = sousdatav_contenu["data"][k]['identifier']
                            identifieurs.append(identifieur)
                        except:
                            identifieurs.append("")
                        try: 
                            publicationDate = sousdatav_contenu["data"][k]['publicationDate']
                            datesPublication.append(publicationDate)
                        except:
                            datesPublication.append("")
                        try: 
                            persistentUrl = sousdatav_contenu["data"][k]['persistentUrl'].replace('https://doi.org/','doi:')
                            persistentUrls.append(persistentUrl)
                            try:
                                contenu = api.get_dataset_versions(persistentUrl)
                                contenu_json = contenu.json()
                                try:
                                    check = search_in_json(contenu_json, entrepot.lower())
                                    checks.append(check)
                                except:
                                    checks.append(False)
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][0]['typeName']=='title':
                                        titre.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][0]['value'])
                                    else:
                                        titre.append('')
                                except:
                                    titre.append('')
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['typeName']=='datasetContact':
                                        auteur.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactName']['value'])
                                    elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='datasetContact':
                                        auteur.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['datasetContactName']['value'])
                                    else:
                                        auteur.append('')
                                except:
                                    auteur.append('')
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['typeName']=='datasetContact':
                                        auteur_affiliation.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactAffiliation']['value'])
                                    elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='datasetContact':
                                        auteur_affiliation.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['datasetContactAffiliation']['value'])
                                    else:
                                        auteur_affiliation.append('')
                                except:
                                    auteur_affiliation.append('')
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['typeName']=='datasetContact':
                                        auteur_email.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactEmail']['value'])
                                    elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='datasetContact':
                                        auteur_email.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['datasetContactEmail']['value'])
                                    else:
                                        auteur_email.append('')
                                except:
                                    auteur_email.append('')
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='dsDescription':
                                        resume.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['dsDescriptionValue']['value'])
                                    elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['typeName']=='dsDescription':
                                        resume.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['value'][0]['dsDescriptionValue']['value'])
                                    else:
                                        resume.append('')
                                except:
                                    resume.append('')
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['typeName']=='subject':
                                        subject.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['value'][0])
                                    elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][5]['typeName']=='subject':
                                        subject.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][5]['value'][0])
                                    else:
                                        subject.append('')
                                except:
                                    subject.append('')
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][6]['typeName']=='publication':
                                        publication_url.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][6]['value'][0]['publicationURL']['value'])
                                    elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][7]['typeName']=='publication':
                                        publication_url.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][7]['value'][0]['publicationURL']['value'])
                                    else:
                                        publication_url.append('')
                                except:
                                    publication_url.append('')
                            except:
                                titre.append("")
                                auteur.append('')
                                auteur_affiliation.append('')
                                auteur_email.append('')
                                resume.append('')
                                subject.append('')
                                publication_url.append('')
                                checks.append(False)
                        except:
                            persistentUrls.append("")
                            titre.append("")
                            auteur.append('')
                            auteur_affiliation.append('')
                            auteur_email.append('')
                            resume.append('')
                            subject.append('')
                            publication_url.append('')
                            checks.append(False)
                        selections.append(s)
                        entrepot_selected.append(entrepot)
                        entrepot_dataverses.append(entrepot_data)
                        
                elif test_type == "dataset":
                    
                    try:
                        identifieur = datav_contenu["data"][j]['identifier']
                        identifieurs.append(identifieur)
                    except:
                        identifieurs.append("")
                    try: 
                        publicationDate = datav_contenu["data"][j]['publicationDate']
                        datesPublication.append(publicationDate)
                    except:
                        datesPublication.append("")
                    try: 
                        persistentUrl = datav_contenu["data"][j]['persistentUrl'].replace('https://doi.org/','doi:')
                        persistentUrls.append(persistentUrl)
                        try:
                            contenu = api.get_dataset_versions(persistentUrl)
                            contenu_json = contenu.json()
                            #st.write(contenu_json)
                            try:
                                check = search_in_json(contenu_json, entrepot.lower())
                                checks.append(check)
                            except:
                                checks.append(False)
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][0]['typeName']=='title':
                                    titre.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][0]['value'])
                                else:
                                    titre.append('')
                            except:
                                titre.append('')
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['typeName']=='datasetContact':
                                    auteur.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactName']['value'])
                                elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='datasetContact':
                                    auteur.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['datasetContactName']['value'])
                                else:
                                    auteur.append('')
                            except:
                                auteur.append('')
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['typeName']=='datasetContact':
                                    auteur_affiliation.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactAffiliation']['value'])
                                elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='datasetContact':
                                    auteur_affiliation.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['datasetContactAffiliation']['value'])
                                else:
                                    auteur_affiliation.append('')
                            except:
                                    auteur_affiliation.append('')
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['typeName']=='datasetContact':
                                    auteur_email.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactEmail']['value'])
                                elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='datasetContact':
                                    auteur_email.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['datasetContactEmail']['value'])
                                else:
                                    auteur_email.append('')
                            except:
                                auteur_email.append('')
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='dsDescription':
                                   resume.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['dsDescriptionValue']['value'])
                                elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['typeName']=='dsDescription':
                                    resume.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['value'][0]['dsDescriptionValue']['value'])
                                else:
                                    resume.append('')
                            except:
                                resume.append('')
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['typeName']=='subject':
                                    subject.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['value'][0])
                                elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][5]['typeName']=='subject':
                                    subject.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][5]['value'][0])
                                else:
                                    subject.append('')
                            except:
                                subject.append('')
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][6]['typeName']=='publication':
                                    publication_url.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][6]['value'][0]['publicationURL']['value'])
                                elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][7]['typeName']=='publication':
                                    publication_url.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][7]['value'][0]['publicationURL']['value'])
                                else:
                                    publication_url.append('')
                            except:
                                publication_url.append('')
                        except:
                            titre.append("")
                            auteur.append('')
                            auteur_affiliation.append('')
                            auteur_email.append('')
                            resume.append('')
                            subject.append('')
                            publication_url.append('')
                            checks.append(False)
                    except:
                        persistentUrls.append("")
                        titre.append("")
                        auteur.append('')
                        auteur_affiliation.append('')
                        auteur_email.append('')
                        resume.append('')
                        subject.append('')
                        publication_url.append('')
                        checks.append(False)
                    selections.append(s)
                    entrepot_selected.append(entrepot)
                    entrepot_dataverses.append(entrepot_data)
    except:
        pass
    df_entrepot = pd.DataFrame({'selection':selections, 
                                'Entrepot':entrepot_selected,
                                'Store':entrepot_dataverses,
                                'ID':identifieurs,
                                'Url':persistentUrls,
                                'Date de publication':datesPublication,
                                'Titre':titre,
                                'Auteur':auteur,
                                'Organisation':auteur_affiliation,
                                "Email":auteur_email,
                                'Résumé':resume,
                                'Thème':subject,
                                'Publication URL':publication_url,
                                'Check':checks
                                })
    return df_entrepot


def Recup_contenu_sans_check(api,s, entrepot_data, entrepot):
    identifieurs = []
    persistentUrls = []
    datesPublication = []
    selections = []
    entrepot_selected = []
    entrepot_dataverses = []
    titre = []
    auteur = []
    auteur_affiliation = []
    auteur_email = []
    resume = []
    subject = []
    publication_url = []
    try:
        datav_contenu = Recup_contenu_dataverse(api,s)
        if len(datav_contenu['data'])==0:
            pass
        else:
            for j in range(len(datav_contenu['data'])):
                test_type = datav_contenu["data"][j]['type']
                if test_type =="dataverse":
                    s2 = datav_contenu["data"][j]['id']
                    sousdatav_contenu = Recup_contenu_dataverse(api,s2)
                    for k in range(len(sousdatav_contenu['data'])):
                        try:
                            identifieur = sousdatav_contenu["data"][k]['identifier']
                            identifieurs.append(identifieur)
                        except:
                            identifieurs.append("")
                        try: 
                            publicationDate = sousdatav_contenu["data"][k]['publicationDate']
                            datesPublication.append(publicationDate)
                        except:
                            datesPublication.append("")
                        try: 
                            persistentUrl = sousdatav_contenu["data"][k]['persistentUrl'].replace('https://doi.org/','doi:')
                            persistentUrls.append(persistentUrl)
                            try:
                                contenu = api.get_dataset_versions(persistentUrl)
                                contenu_json = contenu.json()
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][0]['typeName']=='title':
                                        titre.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][0]['value'])
                                    else:
                                        titre.append('')
                                except:
                                    titre.append('')
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['typeName']=='datasetContact':
                                        auteur.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactName']['value'])
                                    elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='datasetContact':
                                        auteur.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['datasetContactName']['value'])
                                    else:
                                        auteur.append('')
                                except:
                                    auteur.append('')
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['typeName']=='datasetContact':
                                        auteur_affiliation.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactAffiliation']['value'])
                                    elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='datasetContact':
                                        auteur_affiliation.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['datasetContactAffiliation']['value'])
                                    else:
                                        auteur_affiliation.append('')
                                except:
                                    auteur_affiliation.append('')
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['typeName']=='datasetContact':
                                        auteur_email.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactEmail']['value'])
                                    elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='datasetContact':
                                        auteur_email.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['datasetContactEmail']['value'])
                                    else:
                                        auteur_email.append('')
                                except:
                                    auteur_email.append('')
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='dsDescription':
                                        resume.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['dsDescriptionValue']['value'])
                                    elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['typeName']=='dsDescription':
                                        resume.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['value'][0]['dsDescriptionValue']['value'])
                                    else:
                                        resume.append('')
                                except:
                                    resume.append('')
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['typeName']=='subject':
                                        subject.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['value'][0])
                                    elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][5]['typeName']=='subject':
                                        subject.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][5]['value'][0])
                                    else:
                                        subject.append('')
                                except:
                                    subject.append('')
                                try:
                                    if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][6]['typeName']=='publication':
                                        publication_url.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][6]['value'][0]['publicationURL']['value'])
                                    elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][7]['typeName']=='publication':
                                        publication_url.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][7]['value'][0]['publicationURL']['value'])
                                    else:
                                        publication_url.append('')
                                except:
                                    publication_url.append('')
                            except:
                                titre.append("")
                                auteur.append('')
                                auteur_affiliation.append('')
                                auteur_email.append('')
                                resume.append('')
                                subject.append('')
                                publication_url.append('')
                        except:
                            persistentUrls.append("")
                            titre.append("")
                            auteur.append('')
                            auteur_affiliation.append('')
                            auteur_email.append('')
                            resume.append('')
                            subject.append('')
                            publication_url.append('')
                        selections.append(s)
                        entrepot_selected.append(entrepot)
                        entrepot_dataverses.append(entrepot_data)
                        
                elif test_type == "dataset":
                    
                    try:
                        identifieur = datav_contenu["data"][j]['identifier']
                        identifieurs.append(identifieur)
                    except:
                        identifieurs.append("")
                    try: 
                        publicationDate = datav_contenu["data"][j]['publicationDate']
                        datesPublication.append(publicationDate)
                    except:
                        datesPublication.append("")
                    try: 
                        persistentUrl = datav_contenu["data"][j]['persistentUrl'].replace('https://doi.org/','doi:')
                        persistentUrls.append(persistentUrl)
                        try:
                            contenu = api.get_dataset_versions(persistentUrl)
                            contenu_json = contenu.json()
                            #st.write(contenu_json)
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][0]['typeName']=='title':
                                    titre.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][0]['value'])
                                else:
                                    titre.append('')
                            except:
                                titre.append('')
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['typeName']=='datasetContact':
                                    auteur.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactName']['value'])
                                elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='datasetContact':
                                    auteur.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['datasetContactName']['value'])
                                else:
                                    auteur.append('')
                            except:
                                auteur.append('')
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['typeName']=='datasetContact':
                                    auteur_affiliation.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactAffiliation']['value'])
                                elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='datasetContact':
                                    auteur_affiliation.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['datasetContactAffiliation']['value'])
                                else:
                                    auteur_affiliation.append('')
                            except:
                                    auteur_affiliation.append('')
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['typeName']=='datasetContact':
                                    auteur_email.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactEmail']['value'])
                                elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='datasetContact':
                                    auteur_email.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['datasetContactEmail']['value'])
                                else:
                                    auteur_email.append('')
                            except:
                                auteur_email.append('')
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['typeName']=='dsDescription':
                                   resume.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][3]['value'][0]['dsDescriptionValue']['value'])
                                elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['typeName']=='dsDescription':
                                    resume.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['value'][0]['dsDescriptionValue']['value'])
                                else:
                                    resume.append('')
                            except:
                                resume.append('')
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['typeName']=='subject':
                                    subject.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][4]['value'][0])
                                elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][5]['typeName']=='subject':
                                    subject.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][5]['value'][0])
                                else:
                                    subject.append('')
                            except:
                                subject.append('')
                            try:
                                if contenu_json['data'][0]['metadataBlocks']['citation']['fields'][6]['typeName']=='publication':
                                    publication_url.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][6]['value'][0]['publicationURL']['value'])
                                elif contenu_json['data'][0]['metadataBlocks']['citation']['fields'][7]['typeName']=='publication':
                                    publication_url.append(contenu_json['data'][0]['metadataBlocks']['citation']['fields'][7]['value'][0]['publicationURL']['value'])
                                else:
                                    publication_url.append('')
                            except:
                                publication_url.append('')
                        except:
                            titre.append("")
                            auteur.append('')
                            auteur_affiliation.append('')
                            auteur_email.append('')
                            resume.append('')
                            subject.append('')
                            publication_url.append('')
                    except:
                        persistentUrls.append("")
                        titre.append("")
                        auteur.append('')
                        auteur_affiliation.append('')
                        auteur_email.append('')
                        resume.append('')
                        subject.append('')
                        publication_url.append('')
                    selections.append(s)
                    entrepot_selected.append(entrepot)
                    entrepot_dataverses.append(entrepot_data)
    except:
        pass
    df_entrepot = pd.DataFrame({'selection':selections, 
                                'Entrepot':entrepot_selected,
                                'Store':entrepot_dataverses,
                                'ID':identifieurs,
                                'Url':persistentUrls,
                                'Date de publication':datesPublication,
                                'Titre':titre,
                                'Auteur':auteur,
                                'Organisation':auteur_affiliation,
                                "Email":auteur_email,
                                'Résumé':resume,
                                'Thème':subject,
                                'Publication URL':publication_url
                                })
    return df_entrepot


#######################################################################################################################################
############# POUR CONNAITRE LES IDENTIFIANTS DES DATAVERSES ############
#######################################################################################################################################

##################################################################################################################
######### RECUPERATION DES ENTREPOTS RDG #########################################################################
def Recup_dataverses_rdg(api, fichier):
    RDG = api.get_dataverse_contents("root")
    RDG_json = RDG.json()
    liste_dataverses_1= []
    liste_ids = []
    for d in range(len(RDG_json['data'])):
        if RDG_json['data'][d]['type']=="dataverse":
            liste_dataverses_1.append(RDG_json['data'][d]['title'])
            liste_ids.append(RDG_json['data'][d]['id'])

    df_liste_dataverses_1=pd.DataFrame(data=[liste_dataverses_1,liste_ids], index=['Dataverses_niv1','Ids'])
    df_liste_dataverses_1=df_liste_dataverses_1.T
    
    liste = []
    ids = []
    for i in range(len(df_liste_dataverses_1)):
        datav = api.get_dataverse_contents(df_liste_dataverses_1.loc[i,'Ids'])
        datav_dv = datav.json()
        liste_dataverses_2 = []
        ids_niv2 = []
        for d in range(len(datav_dv['data'])):
            try:
                if datav_dv['data'][d]['type']=="dataverse":
                    liste_dataverses_2.append(datav_dv['data'][d]['title'])
                    ids_niv2.append(datav_dv['data'][d]['id'])
            except:
                    liste_dataverses_2.append()
                    ids_niv2.append()
        liste.append(liste_dataverses_2)
        ids.append(ids_niv2)
            
    df_liste_dataverses_1['Dataverses_niv2']=liste
    df_liste_dataverses_1['Ids_niv2']=ids
    df_liste_dataverses_1.to_csv(f"pages/data/rechercheDataGouv/liste_dataverses_rdg.csv")
            
    df_liste_dataverses_2=pd.DataFrame(data=[liste,ids], index=['Dataverses_niv2','Ids_niv2'])
    df_liste_dataverses_2=df_liste_dataverses_2.T
    df_liste_dataverses_2.to_csv(f"pages/data/rechercheDataGouv/liste_dataverses_rdg2.csv")

    data = pd.read_csv(f"pages/data/rechercheDataGouv/liste_dataverses_rdg.csv")
    data.drop(columns=['Unnamed: 0'], inplace=True)
    for i in range(len(data)):
            data.loc[i,'val']=int(len(re.split(',',data.loc[i,'Dataverses_niv2'].replace('[','').replace(']','').replace("'",'').strip())))

    som = sum(data['val'].values)
    new_data = pd.DataFrame(index=np.arange(0,som), columns=['niv1','niv2'])
    i=0
    for j in range(len(data)):
        for k in range(int(data.loc[j,'val'])):
            new_data.loc[i,'niv1']=data.loc[j,'Dataverses_niv1']
            new_data.loc[i,'ids_niv1']=data.loc[j,'Ids']
            new_data.loc[i,'niv2']=re.split(',',data.loc[j,'Dataverses_niv2'].replace('[','').replace(']','').strip())[k]
            new_data.loc[i,'niv2']=new_data.loc[i,'niv2'].replace("'","")
            try:
                new_data.loc[i,'ids_niv2']=re.split(',',data.loc[j,'Ids_niv2'].replace('[','').replace(']','').replace('"','').strip())[k]
            except:
                pass
            i+=1
            print(i)
    new_data['val']=1
    new_data['niv0']="Recherche Data Gouv"
    new_data.to_csv(f"pages/data/rechercheDataGouv/{fichier}")



##################################################################################################################
######### RECUPERATION DES ENTREPOTS DATA INDORES ################################################################
def Recup_dataverses(api, fichier):
    # On peut aller chercher le contenu du dataverse
        # le status est rappelé puis on a une clé "data" dans laquelle on retrouve son contenu.
        # Pour dataindores: d'autres sous-dataverses!
        dataindores = api.get_dataverse_contents("dataindores")
        data_indores = dataindores.json()
        # Ici on récupère les noms de ces dataverses et les id 
        # On crée un premier tableau avec ces élements
        liste_dataverses_1= []
        liste_ids = []
        for d in range(len(data_indores['data'])):
            if data_indores['data'][d]['type']=="dataverse":
                liste_dataverses_1.append(data_indores['data'][d]['title'])
                liste_ids.append(data_indores['data'][d]['id'])
        df_liste_dataverses_1=pd.DataFrame(data=[liste_dataverses_1,liste_ids], index=['Dataverses_niv1','Ids'])
        df_liste_dataverses_1=df_liste_dataverses_1.T
        # A partir de ce tableau, pour chacun des dataverses répertoriés (niv1), on récupère les noms des sous-dataverses (niv2) 
        # On enregistre ces infos dans un csv
        liste = []
        ids = []
        for i in range(len(df_liste_dataverses_1)):
            datav = api.get_dataverse_contents(df_liste_dataverses_1.loc[i,'Ids'])
            datav_dv = datav.json()
            liste_dataverses_2 = []
            ids_niv2 = []
            for d in range(len(datav_dv['data'])):
                try:
                    if datav_dv['data'][d]['type']=="dataverse":
                        liste_dataverses_2.append(datav_dv['data'][d]['title'])
                        ids_niv2.append(datav_dv['data'][d]['id'])
                except:
                        liste_dataverses_2.append()
                        ids_niv2.append()
            liste.append(liste_dataverses_2)
            ids.append(ids_niv2)
            
        df_liste_dataverses_1['Dataverses_niv2']=liste
        df_liste_dataverses_1['Ids_niv2']=ids
        df_liste_dataverses_1.to_csv(f"pages/data/Data_InDoRES/liste_dataverses.csv")
            
        df_liste_dataverses_2=pd.DataFrame(data=[liste,ids], index=['Dataverses_niv2','Ids_niv2'])
        df_liste_dataverses_2=df_liste_dataverses_2.T
        df_liste_dataverses_2.to_csv(f"pages/data/Data_InDoRES/liste_dataverses2.csv")

        data = pd.read_csv(f"pages/data/Data_InDoRES/liste_dataverses.csv")
        data.drop(columns=['Unnamed: 0'], inplace=True)
        for i in range(len(data)):
                data.loc[i,'val']=int(len(re.split(',',data.loc[i,'Dataverses_niv2'].replace('[','').replace(']','').replace("'",'').strip())))

        som = sum(data['val'].values)
        new_data = pd.DataFrame(index=np.arange(0,som), columns=['niv1','niv2'])
        i=0
        for j in range(len(data)):
            for k in range(int(data.loc[j,'val'])):
                new_data.loc[i,'niv1']=data.loc[j,'Dataverses_niv1']
                new_data.loc[i,'ids_niv1']=data.loc[j,'Ids']
                new_data.loc[i,'niv2']=re.split(',',data.loc[j,'Dataverses_niv2'].replace('[','').replace(']','').strip())[k]
                new_data.loc[i,'niv2']=new_data.loc[i,'niv2'].replace("'","")
                new_data.loc[i,'ids_niv2']=re.split(',',data.loc[j,'Ids_niv2'].replace('[','').replace(']','').replace("'",'').strip())[k]
                i+=1
        new_data['val']=1
        new_data['niv0']="Data_InDoRes"
        new_data.to_csv(f"pages/data/Data_InDoRES/{fichier}")

        dat = pd.read_csv(f"pages/data/Data_InDoRES/{fichier}")
        dat_ = dat.copy()
        dat_.drop(columns=['Unnamed: 0'], inplace=True)
        dat_.dropna(axis=0,inplace=True)
        dat_['ids_niv2'] = dat_['ids_niv2'].astype(int)
        liste_bis = []
        ids_bis = []
        for i in range(len(dat)):
            liste_dataverses_3 = []
            ids_niv3 = []
            try:
                datav_ = api.get_dataverse_contents(dat_.loc[i,'ids_niv2'])
                datav_dv_ = datav_.json()       
                try:
                    h = len(datav_dv_['data'])
                    for d in range(h):
                        if datav_dv_['data'][d]['type']=="dataverse":
                            liste_dataverses_3.append(datav_dv_['data'][d]['title'])
                            ids_niv3.append(datav_dv_['data'][d]['id'])
                        else:
                            liste_dataverses_3.append('')
                            ids_niv3.append('')
                except:
                    liste_dataverses_3.append('')
                    ids_niv3.append('')
            except:
                liste_dataverses_3.append('')
                ids_niv3.append('')
            liste_bis.append(liste_dataverses_3)
            ids_bis.append(ids_niv3)

        dat['Dataverses_niv3']=liste_bis
        dat['Ids_niv3']=ids_bis

        for i in range(len(dat)):
            try:
                o = dat.loc[i,'Dataverses_niv3'][0]
                p = dat.loc[i,'Ids_niv3'][0]
                dat.loc[i,'niv3']=o
                dat.loc[i,'ids_niv3']=p
            except:
                dat.loc[i,'niv3']=None
                dat.loc[i,'ids_niv3']=None
        dat.drop(columns=['Dataverses_niv3','Ids_niv3'], inplace=True)
        dat.to_csv(f"pages/data/Data_InDoRES/{fichier}")