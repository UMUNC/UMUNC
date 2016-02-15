#coding=utf8
from django.template import Library
from django.template.defaultfilters import stringfilter
import re
from classytags.arguments import (Argument, MultiValueArgument,
                                  MultiKeywordArgument)
from classytags.core import Options, Tag
from classytags.helpers import AsTag
import math

register = Library()

@stringfilter
def transconference(value):
	if value in [1,2,3,4,5,6,7,8,9]:return 1
	if value in [10,11,12,13,14,15,16]:return 2
	if value in [17,18,19,20,21,22,23]:return 3

def force_unicode(s):
    return unicode(s)

##################################################################################
#截取字符工具,不保留html
##################################################################################

def truncatewords(s,num,end_text='(Read More ...)'):

    re_tag= re.compile(r'<(/)?([^ ]+?)(?: (/)| .*?)?>')
    re_words = re.compile(u'(&.*?;)|[\u4e00-\u9fa5]{1}|[^\u4e00-\u9fa5]{1}',re.UNICODE)

    s = force_unicode(s)

    length=int(num)

    if length<=0:
        return u''

    pos = 0
    words=0
    data=[]
    out=''
    current_word = ''
    while words <= length:
        if words==length:
            break

        #查找第一个标签结束的>
        m= re_tag.search(s,pos)
        if not m:
            break
        pos = m.end()

        #开始从这个位置向后搜索字符,匹配到第一个字符，停止，检查,如果字符是<,说明匹配到了html标签了,则跳出去,否则开始检查下一个标签的>
        while words <= length:
            if words==length:
                break
            m = re_words.search(s,pos)
            if not m:
                break
            current_word = m.group()
            if current_word=='<':
                break
            else:
                if not m.group(1):
                    words+=1
                    data.append(str(m.group()))
                    pos+=1
                else:
                    words+=1
                    data.append(str(m.group()))
                    pos=m.end()

    out = ''.join(data)

    out+=end_text
    return out

##################################################################################
#截取字符工具，保留html
##################################################################################

def truncatewords_html(s,num,end_text='(Read More ...)'):

    html4_singlets = ('br', 'col', 'link', 'base', 'img', 'param', 'area', 'hr', 'input')
    re_tag= re.compile(r'<(/)?([^ ]+?)(?: (/)| .*?)?>')
    re_words = re.compile(u'(&.*?;)|[\u4e00-\u9fa5]{1}|[^\u4e00-\u9fa5]{1}',re.UNICODE)

    s = force_unicode(s)


    length=int(num)

    if length<=0:
        return u''

    pos = 0
    words=0
    current_word = ''
    open_tags=[]
    while words <= length:
        if words==length:
            break

        #查找第一个标签结束的>
        m= re_tag.search(s,pos)
        if not m:
            break
        pos = m.end()
        closing_tag,tagname,self_closing=m.groups()

        #自关闭标签不处理,或者是单标签
        if self_closing or tagname in html4_singlets:
            pass
        elif closing_tag:
            # Check for match in open tags list
            try:
                i = open_tags.index(tagname)
            except ValueError:
                pass
            else:
                #移除该标签，说明该标签已经闭合
                open_tags.remove(tagname)
        else:
            #把标签加入到仍然打开的标签中
            open_tags.insert(0, tagname)

        #开始从这个位置向后搜索字符,匹配到第一个字符，停止，检查,如果字符是<则跳出去,否则开始检查下一个标签的>
        while words <= length:

            if words==length:
                break
            m = re_words.search(s,pos)
            if not m:
                break
            current_word = m.group()
            if current_word=='<':
                break
            else:
                if not m.group(1):
                    words+=1
                    pos+=1
                else:
                    words+=1
                    pos=m.end()
    #如果本身的大小就不够，则不加结尾
    if pos==len(s):
        return s
    out = s[:pos]
    if end_text:
        out += ' ' + end_text
    # Close any tags still open
    for tag in open_tags:
        out += '</%s>' % tag

    # Return string
    return out

register.filter('truncatewords_hans', truncatewords)
register.filter('truncatewords_hans_html', truncatewords_html)
register.filter('transconference', transconference)

class Paginate(AsTag):
    name = 'Paginate'
    options = Options(
        Argument('request'),
        Argument('container'),
        'maxitem',
        Argument('maxitem', resolve=False, required=False, default=30),
        'maxmenuitem',
        Argument('maxmenuitem', resolve=False, required=False, default=10),
        'page',
        Argument('page', resolve=False, required=False, default=0),
        'key',
        Argument('key', resolve=False, required=False, default='paginate_id'),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, request, container, maxitem, maxmenuitem, page, key):
        maxitem, maxmenuitem, page = int(maxitem), int(maxmenuitem), int(page)
        length = len(container)
        maxpage = int(math.ceil(length / maxitem))

        if not page:
            #try:
            page = int(request.GET[key])
            #except:
            #    page = 1;

        if page > maxpage : page = maxpage
        if page < 1: page = 1

        response_page = []

        if maxpage < maxmenuitem:
            for i in range(1, maxpage + 1):
                response_page.append({
                    'id': i,
                    'currectpage': i == page,
                })
        elif page - (maxpage - 1) // 2 < 1:
            for i in range(1, maxmenuitem + 1):
                response_page.append({
                    'id': i,
                    'currectpage': i == page,
                })
        elif page + (maxpage - 1) // 2 > maxpage:
            for i in range(maxpage - maxmenuitem, maxpage + 1):
                response_page.append({
                    'id': i,
                    'currectpage': i == page,
                })
        else:
            for i in range(page - (maxpage - 1) // 2, page + (maxpage - 1) // 2 + 1):
                response_page.append({
                    'id': i,
                    'currectpage': i == page,
                })

        response = {
            'container': container,
            'containerP': container[maxitem * (page - 1): maxitem * page],
            'attr':{
                'currectpage': page,
                'maxpage': maxpage,
                'start': min(maxitem * (page - 1) + 1, length),
                'end': min(maxitem * page, length),
                'length': length,
                'page': response_page,
                'previous': page != 1,
                'next': page != maxpage,
                'key': key,
            }
        }

        return response

register.tag(Paginate)
