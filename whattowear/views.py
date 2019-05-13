from django.views import View
from django.http import HttpResponse

class PingView(View):

    def get(self, request):
        return HttpResponse(status=200)
