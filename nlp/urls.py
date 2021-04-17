from django.conf.urls import url
from nlp import views
from django.urls import path

# got to set "app_name" to something
# before you can use relative paths in your templates
app_name = 'nlp'
urlpatterns = [
    path("",
         views.index,
         name="index"),
    path("register",
         views.register_user,
         name="register"),
    path("comingsoon",
         views.coming_soon,
         name="comingsoon"),
    path("extract_keyphrases_from_text",
         views.extract_key_phrases_from_text,
         name="extract_keyphrases_from_text"),
    path("extract_summary_from_text",
         views.extract_summary_from_text,
         name="extract_summary_from_text")
]