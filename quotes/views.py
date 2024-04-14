from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator

from .forms import AuthorForm, QuoteForm
from .models import Quote, Author


def main(request, page=1):
    quotes = Quote.objects.all().order_by('-created_at')
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


def author_detail(request, author_id):
    author = Author.objects.get(pk=author_id)
    return render(request, 'quotes/author_detail.html', {'author': author})


@login_required
def add_author(request):
    form = AuthorForm(instance=Author())
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES, instance=Author())
        if form.is_valid():
            form.save()
            return redirect(to='quotes:root')
    return render(request, 'quotes/add_author.html',
                  context={'title': 'Add Author', 'page': 'add_author', "form": form})


def authors(request, page=1):
    authors_obj = Author.objects.all().order_by('fullname')
    per_page = 24
    paginator = Paginator(authors_obj, per_page)
    authors_on_page = paginator.page(page)
    return render(request, 'quotes/authors.html',
                  context={'title': 'Autors', 'page': 'autors', 'authors': authors_on_page})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            author = form.cleaned_data['author']
            quote = form.save(commit=False)
            quote.author = author
            quote.save()
            tags = form.cleaned_data['tags']
            quote.tags.set(tags)

            return redirect(to='quotes:root')
    else:
        form = QuoteForm()

    return render(request, 'quotes/add_quote.html', {'form': form})


@login_required
def delete_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    author.delete()
    return redirect('quotes:authors')


@login_required
def edit_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('quotes:author_detail', author_id=author.id)
    else:
        form = AuthorForm(instance=author)
    return render(request, 'quotes/edit_author.html', {'form': form, 'author': author})
