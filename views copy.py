from django.http import HttpResponse

def home(request):
    return HttpResponse("سلام الناز جون! جنگو داره کار می‌کنه 😍")
