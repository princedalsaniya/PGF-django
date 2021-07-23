from django.shortcuts import render, HttpResponse, redirect
from accounts.models import Owner
from django.contrib.auth.decorators import login_required
import cloudinary, cloudinary.api
from .forms import register_new_pg_form, register_facilities_form, register_rules_form, register_photo_form
from .models import pgDetails, pgFacilities, pgPhotos, pgRules, ratings, messages, applicationDetails, pgApplication

# Create your views here.
@login_required
def o_dashboard(request):
    user_type = request.session['user_type']
    user = request.user
    profilePublicID = getattr(Owner.objects.get(user=user), 'profilePicID')
    profilePic = cloudinary.CloudinaryImage(profilePublicID).build_url(width = 200, height = 200, crop = 'fill', gravity="face")
    request.session['profilePublicID'] = profilePublicID
    print("here it is : ", profilePublicID)
    context = {
        'user_type': user_type,
        'user': user,
        'profilePicID': request.session['profilePublicID'],
    }

    return render(request, 'owner/dashboard.html', context)

@login_required
def o_register_pg_details(request):
    owner = Owner.objects.get(user=request.user)
    if request.method == "POST":
        register_form = register_new_pg_form(request.POST)
        if register_form.is_valid:

            pg_type = request.POST.get('type')
            floors = request.POST.get('floors')
            rooms = request.POST.get('rooms')
            total_intakes = request.POST.get('total_intakes')
            available_intakes = request.POST.get('available_intakes')
            start_rent = request.POST.get('start_rent')
            end_rent = request.POST.get('end_rent')
            name = request.POST.get('name')
            address = request.POST.get('address')
            area = request.POST.get('area')
            city = request.POST.get('city')
            state = request.POST.get('state')
            description = request.POST.get('description')
            pgID = get_next_pgID()

            newpg = pgDetails(pgID=pgID, owner=owner, floors=floors, rooms=rooms, name=name, address=address, area=area, city=city, state=state, total_intakes=total_intakes, available_intakes=available_intakes, description=description, start_rent=start_rent, end_rent=end_rent, type=pg_type)
            newpg.save()
            request.session['new_pgID'] = pgID

            return redirect('o_register_rules')

    register_form = register_new_pg_form()
    return render(request, './owner/register_pg_form.html', {'register_form': register_form})

@login_required
def o_register_facilities(request):
    facilities_form = register_facilities_form(request.POST or None)
    if request.method == "POST" and facilities_form.is_valid():
        pgID = request.session['new_pgID']
        pg = pgDetails.objects.get(pgID=pgID)
        ac = facilities_form.cleaned_data.get('ac')
        balcony = facilities_form.cleaned_data.get('balcony')
        laundry = facilities_form.cleaned_data.get('laundry')
        breakfast = facilities_form.cleaned_data.get('breakfast')
        lunch = facilities_form.cleaned_data.get('lunch')
        dinner = facilities_form.cleaned_data.get('dinner')
        parking = facilities_form.cleaned_data.get('parking')
        cleaning = facilities_form.cleaned_data.get('cleaning')
        wifi = facilities_form.cleaned_data.get('wifi')
        tv = facilities_form.cleaned_data.get('tv')
        fridge = facilities_form.cleaned_data.get('fridge')
        ro = facilities_form.cleaned_data.get('ro')
        gym = facilities_form.cleaned_data.get('gym')
        lift = facilities_form.cleaned_data.get('lift')
        generator = facilities_form.cleaned_data.get('generator')

        new_facilities = pgFacilities(pg=pg, ac=ac, balcony=balcony, laundry=laundry, breakfast=breakfast, lunch=lunch, dinner=dinner, parking=parking, cleaning=cleaning, wifi=wifi, tv=tv, fridge=fridge, ro=ro, gym=gym, lift=lift, generator=generator)
        new_facilities.save()
        print("facilities saved")

        return redirect('o_register_pg_photos')

    return render(request, './owner/register_facilities_form.html', {'facilities_form': facilities_form})

@login_required
def o_register_rules(request):
    rules_form = register_rules_form(request.POST or None)
    if request.method=='POST' and rules_form.is_valid():
        pgID = request.session['new_pgID']
        pg = pgDetails.objects.get(pgID=pgID)
        deposit = rules_form.cleaned_data.get('deposit')
        print('deposit : ', deposit)
        haveClosingTime = rules_form.cleaned_data.get('haveClosingTime')
        print('haveClosingTime : ', haveClosingTime)
        visitors = rules_form.cleaned_data.get('visitors')
        print('visitors : ', visitors)
        nonVeg = rules_form.cleaned_data.get('nonVeg')
        print('nonVeg : ', nonVeg)
        oppositeGender = rules_form.cleaned_data.get('oppositeGender')
        print('oppositeGender : ', oppositeGender)
        smoking = rules_form.cleaned_data.get('smoking')
        print('smoking : ', smoking)
        drinking = rules_form.cleaned_data.get('drinking')
        print('drinking : ', drinking)
        loudMusic = rules_form.cleaned_data.get('loudMusic')
        print('loudMusic : ', loudMusic)
        party = rules_form.cleaned_data.get('party')
        print('party : ', party)

        new_rules = pgRules(pg=pg, deposit=deposit, haveClosingTime=haveClosingTime, visitors=visitors, nonVeg=nonVeg, oppositeGender=oppositeGender, smoking=smoking, drinking=drinking, loudMusic=loudMusic, party=party)
        new_rules.save()

        return redirect('o_register_facilities')

    return render(request, './owner/register_rules_form.html', {'rules_form': rules_form})

@login_required
def o_register_pg_photos(request):
    pgID = request.session['new_pgID']
    if request.method == 'POST':
        upload_form = register_photo_form(request.POST)
        if upload_form.is_valid():
            print("Inside if")
            photoPID = request.session['photoPID']
            print(photoPID)
            message = upload_form.cleaned_data.get('message')
            print(message)
            new_photo = pgPhotos(pg=pgDetails.objects.get(pgID=pgID), photoPID=photoPID, message=message)
            new_photo.save()
            print("Photo saved")
            return redirect('o_register_pg_photos')

    return render(request, './owner/register_pg_photos.html', {'tag': pgID})

@login_required
def o_upload_pic(request):
    upload_form = register_photo_form(request.POST or None)
    pgID = request.session['new_pgID']
    photoPID = get_next_photoPID(pgID)
    pid = "PGF/PG_Photos/" + pgID + "_" + photoPID
    request.session['photoPID'] = pid

    return render(request, './owner/upload_photo.html', {'upload_form': upload_form, 'tag': pgID, 'pid': pid})

@login_required
def o_register_success(request):
    pgID = request.session['new_pgID']
    pg = pgDetails.objects.get(pgID=pgID)
    owner = Owner.objects.get(user=request.user)

    print("before object")
    newApplication = pgApplication(pg=pg, owner=owner)
    newApplication.save()
    print("saved the application")

    return render(request, './owner/register_success.html')

@login_required
def o_pglist(request):
    owner = Owner.objects.get(user=request.user)
    pgs = pgDetails.objects.filter(owner=owner)

    return render(request, './owner/pg_list.html', {'pgs': pgs,'profilePicID': request.session['profilePublicID']})

#curr_pgID is stored here.
@login_required
def pg_details(request, pgID):
    pg = pgDetails.objects.get(pgID=pgID)
    pg_facilities = pgFacilities.objects.get(pg=pg)
    pg_rules = pgRules.objects.get(pg=pg)

    request.session['curr_pgID'] = pgID
    edit_pg_details = register_new_pg_form(instance=pg)
    edit_pg_facilities = register_facilities_form(instance=pg_facilities)
    edit_pg_rules = register_rules_form(instance=pg_rules)
    photos = pgPhotos.objects.filter(pg=pg)

    context = {
        'profilePicID': request.session['profilePublicID'],
        'tag': pgID,
        'pg': pg,
        'edit_pg_details': edit_pg_details,
        'edit_pg_facilities': edit_pg_facilities,
        'edit_pg_rules': edit_pg_rules,
        'photos': photos,
    }
    return render(request, './owner/pg_details.html', context)

def edit_pgDetails(request):
    if request.method == "POST":
        edit_details_form = register_new_pg_form(request.POST)
        if edit_details_form.is_valid():
            type = edit_details_form.cleaned_data.get('type')
            floors = edit_details_form.cleaned_data.get('floors')
            rooms = edit_details_form.cleaned_data.get('rooms')
            total_intakes = edit_details_form.cleaned_data.get('total_intakes')
            available_intakes = edit_details_form.cleaned_data.get('available_intakes')
            start_rent = edit_details_form.cleaned_data.get('start_rent')
            end_rent = edit_details_form.cleaned_data.get('end_rent')
            name = edit_details_form.cleaned_data.get('name')
            address = edit_details_form.cleaned_data.get('address')
            area = edit_details_form.cleaned_data.get('area')
            city = edit_details_form.cleaned_data.get('city')
            state = edit_details_form.cleaned_data.get('state')
            description = edit_details_form.cleaned_data.get('description')
            owner = Owner.objects.get(user=request.user)
            pgID = request.session['curr_pgID']
            temp = pgDetails(type=type, floors=floors, rooms=rooms, total_intakes=total_intakes, available_intakes=available_intakes, start_rent=start_rent, end_rent=end_rent, name=name, address=address, area=area, city=city, state=state, description=description, owner=owner, pgID=pgID)
            temp.save()
            print("Updated.")

    return redirect('pg_details', pgID)

def edit_pgFacilities(request):
    if request.method == "POST":
        edit_facilities_form = register_facilities_form(request.POST)
        if edit_facilities_form.is_valid():
            pgID = request.session['curr_pgID']
            pg = pgDetails.objects.get(pgID=pgID)

            temp = pgFacilities.objects.get(pg=pg)

            temp.ac = edit_facilities_form.cleaned_data.get('ac')
            temp.balcony = edit_facilities_form.cleaned_data.get('balcony')
            temp.laundry = edit_facilities_form.cleaned_data.get('laundry')
            temp.breakfast = edit_facilities_form.cleaned_data.get('breakfast')
            temp.lunch = edit_facilities_form.cleaned_data.get('lunch')
            temp.dinner = edit_facilities_form.cleaned_data.get('dinner')
            temp.parking = edit_facilities_form.cleaned_data.get('parking')
            temp.cleaning = edit_facilities_form.cleaned_data.get('cleaning')
            temp.wifi = edit_facilities_form.cleaned_data.get('wifi')
            temp.tv = edit_facilities_form.cleaned_data.get('tv')
            temp.fridge = edit_facilities_form.cleaned_data.get('fridge')
            temp.ro = edit_facilities_form.cleaned_data.get('ro')
            temp.gym = edit_facilities_form.cleaned_data.get('gym')
            temp.lift = edit_facilities_form.cleaned_data.get('lift')
            temp.generator = edit_facilities_form.cleaned_data.get('generator')
            temp.save()

    return redirect('pg_details', request.session['curr_pgID'])

def edit_pgRules(request):
    if request.method == "POST":
        edit_rules_form = register_rules_form(request.POST)
        if edit_rules_form.is_valid():
            pgID = request.session['curr_pgID']
            pg = pgDetails.objects.get(pgID=pgID)

            temp = pgRules.objects.get(pg=pg)
            temp.deposit = edit_rules_form.cleaned_data.get('deposit')
            temp.haveClosingTime = edit_rules_form.cleaned_data.get('haveClosingTime')
            temp.visitors = edit_rules_form.cleaned_data.get('visitors')
            temp.nonVeg = edit_rules_form.cleaned_data.get('nonVeg')
            temp.oppositeGender = edit_rules_form.cleaned_data.get('oppositeGender')
            temp.smoking = edit_rules_form.cleaned_data.get('smoking')
            temp.drinking = edit_rules_form.cleaned_data.get('drinking')
            temp.loudMusic = edit_rules_form.cleaned_data.get('loudMusic')
            temp.party = edit_rules_form.cleaned_data.get('party')

            temp.save()

    return redirect('pg_details', request.session['curr_pgID'])

def delete_photo(request, photoPID):
    pgPhotos.objects.filter(photoPID=photoPID).delete()
    print("delete from database")
    cloudinary.api.delete_resources([photoPID])
    print("delete from cloud")

    return redirect('pg_details', request.session['curr_pgID'])

def upload_new_photo(request):
    upload_form = register_photo_form(request.POST or None)
    pgID = request.session['curr_pgID']
    photoPID = get_next_photoPID(pgID)
    pid = "PGF/PG_Photos/" + pgID + "_" + photoPID
    context = {
        'pid': pid,
        'tag': pgID,
        'upload_form': upload_form,
    }
    if upload_form.is_valid():
        message = upload_form.cleaned_data.get('message')
        new_photo = pgPhotos(pg=pgDetails.objects.get(pgID=pgID), photoPID=pid, message=message)
        new_photo.save()
        print("saved")
        return redirect('pg_details', pgID)
    return render(request, './owner/upload_new_photo.html', context)

#Utility Functions
def get_next_pgID():
    lastPg = pgDetails.objects.all().last()
    if lastPg:
        id = int(getattr(lastPg, 'pgID')[2:])+1
        nextpgID = "pg" + str(id)
        return nextpgID
    return "pg1"

def get_next_photoPID(pgID):
    last_photo = pgPhotos.objects.filter(pg=pgDetails.objects.get(pgID=pgID)).last()
    if last_photo:
        id = int(getattr(last_photo, 'photoPID')[21:])+1
        nextPID = "pic"+str(id)
        return nextPID
    return "pic1"