from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from accounts.models import CustomUser
@csrf_exempt 
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print(f"Trying: {username} / {password}")

        try:
            # ✅ directly get user from CustomUser model
            user = CustomUser.objects.get(username=username)
            print(f"User found: {user}")

            if user.check_password(password):
                print("Password correct!")
                login(request, user)
                return redirect("admin_dashboard")
            else:
                print("Wrong password!")
                return render(request, "accounts/login.html", {"error": "Invalid credentials"})

        except CustomUser.DoesNotExist:
            print("User not found!")
            return render(request, "accounts/login.html", {"error": "Invalid credentials"})

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def manage_users(request):

    # Only admin can access
    if request.user.role != 'admin':
        return redirect('admin_dashboard')

    users = CustomUser.objects.all()
    return render(request, 'dashboard/manage_users.html', {'users': users})


@login_required
def add_user(request):

    if request.user.role != 'admin':
        return redirect('admin_dashboard')

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        return redirect('manage_users')

    return render(request, 'dashboard/add_user.html')


@login_required
def edit_user(request, id):

    if request.user.role != 'admin':
        return redirect('admin_dashboard')

    user = get_object_or_404(CustomUser, id=id)

    if request.method == "POST":
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.role = request.POST.get('role')
        user.save()
        return redirect('manage_users')

    return render(request, 'dashboard/edit_user.html', {'user': user})


@login_required
def delete_user(request, id):

    if request.user.role != 'admin':
        return redirect('admin_dashboard')

    user = get_object_or_404(CustomUser, id=id)
    user.delete()

    return redirect('manage_users')

    return render(request, 'add_user.html')