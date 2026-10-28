from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import ProtectedError
from django.views.decorators.http import require_POST
from . import forms, models

# Create your views here.
def categorias_lista_view(request):
    categorias = models.Categoria.objects.all()

    print("List Method:", request.method)

    return render(request, "categoria/lista.html", {
        "categorias": categorias
    })

def categoria_detalhe_view(request, categoria_id):
    categoria = models.Categoria.objects.get(id=categoria_id)

    print("Detail Method:", request.method)

    return render(request, "categoria/detalhe.html", {
        "categoria": categoria,
    })

def cadastrar_categoria(request):
    if request.method == "POST":
        form = forms.CategoriaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request, "Categoria cadastrada com sucesso!"
            )
            return redirect("noticias:categorias")
    else:
        form = forms.CategoriaForm()

    return render(request, "categoria/form.html", {
        "form": form,
    })


def atualizar_categoria(request, categoria_id):
    categoria = get_object_or_404(models.Categoria, id=categoria_id)

    if request.method == "POST":
        form = forms.CategoriaForm(request.POST, instance=categoria)

        if form.is_valid():
            form.save()
            messages.success(
                request, "Categoria atualizada com sucesso!"
            )
            return redirect("noticias:categorias")
    else:
        form = forms.CategoriaForm(instance=categoria)

    return render(request, "categoria/form.html", {
        "form": form,
        "categoria": categoria,
    })


def excluir_categoria(request, categoria_id):
    categoria = get_object_or_404(models.Categoria, id=categoria_id)

    if request.method == "POST":
        try:
            categoria.delete()
            messages.success(
                request, "Categoria excluída com sucesso!"
            )
        except ProtectedError:
            messages.error(
                request,
                "Não é possível excluir esta categoria, "
                "pois existem notícias vinculadas a ela."
            )

        return redirect("noticias:categorias")

    return render(request, "categoria/confirmar_exclusao.html", {
        "categoria": categoria,
    })

def tags_lista_view(request):
    tags = models.Tag.objects.all()

    return render(request, "tag/lista.html", {
        "tags": tags
    })

def tag_detalhe_view(request, tag_id):
    tag = models.Tag.objects.get(id=tag_id)

    return render(request, "tag/detalhe.html", {
        "tag": tag,
    })

def tag_create_view(request):
    if request.method == "POST":
        form = forms.TagForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request, "Tag cadastrada com sucesso!"
            )
            return redirect("noticias:tags")
    else:
        form = forms.TagForm()

    return render(request, "tag/form.html", {
        "form": form,
    })


def atualizar_tag(request, tag_id):
    tag = get_object_or_404(models.Tag, id=tag_id)

    if request.method == "POST":
        form = forms.TagForm(request.POST, instance=tag)

        if form.is_valid():
            form.save()
            messages.success(
                request, "Tag atualizada com sucesso!"
            )
            return redirect("noticias:tags")
    else:
        form = forms.TagForm(instance=tag)

    return render(request, "tag/form.html", {
        "form": form,
        "tag": tag,
    })


def excluir_tag(request, tag_id):
    tag = get_object_or_404(models.Tag, id=tag_id)

    if request.method == "POST":
        tag.delete()
        messages.success(
            request, "Tag excluída com sucesso!"
        )
        return redirect("noticias:tags")

    return render(request, "tag/confirmar_exclusao.html", {
        "tag": tag,
    })

def noticia_create_view(request):
    if request.method == "POST":
        form = forms.NoticiaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("noticias:noticias")
    else:
        form = forms.NoticiaForm()

    return render(request, "noticia/form.html", {
        "form": form,
    })

def noticia_update_view(request, noticia_id):
    noticia = models.Noticia.objects.get(id=noticia_id)

    if request.method == "POST":
        form = forms.NoticiaForm(request.POST)
        if form.is_valid():
            noticia.titulo = form.cleaned_data["titulo"]
            noticia.texto = form.cleaned_data["texto"]
            noticia.categoria = form.cleaned_data["categoria"]
            noticia.tags.set(form.cleaned_data["tags"])
            noticia.save()
            return redirect("noticias:noticias")
    else:
        form = forms.NoticiaForm(initial={
            "titulo": noticia.titulo,
            "texto": noticia.texto,
            "categoria": noticia.categoria,
            "tags": noticia.tags.all(),
        })

    return render(request, "noticia/form.html", {
        "form": form,
        "noticia": noticia,
    })

def noticia_delete_view(request, noticia_id):
    noticia = models.Noticia.objects.get(id=noticia_id)
    noticia.delete()
    return redirect("noticias:noticias")

def noticias_lista_view(request):
    noticias = models.Noticia.objects.all()

    return render(request, "noticia/lista.html", {
        "noticias": noticias
    })

def noticia_detalhe_view(request, noticia_id):
    noticia = models.Noticia.objects.get(id=noticia_id)

    return render(request, "noticia/detalhe.html", {
        "noticia": noticia,
    })

