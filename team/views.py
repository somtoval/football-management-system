from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile, Player, Coach, Message, UpcomingMatches
from django.contrib.auth import authenticate, login, logout
from .forms import PlayerForm, CoachForm, PlayerCreationForm
from django.contrib.auth.models import User

from datetime import datetime


def index(request):
    players = Player.objects.all()
    print(f'PLAYERS: {players}')
    for player in players:
        print(f'PLAYER USERNAME: {player.user_profile.user.username}')
        print(f'PLAYER FIRSTNAME: {player.user_profile.user.first_name}')
        print(f'PLAYER LASTNAME: {player.user_profile.user.last_name}')
        print(f'PLAYER IMAGE: {player.pic.url}')

    if request.method == 'POST':
        if request.POST.get('form_id') == 'message-form':
            message_name = request.POST.get('message_name')
            message_email = request.POST.get('message_email')
            message_text = request.POST.get('message_text')

            Message.objects.create(name=message_name, email=message_email, message=message_text)
            messages.success(request, 'Your Message has been Sent!')
    context = {'players': players}
    return render(request, 'index.html', context)

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # If the user is not None
        if user is not None:
            login(request, user)

            # Check if "Remember Me" was checked
            if not request.POST.get('remember_me', None):
                # Set session to expire at browser close
                request.session.set_expiry(0)
            else:
                # Set session to expire after 2 weeks
                request.session.set_expiry(1209600)  # 2 weeks in seconds
            messages.success(request, 'You have been successfully logged in!')
            return redirect('account')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'signin.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'signin.html')
    
def signout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out!')
    return redirect('index')

def accounts(request):
    if request.user.userprofile.is_coach == False:
        user_profile = request.user.userprofile
        player_instance = user_profile.player
        form = PlayerForm(instance=player_instance)

        upcoming_matches = UpcomingMatches.objects.all().order_by('-id')
        current_date = datetime.now().date()
        for match in upcoming_matches:
            days_until_match = (match.date - current_date).days
            match.days_until_match = days_until_match

        if request.method == 'POST':
            form = PlayerForm(request.POST, request.FILES, instance=player_instance)
            if form.is_valid():

                # Update user's name if changed in the form
                new_full_name = request.POST.get('full_name')# we are getting the full name form the post request because it is not part of the form
                print("NEW FULL_NAME: %s" % new_full_name)
                if new_full_name != user_profile.user.get_full_name():
                    user_profile.user.first_name, user_profile.user.last_name = new_full_name.split(" ", 1)
                    user_profile.user.save()

                # Update user's email if changed in the form
                new_email = request.POST.get('email')
                if new_email != user_profile.user.email:
                    user_profile.user.email = new_email
                    user_profile.user.save()

                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('account')
            else:
                print(form.errors)  # Print form errors for debugging purposes

        context = {'form': form, 'user_profile': user_profile, 'upcoming_matches': upcoming_matches}
        return render(request, 'account.html', context)
    
    else:
        print('I am a Coach')
        user_profile = request.user.userprofile
        coach_instance = user_profile.coach
        form = CoachForm(instance=coach_instance)
        my_messages = Message.objects.all().order_by('-id')

        upcoming_matches = UpcomingMatches.objects.all().order_by('-id')
        current_date = datetime.now().date()
        for match in upcoming_matches:
            days_until_match = (match.date - current_date).days
            match.days_until_match = days_until_match

        if request.method == 'POST':
            if request.POST.get('form_id') == 'match-form':
                match_name = request.POST.get('match-name')
                match_date = request.POST.get('match-date')
                print(f'Match: {match_name}, Date: {match_date}')
                UpcomingMatches.objects.create(name=match_name, date=match_date)
                messages.success(request, 'Match added successfully!')
            elif request.POST.get('form_id') == 'player-form':
                player_full_name = request.POST.get('player_fullName')
                player_email = request.POST.get('player_email')
                player_age = request.POST.get('player_age')
                player_bio = request.POST.get('player_bio')
                player_wing = request.POST.get('player_wing')
                player_height = request.POST.get('player_height')
                player_speed = request.POST.get('player_speed')
                player_pic = request.FILES['player_pic']
                # player_password1 = request.POST.get('')
                # player_password2 = request.POST.get('')

                print(f'Player Name: {player_full_name}')
                print(f'Player Email: {player_email}')
                print(f'Player Age: {player_age}')
                print(f'Player Bio: {player_bio}')
                print(f'Player Wing: {player_wing}')
                print(f'Player Height: {player_height}')
                print(f'Player Speed: {player_speed}')
                print(f'Player Pic: {player_pic}')

                print(f'Player Username: {player_full_name.split()[0]}')
                
                # Creating the player
                new_player = User.objects.create_user(username=player_full_name.split()[0], email=player_email, password="myplayer123")
                new_player.first_name = player_full_name.split()[0]
                new_player.last_name = player_full_name.split()[1]
                new_player.save()

                new_player_profile = UserProfile.objects.create(user=new_player, is_coach=False)
                new_player_profile.save()

                new_player_player_info = Player.objects.create(user_profile=new_player_profile, age=player_age, speed=player_speed, bio=player_bio, wing=player_wing, height=player_height, pic=player_pic)
                new_player_player_info.save()
            else:
                print(f'Request.POST: {request.POST}')
                form = CoachForm(request.POST, request.FILES, instance=coach_instance)
                if form.is_valid():

                    # Update user's name if changed in the form
                    new_full_name = request.POST.get('full_name')# we are getting the full name form the post request because it is not part of the form
                    print("NEW FULL_NAME: %s" % new_full_name)
                    if new_full_name != user_profile.user.get_full_name():
                        user_profile.user.first_name, user_profile.user.last_name = new_full_name.split(" ", 1)
                        user_profile.user.save()

                    # Update user's email if changed in the form
                    new_email = request.POST.get('email')
                    if new_email != user_profile.user.email:
                        user_profile.user.email = new_email
                        user_profile.user.save()

                    form.save()
                    messages.success(request, 'Profile updated successfully!')
                    return redirect('account')
                else:
                    print(form.errors)  # Print form errors for debugging purposes
                

        context = {'form': form, 'user_profile': user_profile, 'upcoming_matches': upcoming_matches, 'my_messages': my_messages}
        return render(request, 'account.html', context)
    
def deleteMatch(request, pk):
    match = UpcomingMatches.objects.get(id=pk)
    if request.method == "POST":
        match.delete()
        return redirect('account')
    context = {"item": match}
    return render(request, 'delete.html', context)