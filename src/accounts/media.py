from django.shortcuts import render, redirect


def allmedia(request):
    if request.user.is_authenticated and request.user.admin:
        return render(request, 'settings/admin/AllMedia/allmedia.html')
    return redirect('accounts:dashboard')
