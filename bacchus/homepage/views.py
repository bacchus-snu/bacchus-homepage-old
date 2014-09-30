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

def home(request):
	member_id = request.session.get('member_id', '')
	if member_id != '':
		return HttpResponseRedirect('/board/home/')
	board = Board.objects.get(name='home')
	articles = homepage.boards.get_latest_article(board,
		article_per_page=homepage.const.ARTICLE_PER_PAGE_NOTICE)
	variables = RequestContext(request, {'articles': articles, 'member_id': member_id})
	return render_to_response('home.html', variables)

def home_pagination_view(request, page_number):
	print 'asdf'
	member_id = request.session.get('member_id', '')
	print member_id
	if member_id != '':
		return HttpResponseRedirect('/board/home/%s/' % page_number)
	board = Board.objects.get(name='home')
	articles = homepage.boards.get_latest_article(board,
		article_per_page=homepage.const.ARTICLE_PER_PAGE_NOTICE)
	variables = RequestContext(request, {'articles': articles, 'member_id': member_id})
	return render_to_response('home.html', variables)

def notice_view(request):
	return HttpResponseRedirect('/board/notice/')

def notice_pagination_view(request, page_number):
	return HttpResponseRedirect('/board/notice/%s/' % page_number)

def about(request):
	return render_to_response('about.html', RequestContext(request, {'member_id':request.session.get('member_id', '')}))

# services
def service_term(request):
	return render_to_response('services_terms.html')

def service_account(request):
	return render_to_response('services_account.html')

def service_server(request):
	return render_to_response('services_server.html')

def service_lab(request):
	return render_to_response('services_lab.html')

def service_printer(request):
	return render_to_response('home.html')

def service_community(request):
	return render_to_response('home.html')

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
		id = request.POST.get("username")
		pw = request.POST.get("password")
		if check_credentials(id, pw) == None:
			request.session['member_id'] = id
		else:
			request.session['member_id'] = ''
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def logout_view(request):
	del request.session['member_id']
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# board 
def board_write(request, board_name):
	member_id = request.session.get('member_id', '')
	if member_id == '':
		return HttpResponseRedirect('/board/' + board_name + '/')
	if board_name == 'notice' or board_name == 'faq':
		if is_bacchus(member_id) == False:
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

	variables = RequestContext(request, {'form': form, 'board': board, 'member_id': request.session.get('member_id', '')})
	return render_to_response('board_write.html', variables)

def board_list(request, board_name, page_number=0):
	page_number = int(page_number)

	board = Board.objects.get(name=board_name)
	articles = homepage.boards.get_latest_article(board)

	page_count = max(int(
		(board.article_count + homepage.const.ARTICLE_PER_PAGE_DEFAULT - 1) 
		/ homepage.const.ARTICLE_PER_PAGE_DEFAULT
	), 1)

	member_id = request.session.get('member_id', '')

	variables = RequestContext(request, {
		'board': board,
		'articles': articles, 
		'page_count_for_loop': xrange(1, page_count + 1), 
		'page_number': homepage.boards.get_range_pagination(page_count, page_number),
		'member_id': member_id,
		'is_bacchus': is_bacchus(member_id)
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

	variables = RequestContext(request, {
		'board': board,
		'article': article,
		'comments': comments,
		'form': form,
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

	variables = RequestContext(request, {
		'board': board,
		'article': article,
		'form': form,
	})
	
	return render_to_response('article_remove.html', variables)

def is_bacchus(id):
	return id == "jsryu21"

def check_credentials(username, password):
	"""Verifies credentials for username and password.
	Returns None on success or a string describing the error on failure
	# Adapt to your needs
	"""
	LDAP_SERVER = 'ldap://colada.snucse.org'
	# fully qualified AD user name
	LDAP_USERNAME = '%s@snucse.org' % username
	# your password
	LDAP_PASSWORD = password
	try:
		# build a client
		ldap_client = ldap.initialize(LDAP_SERVER)
		# perform a synchronous bind
		ldap_client.set_option(ldap.OPT_REFERRALS,0)
		ldap_client.simple_bind_s(LDAP_USERNAME, LDAP_PASSWORD)
	except ldap.INVALID_CREDENTIALS:
		ldap_client.unbind()
		return 'Wrong username ili password'
	except ldap.SERVER_DOWN:
		return 'AD server not awailable'
	ldap_client.unbind()
	return None
