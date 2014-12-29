# -*- encoding: utf-8 -*-

# django
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core.mail import send_mail

# project
from homepage.models import *
from homepage.forms import *
import homepage.const
import homepage.boards

from oauth import Oauth

def home(request):
    if request.method == 'GET':
        oauth_verifier = request.GET.get('oauth_verifier')
        if oauth_verifier is not None:
            Oauth.Instance().get_access_token(oauth_verifier)
    print(Oauth.Instance().get_bs_class_year())
    username, user_id, bs_year = Oauth.Instance().get_bs_class_year()
    if is_bacchus(user_id):
        return HttpResponseRedirect('/board/home/')
    board = Board.objects.get(name='home')
    articles = homepage.boards.get_latest_article(board)
    if len(articles) > 0:
        article = articles[0]
        variables = RequestContext(request, {'article': article, 'username': username})
        return render_to_response('home.html', variables)
    else:
        variables = RequestContext(request, {'username': username})
        return render_to_response('home.html', variables)

def home_pagination_view(request, page_number):
    username, user_id, bs_year = Oauth.Instance().get_bs_class_year()
    if is_bacchus(user_id):
        return HttpResponseRedirect('/board/home/%s/' % page_number)
    return HttpResponseRedirect('/home/')

def notice_view(request):
    return HttpResponseRedirect('/board/notice/')

def notice_pagination_view(request, page_number):
    return HttpResponseRedirect('/board/notice/%s/' % page_number)

def about(request):
    username, user_id, bs_year = Oauth.Instance().get_bs_class_year()
    return render_to_response('about.html', RequestContext(request, {'username':username}))

# services
def service_term(request):
    username, user_id, bs_year = Oauth.Instance().get_bs_class_year()
    return render_to_response('services_terms.html', RequestContext(request, {'username':username}))

def service_account(request):
    username, user_id, bs_year = Oauth.Instance().get_bs_class_year()
    return render_to_response('services_account.html', RequestContext(request, {'username':username}))

def service_server(request):
    username, user_id, bs_year = Oauth.Instance().get_bs_class_year()
    return render_to_response('services_server.html', RequestContext(request, {'username':username}))

def service_lab(request):
    username, user_id, bs_year = Oauth.Instance().get_bs_class_year()
    return render_to_response('services_lab.html', RequestContext(request, {'username':username}))

def service_printer(request):
    username, user_id, bs_year = Oauth.Instance().get_bs_class_year()
    return render_to_response('services_printer.html', RequestContext(request, {'username':username}))

def service_community(request):
    username, user_id, bs_year = Oauth.Instance().get_bs_class_year()
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
    authorize_url = Oauth.Instance().get_request_token()
    return HttpResponseRedirect(authorize_url)

def logout_view(request):
    Oauth.Instance().request_token = None
    Oauth.Instance().access_token = None
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# board 
def board_write(request, board_name):
    username, user_id, bs_year = Oauth.Instance().get_bs_class_year()
    # 특정 게시판은 바쿠스만 글쓰게
    if board_name == 'home' or board_name == 'notice' or board_name == 'faq':
        if is_bacchus(user_id) == False:
            return HttpResponseRedirect('/board/' + board_name + '/')
    board = None
    try:
        board = Board.objects.get(name=board_name)
    except:
        return HttpResponseRedirect('/')
    # 로그인 안했으면 글쓰지 못하게
    # 로그인 안했어도 Q&A_ACCOUNT는 글쓸 수 있게
    if username is None and board_name != 'qna_account':
        return HttpResponseRedirect('/board/' + board_name + '/')
    if request.method == 'POST':
        if username is None and board_name == 'qna_account':
            form = AccountArticleWriteForm(request.POST, label_suffix='')
        else:
            form = ArticleWriteForm(request.POST, label_suffix='')
        if form.is_valid():
            if username is None and board_name == 'qna_account':
                article = Article.objects.create(
                        board = board,
                        username = form.cleaned_data['name'],
                        bs_year = form.cleaned_data['year'],
                        title = form.cleaned_data['title'],
                        content = form.cleaned_data['content'],
                        email = form.cleaned_data['email'],
                        homepage = form.cleaned_data['homepage'])
                article.set_password(form.cleaned_data['password'])
            else:
                article = Article.objects.create(
                        board = board,
                        user_id = user_id,
                        username = username,
                        bs_year = bs_year,
                        title = form.cleaned_data['title'],
                        content = form.cleaned_data['content'],
                        is_secret = 'is_secret' in form.cleaned_data,
                        email = form.cleaned_data['email'],
                        homepage = form.cleaned_data['homepage'])
            article.save()
            subject = u"[{0}] {1}".format(article.board.name, article.title[0:15])
            content = u"Content : {0}".format(article.content)
            user = u"User :\n\tuser_id : {0}\n\tusername : {1}\n\tbs_year : {2}\n\temail : {3}\n\thomepage : {4}".format(article.user_id, article.username, article.bs_year, article.email, article.homepage)
            article_url = "{0}/show/{1}".format("/".join(request.build_absolute_uri().split('/')[:-3]), str(article.id))
            link = u"Link : {0}".format(article_url)
            message = u"{0}\n\n{1}\n\n{2}".format(content, user, link)
            send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.DEFAULT_FROM_EMAIL], fail_silently = False)
            # 글을 쓰고 보내기 때문에 board_list의 마지막 parameter를 1로 보냄.
            return board_list(request, board.name, 1)
    else:
        if username is None and board_name == 'qna_account':
            form = AccountArticleWriteForm(label_suffix='')
        else:
            form = ArticleWriteForm(label_suffix='')

    variables = RequestContext(request, {'form': form, 'board': board, 'username': username})
    return render_to_response('board_write.html', variables)

def board_list(request, board_name, page_number=1):
    username, user_id, bs_year = Oauth.Instance().get_bs_class_year()
    if board_name == 'home' and not is_bacchus(user_id):
        return HttpResponseRedirect('/home')
    page_number = int(page_number)
    page_number -= 1

    board = Board.objects.get(name=board_name)
    articles = homepage.boards.get_latest_article(board, page_number)

    page_count = max(int(
        (board.article_count + homepage.const.ARTICLE_PER_PAGE_DEFAULT - 1) 
        / homepage.const.ARTICLE_PER_PAGE_DEFAULT
        ), 1)

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
    username, user_id, bs_year = Oauth.Instance().get_bs_class_year()

    if request.method == 'POST':
        if username is None:
            return HttpResponseRedirect('/board/show/%s/' % article_id)
        elif user_id is None:
            return HttpResponseRedirect('/board/show/%s/' % article_id)
        elif bs_year is None:
            return HttpResponseRedirect('/board/show/%s/' % article_id)
        form = CommentWriteForm(request.POST, label_suffix='')
        if form.is_valid():
            comment = Comment.objects.create(
                    article = article,
                    content = form.cleaned_data['content'],
                    name = username,
                    user_id = user_id,
                    bs_year = bs_year,
                    email = form.cleaned_data['email'])
            comment.save()

            article.comment_count += 1
            article.save()
            subject = u"[{0}] {1} - new comment : {2}".format(article.board.name, article.title[0:10], comment.content[0:10])
            content = u"Content : {0}".format(article.content)
            user = u"User :\n\tuser_id : {0}\n\tusername : {1}\n\tbs_year : {2}\n\temail : {3}\n\thomepage : {4}".format(article.user_id, article.username, article.bs_year, article.email, article.homepage)
            comment_content = u"New Comment : {0}".format(comment.content)
            comment_user = u"New Comment User :\n\tuser_id : {0}\n\tusername : {1}\n\tbs_year : {2}\n\temail : {3}".format(comment.user_id, comment.name, comment.bs_year, comment.email)
            article_url = request.build_absolute_uri()
            link = u"Link : {0}".format(article_url)
            message = u"{0}\n\n{1}\n\n{2}\n\n{3}\n\n{4}".format(content, user, comment_content, comment_user, link)
            send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.DEFAULT_FROM_EMAIL], fail_silently = False)
            return HttpResponseRedirect('/board/show/%s/' % article_id)
    else:
        form = CommentWriteForm(label_suffix='')

    comments = Comment.objects.filter(article = article)

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
    username, user_id, bs_year = Oauth.Instance().get_bs_class_year()

    if request.method == 'POST':
        if article.user_id is not None and article.user_id != '':
            if article.user_id != user_id:
                pass
            else:
                article.delete()
        else:
            form = ArticleRemoveForm(request.POST, label_suffix='')
            if form.is_valid() == False:
                pass
            elif article.check_password(form.cleaned_data['password']):
                article.delete()
        return HttpResponseRedirect('/board/%s/' % board.name)
    else:
        if article.user_id is not None and article.user_id != '':
            if article.user_id != user_id:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                form = None
        else:
            form = ArticleRemoveForm(label_suffix='')

    variables = RequestContext(request, {
        'board': board,
        'article': article,
        'form': form,
        'username': username
        })

    return render_to_response('article_remove.html', variables)

def is_bacchus(user_id):
    bacchus = ["jsryu21", "y975y9200", "wookayin", "shuin318", "littlechun4", "kqqk1234", "gwolves", "holys0210", \
	"kcm1700", "bert1234", "vs223", "a9413", "veckal", "sunbi9339"]
    return user_id in bacchus 
