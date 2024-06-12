import pandas as pd
import requests

#url = "https://dbaasp.org/peptide-card?id=8"
url = "http://bioinformatics.cimap.res.in/sharma/PlantAFP/new-search.php?f=organism_target&val=%20Aspergillus%20parasiticus"
r = requests.get(url)
df_list = pd.read_html(r.text) # this parses all the tables in webpages to a list
#df = df_list[9]


print(df_list)