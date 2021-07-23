from django.shortcuts import render, HttpResponse, redirect
from accounts.models import Owner
from django.contrib.auth.decorators import login_required
import cloudinary
from .forms import register_new_pg_form, register_facilities_form, register_rules_form, register_photo_form
from .models import pgDetails, pgFacilities, roomDetails, pgPhotos, pgRules, ratings, messages, applicationDetails

# Create your views here.
@login_required
def o_dashboard(request):
    user_type = request.session['user_type']
    user = request.user
    profilePublicID = getattr(Owner.objects.get(user=user), 'profilePicID')
    profilePic = cloudinary.CloudinaryImage(profilePublicID).build_url(width = 200, height = 200, crop = 'fill', gravity="face")

    context = {
        'user_type': user_type,
        'user': user,
        'profilePic': profilePic,
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
            del request.session['photoPID']
            print("Photo saved")
            return redirect('o_register_success')

    return render(request, './owner/register_pg_photos.html', {'tag': pgID})

def o_upload_pic(request):
    upload_form = register_photo_form(request.POST or None)
    pgID = request.session['new_pgID']
    photoPID = get_next_photoPID(pgID)
    pid = "PGF/PG_Photos/" + pgID + "_" + photoPID
    request.session['photoPID'] = pid

    return render(request, './owner/upload_photo.html', {'upload_form': upload_form, 'tag': pgID, 'pid': pid})

def o_register_success(request):
    return render(request, './owner/register_success.html')

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