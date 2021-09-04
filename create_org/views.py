from django.shortcuts import render , redirect , get_object_or_404 , reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import Model_fields , UserCreationForm  , User_Add
from .models import Organisation
from django.utils.text import slugify
from django.http import JsonResponse 

# Create your views here.
def home(request):
	


	return render (request , 'create_org/home.html' )


def signin_view(request):
	if request.method=='GET':
		return render(request, 'create_org/signin.html', {'form':UserCreationForm()})
	else:
		if request.POST['password1']==request.POST['password2']:
			try:
				user=User.objects.create_user(request.POST['username'], password=request.POST['password1'] ,email=request.POST['email'])
				user.save()
				login(request, user)
				return redirect('create_org:landing')

			except IntegrityError:
				return render(request, 'create_org/signin.html', {'form':UserCreationForm(), 'error':'The username is already taken, try something different'})
		else:
			return render(request, 'create_org/signin.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})




def login_view(request):
	if request.method=='GET':
		return render(request, 'create_org/login.html', {'form':AuthenticationForm()})
	else:
		user=authenticate(request, username=request.POST['username'], password=request.POST['password'])
		if user is None:
			return render(request, 'create_org/login.html', {'form':AuthenticationForm(), 'error': 'No username registered'})
		else:
			login(request, user)
			return redirect('create_org:landing')


@login_required
def landing_page(request):
	
	
	return render (request, 'create_org/landing.html')


@login_required
def logout_view(request):
	if request.method=='POST':
		logout(request)
		return redirect('create_org:home')

@login_required
def new_org(request):
	print(request.user)
	if request.method=='GET':
		return render(request, 'create_org/new_org.html', {'form':Model_fields()})
	else:
		form= Model_fields(request.POST or None , request.FILES or None)
		if form.is_valid():		

			organisation_set=form.save(commit=False)
			organisation_set.owner=request.user
			organisation_set.save()
			return redirect('create_org:view_org')
		else:
			return render(request, 'create_org/new_org.html', {'form':Model_fields() , 'error':form.errors})

@login_required
def view_org(request):
	organisations = Organisation.objects.all().order_by('name')
	return render (request, 'create_org/view_org.html' , {'organisations':organisations})

@login_required
def organisation(request , name):
	organisations=get_object_or_404(Organisation, slug=name)
	if request.method == 'GET':
		user = User.objects.all()
		details = Organisation.objects.get(slug=name)
		# editable=Model_fields(instance=organisations)
		return render(request, 'create_org/organisation.html', {'details':details , 'user':user })
	else:
		try:
			form=Model_fields(request.POST , request.FILES ,instance=organisations)
			form.save()
			updated_value=Organisation.objects.get(slug=name)
			updated_value.slug=slugify(updated_value.name)
			updated_value.save()
			return redirect(reverse('create_org:organisation' , kwargs={'name': organisations.slug}))
		except ValueError:
			return render (request , 'create_org/organisation.html' , {'form':form , 'error':'bad info'})





@login_required
def del_org(request, name):
	organisations = get_object_or_404(Organisation, slug=name, owner=request.user)
	if request.method == 'POST':
		organisations.delete()
		return redirect('create_org:view_org')
	else:
		return render(request, 'create_org/delete_org.html' , {'organisations':organisations})




@login_required
def add_user(request, name):
	organisation= get_object_or_404(Organisation , slug=name )
	for x in organisation.members.all():
		print(x)
	if request.method == 'POST':
		key_of_user=request.POST.get('members')
		user=User.objects.get(id=key_of_user)
		organisation.members.add(user)
		organisation.save()
		return redirect(reverse('create_org:organisation' , kwargs={'name': organisation.slug}))
	else:
		# user = User.objects.all()
		return render(request , 'create_org/add_user.html' , {'organisation':organisation , 'user':user})


@login_required	
def fetch_member(request):
	if request.method=="POST" and request.is_ajax():
		value=request.POST['query']
		member_array=[]
		user = User.objects.all()
		for u in user:
			if (u.username.lower()).startswith(value.lower()):
				member_array.append({'user_id': u.id, 'user_name': u.username})


		return JsonResponse({'error': "Nothing found", 'member_array' : member_array } )

@login_required
def org_members(request, name):
	organisation= get_object_or_404(Organisation , slug=name )
	if request.method=='GET':
		details = Organisation.objects.get(slug=name)
		return render(request , 'create_org/org_members.html' , {'organisation':organisation ,'details':details} )
	else:
		try:
			form=Model_fields(request.POST , request.FILES ,instance=organisation)
			form.save()
			updated_value=Organisation.objects.get(slug=name)
			updated_value.slug=slugify(updated_value.name)
			updated_value.save()
			return redirect(reverse('create_org:organisation' , kwargs={'name': organisation.slug}))
		except ValueError:
			return render (request , 'create_org/organisation.html' , {'form':form , 'error':'bad info'})

@login_required
def delete_members(request , name):
	organisations = get_object_or_404(Organisation, slug=name, owner=request.user)
	if request.method == 'POST':
		del_instance=request.POST['members_id']
		print(del_instance)
		user=User.objects.get(id=del_instance)
		organisations.members.remove(user)
		organisations.save()

		
		return redirect(reverse('create_org:org_members' , kwargs={'name': organisations.slug}))
	else:
		return render(request, 'create_org/org_members.html' , {'organisations':organisations})
