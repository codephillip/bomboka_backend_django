from django.shortcuts import render


def successful_reset(request):
    return render(request, 'reset_success.html')
