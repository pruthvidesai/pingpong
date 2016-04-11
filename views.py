from django.shortcuts import render
from pingpong.forms import UserForm, UserProfileForm


def register(request):

    # a boolean value for telling template whether the registration was successful
    registered = False

    # if it's HTTP POST we're interested in processing form data
    if request.method == 'POST':
        # attempt to grab information from raw form information
        # making use of both UserForm and UserProfileForm
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # if both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # save user's form to database
            user = user_form.save()

            # hash user's password
            # once hashed, save user's object
            user.set_password(user.password)
            user.save()

            # now we sort out UserProfileForm
            # Since we create this attribute ourselves, we commit=False
            # delaying saving models to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # did user provide a profile picture?
            # if so, we need to get the input and put it in UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # now we save the UserProfle model instance
            profile.save()

            # time to update register variable
            registered = True

        # print errors on terminal if forms invalid
        # it'll also be shown to the user
        else:
            print user_form.errors, profile_form.errors

    # if not an HTTP POST, we render our two ModelForm instances
    # render would be empty, ready for input
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # render the template based on the request
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})


