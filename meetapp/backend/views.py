from django.shortcuts import render

def main(request):
    return render(request, 'layout/basic.html')
