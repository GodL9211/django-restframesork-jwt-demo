from django.shortcuts import render


# Create your views here.
def webterminal(request):
    if request.method == 'GET':
        return render(request, 'webterminal_input.html')
    else:
        host = request.POST.get('host')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(host)
        print(username)
        return render(request, 'webterminal.html', locals())
