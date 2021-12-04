from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .filters import PostFilter, DateFilter, AuthorFilter
from .models import Post, Category, Author
from datetime import datetime
from .forms import NewsForm


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 2
    form_class = NewsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())

        context['categories'] = Category.objects.all()
        context['form'] = NewsForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()
        return super().get(request, *args, **kwargs)


class NewsDetail(DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'detail_news.html'
    context_object_name = 'news'


class SearchList(ListView):
    model = Post
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = DateFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['author_filter'] = AuthorFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class NewsCreate(CreateView):
    template_name = 'news_create.html'
    form_class = NewsForm


class NewsUpdate(UpdateView):
    template_name = 'news_create.html'
    form_class = NewsForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDelete(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'









