from homepage.models import *
import homepage.const

def get_latest_article(board, page_number=0, article_per_page=homepage.const.ARTICLE_PER_PAGE_DEFAULT):
    articles = Article.objects.filter(board=board).order_by('-id')[page_number*article_per_page:(page_number+1)*article_per_page]

    return articles


def get_range_pagination(page_count, page_number):
    page_minimum = max(1, page_number - 6)
    page_maximum = min(page_count, page_number + 6)
    return xrange(page_minimum, page_maximum)
