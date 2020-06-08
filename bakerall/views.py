from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.db import models
from rest_framework import generics
from django.http import Http404, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Food, Rating, Comment
from django.shortcuts import render
from .forms import RatingForm
from django.views.generic import DetailView, View
from django.http import HttpResponse
from .serializers import (
    FoodListSerializer,
    FoodDetailSerializer,
    CommentCreateSerializer,
    CreateRatingSerializer,
)
from .service import get_client_ip
from django.contrib.auth.models import User

class FoodListView(generics.ListAPIView):
    """Вывод списка выпечки"""
    serializer_class = FoodListSerializer


    def get_queryset(self):
        foods = Food.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings",
                                     filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return foods

class FoodDetailView(generics.RetrieveAPIView):
    """Вывод выпечки"""
    queryset = Food.objects.filter(draft=False)
    serializer_class = FoodDetailSerializer



class CommentCreateView(APIView):
    """Добавление отзыва"""
    def post(self, request):
        comment = CommentCreateSerializer(data=request.data)
        if comment.is_valid():
            comment.save()
        return Response(status=201)


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга к выпечке"""
    serializer_class = CreateRatingSerializer
    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


def main(request):
    return render(request, '../templates/main.html')

def about(request):
    return render(request, '../templates/about.html')


def order(request):
    return render(request, '../templates/make_order.html')

class FoodDetailViewHtml(DetailView):
    model = Food
    slug_field = "url"

    def food_detail(request, id_food):
        a = Food.objects.get(id=id_food)
        template = '../templates/food_detail.html'
        latest_comments_list = a.comment_set.order_by('-id')[:10]
        return render(request, template, {'eda':a, 'latest_comments_list': latest_comments_list})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm
        return context

class AddStarRating(View):
    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=get_client_ip(request),
                food_id=int(request.POST.get("food")),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


def leave_comment(request, id_food):
    try:
        a = Food.objects.get(id=id_food)
    except:
        raise Http404('Статья не найдена!')

    a.comment_set.create(comment_text=request.POST['text'], author=request.POST['author'])


    return HttpResponseRedirect(reverse('food_detail', args=(a.id,)))

def index(request):
    foods = Food.objects.all()
    paginator = Paginator(foods, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj
    }
    template = "../templates/index.html"
    return render(request, template, context)


def email(request):

    if request.method == 'POST':
        message = request.POST['message']
        gmail = request.POST['gmail']
        send_mail('gmail почта клиента:  ' + gmail,
         'Текст сообщения от клиента:  ' + message,
         settings.EMAIL_HOST_USER,
         ['lev201611@gmail.com'], # <--- вот сдесь ты едешь 2 аккаунт
         fail_silently=False)


        messages.success(request, ('Ваш заказ успешно принят, доставщик свами свяжется'))
        return redirect('email')

    return render(request, '../templates/make_order.html')
