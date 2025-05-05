from django.contrib import admin
from .models import UserProfile, ExerciseHistory, MealHistory
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'height_feet', 'height_inches', 'weight_lbs', 'fitness_goal', 'target_weight_lbs', 'daily_calorie_goal')
    search_fields = ['user__username', 'fitness_goal']
    list_filter = ['fitness_goal']

class ExerciseHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'exercise_name', 'exercise_type', 'duration', 'calories_burned', 'date')
    list_filter = ['exercise_type', 'date']
    search_fields = ['user__username', 'exercise_name']
    date_hierarchy = 'date'

class MealHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_name', 'calories', 'protein', 'carbs', 'fat', 'date')
    list_filter = ['date']
    search_fields = ['user__username', 'food_name']
    date_hierarchy = 'date'

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ExerciseHistory, ExerciseHistoryAdmin)
admin.site.register(MealHistory, MealHistoryAdmin)
