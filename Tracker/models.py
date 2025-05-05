from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Sum, Count

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    height_feet = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    height_inches = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(11)], null=True, blank=True)
    weight_lbs = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)
    fitness_goal = models.CharField(max_length=100, null=True, blank=True)
    target_weight_lbs = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)
    daily_calorie_goal = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def height_in_cm(self):
        if self.height_feet is not None and self.height_inches is not None:
            total_inches = (self.height_feet * 12) + self.height_inches
            return round(total_inches * 2.54, 1)
        return None

    @property
    def weight_in_kg(self):
        if self.weight_lbs is not None:
            return round(self.weight_lbs * 0.45359237, 1)
        return None

    @property
    def target_weight_in_kg(self):
        if self.target_weight_lbs is not None:
            return round(self.target_weight_lbs * 0.45359237, 1)
        return None

    @property
    def total_exercises(self):
        return ExerciseHistory.objects.filter(user=self.user).count()

    @property
    def total_calories_burned(self):
        return ExerciseHistory.objects.filter(user=self.user).aggregate(total=Sum('calories_burned'))['total'] or 0

    @property
    def total_food_items(self):
        return MealHistory.objects.filter(user=self.user).count()

    @property
    def recent_activities(self):
        exercises = ExerciseHistory.objects.filter(user=self.user).order_by('-date')[:5]
        meals = MealHistory.objects.filter(user=self.user).order_by('-date')[:5]
        
        activities = []
        for exercise in exercises:
            activities.append({
                'type': 'exercise',
                'name': exercise.exercise_name,
                'date': exercise.date
            })
        
        for meal in meals:
            activities.append({
                'type': 'meal',
                'name': meal.food_name,
                'date': meal.date
            })
        
        return sorted(activities, key=lambda x: x['date'], reverse=True)[:5]

class Meal(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    food_items = models.TextField()
    calories = models.IntegerField(validators=[MinValueValidator(0)])
    protein = models.FloatField(validators=[MinValueValidator(0)])
    carbs = models.FloatField(validators=[MinValueValidator(0)])
    fat = models.FloatField(validators=[MinValueValidator(0)])
    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-logged_at']

    def __str__(self):
        return f"{self.user.username} - {self.meal_type} ({self.logged_at})"

class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    duration_minutes = models.IntegerField(validators=[MinValueValidator(0)])
    calories_burned = models.IntegerField(validators=[MinValueValidator(0)])
    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-logged_at']

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} ({self.logged_at})"

class BodyMetrics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight_kg = models.FloatField(validators=[MinValueValidator(0)])
    body_fat_percentage = models.FloatField(validators=[MinValueValidator(0)])
    recorded_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']
        verbose_name_plural = "Body Metrics"

    def __str__(self):
        return f"{self.user.username} - {self.recorded_at}"

class ExerciseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=100)
    exercise_type = models.CharField(max_length=50)
    duration = models.IntegerField()  # in minutes
    calories_burned = models.IntegerField()
    sets = models.CharField(max_length=10, blank=True, null=True)
    reps = models.CharField(max_length=10, blank=True, null=True)
    notes = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.exercise_name} - {self.date.strftime('%Y-%m-%d')}"

class MealHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    calories = models.IntegerField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()
    fiber = models.FloatField()
    sugar = models.FloatField()
    sodium = models.FloatField()
    notes = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_name} - {self.date.strftime('%Y-%m-%d')}"
