from django.http import HttpResponse
from django.contrib.auth import get_user_model

def create_admin(request):
    User = get_user_model()

    username = "opbmsadmin"
    password = "klu@12345"
    email = "opbms@gmail.com"

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        return HttpResponse("✅ Superuser created successfully!<br>Username: admin<br>Password: Admin@123")
    else:
        return HttpResponse("⚠️ Superuser already exists.")
