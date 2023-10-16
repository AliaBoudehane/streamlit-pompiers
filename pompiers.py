import streamlit as st
import pandas as pd
pd.set_option('display.max_columns', 60)
import numpy as np

with open('style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.title("Temps de réponse - Brigade des Sapeurs Pompiers de Londres")

sidebar_title = '<p style="color:White; font-size: 26px;">Sommaire</p>'
st.sidebar.markdown(sidebar_title, unsafe_allow_html=True)

pages=["Introduction", "Enrichissements & Data Cleaning","DataVizualization", "Modélisation",
       "Conclusion"]
page=st.sidebar.radio('', pages)

st.sidebar.divider()
st.sidebar.markdown('Auteurs')

st.sidebar.markdown('- <p style="font-size: 14px"> Alia Boudehane | <a href="https://www.linkedin.com/in/alia-boudehane-704172185/" style="color: white;font-size: 14px">LinkedIn</a></p>\
                    \n- <p style="font-size: 14px"> Doravann Chou | <a href="https://www.linkedin.com/in/doravann-chou-81a999269" style="color: white;font-size: 14px">LinkedIn</a></p>\
                    \n- <p style="font-size: 14px"> Maïna Le Roux | <a href="https://www.linkedin.com/in/mainaleroux" style="color: white;font-size: 14px">LinkedIn</a> </p>', unsafe_allow_html=True)


#Page 1
if page == pages[0] : 
  st.image('lfb2.jpeg')
  st.header("Introduction")
  st.subheader('Le Sujet')
  st.markdown("La **:red[London Fire Brigade (LFB)]** est le service d'incendie et de secours le plus actif du pays.\
           Fondée en 1886, elle n'a, depuis lors, cessé de s’améliorer et jouit aujourd’hui d’une réputation reconnue\
            en matière de lutte contre les incendies et de secours d'urgence, faisant d’elle l'une des institutions les\
            plus emblématiques et respectées du pays. \n\n Sur l’année 2014, ils seront notifiés comme étant les sapeurs-pompiers les plus occupés\
            dans le monde en comptabilisant un total de 171 067 appels d’urgence et en traitant 20934 feux ! \
           \nC’est d’ailleurs l’une des plus grandes organisations de lutte contre les incendies et de secours au monde, agissant dans la protection des personnes\
            et biens contre les incendies sur un périmètre de 1587 kilomètres carrés autour du Grand Londres.\
           \n\n Dans cette étude, nous plongerons dans l'analyse des données liées aux performances passées de la London Fire Brigade, en mettant l'accent\
            sur leur **:red[efficacité de temps de réponse].** \n\nNous allons dans un premier temps prendre connaissance de notre jeu de données\
            qui proviennent du site officiel et gouvernemental de la London Fire Brigade. Nous allons étudier puis nettoyer ces données afin de les rendre\
            les plus lisibles et utiles à notre étude.\
           \n\n Nous utiliserons ensuite des techniques d'analyse de données et des modèles de prédiction pour mieux comprendre les tendances historiques\
            et les facteurs qui influencent ces mesures cruciales.")


  st.subheader('Les Données')
  st.markdown('**:red[Source des Jeux de Données]**')
  st.markdown("Nos jeux données sont disponibles sur le site officiel de la ville de Londres - https://data.london.gov.uk, ce qui nous permet d'avoir une entière confiance\
               en leur provenance et leur intégrité. \n\nDurant la phase exploratoire de notre projet, nous avons également été en contact avec des Business\
               Intelligence Analysts de la London Fire Brigade, qui ont répondu rapidement à nos questions, et nous les en remercions.")
  st.markdown('**:red[Description des Données]**')
  st.markdown("Nous avions deux principaux jeux de données disponibles :\
              \n - **Incident Records** : les détails de chaque incident sur lequel la LFB est intervenu depuis le 1er janvier 2009. Des informations sont\
               fournies sur la date et le lieu de l'incident ainsi que sur le type d'incident. \
              \n - **Mobilisation Records** : les détails de chaque véhicule d'incendie envoyé sur les lieux d'un incident depuis janvier 2009.\
              Des informations sont fournies sur l'engin mobilisé, le lieu d'où il a été déployé et les heures d'arrivée sur les lieux de l'incident.")
  
  col1, col2 = st.columns(2)

  with col1:
    st.write("***Incident Records***")
    metadata = pd.read_csv("Metadata.csv")
    st.dataframe(metadata)
  with col2:
    st.write("***Mobilisation Records***")
    metadata_mobi = pd.read_csv("Mobilisations-Metadata.csv")
    st.dataframe(metadata_mobi)

  st.markdown("Nous disposons de 3 colonnes communes aux 2 jeux de données (*IncidentNumber*, *Calyear*, et *HourOfCall*) à partir desquelles\
               nous allons **fusionner nos tables**.")
  
  st.markdown('**:red[DataFrame Consolidé]**')
  st.markdown("Voici un aperçu de notre DataFrame consolidé, avant toute modification :")

  ## Afficher df.head() après fusion
  df_consolidated = pd.read_csv("df_consolidated.csv",index_col = 0)
  df_consolidated.reset_index(inplace = True)
  df_consolidated = df_consolidated.drop(columns = 'index')
  st.dataframe(df_consolidated)

  st.write("La taille de notre dataframe est : **(2220718, 58)**")

  st.markdown("Pour la suite du projet et notamment la partie modélisation, c'est la variable ***:red[AttendanceTimeSeconds]*** que nous choisissons comme\
              notre **variable cible**. Il s'agit du temps de réponse pour un camion mobilisé, comprenant le temps de préparation de la brigade\
               une fois cette dernière informée ainsi que le temps de trajet pour ce rendre sur le lieu de l'incident.")

#Page 2
if page == pages[1] : 
  st.header("Enrichissements & Data Cleaning")
  st.markdown(" ")

  st.subheader('Nos Enrichissements :fire:')
  st.markdown('**:red[La variable Distance]**')
  st.markdown("Nous avons souhaité ajouter à notre dataset la variable ***:red[Distance]***. Cette dernière représente la distance entre la caserne d'où a été mobilisé\
              le camion et le lieu de l'incident, en mètres. Voici comment nous avons procédé : \n\n - **Collecte de données** : pour chaque caserne, nous avons manuellement\
              collecté leurs coordonnées géographiques, soit les latitudes et longitudes.\
              \n - **Conversion de variables** : les données de latitudes et longitudes des lieux d'incidents étant incomplètes (+50% de Nan), nous avons convertis\
               les données *easting_rounded* et *northing_rounded* en latitude et longitude. Nous perdons légèrement en précision sur la localisation exacte mais de façon\
              tout à fait acceptable. \
              \n - **Calcul de la distance** : à partir des coordonnées géographiques des casernes et des lieux d'incidents, nous avons pû calculer une nouvelle variable : la\
               :red[***Distance*** *(en mètre)*] parcourue pour chaque mobilisation.\
              \n - **Vérification** : pour se rassurer sur la pertinence du calcul effectué, nous avons testé plusieurs distances sur Google Maps.")
  
  with st.expander("Calcul de la Distance (code)"):
    code = '''# Fonction pour calculer la distance en mètres entre deux points géographiques (haversine formula)
def haversine(lat1, lon1, lat2, lon2):
    # Rayon de la Terre en mètres
    radius = 6371000

    # Conversion des degrés en radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    # Différences de latitudes et de longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Formule de la haversine
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

    # Distance en mètres
    distance = radius * c
    return distance

# Appliquer la fonction haversine pour calculer la distance et ajouter une colonne "Distance" au DataFrame
df["Distance"] = df.apply(lambda row: haversine(row["Latitude"], row["Longitude"], row["Station_Latitude"], row["Station_Longitude"]), axis=1) '''
    st.code(code,language='python')

  st.markdown(" ")
  st.markdown('**:red[La variable DateOfCall]**')
  st.markdown("Afin de rendre l'analyse plus facile et d'exploiter d'autres axes nous utilisons la variable *'DateOfCall'* pour créer *'MonthOfCall'* et *'DayOfCall'*.")
  st.markdown(" ")

  st.subheader("DataCleaning :male-firefighter:")
  st.markdown("Sans rentrer dans le détail, expliquer les modifications apportées / sélection des variables.\
              \n Afficher un aperçu de df_final\
              et aussi df.info(), autre information intéressante à ce stade")
  
  st.markdown('**:red[Gestion des Doublons]**')
  st.markdown("Nous n'avions aucun doublon dans notre jeu de données.")

  st.markdown('**:red[Gestion des valeurs manquantes]**')
  st.markdown("Concernant les Nans, nous décidons de supprimer toutes les lignes pour lesquels le pourcentage de Nan dans la colonne est inférieur à 2%.\
               Ensuite, pour le reste des valeurs manquantes et afin d’éviter toute fuite de données durant la modélisation nous ne modifierons que les Nans\
              qui ne nécessitent pas une opération de calcul statistique.\
              \n - *DelayCode_Description (75% de Nans)* : il s'agit de la raison pour laquelle la brigade est arrivée en retard sur le lieu de l’incident. Les Nans\
               correspondent aux mobilisations où il n'y a pas eu de retard (onfirmé par le BI Analyst que nous avons contacté). Nous remplaçons donc remplacés par\
                la veleur 'No Delay'.\
               \n - *SpecialServiceType (78% de Nans)* : cette colonne ne contient des informations que si le type de l’intervention est un 'SpecialService'. Nous\
               remplaçon les 78% de Nan par la valeur 'Not a Special Service'.\
              \n\n Suite à la sélection finale des variables que nous conserverons avant d'entâmer la partie modélisation, notre jeu de données ne présente plus aucun Nan.")

  st.markdown('**:red[Variables Conservées dans notre DataFrame Final]**')
  st.markdown("Voici la liste des variables conservées, avant de démarrer nos premières modélisations :\
              \n\n *'IncidentNumber', 'DateOfCall', 'CalYear', 'HourOfCall',\
              'IncidentGroup', 'StopCodeDescription', 'SpecialServiceType', 'PropertyCategory', 'AddressQualifier', 'BoroughName', 'IncidentStationGround',\
              'NumStationsWithPumpsAttending', 'NumPumpsAttending', 'CallCount', 'ResourceMobilisationId', 'TurnoutTimeSeconds', 'TravelTimeSeconds', 'AttendanceTimeSeconds',\
              'DeployedFromStation_Name', 'PumpOrder', 'DelayCode_Description', 'MobilisationTime', 'MonthOfCall', 'DayOfCall', 'Distance'*")
  
  ## Afficher df.head() avant modélisation
  st.markdown('**Aperçu du DataFrame avant la modélisation**')
  df_modelisation = pd.read_csv("df_modelisation.csv",index_col = 0)
  st.dataframe(df_modelisation)

#Page 3
if page == pages[2] : 
  st.header("DataVizualization")
  st.markdown(" ")
  st.subheader("La variable cible : AttendanceTimeSeconds")
  
  ## DataViz : distribution variable cible
  st.markdown('**:red[Distribution de AttendanceTimeSeconds]**')
  st.markdown("Nous constatons visuellement que la distribution de notre variable cible suit une loi normale. La médiane est à 325 secondes,\
               soit **5 minutes et 25 secondes**. Il s'agit donc ici du temps médian pour une équipe de sapeurs-pompiers de se préparer et ce rendre\
              sur les lieux de l'incident. Le maximum est à 1200 secondes, soit 20 min, et il s'agit du seuil maximum utilisé par la LFB elle-même\
              dans ses différents analyses et rapports.")
  st.image('attendancetime_distribution.jpeg')

  ## DataViz Attendance Time selon carte de Londres
  st.markdown(" ")
  st.markdown('**:red[Cartes de Londres]**')
  
  display = st.radio(':gray[Que souhaitez-vous montrer ?]', (':gray[Temps de Réponse par Quartier]', ':gray[Temps de Réponse par Secteur Caserne]'))
  if display == ':gray[Temps de Réponse par Quartier]':
    ## Map par Quartier
    path_to_html = "map2.html" 
    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()
    # Show in streamlit
    st.components.v1.html(html_data,width=800, height=600)
  elif display == ':gray[Temps de Réponse par Secteur Caserne]':
    ## Map par Station Ground
    path_to_html = "map1.html" 
    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()
    # Show in streamlit
    st.components.v1.html(html_data,width=800, height=600)
  
  ## DataViz Attendance Time selon heure de la journée
  st.markdown(" ")
  st.markdown("**:red[Les Temps de Réponse selon l'Heure de la Journée]**")
  st.markdown("Le graphique ci-dessous nous permet de visualiser le **Temps de Préparation** (TurnoutTime), le **Temps de Trajet** (TravelTime)\
              et le **Temps de Réponse** total (AttendanceTime) des brigades selon l'heure de la journée.")
  path_to_plot1 = "plot1.html" 
  with open(path_to_plot1,'r') as f:
    html_data = f.read()
  st.components.v1.html(html_data,width=1000, height=450)

  with st.expander(label = "Lecture du graphique"):
    st.write("**Constat temps de trajet :** Assez logiquement, nous observons que le temps de trajet pour se rendre sur le lieu de l'incident\
              est plus important en journée, au moment où le trafic routier est plus dense. Le temps de trajet est plus rapide entre 21h le soir et 9h le matin.\
            \n\n **Constat temps de trajet temps de préparation (Turnout) :**  Il est intéressant de voir qu'il existe une différence du temps de préparation\
             des équipes entre minuit et 7h du matin. Est-ce dû au fait qu'il y a moins de personnel la nuit ?\
             \n\n**Constat temps de réponse total :** Le temps de réponse total est la somme des deux temps précédents. Les temps forts / faibles de chacune\
              des deux variables précédentes font que le temps total s'équilibre sur la journée, à l'exception du créneau 7h - 10h et  20h et Minuit (temps de trajet ET temps de préparation rapides).")

  ## DataViz Temps de trajet selon le retard
  st.markdown(" ")
  st.markdown("**:red[Temps de Trajet moyen selon la raison du retard]**")
  st.markdown("Le graphique ci-dessous nous permet de visualiser le **Temps de Trajet moyen** (en secondes toujours) selon la raison du retard. Lorsqu'il n'y a pas eu de retard,\
              cela est représenté par la valeur '*No delay*'.")
  path_to_plot5 = "plot5.html" 
  with open(path_to_plot5,'r') as f:
    html_data = f.read()
  st.components.v1.html(html_data,width=800, height=450)

  with st.expander(label = "Lecture du graphique"):
    st.write("**Constat :** Sans surprise, lorsqu'il n'y a pas de retard le temps de trajet est exemplaire. Par ailleurs, le motif d' *'Adresse incomplète'*\
            est celui qui fait le plus perdre de temps aux equipes, suivi d'une autre cause moins explicite qui indique que l'équipe est arrivée mais\
            qu'elle a été retenue pour une autre raison ou encore que l'équipe était déjà en intervention à l'exterieur au moment de l'appel par le centre de contrôle.")

## DataViz Temps de réponse et Distance
  st.markdown(" ")
  st.markdown("**:red[Temps de Trajet moyen et Distance moyenne parcourue par Quartier]**")
  st.markdown("Le graphique ci-dessous affiche par quartier de Londres le Temps de Réponse moyen ainsi que la Distance moyenne parcourue")
  
  path_to_plot6 = "plot6.html" 
  with open(path_to_plot6,'r') as f:
    html_data = f.read()
  st.components.v1.html(html_data,width=1000, height=450)

  with st.expander(label = "Lecture du graphique"):
    st.write("**Constat :** Alors que nous pensions plus évidente la corrélation entre le Temps de Réponse et la Distance, nous constatons ici, en regardant ces deux métriques\
             par Quartier de Londres, qu'il n'existe pas de façon évidente une relation entre ces deux variables.")

## DataViz Volume d'Incidents et de Mobilisations
  st.markdown(" ")
  st.subheader("Le volume d'Incidents et de Mobilisations")

  ## DataViz Nombre d'incident selon heure de la journée
  st.markdown("**:red[Nombre d'Incidents selon Heure de la Journée]**")
  st.markdown("Le graphique ci-dessous nous permet de visualiser le **Volume d'incidents** selon l'heure de la journée, avec une disctinction faite selon le **Type d'incident**.\
              Il est également possible d'afficher l'année de son choix.")
  path_to_plot2 = "plot2.html" 
  with open(path_to_plot2,'r') as f:
    html_data = f.read()
  st.components.v1.html(html_data,width=900, height=450)

  with st.expander(label = "Lecture du graphique"):
    st.write("**Constat :** Il est nettement visible - et c'est assez logique - qu'il existe une différence du volume d’incidents selon l’heure de la journée\
            et cela quelque soit l'année. Le graphique nous montre également une surreprésentation des incidents de type “False Alarm”.")

  ## DataViz Nombre de mobilisation par quartier
  st.markdown(" ")
  st.markdown("**:red[Répartition des Mobilisations par Quartier]**")
  st.markdown("Le graphique ci-dessous nous permet de visualiser la **quantité de mobilisations** selon les quartiers de Londres, **depuis 2009**,\
              en mettant également en avant le type d'incident. Les quartiers sont triés de façon descendante selon la moyenne du Temps de Réponse ")
  path_to_plot3 = "plot3.html" 
  with open(path_to_plot3,'r') as f:
    html_data = f.read()
  st.components.v1.html(html_data,width=1000, height=450)

  with st.expander(label = "Lecture du graphique"):
    st.write("**Constat :** Nous observons que certains des quartiers qui ont un bon temps de réponse ont aussi une grosse proportion de fausses alarmes. Aussi,\
             la quantité d'incidents ne semble pas influencer la performance de rapidité du temps de réponse. Le type d'incident ne doit donc que partiellement\
            influencer la disparité des performances par quartier.")
    


if page == pages[4]:
  st.markdown(" ")
  st.image('lfb1.svg.png', width = 300)
  st.header('Conclusion')

  
