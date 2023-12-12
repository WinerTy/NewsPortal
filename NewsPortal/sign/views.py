from django.shortcuts import render

# Create your views here.
class Test():
    def test(request):
        return render(request, 'BD/register.html')