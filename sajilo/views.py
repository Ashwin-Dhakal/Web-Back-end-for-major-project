from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import All_hostel




def index(request):
    return render(request,'sajilo/index.html')



def searchlist(request):
    question1 = str.lower(request.GET.get('q1'))
    question2= str.lower(request.GET.get('q2'))
    if question1 and question2:
        context = {
            "question1": question1,
            "question2": question2,
        }
        len_1 = len(question1)
        len_2 = len(question2)



        return render(request, 'sajilo/searchlist.html', context)



# def searchlist(request):
#     query1= str.lower(request.GET.get('q1'))
#     query2= str.lower(request.GET.get('q2'))
#     if query1 and query2:
#         # queryset_list = All_hostel.objects.filter(Q(gender=query1) &
#                                                 Q(location=query2)).distinct()
#         # context={'queryset_list':queryset_list}
#         return render(request,'sajilo/searchlist.html')
#     else:
#         return render(request, 'sajilo/404.html')




