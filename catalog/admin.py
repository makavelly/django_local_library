from django.contrib import admin

from .models import Genre, Language, Author, Book, BookInstance

#admin.site.register(Genre)
#admin.site.register(Language)
#admin.site.register(Author)
#admin.site.register(Book)
#admin.site.register(BookInstance)

class BookInstanceInline(admin.TabularInline):
#class BookInstanceInline(admin.StackedInline):
	model = BookInstance
	extra = 0

class BookInline(admin.TabularInline):
	model = Book
	extra = 0
	
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
	pass

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
	pass
	
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
	fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
	inlines = [BookInline]
	
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'display_genre')
	inlines = [BookInstanceInline]
	
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
	#list_display = ('__str__', 'status', 'due_back')
	list_display = ('book', 'status', 'due_back', 'borrower', 'id')
	list_filter = ('status', 'due_back')
	fieldsets = (
		(None, {'fields': ('book', 'imprint', 'id')}),
		('Availability', {'fields': ('status', 'due_back', 'borrower')}),
	)
	
#admin.register(Author, AuthorAdmin)