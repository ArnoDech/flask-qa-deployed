from flask import Flask, render_template,request
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression

def createapp():
    global returnvaluestest
    returnvaluestest = []


    app=Flask(__name__)


    @app.route('/menu')
    def menu():
        return render_template('menu.html')


    @app.route('/test')
    def home():
        return render_template('index.html')


    @app.route('/traitement',methods=["POST"])
    def recuperation():
        donnees = request.form
        #initialisation des variables de calcul de machine learning
        marque=donnees.get('marque')
        modele=donnees.get('modele')
        designationcommerciale=donnees.get('designationcommerciale')
        carburant=donnees.get('carburant')
        hybride = donnees.get('hybride')
        puissanceadmin=donnees.get('puissanceadmin')
        boitevitesse=donnees.get('boitevitesse')
        co2=donnees.get('co2')
        masse=donnees.get('masse')
        champv9=donnees.get('champv9')
        Carrosserie=donnees.get('Carrosserie')
        gamme=donnees.get('gamme')
        #Construction du DataFrame de valeurs catégorielles
        cat_values=pd.DataFrame([[marque,modele,designationcommerciale,carburant,hybride,boitevitesse,champv9,Carrosserie,gamme]],columns=['lib_mrq','lib_mod_doss','dscom','cod_cbr','hybride','typ_boite_nb_rapp','champ_v9','Carrosserie','gamme'])
        #print(cat_values)
        #Construction du DataFrame de valeurs numériques
        num_values=pd.DataFrame([[puissanceadmin,co2,masse]],columns=['puiss_admin_98','co2','masse_ordma_min'])
        #print(num_values)
        if marque !='' and modele!='' and designationcommerciale!='' and carburant!='' and puissanceadmin !='' and boitevitesse !='' and co2!='' and masse !='' and champv9 !='' and gamme !='' and hybride!='':
            machinelearning(cat_values,num_values,returnvaluestest)
            print(f' La consommation de votre véhicules est de : {returnvaluestest}L/100 Km')
            return render_template("index.html",marque=marque,modele=modele,designationcommerciale=designationcommerciale,carburant=carburant,puissanceadmin=puissanceadmin,boitevitesse=boitevitesse,co2=co2,masse=masse,champv9=champv9, gamme=gamme,returnvaluestest=returnvaluestest)
        else :
            return render_template("index.html")


    #algo de machine learning
    def machinelearning(datacat,datanum,valuestest):
        global returnvaluestest
        data = pd.read_excel('Ref.xlsx')
        data=data.drop(['conso_urb','conso_exurb','masse_ordma_max'],axis=1)
        # remplacement des valeurs nulles du champ V9 par chaine de caractère vide
        data['champ_v9'] = data['champ_v9'].replace(np.nan, '')
        #séparation des variables catégorielles et numériques
        cat = data.select_dtypes(include=['object'])
        num = data.select_dtypes(exclude=['object'])
        cat = pd.concat([cat, datacat], axis=0, ignore_index=True)
        for col in cat:
            cat[col] = cat[col].astype('category')
            cat[col] = cat[col].cat.codes
        predictcat = cat.iloc[55010]
        predictcat = pd.DataFrame([[predictcat[0], predictcat[1], predictcat[2], predictcat[3], predictcat[4],
                                predictcat[5], predictcat[6], predictcat[7], predictcat[8]]],
                              columns=['lib_mrq', 'lib_mod_doss', 'dscom', 'cod_cbr', 'hybride', 'typ_boite_nb_rapp',
                                       'champ_v9', 'Carrosserie', 'gamme'])
        cat = cat.drop([55010])
        num = num.drop(['conso_mixte'], axis=1)
        X = pd.concat([cat, num], axis=1)
        predict = pd.concat([predictcat, datanum], axis=1)
        Y = data['conso_mixte']
        regression_alg = LinearRegression()
        regression_alg.fit(X, Y)
        test_predictions = regression_alg.predict(predict)
        valuestest= test_predictions
        returnvaluestest=valuestest
        returnvaluestest = round(returnvaluestest[0], 2)


    if __name__ =='__main__':
        app.run(debug=True)

    return app