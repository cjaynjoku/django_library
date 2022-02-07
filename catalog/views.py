import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import RenewBookForm
# Create your views here.
from .models import Book, Author, BookInstance


@login_required
def index(request):
    """View function for our homepage site"""

    # Generate count of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Available books(status='a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The all() is implied by default
    num_authors = Author.objects.count()

    books_with_genre_count = Book.objects.filter(genre__name__icontains='fiction').count()
    books_count = Book.objects.filter(title__icontains='the').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'books_with_genre_count': books_with_genre_count,
        'books_count': books_count,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    login_url = '/login/'
    redirect_field_name = '/' # Replaces the "next"  parameter
    paginate_by = 10

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book


""" The generic class based view above, can also be represented as:
    from django.shortcuts import get_object_or_404

def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})
"""

class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
     model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view, listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinsance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

@login_required
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then the Form data
    if request.method == 'POST':
        # Create a form instance, and populate it with data from the request(binding):
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('index'))

    # Else if this is any other method, create the default form

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance
    }
    return render(request, 'book_renew_librarian.html', context)

"""By default, these views will redirect on success to a page displaying the newly created/edited model item,
 which in our case will be the author detail view"""
class AuthorCreate(LoginRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/20222'}
    template_name_suffix = "_notform"

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__'
    template_name_suffix = "_notform"

class AuthorDelete(DeleteView):
    model= Author
    # reverse lazy is used here because we are providing a url to a class based view attribute
    success_url = reverse_lazy('authors')


class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre']
    initial = {'summary': 'Fiction'}

class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre']

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

