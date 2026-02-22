from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, Profile
from .forms import BookForm, RegisterForm, ProfileForm


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 8  

    def get_queryset(self):
        qs = Book.objects.all().order_by('-id')
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(title__icontains=search)
        return qs


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_create.html'
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'books/register.html'
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    template_name = 'books/login.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('book_list')


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_update.html'
    success_url = reverse_lazy('book_list')


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'books/book_delete.html'
    success_url = reverse_lazy('book_list')