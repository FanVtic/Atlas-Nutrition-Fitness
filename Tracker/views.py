from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import ExerciseHistory, MealHistory, UserProfile
from .forms import CustomUserCreationForm, UserProfileForm
import json
import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.db.models import Sum
from datetime import datetime, timedelta

#MpAPX370pR9DhMu9XVcFrA==iN04uaJGdT0qoW53

# Create your views here.
def home(request):
    return render(request, 'home.html')

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Ensure user has a profile
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(user=user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

@login_required
def foodie(request):
    if request.method == 'POST':
        if 'track_meal' in request.POST:
            # Handle meal tracking
            food_name = request.POST.get('food_name')
            calories = int(request.POST.get('calories', 0))
            protein = float(request.POST.get('protein', 0))
            carbs = float(request.POST.get('carbs', 0))
            fat = float(request.POST.get('fat', 0))
            fiber = float(request.POST.get('fiber', 0))
            sugar = float(request.POST.get('sugar', 0))
            sodium = float(request.POST.get('sodium', 0))
            notes = request.POST.get('notes', '')

            MealHistory.objects.create(
                user=request.user,
                food_name=food_name,
                calories=calories,
                protein=protein,
                carbs=carbs,
                fat=fat,
                fiber=fiber,
                sugar=sugar,
                sodium=sodium,
                notes=notes
            )
            return redirect('foodie')

        # Handle food search
        query = request.POST['query']
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
        api_request = requests.get(api_url + query, headers={'X-Api-Key':'MpAPX370pR9DhMu9XVcFrA==iN04uaJGdT0qoW53'})
        try:
            api = json.loads(api_request.content)
            print(api_request.content)
        except Exception as e:
            api = 'oops! There was an Error'
            print(e)
        return render(request, 'foodie.html', {
            'api': api,
            'meal_history': MealHistory.objects.filter(user=request.user)[:5]
        })
    else: 
        return render(request, 'foodie.html', {
            'query': 'Enter a valid Query',
            'meal_history': MealHistory.objects.filter(user=request.user)[:5]
        })

@login_required
def exercises(request):
    if request.method == 'POST':
        if 'track_exercise' in request.POST:
            # Handle exercise tracking
            exercise_name = request.POST.get('exercise_name')
            exercise_type = request.POST.get('exercise_type')
            duration = int(request.POST.get('duration', 0))
            sets = request.POST.get('sets')
            reps = request.POST.get('reps')
            notes = request.POST.get('notes', '')

            # Calculate calories burned using the API
            try:
                api_url = 'https://api.api-ninjas.com/v1/caloriesburned?activity={}'.format(exercise_name.lower())
                response = requests.get(
                    api_url, 
                    headers={'X-Api-Key':'MpAPX370pR9DhMu9XVcFrA==iN04uaJGdT0qoW53'}
                )
                
                if response.status_code == requests.codes.ok:
                    calorie_data = json.loads(response.text)
                    if calorie_data:
                        # Calculate calories based on duration
                        calories_per_hour = calorie_data[0]['calories_per_hour']
                        calories_burned = int((calories_per_hour / 60) * duration)
                    else:
                        # Default calculation if exercise not found
                        calories_burned = int(duration * 5)  
                else:
                    calories_burned = int(duration * 5)  
            except Exception as e:
                print(f"Error calculating calories: {e}")
                calories_burned = int(duration * 5)  

            ExerciseHistory.objects.create(
                user=request.user,
                exercise_name=exercise_name,
                exercise_type=exercise_type,
                duration=duration,
                calories_burned=calories_burned,
                sets=sets,
                reps=reps,
                notes=notes
            )
            return redirect('exercises')

        # Handle exercise search
        original_query = request.POST['query'].strip()
        query = original_query.lower()  #
        print(f"Original search query: {original_query}")  
        
        #Different search variations
        search_variations = [
            query,  
            query.replace(' ', ''),  
            query + 's',  
            query.replace(' ', '') + 's'  
        ]
        
        api = None
        found_term = None
        for search_term in search_variations:
            print(f"Trying search term: {search_term}")  
            
            # Try searching by name
            api_url = 'https://api.api-ninjas.com/v1/exercises?name='
            api_request = requests.get(
                api_url + search_term, 
                headers={'X-Api-Key':'MpAPX370pR9DhMu9XVcFrA==iN04uaJGdT0qoW53'}
            )
            print(f"API Response Status for {search_term}: {api_request.status_code}")  
            
            try:
                result = json.loads(api_request.content)
                print(f"API Response for {search_term}: {result}")  
                if result and isinstance(result, list) and len(result) > 0:  
                    api = result
                    found_term = search_term
                    print(f"Found results with term: {search_term}")  
                    break
            except Exception as e:
                print(f"Error parsing API response for {search_term}: {e}")  
                continue
        
        # If no results found by name variations, try muscle search
        if not api:
            print("No results found by name variations, trying muscle search...")  
            muscle_api_url = 'https://api.api-ninjas.com/v1/exercises?muscle='
            muscle_api_request = requests.get(
                muscle_api_url + query,
                headers={'X-Api-Key':'MpAPX370pR9DhMu9XVcFrA==iN04uaJGdT0qoW53'}
            )
            try:
                result = json.loads(muscle_api_request.content)
                if result and isinstance(result, list) and len(result) > 0:
                    api = result
                    found_term = f"muscle: {query}"
            except Exception as e:
                print(f"Error parsing muscle API response: {e}")  
                api = None

        # Prepare context for template
        context = {
            'exercise_history': ExerciseHistory.objects.filter(user=request.user)[:5]
        }

        if not api or not isinstance(api, list) or len(api) == 0:
            print("No exercises found after all search attempts")  
            context.update({
                'api': [],
                'message': f'No exercises found for "{original_query}"'
            })
        else:
            print(f"Found exercise data with term: {found_term}")  
            print(f"Final API data: {api}")  
            context.update({
                'api': api,
                'search_term_used': found_term
            })

        return render(request, 'exercises.html', context)
    else: 
        return render(request, 'exercises.html', {
            'query': 'Enter a valid exercise name or muscle group',
            'exercise_history': ExerciseHistory.objects.filter(user=request.user)[:5]
        })

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    # Get user's activity data
    total_exercises = ExerciseHistory.objects.filter(user=request.user).count()
    total_calories_burned = ExerciseHistory.objects.filter(user=request.user).aggregate(total=Sum('calories_burned'))['total'] or 0
    total_food_items = MealHistory.objects.filter(user=request.user).count()
    
    # Get recent activities
    exercises = ExerciseHistory.objects.filter(user=request.user).order_by('-date')[:5]
    meals = MealHistory.objects.filter(user=request.user).order_by('-date')[:5]
    
    recent_activities = []
    for exercise in exercises:
        recent_activities.append({
            'type': 'exercise',
            'name': exercise.exercise_name,
            'date': exercise.date,
            'id': exercise.id
        })
    
    for meal in meals:
        recent_activities.append({
            'type': 'meal',
            'name': meal.food_name,
            'date': meal.date,
            'id': meal.id
        })
    
    recent_activities = sorted(recent_activities, key=lambda x: x['date'], reverse=True)[:5]

    # Get progress data for the chart
    progress_dates = []
    calories_data = []
    
    # Get last 7 days of exercise data
    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        calories = ExerciseHistory.objects.filter(
            user=request.user,
            date__date=date.date()
        ).aggregate(total=Sum('calories_burned'))['total'] or 0
        
        progress_dates.append(date.strftime('%Y-%m-%d'))
        calories_data.append(calories)
    
    progress_dates.reverse()
    calories_data.reverse()

    context = {
        'user': request.user,
        'form': form,
        'total_exercises': total_exercises,
        'total_calories_burned': total_calories_burned,
        'total_food_items': total_food_items,
        'recent_activities': recent_activities,
        'progress_dates': json.dumps(progress_dates),
        'calories_data': json.dumps(calories_data)
    }
    
    return render(request, 'profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def delete_exercise(request, exercise_id):
    try:
        exercise = ExerciseHistory.objects.get(id=exercise_id, user=request.user)
        exercise.delete()
        messages.success(request, 'Exercise deleted successfully!')
    except ExerciseHistory.DoesNotExist:
        messages.error(request, 'Exercise not found.')
    return redirect('profile')

@login_required
def delete_meal(request, meal_id):
    try:
        meal = MealHistory.objects.get(id=meal_id, user=request.user)
        meal.delete()
        messages.success(request, 'Meal deleted successfully!')
    except MealHistory.DoesNotExist:
        messages.error(request, 'Meal not found.')
    return redirect('profile')