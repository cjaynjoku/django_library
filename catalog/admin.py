from django.contrib import admin

from .models import Book, Author, Genre, BookInstance, Language

# Register your models here.
#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(Book Instance)
admin.site.register(Language)


class BookInline(admin.StackedInline):
    model = Book
    extra = 0

@admin.register(Author)  # You can add all the models here
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

# Registering the Admin classes for Book, using a decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


# Registering the admin classes for BookInstance using a decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrower', 'status', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability',{
            'classes':('collapse',),
            'fields': ('status', 'due_back', 'borrower')
        }),

    )

