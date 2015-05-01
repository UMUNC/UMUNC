#coding=utf8
from django.template import Library 
from django.template.defaultfilters import stringfilter 
import re

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