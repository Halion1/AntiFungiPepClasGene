from requests_html import HTMLSession
from bs4 import BeautifulSoup

def access(sheet, len_max):
    mat = []

    for i in range(5000, 5497):
        # ENTERING TO THE WEBSITE according to the ID
        a=sheet.cell(i,1)
        url="https://dbaasp.org/peptide-card?id="+str(a.value)

        session = HTMLSession()

        r = session.get(url)
        r.html.render()
        #r.html.render(timeout=10)

        soup = BeautifulSoup(r.html.html, "lxml")
        infotable = soup.find('div', class_="container-fluid physico-chemical-property-container m-t-50")

        if infotable is None:
            for n in range(10):
                values0 = []
                v = ""
                values0.append(v)
            mat.append(values0)

        else:
            table = infotable.find("tr", {"class": "odd"})
            values1 = [tag.text for tag in table]
            mat.append(values1)

    return(mat)