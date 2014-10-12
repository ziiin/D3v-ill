from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render
from store.models import userDetail
from store.models import authDb
from store.models import logDb
from django import forms
from django.core.mail import send_mail
import worker as w
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

def home (request):
    return HttpResponse ("This is home")

def registerForm (request):
    return render (request, 'register.html')

def doReg (request):
    # doreg/?user=test1&email=email%40gmail.com&phone=455445&msg=test_message&
    # homelo=hla1&homela=hlo1&officelo=olo1&officela=ola1
    message = ""
    cur_u = w.cur_user (request)
    if cur_u == None:
        print "Not Logged in"
        return HttpResponse ("Please Login")
    base_row = userDetail.objects.filter(uname=cur_u)
    if len(base_row) != 0:
        return HttpResponse ("User Exists")
    rowData = dict()
    rowData["user"] = cur_u
    for key in request.GET:
        if key == "email":
            value = request.GET[key]
        else:
            value = str(request.GET[key])
        '''
        elif key in ["homelo", "officelo"]:
            value = str(request.GET[key])
            value = w.validateLongi(value)
            if value == None:
                return HttpResponse ("BAD longitude")
        elif key in ["homela", "officela"]:
            value = str(request.GET[key])
            value = w.validateLati (value)
            if value == None:
                return HttpResponse ("BAD longitude")

        else:
            value = str(request.GET[key])
        '''
        message+= key + ": " + str(value) + ": "
        rowData[key] = value
    row = userDetail (uname = rowData["user"], email=rowData["email"],       \
                      phone = rowData["phone"], msg=rowData["msg"],          \
                      homelo = "10.1111", homela = "10.1111",\
                      officelo = "10.1111",                        \
                      officela = "10.1111" )
    row.save()
    
    message +="   Dict: " + str(rowData)
    
    return HttpResponse (message)

def searchForm (request):
    return render (request, 'search.html')

def search (request):
    # search?user=test1
    # get details of this user
    # find all users with home and office location close by 2km
    base_user = ""
    base_hlo = 0.0
    base_hla = 0.0
    base_olo = 0.0
    base_ola = 0.0

    '''
    if "user" in request.GET:
        base_user = str(request.GET["user"])
    else:
        return HttpResponse ("Username not Provided")
    '''
    cur_u = w.cur_user (request);  
    if cur_u == None:         
        print "Not Logged in" 
        return HttpResponse ("Please Login")
    else:
        base_user = cur_u

    print base_user
    base_row = userDetail.objects.filter(uname=base_user)
    
    if len(base_row) == 0:
        return HttpResponse ("User Not available")
    if len(base_row) != 1:
        print "User not unique, Continuing with first row"
    
    base_hlo = float(base_row[0].homelo)
    base_hla = float(base_row[0].homela)
    base_olo = float(base_row[0].officelo)
    base_ola = float(base_row[0].officela)

    allRows = userDetail.objects.all()
    result = list()
    for row in allRows:
        hlo = float(row.homelo)
        hla = float(row.homela)
        olo = float(row.officelo)
        ola = float(row.officela)

        res_hlo, res_hla = w.is_dist_km_far (base_hlo, base_hla, hlo, hla)
        res_olo, res_ola = w.is_dist_km_far (base_olo, base_ola, olo, ola)

        if res_hlo != None and res_hla != None and \
            res_olo != None and res_ola != None:
                if str(row.uname) != str(base_row[0].uname):
                    result.append(str(row.uname))

    resStr = ""
    for s in result:
        resStr+= s + ','
    return HttpResponse (resStr[0:-1])

def requestForm (request):
    # render form
    return render (request, 'request_access.html')

def requestHandler (request):
    # ?fuser=ajeet&tuser=ajet1&phone=T
    if "tuser" in request.GET:
        #fuser = str(request.GET["fuser"])
        tuser = str(request.GET["tuser"])
    else:
        return HttpResponse ("Username Not available")

    cur_u = w.cur_user (request);  
    if cur_u == None:         
        print "Not Logged in" 
        return HttpResponse ("Please Login")
    else:
        fuser = cur_u

    
    msg = "NONE"
    if "msg" in request.GET:
        msg = str(request.GET["msg"])
    else:
        print "[requestHandler]: Message not Provided"
    
    row = logDb (from_user = fuser, to_user = tuser, re_type = "0100", \
            re_msg = msg)
    row.save()
    row1 = authDb (from_user = fuser, to_user = tuser, re_status = "0100")
    row1.save()

    # [TODO] DO not allow redundant requests and blocked requests
    # [TODO] Handle False users as fuser and tuser
    
    
    print fuser, tuser, msg
    return HttpResponse ("Request Sent")

    # insert in logDb, with mask as 0100
    # insert in authDB, with same mask

def grantForm (request):
   return render (request, 'grant_access.html') 

def grantHandler (request):
    # ?fuser=&tuser=&accept_p=T&reject_p=T&block=T
    fuser = ""
    tuser =""
    if "fuser" in request.GET :
        fuser = str(request.GET["fuser"])
        #tuser = str(request.GET["tuser"])
    else:
        return HttpResponse ("Username Not available")
    cur_u = w.cur_user (request)
    if cur_u == None: 
        print "Not Logged in" 
        return HttpResponse ("Please Login")
    else:
        tuser = cur_u
    print fuser, tuser
    accepted = False
    rejected = False
    blocked = False

    if "accept_p" in request.GET:
        if str(request.GET["accept_p"]) == "T":
            accepted = True
    
    if "reject_p" in request.GET:
        if str(request.GET["reject_p"]) == "T":
            rejected = True
    if "block" in request.GET:
        if str(request.GET["block"]) == "T":
            blocked = True

    #[TODO] filter for cases like reject and accept cases
    
    authRow = authDb.objects.filter(from_user = fuser, to_user = tuser)

    if len (authRow) == 0:
        print "No entry found in authDb for : " + fuser +" : " +  tuser

    statusStr = str(authRow[0].re_status)
    newStatus = statusStr

    if statusStr[0] == '1':
        # [TODO] Dont allow to change/edit anything
        pass
    elif statusStr[0] == '0' and blocked == True:
        newStatus = "1101"
    elif statusStr[1] == '1' and statusStr[2]=='0':
        # request sent but not accepted
        if accepted == True:
            # change statusStr[2] = "1"
            newStatus = "0110"
            pass
        if rejected == True:
            # change statusStr[3] = '1'
            newStatus = "0101"
            pass
    authRow[0].re_status = newStatus
    authRow[0].save()
    row = logDb(from_user = fuser, to_user = tuser, re_type = newStatus, \
            re_msg = "Action taken")
    row.save()
    # insert new status to authDB and logDb
    # status, accepted, rejected or blocked.
    # feed logDB, 0110, 0001, 1000 respectively
    # feed authDB with the same mask
    return HttpResponse ("Action for request taken")

def listRequestsForm (request):
    # render form with only one user as input
    return render (request, 'list_requests.html')

def listRequests (request):
    user = ""
    userList = []
    cur_u = w.cur_user (request)
    if cur_u == None:
        print "Not Logged in"
        return HttpResponse ("Please Login")
    else:
        user = cur_u
    print "Cur user: ", cur_u
    '''
    if "user" in request.GET:
        user = request.GET["user"]
    else:
        return HttpResponse ("User-name Not Provided")
    '''
    allRows = authDb.objects.filter(to_user = user)

    for row in allRows: 
        reStatus = str(row.re_status)
        if reStatus[0] != "1" and reStatus[3] != "1":
            if reStatus[1] =="1" and reStatus[2] == "0":
                userList.append(str(row.from_user))
    print str(userList)
    return HttpResponse ( str(userList))
    # get the user sent from the from
    # search among all objects in authDb for pending, not blocked users
    # and show them in list

def mailForm (request):
    return render (request, 'send_mail.html')

def sendMail (request):
    
    mailDetails = dict()
    for addr_type in ["to"]:
        if addr_type in request.GET:
            emailAddress = str(request.GET[addr_type])
            f = forms.EmailField()
            try:
                emailAddress = f.clean(emailAddress)
                mailDetails[addr_type] = emailAddress
            except ValidationError:
                return HttpResponse ("Invalid Address for : " + addr_type)
        else:
            return HttpResponse ("Provide address for: " + addr_type )
    for ctx in ["sub", "body"]:
        if ctx in request.GET:
            data = str (request.GET[ctx])
            mailDetails[ctx] = data
        else:
            return HttpResponse ("Provide data for : " + ctx)

    toList = [mailDetails["to"]]
    send_mail (mailDetails["sub"], mailDetails["body"], "d3vill.inmobi@gmail.com",\
            toList)
    return HttpResponse (str(mailDetails))


'''
Login and logout feature.
'''
@csrf_exempt
def register_form (request):
    return render(request, "register_app.html")

@csrf_exempt
def register(request):
    uname = request.POST.get('username', '')
    password = request.POST.get('password', '')
    re_password = request.POST.get('re_password', '')
    
    if password != re_password:
        print "password not same"
        return HttpResponse("Retry")

    user = User.objects.create_user(username = uname, password = re_password)

    user.is_staff = True
    user.save()
    return HttpResponse("Successfully registered")


@csrf_exempt
def login_view(request):
    userName = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=userName, password=password)
    m = User.objects.get(username=userName)
    if "member_id" in request.session:
        Id = request.session['member_id'] 
        m = User.objects.get(id=Id)
        return HttpResponse("already logged in as user: " + m.username)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        #auth.login(request, user)
        # Redirect to a success page.
        #return HttpResponseRedirect("/loggedin")
        # logged in url is handled by a function which prints message showing username.
        print "Mile stone 1"
        request.session['member_id'] = m.id
        print "session: mem id is : " + str(m.id)
        return HttpResponse("User is" + str(user.username))
    else:
        # invalid is handles by function displaying invalid user
        print "milestone 2"
        return HttpResponse("false User")

@csrf_exempt
def login_form (request):
    # displays option fill in username and password and
    # sends a POST request to login
    return render(request, 'login.html')
    pass


@csrf_exempt
def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")


@csrf_exempt
def invalid (request):
    return HttpResponse("Invalid")

@csrf_exempt
def loggedin (request):
    if "member_id" not in request.session:
        return HttpResponse("User-name not Not logged in")
    print request.session['member_id']
    Id = request.session['member_id']
    m = User.objects.get(id=Id)
    if True:
        member_id = request.session['member_id']
        return HttpResponse("User is" + str(m.username) + " id:  " + str(member_id))
    else:
        return HttpResponse("User-name not available")


'''
User email id verification
'''

def gdlHome (request):
    return render(request, 'gdl_home.html')

def gdlOffice (request):
    return render(request, 'gdl_office.html')

def feedLoc (request):
    # handler for gdl map to edit location data
    pass

def syncHome(request):
    # get currently logged in user
    # the hlo, hla key pairs
    # get the user detail row with user as logged in user
    # replace the new pairs and save the row
    hlo = ""
    hla = ""
    if "hlo" in request.GET:
        hlo = str(request.GET["hlo"]) 
        hlo = w.validateLongi(hlo)
        if hlo == None:
            return HttpResponse ("Bad longitude")
    if "hla" in request.GET:
        hla = str(request.GET["hla"])
        hla = w.validateLati(hla)
        if hla == None:
            return HttpResponse ("Bad latitude")

        
    cur_u = w.cur_user (request)
    if cur_u == None:
        print "Not Logged in"
        return HttpResponse ("Please Login")
    base_row = userDetail.objects.filter(uname=cur_u)
    print hlo, hla, str(base_row[0].homelo), str(base_row[0].homela)
    base_row[0].homelo = 11.1155
    base_row[0].homela = 11.5555
    
    uname = base_row[0].uname
    email = base_row[0].email
    phone = base_row[0].phone
    msg = base_row[0].msg
    ola = base_row[0].officela
    olo = base_row[0].officelo

    base_row[0].delete()
    row = userDetail (uname = uname, email = email, phone = phone,\
            msg = msg, homela = hla, homelo = hlo, \
            officela = ola, officelo = olo)
    row.save()
    return HttpResponse ("Done Updation")

def syncOffice(request):
    # get currently logged in user
    # the hlo, hla key pairs
    # get the user detail row with user as logged in user
    # replace the new pairs and save the row
    olo = ""
    ola = ""
    if "olo" in request.GET:
        olo = str(request.GET["olo"]) 
        olo = w.validateLongi(olo)
        if olo == None:
            return HttpResponse ("Bad longitude")
    if "ola" in request.GET:
        ola = str(request.GET["ola"])
        ola = w.validateLati(ola)
        if ola == None:
            return HttpResponse ("Bad latitude")

        
    cur_u = w.cur_user (request)
    if cur_u == None:
        print "Not Logged in"
        return HttpResponse ("Please Login")
    base_row = userDetail.objects.filter(uname=cur_u)

    uname = base_row[0].uname
    email = base_row[0].email
    phone = base_row[0].phone
    msg = base_row[0].msg
    hla = base_row[0].homela
    hlo = base_row[0].homelo

    base_row[0].delete()
    row = userDetail (uname = uname, email = email, phone = phone,\
            msg = msg, homela = hla, homelo = hlo, \
            officela = ola, officelo = olo)
    row.save()
    return HttpResponse ("Done Updation")
