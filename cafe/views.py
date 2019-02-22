from django.shortcuts import render
from django.http import HttpResponse

def home(request):	
	# Construct a dictionary to pass to the template engine as its context.
	context_dict = {}
	
	return render(request, 'cafe/home.html', context=context_dict)


def about (request):
	
	context_dict = {'boldmessage': "This is about page "}

	return render(request, 'cafe/about.html', context=context_dict)

def cafes(request):	

	context_dict = {}
	
	return render(request, 'cafe/cafes.html', context=context_dict)

def chosen_cafe(request):	

	context_dict = {}
	
	return render(request, 'cafe/chosen_cafe.html', context=context_dict)
	

def sign_up(request):
	# # A boolean value for telling the template
	# # whether the registration was successful.
	# # Set to False initially. Code changes value to
	# # True when registration succeeds.
	# registered = False
	# # If it's a HTTP POST, we're interested in processing form data.
	# if request.method == 'POST':
		# # Attempt to grab information from the raw form information.
		# # Note that we make use of both UserForm and UserProfileForm.
		# user_form = UserForm(data=request.POST)
		# profile_form = UserProfileForm(data=request.POST)
		
		# # If the two forms are valid...
		# if user_form.is_valid() and profile_form.is_valid():
			# # Save the user's form data to the database.
			# user = user_form.save()
			# # Now we hash the password with the set_password method.
			# # Once hashed, we can update the user object.
			# user.set_password(user.password)
			# user.save()
			
			# # Now sort out the UserProfile instance.
			# # Since we need to set the user attribute ourselves,
			# # we set commit=False. This delays saving the model
			# # until we're ready to avoid integrity problems.
			# profile = profile_form.save(commit=False)
			# profile.user = user

			# # Now we save the UserProfile model instance.
			# profile.save()
			
			# # Update our variable to indicate that the template
			# # registration was successful.
			# registered = True
		# else:
			# # Invalid form or forms - mistakes or something else?
			# # Print problems to the terminal.
			# print(user_form.errors, profile_form.errors)
	# else:
		# # Not a HTTP POST, so we render our form using two ModelForm instances.
		# # These forms will be blank, ready for user input.
		# user_form = UserForm()
		# profile_form = UserProfileForm()
	# # Render the template depending on the context.
	# return render(request, 'cafe/sign_up.html', 
	# {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
	context_dict = {}
	
	return render(request, 'cafe/sign_up.html', context=context_dict)
	
def user_login(request):
	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.We use 
		# request.POST.get('<variable>') as opposed to request.POST['<variable>'], 
		# because the request.POST.get('<variable>') returns None if value doesn't
		# exist, while request.POST['<variable>'] will raise a KeyError exception.
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)
		
		# If we have a User object, the details are correct.
		# If None (Python's way of representing the absence of a value),
		# Display Error message.
	
		if user:
			# If the account is valid we can log the user in.
			# We'll send the user back to the homepage.
			login(request, user)
			return HttpResponseRedirect(reverse('home'))
		else:
			# Bad login details were provided. So we can't log the user in.
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")
			#return HttpResponseRedirect(reverse('login'))
			
	# The request is not a HTTP POST, so display the login form.
	# This scenario would most likely be a HTTP GET.
	else:
		# No context variables to pass to the template system, hence the
		# blank dictionary object...
		return render(request, 'cafe/login.html', {})
	
def my_account(request):	

	context_dict = {}
	
	return render(request, 'cafe/my_account.html', context=context_dict)

# # Use the login_required() decorator to ensure only those logged in can
# # access the view.
# #@login_required
# def user_logout(request):
	# # Since we know the user is logged in, we can now just log them out.
	# logout(request)
	# # Take the user back to the homepage.
	# return HttpResponseRedirect(reverse('home'))