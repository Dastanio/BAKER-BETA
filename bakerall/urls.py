from django.urls import path
from . import views


urlpatterns = [
    path('food/', views.FoodListView.as_view()),
    path('food/<int:pk>/', views.FoodDetailView.as_view()),
    path('food_detail/<int:id_food>/', views.FoodDetailViewHtml.food_detail, name='food_detail'),
    path('food_detail/<int:id_food>/leave_comment', views.leave_comment, name = 'leave_comment'),
    path('add-rating/', views.AddStarRating.as_view(), name="add_rating"),
    path('comment/', views.CommentCreateView.as_view()),
    path('rating/', views.AddStarRatingView.as_view()),
    path('email/', views.email, name="email"),
    path('menu/',  views.index, name="index"),
    path('', views.main, name="main"),
    path('about/', views.about, name="about"),
]