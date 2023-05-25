from django.shortcuts import render
from .models import BiensImmobilier
from django.db.models import Q
import requests
from bs4 import BeautifulSoup

# Create your views here.
def index(request):
    biens_immobiliers = BiensImmobilier.objects.order_by('-id').all()
    return render(request, 'index.html', {'biens_immobiliers': biens_immobiliers})

def scrap(request):
    try:
        elemenet = BiensImmobilier.objects.latest('id')
        page = int(elemenet.page)+1
    except:
        page = 1
    # Collecter les données du site 1-	https://www.immobilier.com.tn/
    url1 = 'https://www.immobilier.com.tn/resultat-recherche?ta=2&r=0&tb=&pcs=&smi=&pma=&page='+str(page)
    response1 = requests.get(url1)
    soup1 = BeautifulSoup(response1.content, "html.parser")
    data1 = soup1.find_all('div', class_='col-12 layout-list')

    # Collecter les données du site https://www.tunisie-annonce.com/
    url2 = 'http://www.tunisie-annonce.com/AnnoncesImmobilier.asp?rech_cod_cat=1&rech_cod_rub=101&rech_cod_typ=10101&rech_cod_sou_typ=&rech_cod_pay=TN&rech_cod_reg=&rech_cod_vil=&rech_cod_loc=&rech_prix_min=&rech_prix_max=&rech_surf_min=&rech_surf_max=&rech_age=&rech_photo=&rech_typ_cli=&rech_order_by=31&rech_page_num='+str(page)
    response2 = requests.get(url2)
    soup2 = BeautifulSoup(response2.content, 'html.parser')
    data2 = soup2.find_all('tr', class_='Tableau1')

    # Stocker les données collectées dans la base de données
    try:
        for item1 in data1:
            localisation = item1.find('div', class_='info').find('small').text.strip() 
            prix_1 = item1.find('div', class_='price price-location').find('span').text.strip()
            prix_2 =prix_1.replace("DT", "")
            prix =prix_2.replace(" ", "")
            #pieces = item1.find('ul', class_='amenities').find('li').text.strip()
            try:
                result = item1.find('ul', class_='amenities').find_all('li')[1]
                if result is not None:
                    pieces = result.text.strip()
                else:
                    pieces = "N/A"
            except:
                pass
            superficie = item1.find('ul', class_='amenities').find_all('li')[0].text.strip()
            description = item1.find('div',class_='description').text.strip()
            type1 = item1.select('ul.amenities li')
            if type1:
                last_li_element = type1[-1]
                type = last_li_element.text.strip()
            else:
                type = "N/A"
            try:
                site = item1.find('a', class_='annonce-card annonce-square').get('href')
            except:
                site = 'https://www.immobilier.com.tn/'

            # Ajouter les données dans la table  BiensImmobilier
            BiensImmobilier.objects.create(nom="immobilier", 
                                        site=site, 
                                        localisation=localisation, 
                                        prix=prix,
                                        url=site,
                                            pieces=pieces, superficie=superficie, description=description, type=type, page=page)
    except:
        pass

    for item2 in data2:
        localisation = item2.contents[1].text.strip()
        prix_1 = item2.contents[7].text.strip()
        prix =prix_1.replace(" ", "")
        pieces_1 = item2.contents[3].text.strip()
        pieces_2 = pieces_1.replace("App.","")
        pieces = pieces_2.replace("pièc","")

        type=item2.contents[3].text.strip()[:4]
        superficie = "Non"
        description=item2.contents[5].text.strip()
        site1 =item2.contents[5].find('a').get('href')
        site = "http://www.tunisie-annonce.com/"+site1
        nom='tunisie-annonce'
        BiensImmobilier.objects.create(nom=nom, site=site, url=site, localisation=localisation, prix=prix, pieces=pieces, superficie=superficie, description=description, type=type, page=page)
 
    biens_immobiliers = BiensImmobilier.objects.order_by('-id').all()
    return render(request, 'index.html', {'biens_immobiliers': biens_immobiliers})

def search(request):
    query = request.POST.get('query')
    if query.isnumeric():
        biens_immobiliers = BiensImmobilier.objects.filter(Q(nom__contains=query)|Q(localisation__contains=query)|Q(prix__contains=float(query))|Q(pieces__contains=query)|Q(superficie__contains=query)|Q(description__contains=query)|Q(type__contains=query))
    else:
        biens_immobiliers = BiensImmobilier.objects.filter(Q(nom__contains=query)|Q(localisation__contains=query)|Q(pieces__contains=query)|Q(superficie__contains=query)|Q(description__contains=query)|Q(type__contains=query))

    return render(request, 'index.html', {'biens_immobiliers': biens_immobiliers})

def sortbyprice(request):
    biens_immobiliers = BiensImmobilier.objects.all().order_by('prix')
    return render(request, 'index.html', {'biens_immobiliers': biens_immobiliers})

def sortby_price(request):
    biens_immobiliers = BiensImmobilier.objects.all().order_by('-prix')
    return render(request, 'index.html', {'biens_immobiliers': biens_immobiliers})

def sup_inf(request):
    if 'inf' in request.POST:
        query = request.POST.get('query')
        biens_immobiliers = BiensImmobilier.objects.filter(prix__lt=query)
        return render(request, 'index.html', {'biens_immobiliers': biens_immobiliers})

    else:
        query = request.POST.get('query')
        biens_immobiliers = BiensImmobilier.objects.filter(prix__gt=query)
        return render(request, 'index.html', {'biens_immobiliers': biens_immobiliers})