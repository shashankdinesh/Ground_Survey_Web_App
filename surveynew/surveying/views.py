from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .models import Users, exampledata, datanew
from math import radians, cos, sin, asin, sqrt, atan2, degrees,pi,ceil,floor
import xlsxwriter,os


def datawrr():
    import xlsxwriter, gdal
    hf = {}
    ds = gdal.Open("C:/Users\Hp\Desktop\DATA\demdata\ASD\cdng43r.tif")
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray()
    workbook = xlsxwriter.Workbook('C:/Users\Hp\Desktop\DATA\data.xlsx')
    worksheet1 = workbook.add_worksheet()
    worksheet2 = workbook.add_worksheet()
    lon = 76.99986111111112
    lat = 26.000138888888888
    x = 0.0002777777777777778
    y = -0.0002777777777777778
    a = 0
    c = 0
    row = 0
    for i in arr:
        a = 0
        lat = lat + (c * y)
        c += 1
        for j in i:
            hf[j] = [[lat, lon + (a * x)], [lat, lon + ((a + 1) * x)]]
            worksheet1.write(row, 0, j)
            worksheet1.write(row, 1, lat)
            worksheet1.write(row, 2, lon + (a * x))
            worksheet1.write(row, 3, lat)
            worksheet1.write(row, 4, lon + ((a + 1) * x))
            a += 1
            row += 1

    workbook.close()


def haversine(pointA, pointB):
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = pointA[1]
    lon1 = pointA[0]

    lat2 = pointB[1]
    lon2 = pointB[0]

    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def location(request):
    return render(request,'gui.html', {'title':'YOUR LOCATION'})

def usef(request):
    londe = [[26, 78]]
    name=None
    if request.method == 'POST':
        name = request.POST.get('token2', '')
    return render(request, 'usef.html', {'title': 'YOUR LOCATION', 'l': londe,'to':name})

def search(request):
    londe = [[26, 78]]
    latitude=[]
    longitude=[]
    name=None
    tod=0
    u=0
    if request.method == 'POST':
        name = request.POST.get('token1', '')
    fa = exampledata.object.all()
    for a in fa:
        if a.chaturloki == name:
            pla = a.lat
            plo = a.lon
            e = a.ele
            d = a.distance
            ang = a.ang
            tod = a.totaldistance
            londe.append([pla, plo])
    for s in londe:
        if u ==0:
            u+=1
            continue
        latitude.append(s[0])
        longitude.append(s[1])
    n = max(latitude)
    s = min(latitude)
    e = max(longitude)
    w = min(longitude)
    if londe ==1:
        n = 26.23049119761041
        s = 26.175659888923647
        e = 78.24051156666417
        w = 78.123953491713
    return render(request, 'search.html',{'title': 'YOUR LOCATION', 'l': londe, 'to': name, 'tod': tod, 'north': n, 'south': s, 'east': e,'west': w})


def req(request):
    name=None
    if request.method == 'POST':
        name = request.POST.get('token3', '')
    return render(request, 'req.html', {'title': 'SURVEYOR', 'to': name})

def datareq(request):
    if request.method == 'POST':
        name = request.POST.get('email', '')
        password = request.POST.get('pwd', '')
        pnum = request.POST.get('phn', '')
        print(name,password,pnum)
        var=Users(username=name, password=password, phone_number=pnum)
        var.save()

def clear(request):
    londe = [[26, 78]]
    tod=0
    name=None
    latitude=[]
    longitude=[]
    if request.method == 'POST':
        name = request.POST.get('token6', '')
        print (name,"tokennnnnnnnnnnnnnnnnn6666666666666")
        exampledata.object.filter(chaturloki= name).delete()
    n = 26.23049119761041
    s = 26.175659888923647
    e = 78.24051156666417
    w = 78.123953491713
    return render(request, 'search.html',{'title': 'YOUR LOCATION', 'l': londe, 'to': name, 'tod': tod, 'north': n, 'south': s, 'east': e,'west': w})


def signup(request):
    return render(request, 'register.html', {'title': 'REGISTER'})

def lorpa(toki,tdsa,length,sha):
    for b in range(len(sha)):
        if sha[b].chaturloki == toki:
            tdsa.append(sha[b].totaldistance)
    flen = max(tdsa)
    n = flen / length
    return flen,n

def lorpb(sha,toki,murga):
    for c in range(len(sha)):
        if sha[c].chaturloki == toki:
            murga.append([sha[c].lat,sha[c].lon])

    return murga

def lorpc(murga,fmur):
    for i in range(len(murga)):
        fmur.append(murga[0])
    return fmur

def lorpd(sha,k,toki,fmur):
    ang=None
    for a in range(len(sha)-1):
        if sha[a].chaturloki == toki and sha[a].totaldistance < k and sha[a + 1].totaldistance > k:
            print("we are inside")
            pla = sha[a].lat
            plo = sha[a].lon
            ang = sha[a + 1].ang
            distance = (k - sha[a].totaldistance)
            if pla != None and plo != None and distance != 0 and ang != 0:
                y, m = latlongenerator(float(distance), float(pla), float(plo), float(ang))
                fmur.append([y, m])
        if sha[a].chaturloki == toki and sha[a].totaldistance == k:
            fmur.append([sha[a].lat, sha[a].lon])
    return fmur,ang+90

def lorpf(murga):

    return murga[len(murga)-1][0],murga[len(murga)-1][1]


def lorpg(sha,lent,toki,of):
    ko=None
    for a in range(len(sha)-1):
        if sha[a].chaturloki == toki:
            ang = sha[a + 1].ang
            ko=ang+90

    return of,ko



def lorp(request):
    femth = []
    latitude=[]
    longitude=[]
    u=0
    ata = []
    tdsa=[]
    fmur = [[26, 78]]
    toki = None
    length,gth,sth,kth,mth,oth = None,None,None,None,None,None
    y,m,ochan,oflen,ofin=None,None,None,None,None
    murga=[]
    ofmur=[]
    if request.method == 'POST':
        toki = request.POST.get('token5', '')
        gth = request.POST.get('ls', '')
        length=spliter(gth)
        sth = request.POST.get('ofchan', '')
        oth=request.POST.get('ofconchan', '')
        kth = request.POST.get('oflen', '')
        oflen=spliter(kth)
        mth = request.POST.get('ofin', '')
        ofin=spliter(mth)
    print(toki, "tokiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    sha = exampledata.object.all()
    if sth !="NIL":
        ofchan = spliter(sth)
        for g in ofchan:
            th=[]
            of=[]
            of,ko = lorpd(sha, g, toki, of)
            oof = [[of[0][0],of[0][1]]]
            pla = of[0][0]
            plo = of[0][1]
            if pla != None and plo != None and oflen[0] != 0 and ko != 0:
                y, m = latlongenerator(float(oflen[0]), float(pla), float(plo), float(ko))
                of.append([y, m])
            j=oflen[0]/ofin[0]
            r = ceil(j)
            s = floor(j)
            if (j - s) > (r -j):
                j = int(r)
            else:
                j = int(s)
            for k in range(j-1):
                th.append((j + 1) * float(ofin[0]))
            for t in th:
                if of[0][0] != None and of[0][1] != None and t != 0 and ko != 0:
                    y, m = latlongenerator(float(t), float(of[0][0]), float(of[0][1]), float(ko))
                    of.append([y, m])
                    f, x = latlongenerator(float(t), float(of[0][0]), float(of[0][1]), float(ko+180))
                    oof.append([f, x])
            ofmur.append(of)
            ofmur.append(oof)
        print(ofmur,"oooooooooooooooooooooooooooooooffffffffffffffffffffffffffffffffffmmmmmmmmmmmmmmmmmmmmmmmmmmmmmuuuuuuuuuuuuuuuuuuuuurrrrrrrrrrrrrrrrrrrrrrrr")
    else:
        dsa=[]
        emth=[]
        ofchan = spliter(oth)
        tot, u = lorpa(toki, dsa, float(ofchan[0]), sha)
        csd = ceil(u)
        qsd = floor(u)
        if (u - qsd) > (csd - u):
            u = int(csd)
        else:
            u = int(qsd)
        for h in range(u - 1):
            emth.append((h + 1) * float(ofchan[0]))
        ofchan=emth
        for g in emth:
            th = []
            of = []
            of, ko = lorpd(sha, g, toki, of)
            oof = [[of[0][0], of[0][1]]]
            pla = of[0][0]
            plo = of[0][1]
            if pla != None and plo != None and oflen[0] != 0 and ko != 0:
                y, m = latlongenerator(float(oflen[0]), float(pla), float(plo), float(ko))
                of.append([y, m])
            j = oflen[0] / ofin[0]
            r = ceil(j)
            s = floor(j)
            if (j - s) > (r - j):
                j = int(r)
            else:
                j = int(s)
            for k in range(j - 1):
                th.append((j + 1) * float(ofin[0]))
            for t in th:
                if of[0][0] != None and of[0][1] != None and t != 0 and ko != 0:
                    y, m = latlongenerator(float(t), float(of[0][0]), float(of[0][1]), float(ko))
                    of.append([y, m])
                    f, x = latlongenerator(float(t), float(of[0][0]), float(of[0][1]), float(ko + 180))
                    oof.append([f, x])
            ofmur.append(of)
            ofmur.append(oof)
        print(ofmur,"oooooooooooooooooooooooooooooooffffffffffffffffffffffffffffffffffmmmmmmmmmmmmmmmmmmmmmmmmmmmmmuuuuuuuuuuuuuuuuuuuuurrrrrrrrrrrrrrrrrrrrrrrr")
    flen,n=lorpa(toki,tdsa,float(length[0]),sha)
    c=ceil(n)
    q=floor(n)
    if (n-q)>(c-n):
        n=int(c)
    else:
        n=int(q)
    murga=lorpb(sha,toki,murga)
    fmur=lorpc(murga,fmur)
    for h in range(n-1):
        femth.append((h + 1) * float(length[0]))
    for k in femth:
        fmur,i=lorpd(sha,k,toki,fmur)
    fmur.append([murga[len(murga)-1][0],murga[len(murga)-1][1]])
    print(fmur,"ffffffffffffffffffmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuurrrrrrrrrrrrrrrrrrrrrrrrrr")
    for s in fmur:
        if u==0:
            u+=1
            continue
        latitude.append(s[0])
        longitude.append(s[1])
    n = max(latitude)
    s = min(latitude)
    e = max(longitude)
    w = min(longitude)
    return render(request, 'searched.html', {'title': 'SURVEYOR', 'l': fmur, 'to': toki,'oflon':ofmur,'north':n,'south':s,'east':e,'west':w,'chain':ofchan,'inter':ofin,'femt':femth})


def dentry(request):
    name = None
    if request.method == 'POST':
        name = request.POST.get('token4', '')
    return render(request, 'test.html', {'title': 'REGISTER','to':name})

def signin (request):
    print('bahar')
    if request.method == 'POST':
        print('andar')
        name = request.POST.get('email', '')
        password = request.POST.get('pwd', '')
        print('agae a gaye',name, password)
        v=Users.object.all()
        print('ab nahi ghil raha')
        for i in v:
            if i.username==name and i.password==password:
                tokio = i.phone_number
                #exampledata.object.filter(chaturloki=tokio).delete()
                print(tokio,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return render(request, 'option.html', {'title': 'SURVEYOR','to':i.phone_number})
    return render(request, 'gui.html', {'title': 'LOGIN'})

def register(request):
    if request.method == 'POST':
        name = request.POST.get('email', '')
        password = request.POST.get('pwd', '')
        pnum = request.POST.get('phn', '')
        print(name,password,pnum)
        var=Users(username=name, password=password, phone_number=pnum)
        var.save()
        return render(request, 'option.html', {'title': 'SURVEYOR','to':pnum})
    else:
        return render(request, 'register.html', {'title': 'REGISTER'})


def latlonview(request):
    y,m=None,None
    latitude = []
    longitude = []
    ata=[]
    toki=None
    londe=[[26,78]]
    dictionary={}
    #print(request.method =='POST')
    if request.method =='POST':
        print("Point 1")
        lat=request.POST.get('lat','')
        lon = request.POST.get('lon', '')
        angle = request.POST.get('angle', '')
        distance = request.POST.get('distance', '')
        elevation = request.POST.get('elevation', '')
        toki = request.POST.get('token', '')
        print(lat,lon,angle,distance,toki )
        point = datanew(lat=lat, lon=lon, ele=elevation,loki=toki)
        point.save()
        if lat !=None and lon !=None and len(distance)!=0 and len(angle)!=0:
            y,m=latlongenerator(float(distance), float(lat), float(lon), float(angle))
    sha=datanew.object.all()
    for a in sha:
        if a.loki==toki:
            pla = a.lat
            plo = a.lon
            e=a.ele
            londe.append([pla,plo])
            ata.append([pla,plo,e])
    if y!=None and m!=None:
        londe.append([y,m])
    return render(request, 'usef.html',{'title':'YOUR LOCATION','l':londe,'to':toki})

def task(request):
    ata=[]
    londe = [[26, 78]]
    toki = None
    if request.method == 'POST':
        toki = request.POST.get('token2', '')
    sha = datanew.object.all()
    for a in sha:
        if a.loki==toki:
            pla = a.lat
            plo = a.lon
            e=a.ele
            ata.append([pla,plo,e])
    exelwrite(ata,toki)
    pa=os.path.join(settings.MEDIA_ROOT,'/home/bfdgfhvjhkhbkj/OnlineSurvey/media/%s.xlsx'%toki)
    with open(pa, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type = "applicationvnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename = ' + os.path.basename(pa)
        return response
    return render(request, 'search.html', {'title': 'YOUR LOCATION', 'l': londe,'to':toki})
    return render(request, 'usef.html', {'title': 'YOUR LOCATION','l':londe,'to':toki})

def fview(request):
    latitude=[]
    longitude=[]
    u=0
    y, m = None, None
    londe=[[26,78]]
    ata=[]
    l=0
    tod=None
    cor=[]
    toki=None
    if request.method == 'POST':
        lat = request.POST.get('lat', '')
        lon = request.POST.get('lon', '')
        angle = request.POST.get('angle', '')
        distance = request.POST.get('distance', '')
        elevation = request.POST.get('elevation', '')
        toki = request.POST.get('token1', '')
        print(lat, lon, angle, distance)
        sha = exampledata.object.all()
        for a in sha:
            if a.chaturloki == toki:
                cor.append([a.lat,a.lon])
        cor.append([lat,lon])

        for i in range(len(cor) - 1):
                l = l + (haversine((float(cor[i][1]),float(cor[i][0])), (float(cor[i+1][1]),float(cor[i+1][0])))*1000)
        point = exampledata(lat=lat, lon=lon, ele=elevation, distance=distance, ang=angle, chaturloki=toki, totaldistance=l)
        point.save()
        fa = exampledata.object.all()
        for a in fa:
            if a.chaturloki==toki:
                pla = a.lat
                plo = a.lon
                e = a.ele
                d=a.distance
                ang=a.ang
                tod=a.totaldistance
                londe.append([pla, plo])
                ata.append([pla, plo,e,d,ang])
    for s in londe:
        if u==0:
            u+=1
            continue
        latitude.append(s[0])
        longitude.append(s[1])
    n = max(latitude)
    s = min(latitude)
    e = max(longitude)
    w = min(longitude)
    return render(request,'search.html', {'title':'YOUR LOCATION','l':londe,'to':toki,'tod':tod,'north':n,'south':s,'east':e,'west':w})


def spliter (latlon):
    #list = ["[", "[", "2", "0", ".", "8", "7", "5", "6", "3", "7", "9", "0", "4", ",", "7", "8", ".", "1", "2", "5", "7", "8", "3", "1", "5", "2", "]", ",", "[", "2", "0", ".", "8", "7", "5", "6", "3", "7", "8", "8", "8", ",", "7","8", ".", "1", "2", "5", "7", "8", "3", "1", "1", "1", "]", "]"]
    list=latlon
    string = []
    coords = []
    var = ""
    count = 0
    # print length

    for i in range(len(list)):
        if list[i] == "[" or list[i] == "]":
            continue
        if list[i] == "." or list[i] == "0" or list[i] == "1" or list[i] == "2" or list[i] == "3" or list[i] == "4" or list[i] == "5" or list[i] == "6" or list[i] == "7" or list[i] == "8" or list[i] == "9" or list[i] == ",":
            var = var + list[i]
    string.append(var)
    coordsString = string[0].split(",")
    print(coordsString,"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
    for k in range(len(coordsString)):
        coords.append(float(coordsString[k]))
    print (coords)
    return coords

def spliterer (l):
    list = l
    #list=latlon
    string = []

    var = ""
    var2 = ""
    count = 0
    for i in range(len(list)):
        if list[i] == "[" or list[i] == "]" or list[i] == "." or list[i] == "0" or list[i] == "1" or list[i] == "2" or list[i] == "3" or list[i] == "4" or \
                        list[
                            i] == "5" or list[i] == "6" or list[i] == "7" or list[i] == "8" or list[i] == "9" or list[i] == ",":
            var = var + list[i]
    string.append(var)

    #print(string)
    oordsString = string[0].split("[[[")
    #print(coordsString, len(coordsString))
    oordsString =  oordsString[1].split("]]]")
    #print(coordsString, len(coordsString))
    oordsString = oordsString[0].split("]],[[")
    #print (oordsString,len(oordsString))
    u=[]
    for k in oordsString:
        boordsString = k.split("],[")
        a=[]
        #print(boordsString)
        for y in boordsString:
            coordsString = y.split(",")
            coords=[]
            for k in range(len(coordsString)):
                coords.append(float(coordsString[k]))
            a.append(coords)
        u.append(a)
    return u


def report(request):
    ata=[]
    er=None
    al=None
    offsetwriter=[]
    londe=[[26,78]]
    chain=None
    toki,lalo,elev,latlon,eqw,wqe,interval=None,None,None,None,None,None,None
    if request.method == 'POST':
        toki = request.POST.get('token5', '')
        latlon = request.POST.get('rojlalo', '')
        print(latlon,"dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd")
        elev = request.POST.get('elevate', '')
        eqw= request.POST.get('offlalo', '')
        wqe = request.POST.get('offele', '')
        cha = request.POST.get('cha', '')
        print(cha,"chaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        chain=spliter(cha)
        print (chain,"chainnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
        inter = request.POST.get('in', '')
        interval = spliter(inter)
        er = request.POST.get('ha', '')
        al = spliter(er)
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbhhhhhhhhhhhhhhhhhhiiiiiiiiiiiiiiiiiiiiiiiisssssssssssssssuuuuuuuuuuuuuurrrrrrrrrrrrruuuuuuuuuu")
    coords=spliter(latlon)
    print(coords,"cooooooooooooooooooooooooooooooooorrrrrrrrrrrrrrrrrrdddddddddddddssssssssssssss")
    el = spliter(elev)
    print(el,"eeeeeeeeeeeeellllllllllllllllllllllllllllllllllllllllllllllllllll")
    ofel=spliter(wqe)
    ofl=[]
    for s in range(len(chain)):
        ofl.append(chain[s])
    for o in range(len(chain)):
        ofl.append(chain[o])
    lalot=spliterer(eqw)
    g=0
    ofset=0
    for i in lalot:
        r=0
        for j in i:
            offsetwriter.append([ofl[ofset],interval[0]*r,j[0],j[1],ofel[g]])
            g+=1
            r+=1
        ofset+=1

    print(toki,"tokiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    exelwrite1(coords,el,toki,offsetwriter)
    pa=os.path.join(settings.MEDIA_ROOT,'C:/Users\Hp\Desktop/%s.xlsx'%toki)
    with open(pa, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type = "applicationvnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename = ' + os.path.basename(pa)
        return response
    return render(request, 'search.html', {'title': 'YOUR LOCATION', 'l': londe,'to':toki})


'''def report(request):
    ata=[]
    londe=[[26,78]]
    toki,lalo,elev=None,None,None
    if request.method == 'POST':
        toki = request.POST.get('token5', '')
        latlon = request.POST.get('lalo', '')
        elev = request.POST.get('elevate', '')
    coords=spliter(lalo)
    el = spliter(elev)
    print(toki,"tokiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    sha = exampledata.object.all()
    for a in sha:
        if a.chaturloki==toki:
            print("we are inside")
            pla = a.lat
            plo = a.lon
            e = a.ele
            d = a.distance
            ang = a.ang
            ho=a.chaturloki
            ata.append([pla, plo, e, d, ang])
    exelwrite1(ata,toki)
    pa=os.path.join(settings.MEDIA_ROOT,'/home/bfdgfhvjhkhbkj/OnlineSurvey/media/%s.xlsx'%toki)
    with open(pa, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type = "applicationvnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename = ' + os.path.basename(pa)
        return response
    return render(request, 'search.html', {'title': 'YOUR LOCATION', 'l': londe,'to':toki})'''





def pview(request):
    y, m = None, None
    londe=[[26,78]]
    ata=[]
    u=0
    toki=None
    tod=None
    latitude=[]
    longitude=[]
    if request.method == 'POST':
        lat = request.POST.get('lats', '')
        lon = request.POST.get('lons', '')
        elevation = request.POST.get('elevations', '')
        toki = request.POST.get('token', '')
        point = exampledata(lat=lat, lon=lon, ele=elevation, distance=0,ang=0,chaturloki=toki,totaldistance=0)
        point.save()
        sha = exampledata.object.all()
        for a in sha:
            if a.chaturloki==toki:
                pla = a.lat
                plo = a.lon
                tod = a.totaldistance
                londe.append([pla, plo])
    for s in londe:
        if u==0:
            u+=1
            continue
        latitude.append(s[0])
        longitude.append(s[1])
    n = max(latitude)
    s = min(latitude)
    e = max(longitude)
    w = min(longitude)
    return render(request,'search.html', {'title':'YOUR LOCATION','l':londe,'to':toki,'tod':tod,'north':n,'south':s,'east':e,'west':w})




def latlongenerator(d,lat1,lon1,brng):
    R = 6371000
    distRatio = d/R
    distRatioSine = sin(distRatio)
    distRatioCosine = cos(distRatio)
    startLatRad = radians(lat1)
    startLonRad = radians(lon1)
    startLatCos = cos(startLatRad)
    startLatSin = sin(startLatRad)
    initialBearingRadians = radians(brng)
    endLatRads = asin((startLatSin * distRatioCosine) + (startLatCos * distRatioSine * cos(initialBearingRadians)))
    endLonRads = startLonRad+ atan2(sin(initialBearingRadians) * distRatioSine * startLatCos,distRatioCosine - startLatSin * sin(endLatRads))
    return degrees(endLatRads),degrees(endLonRads)


def exelwrite(ata,toki):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('/home/bfdgfhvjhkhbkj/OnlineSurvey/media/%s.xlsx'%toki)
    worksheet = workbook.add_worksheet()
    col1_name = 'S.NO:'
    col2_name = 'LATITUDE'
    col3_name = 'LONGITUDE'
    col4_name = 'ELEVATION'
    worksheet.write(0, 0, col1_name)
    worksheet.write(0, 1, col2_name)
    worksheet.write(0, 2, col3_name)
    worksheet.write(0, 3, col4_name)
    # Some data we want to write to the worksheet.
    row = 1
    col = 0
    for i in ata:
        worksheet.write(row, col, row)
        worksheet.write(row, col + 1,i[0])
        worksheet.write(row, col+2, i[1])
        worksheet.write(row, col + 3, i[2])
        row += 1
    workbook.close()

'''def exelwrite1(ata,toki):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('/home/bfdgfhvjhkhbkj/OnlineSurvey/media/%s.xlsx'%toki)
    worksheet = workbook.add_worksheet()
    col1_name = 'S.NO:'
    col2_name = 'LATITUDE'
    col3_name = 'LONGITUDE'
    col4_name = 'ELEVATION'
    col5_name = 'DISTANCE'
    col6_name = 'ANGLE'
    worksheet.write(0, 0, col1_name)
    worksheet.write(0, 1, col2_name)
    worksheet.write(0, 2, col3_name)
    worksheet.write(0, 3, col4_name)
    worksheet.write(0, 4, col5_name)
    worksheet.write(0, 5, col6_name)
    # Some data we want to write to the worksheet.
    row = 1
    col = 0
    for i in ata:
        worksheet.write(row, col, row)
        worksheet.write(row, col + 1,i[0])
        worksheet.write(row, col+2, i[1])
        worksheet.write(row, col + 3, i[2])
        worksheet.write(row, col + 4, i[3])
        worksheet.write(row, col + 5, i[4])
        row += 1
    workbook.close()'''

def exelwrite1(coord,el,toki,offsetwriter):
    gta=[]
    ata=[]
    j=0
    for i in range(len(el)):
        gta.append([coord[j],coord[j+1]])
        j+=2
    print(gta)
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('C:/Users\Hp\Desktop/%s.xlsx'%toki)
    worksheet1 = workbook.add_worksheet()
    worksheet2 = workbook.add_worksheet()
    col1_name = 'S.NO:'
    col2_name = 'LATITUDE'
    col3_name = 'LONGITUDE'
    col4_name = 'ELEVATION'
    col5_name = 'S.NO:'
    col6_name = 'CHAINAGE'
    col7_name = 'DISTANCE FROM ROAD'
    col8_name = 'LATITUDE'
    col9_name = 'LONGITUDE'
    col10_name = 'ELEVATION'
    worksheet1.write(0, 0, col1_name)
    worksheet1.write(0, 1, col2_name)
    worksheet1.write(0, 2, col3_name)
    worksheet1.write(0, 3, col4_name)
    worksheet2.write(0, 0, col5_name)
    worksheet2.write(0, 1, col6_name)
    worksheet2.write(0, 2, col7_name)
    worksheet2.write(0, 3, col8_name)
    worksheet2.write(0, 4, col9_name)
    worksheet2.write(0, 5, col10_name)

    # Some data we want to write to the worksheet.
    row = 1
    col = 0
    for i in range(len(el)):
        worksheet1.write(row, col, row)
        worksheet1.write(row, col + 1,gta[i][0])
        print(gta[i][0])
        worksheet1.write(row, col+2, gta[i][1])
        worksheet1.write(row, col + 3,el[i])
        row += 1
    ow = 1
    ol = 0
    for h in offsetwriter:
        worksheet2.write(ow, ol, ow)
        worksheet2.write(ow, ol+1, h[0])
        worksheet2.write(ow, ol+2, h[1])
        worksheet2.write(ow,  ol+3,h[2])
        worksheet2.write(ow,  ol+4, h[3])
        worksheet2.write(ow,  ol+5, h[4])
        ow+=1
    workbook.close()