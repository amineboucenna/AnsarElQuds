from django.urls import path,include
import App.views as views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path(route='sign-in/',view=views.Login,name="sign-in"),
    path(route='sign-up/',view=views.Register,name="sign-up"),
    path(route='sign-out/',view=views.Logout,name="sign-out"),
    path(route='',view=views.Profile,name="profile"),
    path(route='settings/',view=views.Settings,name="settings"),
    path(route='news/',view=views.NewsPage,name="news"),
    path('news/upvote/<int:article_id>/', views.upvote_news, name='upvote-news'),
    path('news/downvote/<int:article_id>/', views.downvote_news, name='downvote-news'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
