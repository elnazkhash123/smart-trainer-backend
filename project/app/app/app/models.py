# from django.db import models

# class UserProfile(models.Model):
#     language = models.CharField(max_length=2, choices=[('en', 'English'), ('fa', 'Persian')], default='en')
#     name = models.CharField(max_length=100)
#     gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
#     height_cm = models.FloatField()
#     weight_kg = models.FloatField()
#     bmi = models.FloatField()
#     level = models.CharField(max_length=20, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advance', 'Advance')])
#     posture_issues = models.JSONField(default=list)  # Store posture issues as a JSON list
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

# class WorkoutProgram(models.Model):
#     user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='workout_programs')
#     week_number = models.IntegerField()
#     description = models.TextField()
#     frequency = models.CharField(max_length=100)
#     intensity = models.CharField(max_length=100)
#     time = models.CharField(max_length=100)
#     type = models.CharField(max_length=100)

#     def __str__(self):
#         return f"Week {self.week_number} for {self.user_profile.name}"

# class WorkoutDay(models.Model):
#     program = models.ForeignKey(WorkoutProgram, on_delete=models.CASCADE, related_name='week')
#     day = models.CharField(max_length=20)
#     focus = models.CharField(max_length=100, blank=True, null=True)
#     exercise = models.CharField(max_length=100, blank=True, null=True)  # For rest days

#     def __str__(self):
#         return f"{self.day} - {self.program}"

# class Exercise(models.Model):
#     workout_day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE, related_name='%(class)s_exercises')
#     exercise_type = models.CharField(max_length=20, choices=[('warm_up', 'Warm-Up'), ('main_workout', 'Main Workout'), ('cool_down', 'Cool-Down')])
#     exercise_name = models.CharField(max_length=100)
#     target = models.CharField(max_length=100)
#     sets = models.IntegerField(blank=True, null=True)
#     reps = models.CharField(max_length=50, blank=True, null=True)
#     duration = models.CharField(max_length=50, blank=True, null=True)
#     rir = models.IntegerField(blank=True, null=True)
#     alternative = models.JSONField(blank=True, null=True)  # For alternative exercises

#     class Meta:
#         abstract = True

# class WarmUpExercise(Exercise):
#     pass

# class MainWorkoutExercise(Exercise):
#     pass

# class CoolDownExercise(Exercise):
#     pass

# class Translation(models.Model):
#     language = models.CharField(max_length=2, choices=[('en', 'English'), ('fa', 'Persian')])
#     key = models.CharField(max_length=100)
#     value = models.TextField()

#     def __str__(self):
#         return f"{self.language} - {self.key}"

# class ExerciseTarget(models.Model):
#     language = models.CharField(max_length=2, choices=[('en', 'English'), ('fa', 'Persian')])
#     exercise_name = models.CharField(max_length=100)
#     target = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.language} - {self.exercise_name}"

# from .models import UserProfile, WorkoutProgram, WorkoutDay, WarmUpExercise, MainWorkoutExercise, CoolDownExercise, Translation, ExerciseTarget
# from datetime import datetime

# class SmartTrainerProfile:
#     def __init__(self, user_profile=None, language="en"):
#         self.user_profile = user_profile or UserProfile(language=language)
#         self.translations = {
#             lang: {t.key: t.value for t in Translation.objects.filter(language=lang)}
#             for lang in ['en', 'fa']
#         }
#         self.exercise_targets = {
#             lang: {t.exercise_name: t.target for t in ExerciseTarget.objects.filter(language=lang)}
#             for lang in ['en', 'fa']
#         }
#         self.days_of_week = {
#             "en": ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
#             "fa": ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"]
#         }

#     def translate(self, key):
#         return self.translations[self.user_profile.language].get(key, key)

#     def translate_target(self, exercise):
#         return self.exercise_targets[self.user_profile.language].get(exercise, "Unknown")

#     def collect_basic_info(self, data):
#         self.user_profile.name = data.get('name')
#         self.user_profile.gender = data.get('gender')
#         self.user_profile.height_cm = float(data.get('height_cm'))
#         self.user_profile.weight_kg = float(data.get('weight_kg'))
#         self.user_profile.level = data.get('level')
#         self.user_profile.save()

#     def calculate_bmi(self):
#         height_m = self.user_profile.height_cm / 100
#         bmi = self.user_profile.weight_kg / (height_m ** 2)
#         self.user_profile.bmi = round(bmi, 2)
#         self.user_profile.save()

#     def collect_posture_analysis(self, data):
#         posture_issues = data.get('posture_issues', [])
#         self.user_profile.posture_issues = posture_issues if posture_issues != ['None'] else []
#         self.user_profile.save()

#     def generate_beginner_general_program(self):
#         if self.user_profile.level != "Beginner":
#             return False, self.translate("invalid_choice")

#         WorkoutProgram.objects.filter(user_profile=self.user_profile).delete()  # Clear existing programs
#         days = self.days_of_week[self.user_profile.language]
#         program_data = [
#             {
#                 "week_number": 1,
#                 "description": self.translate("week_1") + " - " + ("برنامه هفته اول برای مبتدی‌ها - تمرکز بر پایه‌سازی قدرت و تحرک" if self.user_profile.language == "fa" else "focus on building strength and mobility"),
#                 "frequency": "۳ جلسه در هفته (دوشنبه، چهارشنبه، جمعه)" if self.user_profile.language == "fa" else "3 sessions per week (Monday, Wednesday, Friday)",
#                 "intensity": "وزن بدن یا مقاومت سبک - RIR ۲" if self.user_profile.language == "fa" else "Bodyweight or light resistance - RIR 2",
#                 "time": "۳۰-۴۵ دقیقه در هر جلسه" if self.user_profile.language == "fa" else "30-45 minutes per session",
#                 "type": "تمرینات کل بدن" if self.user_profile.language == "fa" else "Full-body workouts",
#                 "week": [
#                     {
#                         "day": days[2],
#                         "focus": "پایین‌تنه (باسن، همسترینگ، چهارسر)" if self.user_profile.language == "fa" else "Lower body (Glutes, Hamstrings, Quads)",
#                         "warm_up": [
#                             {"exercise": "Arm Circles", "target": self.translate_target("Arm Circles"), "duration": "30 seconds"},
#                             {"exercise": "Hip Circles", "target": self.translate_target("Hip Circles"), "duration": "30 seconds"},
#                             {"exercise": "Leg Swings (Forward/Backward)", "target": self.translate_target("Leg Swings (Forward/Backward)"), "duration": "30 seconds per leg"},
#                             {"exercise": "Torso Twists", "target": self.translate_target("Torso Twists"), "duration": "30 seconds"},
#                             {"exercise": "Marching in Place", "target": self.translate_target("Marching in Place"), "duration": "1 minute"}
#                         ],
#                         "main_workout": [
#                             {"exercise": "Bodyweight Squat", "target": self.translate_target("Bodyweight Squat"), "sets": 2, "reps": 10},
#                             {"exercise": "Glute Bridge", "target": self.translate_target("Glute Bridge"), "sets": 2, "reps": 12},
#                             {"exercise": "Standing Kickback (Resistance Band)", "target": self.translate_target("Standing Kickback (Resistance Band)"), "sets": 2, "reps": "10 per leg"},
#                             {"exercise": "Hamstring Curl Lying Down (Towel/Slider)", "target": self.translate_target("Hamstring Curl Lying Down (Towel/Slider)"), "sets": 2, "reps": 10},
#                             {"exercise": "Side-Lying Leg Raise", "target": self.translate_target("Side-Lying Leg Raise"), "sets": 2, "reps": "10 per side"}
#                         ],
#                         "cool_down": [
#                             {"exercise": "Seated Hamstring Stretch", "target": self.translate_target("Seated Hamstring Stretch"), "duration": "30 seconds"},
#                             {"exercise": "Child’s Pose", "target": self.translate_target("Child’s Pose"), "duration": "30 seconds"},
#                             {"exercise": "Cat-Cow Stretch", "target": self.translate_target("Cat-Cow Stretch"), "duration": "30 seconds"},
#                             {"exercise": "Standing Quad Stretch", "target": self.translate_target("Standing Quad Stretch"), "duration": "30 seconds per leg"},
#                             {"exercise": "Shoulder Stretch", "target": self.translate_target("Shoulder Stretch"), "duration": "30 seconds"}
#                         ]
#                     },
#                     # ... (Add other days and weeks similarly, truncated for brevity)
#                 ]
#             },
#             # ... (Add weeks 2, 3, and 4 similarly, following the original structure)
#         ]

#         for week_data in program_data:
#             program = WorkoutProgram.objects.create(
#                 user_profile=self.user_profile,
#                 week_number=week_data['week_number'],
#                 description=week_data['description'],
#                 frequency=week_data['frequency'],
#                 intensity=week_data['intensity'],
#                 time=week_data['time'],
#                 type=week_data['type']
#             )
#             for day_data in week_data['week']:
#                 workout_day = WorkoutDay.objects.create(
#                     program=program,
#                     day=day_data['day'],
#                     focus=day_data.get('focus'),
#                     exercise=day_data.get('exercise')
#                 )
#                 if 'warm_up' in day_data:
#                     for exercise in day_data['warm_up']:
#                         WarmUpExercise.objects.create(
#                             workout_day=workout_day,
#                             exercise_type='warm_up',
#                             exercise_name=exercise['exercise'],
#                             target=exercise['target'],
#                             duration=exercise.get('duration')
#                         )
#                 if 'main_workout' in day_data:
#                     for exercise in day_data['main_workout']:
#                         MainWorkoutExercise.objects.create(
#                             workout_day=workout_day,
#                             exercise_type='main_workout',
#                             exercise_name=exercise['exercise'],
#                             target=exercise['target'],
#                             sets=exercise.get('sets'),
#                             reps=exercise.get('reps'),
#                             rir=exercise.get('rir'),
#                             alternative=exercise.get('alternative')
#                         )
#                 if 'cool_down' in day_data:
#                     for exercise in day_data['cool_down']:
#                         CoolDownExercise.objects.create(
#                             workout_day=workout_day,
#                             exercise_type='cool_down',
#                             exercise_name=exercise['exercise'],
#                             target=exercise['target'],
#                             duration=exercise.get('duration')
#                         )

#         return True, "Program generated successfully."

#     def build_profile(self, data):
#         self.user_profile.language = 'fa' if data.get('language') == 'Persian' else 'en'
#         self.collect_basic_info(data)
#         self.calculate_bmi()
#         self.collect_posture_analysis(data)
#         success, message = self.generate_beginner_general_program()
#         self.user_profile.save()
#         return success, message

# from django.shortcuts import render, redirect
# from .forms import UserProfileForm
# from .utils import SmartTrainerProfile
# from .models import Translation

# def create_profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             trainer = SmartTrainerProfile(user_profile=profile)
#             success, message = trainer.build_profile(form.cleaned_data)
#             if success:
#                 profile.save()
#                 return redirect('display_profile', profile_id=profile.id)
#             else:
#                 form.add_error(None, message)
#     else:
#         form = UserProfileForm()
    
#     translations = {t.key: t.value for t in Translation.objects.filter(language='en')}  # Default to English
#     return render(request, 'smart_trainer/create_profile.html', {'form': form, 'translations': translations})

# def display_profile(request, profile_id):
#     profile = UserProfile.objects.get(id=profile_id)
#     translations = {t.key: t.value for t in Translation.objects.filter(language=profile.language)}
#     return render(request, 'smart_trainer/display_profile.html', {
#         'profile': profile,
#         'translations': translations,
#         'days_of_week': ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] if profile.language == 'en' else ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"]
#     })

# from django.urls import path
# from . import views

# app_name = 'smart_trainer'

# urlpatterns = [
#     path('create/', views.create_profile, name='create_profile'),
#     path('profile/<int:profile_id>/', views.display_profile, name='display_profile'),
# ]

# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('trainer/', include('smart_trainer.urls')),
# ]

# from django.core.management.base import BaseCommand
# from smart_trainer.models import Translation, ExerciseTarget

# class Command(BaseCommand):
#     help = 'Load translations and exercise targets into the database'

#     def handle(self, *args, **kwargs):
#         translations = {
#             "en": {
#                 "select_language": "Select language:",
#                 "your_name": "Your name:",
#                 "your_gender": "Your gender:",
#                 "your_height": "Your height (cm):",
#                 "your_weight": "Your weight (kg):",
#                 "level": "What’s your level: (beginner, intermediate, advance)?",
#                 "posture_issues": "Do you have posture issues?",
#                 "invalid_choice": "Invalid choice. Try again.",
#                 "invalid_input": "Invalid input. Try again.",
#                 "non_negative": "Value must be non-negative. Try again.",
#                 "profile_saved": "Profile and workout programs saved to {}",
#                 "user_profile": "User Profile and Workout Programs",
#                 "week_separator": "=== Week {} ===",
#                 "day_separator": "--- Day: {} ---",
#                 "focus": "Focus",
#                 "warm_up": "Warm-Up",
#                 "main_workout": "Main Workout",
#                 "cool_down": "Cool-Down",
#                 "rest": "Rest",
#                 "week_1": "Week 1",
#                 "week_2": "Week 2",
#                 "week_3": "Week 3",
#                 "week_4": "Week 4"
#             },
#             "fa": {
#                 "select_language": "زبان را انتخاب کنید:",
#                 "your_name": "نام شما:",
#                 "your_gender": "جنسیت شما:",
#                 "your_height": "قد شما (سانتی‌متر):",
#                 "your_weight": "وزن شما (کیلوگرم):",
#                 "level": "سطح خود را بگویید؟ (مبتدی، متوسط، حرفه‌ای)",
#                 "posture_issues": "آیا مشکل بدنی دارید؟",
#                 "invalid_choice": "انتخاب نامعتبر. دوباره امتحان کنید.",
#                 "invalid_input": "ورودی نامعتبر. دوباره امتحان کنید.",
#                 "non_negative": "مقدار باید غیرمنفی باشد. دوباره امتحان کنید.",
#                 "profile_saved": "پروفایل و برنامه‌های تمرینی در {} ذخیره شد",
#                 "user_profile": "پروفایل کاربر و برنامه‌های تمرینی",
#                 "week_separator": "=== هفته {} ===",
#                 "day_separator": "--- روز: {} ---",
#                 "focus": "تمرکز",
#                 "warm_up": "گرم‌کردن",
#                 "main_workout": "تمرین اصلی",
#                 "cool_down": "سرد کردن",
#                 "rest": "استراحت",
#                 "week_1": "هفته ۱",
#                 "week_2": "هفته ۲",
#                 "week_3": "هفته ۳",
#                 "week_4": "هفته ۴"
#             }
#         }

#         exercise_targets = {
#             "en": {
#                 "Arm Circles": "Shoulders",
#                 # ... (Add all exercise targets from the original code, truncated for brevity)
#             },
#             "fa": {
#                 "Arm Circles": "شانه‌ها",
#                 # ... (Add all exercise targets from the original code, truncated for brevity)
#             }
#         }

#         Translation.objects.all().delete()
#         ExerciseTarget.objects.all().delete()

#         for lang, trans_dict in translations.items():
#             for key, value in trans_dict.items():
#                 Translation.objects.create(language=lang, key=key, value=value)

#         for lang, target_dict in exercise_targets.items():
#             for exercise_name, target in target_dict.items():
#                 ExerciseTarget.objects.create(language=lang, exercise_name=exercise_name, target=target)

#         self.stdout.write(self.style.SUCCESS('Successfully loaded translations and exercise targets'))

# from django import forms
# from .models import UserProfile

# class UserProfileForm(forms.ModelForm):
#     language = forms.ChoiceField(choices=[('English', 'English'), ('Persian', 'Persian')])
#     posture_issues = forms.MultipleChoiceField(
#         choices=[('None', 'None'), ('Hunchback', 'Hunchback'), ('Forward head', 'Forward head'), 
#                  ('Pelvic tilt', 'Pelvic tilt'), ('Shoulder imbalance', 'Shoulder imbalance')],
#         widget=forms.CheckboxSelectMultiple
#     )

#     class Meta:
#         model = UserProfile
#         fields = ['language', 'name', 'gender', 'height_cm', 'weight_kg', 'level', 'posture_issues']
#         widgets = {
#             'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
#             'level': forms.Select(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advance', 'Advance')]),
#         }

# from django.db import models

# class UserProfile(models.Model):
#     language = models.CharField(max_length=2, choices=[('en', 'English'), ('fa', 'Persian')], default='en')
#     name = models.CharField(max_length=100)
#     gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
#     height_cm = models.FloatField()
#     weight_kg = models.FloatField()
#     bmi = models.FloatField()
#     level = models.CharField(max_length=20, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advance', 'Advance')])
#     posture_issues = models.JSONField(default=list)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

# class WorkoutProgram(models.Model):
#     user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='workout_programs')
#     week_number = models.IntegerField()
#     description = models.TextField()
#     frequency = models.CharField(max_length=100)
#     intensity = models.CharField(max_length=100)
#     time = models.CharField(max_length=100)
#     type = models.CharField(max_length=100)

#     def __str__(self):
#         return f"Week {self.week_number} for {self.user_profile.name}"

# class WorkoutDay(models.Model):
#     program = models.ForeignKey(WorkoutProgram, on_delete=models.CASCADE, related_name='week')
#     day = models.CharField(max_length=20)
#     focus = models.CharField(max_length=100, blank=True, null=True)
#     exercise = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return f"{self.day} - {self.program}"

# class Exercise(models.Model):
#     workout_day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE, related_name='%(class)s_exercises')
#     exercise_type = models.CharField(max_length=20, choices=[('warm_up', 'Warm-Up'), ('main_workout', 'Main Workout'), ('cool_down', 'Cool-Down')])
#     exercise_name = models.CharField(max_length=100)
#     target = models.CharField(max_length=100)
#     sets = models.IntegerField(blank=True, null=True)
#     reps = models.CharField(max_length=50, blank=True, null=True)
#     duration = models.CharField(max_length=50, blank=True, null=True)
#     rir = models.IntegerField(blank=True, null=True)
#     alternative = models.JSONField(blank=True, null=True)

#     class Meta:
#         abstract = True

# class WarmUpExercise(Exercise):
#     pass

# class MainWorkoutExercise(Exercise):
#     pass

# class CoolDownExercise(Exercise):
#     pass

# class Translation(models.Model):
#     language = models.CharField(max_length=2, choices=[('en', 'English'), ('fa', 'Persian')])
#     key = models.CharField(max_length=100)
#     value = models.TextField()

#     def __str__(self):
#         return f"{self.language} - {self.key}"

# class ExerciseTarget(models.Model):
#     language = models.CharField(max_length=2, choices=[('en', 'English'), ('fa', 'Persian')])
#     exercise_name = models.CharField(max_length=100)
#     target = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.language} - {self.exercise_name}"

# from django.shortcuts import render, redirect
# from .utils import SmartTrainerProfile
# from .models import Translation, UserProfile

# def create_profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             trainer = SmartTrainerProfile(user_profile=profile)
#             success, message = trainer.build_profile(form.cleaned_data)
#             if success:
#                 profile.save()
#                 return redirect('display_profile', profile_id=profile.id)
#             else:
#                 form.add_error(None, message)
#     else:
#         form = UserProfileForm()
    
#     translations = {t.key: t.value for t in Translation.objects.filter(language='en')}
#     return render(request, 'app/create_profile.html', {'form': form, 'translations': translations})

# def display_profile(request, profile_id):
#     profile = UserProfile.objects.get(id=profile_id)
#     translations = {t.key: t.value for t in Translation.objects.filter(language=profile.language)}
#     return render(request, 'app/display_profile.html', {
#         'profile': profile,
#         'translations': translations,
#         'days_of_week': ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] if profile.language == 'en' else ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"]
#     })

# from django.urls import path
# from . import views

# app_name = 'app'

# urlpatterns = [
#     path('create/', views.create_profile, name='create_profile'),
#     path('profile/<int:profile_id>/', views.display_profile, name='display_profile'),
# ]

# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('trainer/', include('app.urls')),
# ]

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'app',
# ]

# from django.core.management.base import BaseCommand
# from app.models import Translation, ExerciseTarget

# class Command(BaseCommand):
#     help = 'Load translations and exercise targets into the database'

#     def handle(self, *args, **kwargs):
#         translations = {
#             "en": {
#                 "select_language": "Select language:",
#                 "your_name": "Your name:",
#                 "your_gender": "Your gender:",
#                 "your_height": "Your height (cm):",
#                 "your_weight": "Your weight (kg):",
#                 "level": "What’s your level: (beginner, intermediate, advance)?",
#                 "posture_issues": "Do you have posture issues?",
#                 "invalid_choice": "Invalid choice. Try again.",
#                 "invalid_input": "Invalid input. Try again.",
#                 "non_negative": "Value must be non-negative. Try again.",
#                 "profile_saved": "Profile and workout programs saved to {}",
#                 "user_profile": "User Profile and Workout Programs",
#                 "week_separator": "=== Week {} ===",
#                 "day_separator": "--- Day: {} ---",
#                 "focus": "Focus",
#                 "warm_up": "Warm-Up",
#                 "main_workout": "Main Workout",
#                 "cool_down": "Cool-Down",
#                 "rest": "Rest",
#                 "week_1": "Week 1",
#                 "week_2": "Week 2",
#                 "week_3": "Week 3",
#                 "week_4": "Week 4"
#             },
#             "fa": {
#                 "select_language": "زبان را انتخاب کنید:",
#                 "your_name": "نام شما:",
#                 "your_gender": "جنسیت شما:",
#                 "your_height": "قد شما (سانتی‌متر):",
#                 "your_weight": "وزن شما (کیلوگرم):",
#                 "level": "سطح خود را بگویید؟ (مبتدی، متوسط، حرفه‌ای)",
#                 "posture_issues": "آیا مشکل بدنی دارید؟",
#                 "invalid_choice": "انتخاب نامعتبر. دوباره امتحان کنید.",
#                 "invalid_input": "ورودی نامعتبر. دوباره امتحان کنید.",
#                 "non_negative": "مقدار باید غیرمنفی باشد. دوباره امتحان کنید.",
#                 "profile_saved": "پروفایل و برنامه‌های تمرینی در {} ذخیره شد",
#                 "user_profile": "پروفایل کاربر و برنامه‌های تمرینی",
#                 "week_separator": "=== هفته {} ===",
#                 "day_separator": "--- روز: {} ---",
#                 "focus": "تمرکز",
#                 "warm_up": "گرم‌کردن",
#                 "main_workout": "تمرین اصلی",
#                 "cool_down": "سرد کردن",
#                 "rest": "استراحت",
#                 "week_1": "هفته ۱",
#                 "week_2": "هفته ۲",
#                 "week_3": "هفته ۳",
#                 "week_4": "هفته ۴"
#             }
#         }

#         exercise_targets = {
#             "en": {
#                 "Arm Circles": "Shoulders",
#                 "Hip Circles": "Hips",
#                 # ... (Add all exercise targets from your original code)
#             },
#             "fa": {
#                 "Arm Circles": "شانه‌ها",
#                 "Hip Circles": "لگن",
#                 # ... (Add all exercise targets from your original code)
#             }
#         }

#         Translation.objects.all().delete()
#         ExerciseTarget.objects.all().delete()

#         for lang, trans_dict in translations.items():
#             for key, value in trans_dict.items():
#                 Translation.objects.create(language=lang, key=key, value=value)

#         for lang, target_dict in exercise_targets.items():
#             for exercise_name, target in target_dict.items():
#                 ExerciseTarget.objects.create(language=lang, exercise_name=exercise_name, target=target)

#         self.stdout.write(self.style.SUCCESS('Successfully loaded translations and exercise targets'))





# from django.db import models

# class UserProfile(models.Model):
#     name = models.CharField(max_length=100)
#     age = models.IntegerField()
#     height = models.FloatField()
#     weight = models.FloatField()

#     def __str__(self):
#         return self.name

# # app/forms.py

# from django import forms
# from .models import UserProfile

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = '__all__'  # یا لیست دقیق‌تری بذار مثل ['name', 'gender', 'height', 'weight', 'goal']

# from django.shortcuts import render, redirect
# from . forms import UserProfileForm

# def create_profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('profile_success')
#     else:
#         form = UserProfileForm()
#     return render(request, 'profile_form.html', {'form': form})

# def profile_success(request):
#     return render(request, 'success.html')


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.create_profile, name='create_profile'),
#     path('success/', views.profile_success, name='profile_success'),
# ]

# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('app.urls')),
# ]

from django.db import models


class PostureIssue(models.Model):
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=2, choices=[('en', 'English'), ('fa', 'Persian')], default='en')

    def __str__(self):
        return f"{self.language} - {self.name}"

    class Meta:
        unique_together = ('name', 'language')


class UserProfile(models.Model):
    language = models.CharField(max_length=2, choices=[('en', 'English'), ('fa', 'Persian')], default='en')
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    height_cm = models.FloatField()
    weight_kg = models.FloatField()
    bmi = models.FloatField(blank=True, null=True)
    level = models.CharField(max_length=20, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')])
    posture_issues = models.ManyToManyField(PostureIssue, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.height_cm and self.weight_kg:
            self.bmi = self.weight_kg / ((self.height_cm / 100) ** 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class WorkoutProgram(models.Model):
    PROGRAM_TYPES = [
        ('Strength', 'Strength'),
        ('Cardio', 'Cardio'),
        ('Flexibility', 'Flexibility'),
        ('Hybrid', 'Hybrid'),
    ]
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='workout_programs')
    week_number = models.IntegerField()
    description = models.TextField()
    frequency = models.CharField(max_length=100)
    intensity = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=PROGRAM_TYPES)

    def __str__(self):
        return f"Week {self.week_number} for {self.user_profile.name}"


class WorkoutDay(models.Model):
    DAYS_OF_WEEK = [
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]
    program = models.ForeignKey(WorkoutProgram, on_delete=models.CASCADE, related_name='days')
    day = models.CharField(max_length=20, choices=DAYS_OF_WEEK)
    focus = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.day} - {self.program}"


class Exercise(models.Model):
    EXERCISE_TYPES = [
        ('warm_up', 'Warm-Up'),
        ('main_workout', 'Main Workout'),
        ('cool_down', 'Cool-Down'),
    ]
    workout_day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE, related_name='exercises')
    exercise_type = models.CharField(max_length=20, choices=EXERCISE_TYPES)
    exercise_name = models.CharField(max_length=100)
    target = models.CharField(max_length=100)
    sets = models.IntegerField(blank=True, null=True)
    reps = models.CharField(max_length=50, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    rir = models.IntegerField(blank=True, null=True)
    alternative = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.exercise_name} ({self.exercise_type})"


class Translation(models.Model):
    language = models.CharField(max_length=2, choices=[('en', 'English'), ('fa', 'Persian')])
    key = models.CharField(max_length=100)
    value = models.TextField()

    def __str__(self):
        return f"{self.language} - {self.key}"

    class Meta:
        unique_together = ('language', 'key')


class ExerciseTarget(models.Model):
    language = models.CharField(max_length=2, choices=[('en', 'English'), ('fa', 'Persian')])
    exercise_name = models.CharField(max_length=100)
    target = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.language} - {self.exercise_name}"

    class Meta:
        unique_together = ('language', 'exercise_name')