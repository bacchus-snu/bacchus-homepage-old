# -*- encoding: utf-8 -*-

# django
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext

# project
from homepage.models import *
from homepage.forms import *
import homepage.const
import homepage.boards

import base64
import ldap
from ad import login

def home(request):
    user_id = request.session.get('user_id')
    if is_bacchus(user_id):
        return HttpResponseRedirect('/board/home/')
    board = Board.objects.get(name='home')
    articles = homepage.boards.get_latest_article(board)
    if len(articles) > 0:
        article = articles[0]
        username = request.session.get('username')
        variables = RequestContext(request, {'article': article, 'username': username})
        return render_to_response('home.html', variables)
    else:
        username = request.session.get('username')
        variables = RequestContext(request, {'username': username})
        return render_to_response('home.html', variables)

def home_pagination_view(request, page_number):
    user_id = request.session.get('user_id')
    if is_bacchus(user_id):
        return HttpResponseRedirect('/board/home/%s/' % page_number)
    return HttpResponseRedirect('/home/')

def notice_view(request):
    return HttpResponseRedirect('/board/notice/')

def notice_pagination_view(request, page_number):
    return HttpResponseRedirect('/board/notice/%s/' % page_number)

def about(request):
    username = request.session.get('username')
    return render_to_response('about.html', RequestContext(request, {'username':username}))

# services
def service_term(request):
    username = request.session.get('username')
    return render_to_response('services_terms.html', RequestContext(request, {'username':username}))

def service_account(request):
    username = request.session.get('username')
    return render_to_response('services_account.html', RequestContext(request, {'username':username}))

def service_server(request):
    username = request.session.get('username')
    return render_to_response('services_server.html', RequestContext(request, {'username':username}))

def service_lab(request):
    username = request.session.get('username')
    return render_to_response('services_lab.html', RequestContext(request, {'username':username}))

def service_printer(request):
    username = request.session.get('username')
    return render_to_response('services_printer.html', RequestContext(request, {'username':username}))

def service_community(request):
    username = request.session.get('username')
    return render_to_response('services_community.html', RequestContext(request, {'username':username}))

# faq
def faq_view(request):
    return HttpResponseRedirect('/board/faq/')

def faq_pagination_view(request, page_number):
    return HttpResponseRedirect('/board/faq/%s/' % page_number)

# qna_server
def qna_server_view(request):
    return HttpResponseRedirect('/board/qna_server/')

def qna_server_pagination_view(request, page_number):
    return HttpResponseRedirect('/board/qna_server/%s/' % page_number)

# qna_printer 
def qna_printer_view(request):
    return HttpResponseRedirect('/board/qna_printer/')

def qna_printer_pagination_view(request, page_number):
    return HttpResponseRedirect('/board/qna_printer/%s/' % page_number)

# qna_lab
def qna_lab_view(request):
    return HttpResponseRedirect('/board/qna_lab/')

def qna_lab_pagination_view(request, page_number):
    return HttpResponseRedirect('/board/qna_lab/%s/' % page_number)

# qna_account
def qna_account_view(request):
    return HttpResponseRedirect('/board/qna_account/')

def qna_account_pagination_view(request, page_number):
    return HttpResponseRedirect('/board/qna_account/%s/' % page_number)

def login_view(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id")
        password = request.POST.get("password")
        username = login(user_id, password)
        if username != False:
            request.session['user_id'] = user_id
            request.session['username'] = username
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def logout_view(request):
    del request.session['user_id']
    del request.session['username']
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# board 
def board_write(request, board_name):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    # 로그인 안했으면 글쓰지 못하게
    if user_id == False:
        return HttpResponseRedirect('/board/' + board_name + '/')
    # 특정 게시판은 바쿠스만 글쓰게
    if board_name == 'home' or board_name == 'notice' or board_name == 'faq':
        if is_bacchus(user_id) == False:
            return HttpResponseRedirect('/board/' + board_name + '/')
    board = None
    try:
        board = Board.objects.get(name=board_name)
    except:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = ArticleWriteForm(request.POST, label_suffix='')
        if form.is_valid():
            secret = False
            if 'is_secret' in form.cleaned_data: 
                secret = True

            article = Article.objects.create(
                    board = board,
                    title = form.cleaned_data['title'],
                    content = form.cleaned_data['content'],
                    is_secret = secret,
                    name = form.cleaned_data['name'],
                    email = form.cleaned_data['email'],
                    homepage = form.cleaned_data['homepage'])
            article.set_password(form.cleaned_data['password'])
            article.save()
            return board_list(request, board.name, 0)
    else:
        form = ArticleWriteForm(label_suffix='')

    variables = RequestContext(request, {'form': form, 'board': board, 'username': username})
    return render_to_response('board_write.html', variables)

def board_list(request, board_name, page_number=1):
    page_number = int(page_number)
    page_number -= 1

    board = Board.objects.get(name=board_name)
    articles = homepage.boards.get_latest_article(board, page_number)

    page_count = max(int(
        (board.article_count + homepage.const.ARTICLE_PER_PAGE_DEFAULT - 1) 
        / homepage.const.ARTICLE_PER_PAGE_DEFAULT
        ), 1)

    user_id = request.session.get('user_id')
    username = request.session.get('username')
    variables = RequestContext(request, {
        'board': board,
        'articles': articles, 
        'page_count_for_loop': xrange(1, page_count + 1), 
        'page_number': homepage.boards.get_range_pagination(page_count, page_number),
        'username': username,
        'is_bacchus': is_bacchus(user_id)
        })
    return render_to_response('board_list.html', variables)

def article_show(request, article_id):
    article = Article.objects.get(id=article_id)
    board = article.board

    article.read_count += 1
    article.save()

    if request.method == 'POST':
        form = CommentWriteForm(request.POST, label_suffix='')
        if form.is_valid():
            comment = Comment.objects.create(
                    article = article,
                    content = form.cleaned_data['content'],
                    name = form.cleaned_data['name'],
                    email = form.cleaned_data['email'])
            comment.set_password(form.cleaned_data['password'])
            comment.save()

            article.comment_count += 1
            article.save()
            return HttpResponseRedirect('/board/show/%s/' % article_id)
    else:
        form = CommentWriteForm(label_suffix='')

    comments = Comment.objects.filter(article = article)
    username = request.session.get('username')

    variables = RequestContext(request, {
        'board': board,
        'article': article,
        'comments': comments,
        'form': form,
        'username': username
        })

    return render_to_response('article_show.html', variables)

def article_remove(request, article_id):
    article = Article.objects.get(id=article_id)
    board = article.board

    if request.method == 'POST':
        form = ArticleRemoveForm(request.POST, label_suffix='')
        if form.is_valid():
            if article.check_password(form.cleaned_data['password']):
                article.delete()
                return HttpResponseRedirect('/board/%s/' % board.name)
    else:
        form = ArticleRemoveForm(label_suffix='')

    username = request.session.get('username')
    variables = RequestContext(request, {
        'board': board,
        'article': article,
        'form': form,
        'username': username
        })

    return render_to_response('article_remove.html', variables)

def is_bacchus(user_id):
    return user_id == "jsryu21"
