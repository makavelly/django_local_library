from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

#from .forms import RenewBookForm
from .forms import RenewBookModelForm

from django.contrib.auth.decorators import permission_required

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

class AuthorDetailView(generic.DetailView):
	model = Author
	
	
class AuthorListView(generic.ListView):
	model = Author
	paginate_by = 10

class BookDetailView(generic.DetailView):
	model = Book

class BookListView(generic.ListView):
	model = Book
	#contex_object_name = 'my_book_list' # your own name for the list as a template variable
	#queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
	#template_name = 'catalog/books/my_arbitrary_template_name_list.html'  # Specify your own template name/location

	#def get_queryset(self):
	#	return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
	
def index(request):
	"""
	View function for home page of site.
	"""
	# Generate counts of some of the main objects
	num_books = Book.objects.all().count()
	num_books_contain_AND = Book.objects.filter(title__icontains='and').count()
	num_instances = BookInstance.objects.all().count()
	# Available books (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()
	num_authors = Author.objects.count() # The 'all()' is implied by default.
	num_genres = Genre.objects.count()
	
	# Get number of client's visits and set it to 0 if 'num_visits' key doesn't exist
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1
	
	# Render the HTML template index.html with the data in the context variable
	context = {
		'num_books': num_books,
		'num_instances': num_instances, 
		'num_instances_available': num_instances_available, 
		'num_authors': num_authors,
		'num_genres': num_genres,
		'num_books_contain_AND': num_books_contain_AND,
		'num_visits': num_visits,
	}
	return render(request, 'catalog/index.html', context)
	
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	"""
	Generic class-based view listing books on loan to current user. 
	"""
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 10
	
	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
	
	
class AllLoanedBooksListView(PermissionRequiredMixin, generic.ListView):
	"""
	Generic class-based view listing all books on loan to all users. 
	"""
	permission_required = 'catalog.can_mark_returned'
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_all.html'
	paginate_by = 10
	
	def get_queryset(self):
		return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
	book_inst = get_object_or_404(BookInstance, pk=pk)
	
	# If this is a POST request then process the Form data
	if request.method == 'POST':
		# Create a form instance and populate it with data from the request (binding):
		form = RenewBookModelForm(request.POST)
		# Check if the form is valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required 
			# (here we just write it to the model due_back field)
			book_inst.due_back = form.cleaned_data['due_back']
			book_inst.save()
			# redirect to a new URL:
			return HttpResponseRedirect(reverse('all-borrowed') )
	# If this is a GET (or any other method) create the default form.
	else:
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
		form = RenewBookModelForm(initial={'due_back': proposed_renewal_date,})
		
	return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

@permission_required('catalog.can_mark_returned')
def renew_book_librarian_manual(request, pk):
	book_inst = get_object_or_404(BookInstance, pk=pk)
	
	# If this is a POST request then process the Form data
	if request.method == 'POST':
		# Create a form instance and populate it with data from the request (binding):
		form = RenewBookForm(request.POST)
		# Check if the form is valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required 
			# (here we just write it to the model due_back field)
			book_inst.due_back = form.cleaned_data['renewal_date']
			book_inst.save()
			# redirect to a new URL:
			return HttpResponseRedirect(reverse('all-borrowed') )
	# If this is a GET (or any other method) create the default form.
	else:
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
		form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})
		
	return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

class AuthorCreate(CreateView):
	model = Author
	fields = '__all__'
	initial={'date_of_death': '05/01/2018'}
	
class AuthorUpdate(UpdateView):
	model = Author
	fields = ['first_name','last_name','date_of_birth','date_of_death']
	
class AuthorDelete(DeleteView):
	model = Author
	success_url = reverse_lazy('authors')
	
class BookCreate(CreateView):
	model = Book
	fields = '__all__'
	
class BookUpdate(UpdateView):
	model = Book
	fields = '__all__'
	
class BookDelete(DeleteView):
	model = Book
	success_url = reverse_lazy('books')