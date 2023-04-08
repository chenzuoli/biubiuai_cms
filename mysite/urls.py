from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

from .views import chenzuoli, chatgpt, qa_gpt, grammar_correction_gpt, summarizer_gpt, natural_lang_to_openai_api_gpt, text_to_command, translator, natural_lang_to_stripe_api_gpt

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("chenzuoli/", chenzuoli, name="chenzuoli"),
    path('chatgpt/', chatgpt, name='chatgpt'),
    path('qa_gpt/', qa_gpt, name='qa_gpt'),
    path('grammar_correction_gpt/', grammar_correction_gpt, name='grammar_correction_gpt'),
    path('summarizer_gpt/', summarizer_gpt, name='summarizer_gpt'),
    path('natural_lang_to_openai_api_gpt/', natural_lang_to_openai_api_gpt, name='natural_lang_to_openai_api_gpt'),
    path('text_to_command/', text_to_command, name='text_to_command'),
    path('translator/', translator, name='translator'),
    path('natural_lang_to_stripe_api_gpt/', natural_lang_to_stripe_api_gpt, name='natural_lang_to_stripe_api_gpt'),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
