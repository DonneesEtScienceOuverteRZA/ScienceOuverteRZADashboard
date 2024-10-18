#### IMPORTATIONS ###
import pandas as pd

fichier1 = "pages/data/uuid_ancienGN_clean.csv"
fichier2 = "pages/data/uuid_cat_InDoRes_clean.csv"

#### MAIN ####
if __name__ == "__main__":
    data1 = pd.read_csv(fichier1, index_col=[0])
    data2 = pd.read_csv(fichier2, index_col=[0])
    print("il y a ", len(data1), " uuids dans l'ancien GN")
    print("il y a ", len(data2), " uuids dans cat.InDoRes")
    col1 = data1.columns.values[0]
    col2 = data2.columns.values[0]

    
    data2["check"]=0
    for i in range(len(data2)):
        for j in range(len(data1)):
            if data2.loc[i, "check"]==1:
                pass
            else: 
                if data1.loc[j,col1]==data2.loc[i,col2]:
                    data2.loc[i,"check"]=1
                else:
                    pass
    data2.to_csv("pages/data/uuid_cat_InDoRes_clean_compared.csv")
    print("il y a ", len(data2[data2["check"]==1]), " uuids dans cat.InDoRes qui étaient dans l'ancien GN")
