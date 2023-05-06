from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, PageChooserPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index


class HomePage(Page):
    """
    home page model
    """
    template = "home/home_page.html"

    banner_title = models.CharField(max_length=100, blank=False, null=True)

    banner_subtitle = RichTextField(features=["bold", "italic"])

    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    base_text = RichTextField(default="主页内容")

    baseimg = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    chatboximage = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        blank=False
    )

    texttoimg = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        blank=False
    )

    imgtoimg = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True
    )

    banner_ctl = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    content_panels = Page.content_panels + [
        FieldPanel('banner_title'),
        FieldPanel('banner_subtitle'),
        FieldPanel("base_text"),
        FieldPanel("baseimg"),
        FieldPanel("banner_image"),
        FieldPanel("chatboximage"),
        FieldPanel("texttoimg"),
        FieldPanel("imgtoimg"),
        PageChooserPanel("banner_ctl")
    ]

    class Meta:
        verbose_name = "Oh New Page"
        verbose_name_plural = "HomePages"


class AboutPage(Page):
    # 关于我们页面有一个标题字段和一个内容字段
    content = RichTextField()

    # contact info
    aboutcontact = RichTextField(
        default="联系方式: 15313621879\n邮箱: chenzuoli709@163.com")

    # about image
    aboutimg = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True
    )

    # 指定后台管理界面中可以编辑的字段
    content_panels = Page.content_panels + [
        FieldPanel('content'),
        FieldPanel('aboutcontact'),
        FieldPanel('aboutimg')
    ]


class ContactPage(Page):
    # 联系我们页面有一个标题字段和一个图片字段
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
        blank=True,
    )

    # 指定后台管理界面中可以编辑的字段
    content_panels = Page.content_panels + [
        FieldPanel('image')
    ]


class BlankPage(Page):
    # 关于我们页面有一个标题字段和一个内容字段
    content = RichTextField()

    # 指定后台管理界面中可以编辑的字段
    content_panels = Page.content_panels + [
        FieldPanel('content')
    ]


class BlogPage(Page):

    # Database fields

    body = RichTextField()
    date = models.DateField("Post date")
    videourl = models.CharField(max_length=500, blank=True, null=True)

    blogimg = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # Search index configuration

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date'),
    ]

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body'),
        FieldPanel('videourl'),
        FieldPanel('blogimg'),
        InlinePanel('related_links', heading="Related links",
                    label="Related link"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel('feed_image'),
    ]

    # Parent page / subpage type rules

    # parent_page_types = ['blog.BlogIndex']
    # subpage_types = []


class BlogPageRelatedLink(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE,
                       related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]


class ChatGPTPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    subpage_types = []

    parent_page_types = ['home.HomePage']


# chatbotOnlinePage model for chatbot_online_page.html
class ChatbotOnlinePage(Page):
    template = "home/chatbot_online_page.html"

    chatbot_online_title = models.CharField(
        max_length=100, blank=False, null=True)

    chatbot_online_subtitle = RichTextField(features=["bold", "italic"])

    chatbot_online_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    chatbot_online_ctl = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    content_panels = Page.content_panels + [
        FieldPanel('chatbot_online_title'),
        FieldPanel('chatbot_online_subtitle'),
        FieldPanel("chatbot_online_image"),
        PageChooserPanel("chatbot_online_ctl")
    ]

    class Meta:
        verbose_name = "Chatbot Online Page"
        verbose_name_plural = "ChatbotOnlinePages"


# chatimgOnlinePage model for chatimg_online_page.html
class ChatimgOnlinePage(Page):
    template = "home/chatimg_online_page.html"

    chatimg_online_title = models.CharField(
        max_length=100, blank=False, null=True)

    chatimg_online_subtitle = RichTextField(features=["bold", "italic"])

    chatimg_online_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    chatimg_online_ctl = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    content_panels = Page.content_panels + [
        FieldPanel('chatimg_online_title'),
        FieldPanel('chatimg_online_subtitle'),
        FieldPanel("chatimg_online_image"),
        PageChooserPanel("chatimg_online_ctl")
    ]

    class Meta:
        verbose_name = "Chatimg Online Page"
        verbose_name_plural = "ChatimgOnlinePages"


class OpenaiChatbotPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    subpage_types = []

    parent_page_types = ['home.HomePage']


class ListPage(Page):
    """
    List page
    按照3列方式排列
    """
    my_list = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('my_list'),
    ]
