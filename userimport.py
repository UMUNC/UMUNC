from django.contrib.auth.models import User
from umunc_iris.models import profile, country
from umunc_cheetah.models import room
from umunc_mpc.models import Press
import simplejson
def calc(data):
	for one in data:
		tuser = User.objects.create_user(username=one['username'],password=one['username'],email='i@umunc.org')
		tuser.save()
		tprofile = profile(
			User=tuser,
			Leader=False,
			Init=False,
			Name=one['name'],
			Sex=True,
			Age=0,
			IDNum='',
			School='',
			Grade=1,
			GName='',
			GPhone='',
			Phone='',
			Phone2='',
			QQ='',
			Wechat='',
			MunAge=0,
			MunRsm='',
			MunJoined=False,
			Commitee=1,
			Review='',
			Status=1,)
		tcountry, code = country.objects.get_or_create(Name=one['country'])
		tprofile.Country = tcountry
		tprofile.Identify = one['identify']
		tprofile.save()
		if one ['type'] == 'NG':
			troom, code = room.objects.get_or_create(Name=one['country'])
			troom.User.add(tuser)
			troom.save()
		if one ['type'] == 'ALH':
			troom, code = room.objects.get_or_create(Name='联合国安全理事会')
			troom.User.add(tuser)
			troom.save()
			try:
				troom, code = room.objects.get(Name=one['country'])
				troom.User.add(tuser)
				troom.save()
			except:
				pass
		if one ['type'] == 'WJT':
			troom, code = room.objects.get_or_create(Name=one['country'])
			troom.User.add(tuser)
			troom.save()
			troom, code = room.objects.get_or_create(Name='外交团')
			troom.User.add(tuser)
			troom.save()
		if one ['type'] == 'MPC':
			tpress, code = Press.objects.get_or_create(name=one['country'])
			tpress.user.add(tuser)
			tpress.save()
			troom, code = room.objects.get_or_create(Name=one['country'])
			troom.User.add(tuser)
			troom.save()
			troom, code = room.objects.get_or_create(Name='MPC媒体中心')
			troom.User.add(tuser)
			troom.save()
	for one in data:
		tuser = User.objects.get(username=one['username'])
		troom, code = room.objects.get_or_create(Name='联动体系中心')
		troom.User.add(tuser)
		troom.save()
		troom, code = room.objects.get_or_create(Name='技术团队支持')
		troom.User.add(tuser)
		troom.save()

data = '''
[
{"username":"wangaofei","country":"美利坚合众国","identify":"总统","name":"王傲飞","type":"NG"},
{"username":"shixiaoqi","country":"美利坚合众国","identify":"副总统","name":"石小琦","type":"NG"},
{"username":"caiwwenjun","country":"美利坚合众国","identify":"国务卿","name":"蔡文君","type":"NG"},
{"username":"zhuguokaize","country":"美利坚合众国","identify":"副国务卿","name":"朱郭恺泽","type":"NG"},
{"username":"libowen","country":"美利坚合众国","identify":"国家安全事务助理","name":"李博文","type":"NG"},
{"username":"xuminglian","country":"美利坚合众国","identify":"国防部长","name":"徐铭濂","type":"NG"},
{"username":"wangminghe","country":"美利坚合众国","identify":"商务部长","name":"王鸣鹤","type":"NG"},
{"username":"rangyukun","country":"美利坚合众国","identify":"国土安全部长","name":"唐煜坤","type":"NG"},
{"username":"wangyujue","country":"美利坚合众国","identify":"国家情报总监","name":"王玉珏","type":"NG"},
{"username":"tianyuqi","country":"美利坚合众国","identify":"参谋长联席会议主席","name":"田雨琪","type":"NG"},
{"username":"sunyaoqian","country":"美利坚合众国","identify":"发言人","name":"孙瑶倩","type":"NG"},
{"username":"chiliyuan","country":"中华人民共和国","identify":"中共中央总书记、国家主席、中央军委主席","name":"迟力源","type":"NG"},
{"username":"zhuyuquan","country":"中华人民共和国","identify":"国务院总理","name":"朱昱全","type":"NG"},
{"username":"wangzeji","country":"中华人民共和国","identify":"国务院副总理","name":"王泽基","type":"NG"},
{"username":"liuwenheng","country":"中华人民共和国","identify":"国务院副总理","name":"刘文衡","type":"NG"},
{"username":"litong","country":"中华人民共和国","identify":"国务委员","name":"李童","type":"NG"},
{"username":"wuyichen","country":"中华人民共和国","identify":"国家安全部部长","name":"吴羿辰","type":"NG"},
{"username":"chenzhuo","country":"中华人民共和国","identify":"国防部部长","name":"陈卓","type":"NG"},
{"username":"jiangwenqing","country":"中华人民共和国","identify":"商务部部长","name":"蒋文青","type":"NG"},
{"username":"dingyanfang","country":"中华人民共和国","identify":"外交部部长","name":"丁彦方","type":"NG"},
{"username":"sunjiayi","country":"中华人民共和国","identify":"外交部副部长","name":"孙嘉逸","type":"NG"},
{"username":"sunruowen","country":"中华人民共和国","identify":"外交部发言人","name":"孙若文","type":"NG"},
{"username":"suyu","country":"俄罗斯联邦","identify":"总统","name":"苏钰","type":"NG"},
{"username":"zhangwendao","country":"俄罗斯联邦","identify":"总理","name":"张文韬","type":"NG"},
{"username":"yerubing","country":"俄罗斯联邦","identify":"第一副总理","name":"叶茹冰","type":"NG"},
{"username":"renyuxiang","country":"俄罗斯联邦","identify":"外交部长","name":"任宇祥","type":"NG"},
{"username":"wangyetong","country":"俄罗斯联邦","identify":"外交副部长","name":"王业通","type":"NG"},
{"username":"shipucun","country":"俄罗斯联邦","identify":"国防部长","name":"史璞存","type":"NG"},
{"username":"yuewenshen","country":"俄罗斯联邦","identify":"经济发展部长","name":"岳文莘","type":"NG"},
{"username":"mengxin","country":"俄罗斯联邦","identify":"联邦安全局局长","name":"孟昕","type":"NG"},
{"username":"youjiangyu","country":"俄罗斯联邦","identify":"外交部新闻发言人","name":"尤江羽","type":"NG"},
{"username":"majunyao","country":"俄罗斯联邦","identify":"联邦武装力量总参谋长","name":"马骏骁","type":"NG"},
{"username":"bihaoyu","country":"俄罗斯联邦","identify":"工业与贸易部部长","name":"毕皓宇","type":"NG"},
{"username":"zhongwenshan","country":"大不列颠以及北爱尔兰联合王国","identify":"首相","name":"钟汶珊","type":"NG"},
{"username":"lujunfei","country":"大不列颠以及北爱尔兰联合王国","identify":"财政大臣","name":"卢俊妃","type":"NG"},
{"username":"gongyaning","country":"大不列颠以及北爱尔兰联合王国","identify":"内政大臣","name":"巩雅宁","type":"NG"},
{"username":"yaojiacheng","country":"大不列颠以及北爱尔兰联合王国","identify":"外交大臣","name":"姚嘉程","type":"NG"},
{"username":"wangkunting","country":"大不列颠以及北爱尔兰联合王国","identify":"国防大臣","name":"王坤婷","type":"NG"},
{"username":"liuhanqi","country":"大不列颠以及北爱尔兰联合王国","identify":"能源和气候变化大臣","name":"刘寒琦","type":"NG"},
{"username":"zhanghaowen","country":"大不列颠以及北爱尔兰联合王国","identify":"内阁办公室国务大臣","name":"张浩雯","type":"NG"},
{"username":"zhaichaoqun","country":"大不列颠以及北爱尔兰联合王国","identify":"商业、创新和技能大臣兼贸易委员会主席","name":"翟超群","type":"NG"},
{"username":"yangyuxiao","country":"大不列颠以及北爱尔兰联合王国","identify":"首相府官方发言人","name":"杨予潇","type":"NG"},
{"username":"xunuo","country":"大不列颠以及北爱尔兰联合王国","identify":"军情六处局长","name":"许诺","type":"NG"},
{"username":"lisicheng","country":"法兰西共和国","identify":"总统","name":"李思成","type":"NG"},
{"username":"lizhilong","country":"法兰西共和国","identify":"总理","name":"李智龙","type":"NG"},
{"username":"zhangluyu","country":"法兰西共和国","identify":"外交与国际发展部长","name":"张鲁渝","type":"NG"},
{"username":"yanlongcheng","country":"法兰西共和国","identify":"法国外交部秘书长","name":"闫龙程","type":"NG"},
{"username":"zhangxiaodan","country":"法兰西共和国","identify":"财政与公共账目部长","name":"张潇丹","type":"NG"},
{"username":"zhaohaoyi","country":"法兰西共和国","identify":"国防部长","name":"赵浩玄","type":"NG"},
{"username":"liuchunshan","country":"法兰西共和国","identify":"经济、工业和数字经济部长","name":"刘春杉","type":"NG"},
{"username":"liwen","country":"法兰西共和国","identify":"外贸、旅游促进国务秘书","name":"李文","type":"NG"},
{"username":"mengyanzheng","country":"法兰西共和国","identify":"内政部长","name":"孟彦铮","type":"NG"},
{"username":"yangjiayu","country":"法兰西共和国","identify":"农业_食品和林业部长兼政府发言人","name":"杨佳玉","type":"NG"},
{"username":"wangyanzhao","country":"美利坚合众国","identify":"常任理事国 驻安理会代表","name":"王彦钊","type":"ALH"},
{"username":"chenzhengjie","country":"美利坚合众国","identify":"常任理事国 驻安理会代表","name":"陈正杰","type":"ALH"},
{"username":"lvfengjin","country":"中华人民共和国","identify":"常任理事国 驻安理会代表","name":"吕奉瑾","type":"ALH"},
{"username":"lvyingming","country":"中华人民共和国","identify":"常任理事国 驻安理会代表","name":"吕英铭","type":"ALH"},
{"username":"keshirui","country":"法兰西共和国","identify":"常任理事国 驻安理会代表","name":"柯诗蕊","type":"ALH"},
{"username":"sunhongyun","country":"法兰西共和国","identify":"常任理事国 驻安理会代表","name":"孙洪运 ","type":"ALH"},
{"username":"wangganfeng","country":"大不列颠以及北爱尔兰联合王国","identify":"常任理事国 驻安理会代表","name":"王淦锋","type":"ALH"},
{"username":"limengze","country":"大不列颠以及北爱尔兰联合王国","identify":"常任理事国 驻安理会代表","name":"李梦泽","type":"ALH"},
{"username":"qianruntong","country":"俄罗斯联邦","identify":"常任理事国 驻安理会代表","name":"钱润彤","type":"ALH"},
{"username":"wangfangqi","country":"俄罗斯联邦","identify":"常任理事国 驻安理会代表","name":"王方祺","type":"ALH"},
{"username":"yangyueying","country":"安哥拉共和国","identify":"非常任理事国 驻安理会代表","name":"杨_滢","type":"ALH"},
{"username":"zhaochaoyue","country":"安哥拉共和国","identify":"非常任理事国 驻安理会代表","name":"赵超越","type":"ALH"},
{"username":"liulinlin","country":"日本国","identify":"非常任理事国 驻安理会代表","name":"刘琳琳","type":"ALH"},
{"username":"liuyongxi","country":"日本国","identify":"非常任理事国 驻安理会代表","name":"刘咏熙","type":"ALH"},
{"username":"liuwentong","country":"马来西亚联邦","identify":"非常任理事国 驻安理会代表","name":"刘文童","type":"ALH"},
{"username":"wangxiaohan","country":"马来西亚联邦","identify":"非常任理事国 驻安理会代表","name":"王潇寒","type":"ALH"},
{"username":"dengzhihang","country":"阿拉伯埃及共和国","identify":"非常任理事国 驻安理会代表","name":"邓智航","type":"ALH"},
{"username":"zhaozhan","country":"阿拉伯埃及共和国","identify":"非常任理事国 驻安理会代表","name":"赵展","type":"ALH"},
{"username":"fuchenglong","country":"委内瑞拉玻利瓦尔共和国","identify":"非常任理事国 驻安理会代表","name":"符成龙","type":"ALH"},
{"username":"caozhuoru","country":"委内瑞拉玻利瓦尔共和国","identify":"非常任理事国 驻安理会代表","name":"曹卓如","type":"ALH"},
{"username":"jiangyiyue","country":"西班牙王国","identify":"非常任理事国 驻安理会代表","name":"蒋一阅","type":"ALH"},
{"username":"zhoukunzhuo","country":"西班牙王国","identify":"非常任理事国 驻安理会代表","name":"周_卓","type":"ALH"},
{"username":"linxiaoyu","country":"新西兰","identify":"非常任理事国 驻安理会代表","name":"林晓宇","type":"ALH"},
{"username":"zhangziyi","country":"新西兰","identify":"非常任理事国 驻安理会代表","name":"张子怡","type":"ALH"},
{"username":"zhouxiaosong","country":"塞内加尔共和国","identify":"非常任理事国 驻安理会代表","name":"周晓嵩","type":"ALH"},
{"username":"caozixian","country":"塞内加尔共和国","identify":"非常任理事国 驻安理会代表","name":"曹子贤","type":"ALH"},
{"username":"xiaomuyun","country":"乌拉圭东岸共和国","identify":"非常任理事国 驻安理会代表","name":"肖沐昀","type":"ALH"},
{"username":"caipeizhe","country":"乌拉圭东岸共和国","identify":"非常任理事国 驻安理会代表","name":"蔡沛哲","type":"ALH"},
{"username":"maqingyun","country":"乌克兰","identify":"非常任理事国 驻安理会代表","name":"马清云","type":"ALH"},
{"username":"weiweiyu","country":"乌克兰","identify":"非常任理事国 驻安理会代表","name":"卫蔚宇","type":"ALH"},
{"username":"yangcongyuan","country":"土耳其共和国","identify":"安理会观察国 驻联代表","name":"杨丛源","type":"ALH"},
{"username":"quhongyi","country":"阿拉伯叙利亚共和国","identify":"安理会观察国 驻联代表","name":"曲虹屹","type":"ALH"},
{"username":"yangzexuan","country":"伊拉克共和国","identify":"安理会观察国 驻联代表","name":"杨泽轩","type":"ALH"},
{"username":"cheliwei","country":"德意志联邦共和国","identify":"安理会观察国 驻联代表","name":"车立威","type":"ALH"},
{"username":"liyanan","country":"意大利共和国","identify":"安理会观察国 驻联代表","name":"李亚楠","type":"ALH"},
{"username":"liuaodong","country":"比利时王国","identify":"安理会观察国 驻联代表","name":"刘傲冬","type":"ALH"},
{"username":"diaowenshu","country":"丹麦王国","identify":"安理会观察国 驻联代表","name":"刁文舒","type":"ALH"},
{"username":"wangxueying","country":"约旦哈希姆王国","identify":"安理会观察国 驻联代表","name":"王雪颖","type":"ALH"},
{"username":"quyihui","country":"伊朗伊斯兰共和国","identify":"安理会观察国 驻联代表","name":"屈毅辉","type":"ALH"},
{"username":"xiahaoyuan","country":"沙特阿拉伯王国","identify":"安理会观察国 驻联代表","name":"夏浩原","type":"ALH"},
{"username":"zhangxiaoshuo","country":"希腊共和国","identify":"安理会观察国 驻联代表","name":"张小烁","type":"ALH"},
{"username":"hujingao","country":"黎巴嫩共和国","identify":"安理会观察国 驻联代表","name":"胡敬澳","type":"ALH"},
{"username":"songshuangning","country":"以色列国","identify":"安理会观察国 驻联代表","name":"宋双宁","type":"ALH"},
{"username":"yuanhuaze","country":"阿富汗伊斯兰共和国","identify":"安理会观察国 驻联代表","name":"袁华泽","type":"ALH"},
{"username":"lizhiyuan","country":"德意志联邦共和国","identify":"外交部长","name":"李志远","type":"WJT"},
{"username":"liyifan","country":"德意志联邦共和国","identify":"国防部长","name":"李一凡","type":"WJT"},
{"username":"huangchenyu","country":"德意志联邦共和国","identify":"外交部副部长","name":"黄辰宇","type":"WJT"},
{"username":"hexian","country":"意大利共和国","identify":"外交与国际合作部部长","name":"何娴","type":"WJT"},
{"username":"lijiaze","country":"意大利共和国","identify":"国防部长","name":"李佳泽","type":"WJT"},
{"username":"duruotong","country":"意大利共和国","identify":"外交与国际合作部副部长","name":"杜若彤","type":"WJT"},
{"username":"liyexiang","country":"比利时王国","identify":"副首相兼外交、外贸、财政大臣","name":"李业翔","type":"WJT"},
{"username":"zhuzhaohui","country":"比利时王国","identify":"国防大臣","name":"朱兆慧","type":"WJT"},
{"username":"liyiru","country":"比利时王国","identify":"联邦外交部秘书长","name":"李意如","type":"WJT"},
{"username":"wujiayi","country":"丹麦王国","identify":"外交大臣","name":"吴佳忆","type":"WJT"},
{"username":"tongyao","country":"丹麦王国","identify":"国防大臣","name":"仝瑶","type":"WJT"},
{"username":"cuikaiming","country":"土耳其共和国","identify":"外交部长","name":"崔楷铭","type":"WJT"},
{"username":"wujunhao","country":"土耳其共和国","identify":"国防部长","name":"武俊豪","type":"WJT"},
{"username":"wangtianyu","country":"土耳其共和国","identify":"外交部副部长","name":"王甜宇","type":"WJT"},
{"username":"heyirui","country":"阿拉伯叙利亚共和国","identify":"外交部长","name":"何宜芮","type":"WJT"},
{"username":"wutingyan","country":"阿拉伯叙利亚共和国","identify":"国防部长（军职）","name":"吴亭妍","type":"WJT"},
{"username":"xuxinqi","country":"阿拉伯叙利亚共和国","identify":"外交部常务副部长","name":"徐馨琦","type":"WJT"},
{"username":"xushihao","country":"伊拉克共和国","identify":"外交部长","name":"谢仕昊","type":"WJT"},
{"username":"zhaozhengran","country":"伊拉克共和国","identify":"国防部长","name":"赵铮然","type":"WJT"},
{"username":"chenziyue","country":"伊拉克共和国","identify":"外交部副部长","name":"陈子悦","type":"WJT"},
{"username":"sunpengfei","country":"伊朗伊斯兰共和国","identify":"外交部长","name":"孙鹏飞","type":"WJT"},
{"username":"mengzifan","country":"伊朗伊斯兰共和国","identify":"国防与武装力量后勤部部长（军职）","name":"孟子凡","type":"WJT"},
{"username":"zhangzongxu","country":"伊朗伊斯兰共和国","identify":"外交部副部长","name":"张宗旭","type":"WJT"},
{"username":"litianyi","country":"约旦哈希姆王国","identify":"首相兼国防大臣","name":"李天一","type":"WJT"},
{"username":"yanghaozhe","country":"约旦哈希姆王国","identify":"副首相兼外交与侨务大臣","name":"杨瀚_","type":"WJT"},
{"username":"lvminghao","country":"沙特阿拉伯王国","identify":"王储继承人兼第二副首相和国防大臣","name":"吕明昊","type":"WJT"},
{"username":"bingjiyuan","country":"沙特阿拉伯王国","identify":"外交大臣","name":"邴纪元","type":"WJT"},
{"username":"liminze","country":"沙特阿拉伯王国","identify":"副外长","name":"李_泽","type":"WJT"},
{"username":"zhanghengzhi","country":"希腊共和国","identify":"外长","name":"张恒之","type":"WJT"},
{"username":"wangxinzhi","country":"希腊共和国","identify":"国防部长","name":"王新智","type":"WJT"},
{"username":"lihanlin","country":"日本国","identify":"外务大臣","name":"李瀚琳","type":"WJT"},
{"username":"lianghuihao","country":"日本国","identify":"防卫大臣","name":"梁雯豪","type":"WJT"},
{"username":"wumingda","country":"黎巴嫩共和国","identify":"外交与侨民事务部长","name":"吴明达","type":"WJT"},
{"username":"songzixuan","country":"黎巴嫩共和国","identify":"总理","name":"宋子璇","type":"WJT"},
{"username":"lvyichen","country":"黎巴嫩共和国","identify":"副总理兼国防部长","name":"吕艺宸","type":"WJT"},
{"username":"lirunqi","country":"以色列国","identify":"总理","name":"李润奇","type":"WJT"},
{"username":"liutong","country":"以色列国","identify":"副外交部长","name":"刘通","type":"WJT"},
{"username":"zhangjiahui","country":"以色列国","identify":"国防部长","name":"张佳慧","type":"WJT"},
{"username":"fuenchen","country":"阿富汗伊斯兰共和国","identify":"外长","name":"付恩臣","type":"WJT"},
{"username":"zhangsilei","country":"阿富汗伊斯兰共和国","identify":"副外长","name":"张思磊","type":"WJT"},
{"username":"zhangzhiyou","country":"阿富汗伊斯兰共和国","identify":"代理国防部长","name":"张智有","type":"WJT"},
{"username":"tianfanfan","country":"阿拉伯埃及共和国","identify":"外交部长","name":"田__","type":"WJT"},
{"username":"kangmingchen","country":"阿拉伯埃及共和国","identify":"总理","name":"康明晨","type":"WJT"},
{"username":"yangzehao","country":"阿拉伯埃及共和国","identify":"国防部长","name":"杨泽昊","type":"WJT"},
{"username":"sunyuanwei","country":"挪威王国","identify":"外交大臣","name":"孙元伟","type":"WJT"},
{"username":"liluyu","country":"挪威王国","identify":"国防部长","name":"李璐羽","type":"WJT"},
{"username":"zhuzhaorui","country":"瑞典王国","identify":"外交部长","name":"朱兆锐","type":"WJT"},
{"username":"jiawenxuan","country":"瑞典王国","identify":"国防部长","name":"贾文轩","type":"WJT"},
{"username":"wangtingyuan","country":"芬兰共和国","identify":"外交部长","name":"王亭元","type":"WJT"},
{"username":"xiayichen","country":"芬兰共和国","identify":"国防部长","name":"夏_辰","type":"WJT"},
{"username":"wangtianwei","country":"爱沙尼亚共和国","identify":"外交部长","name":"王天蔚","type":"WJT"},
{"username":"zhaoxianyu","country":"爱沙尼亚共和国","identify":"外交助理","name":"赵翔宇","type":"WJT"},
{"username":"liushuaichen","country":"拉脱维亚共和国","identify":"外交部长","name":"刘帅辰","type":"WJT"},
{"username":"zhanghengwei","country":"拉脱维亚共和国","identify":"外交助理","name":"张恒玮","type":"WJT"},
{"username":"yangyifei","country":"乌克兰","identify":"总统","name":"杨逸飞","type":"WJT"},
{"username":"xiaoxiao","country":"乌克兰","identify":"外交部长","name":"肖尧","type":"WJT"},
{"username":"supeizhe","country":"乌克兰","identify":"外交助理","name":"苏培哲","type":"WJT"},
{"username":"lvtiancheng","country":"白俄罗斯共和国","identify":"外交部长","name":"吕天成","type":"WJT"},
{"username":"zhangchanggao","country":"白俄罗斯共和国","identify":"国防部长","name":"张昌镐","type":"WJT"},
{"username":"yangyibin","country":"波兰共和国","identify":"外交部长","name":"杨亦彬","type":"WJT"},
{"username":"liushixuan","country":"波兰共和国","identify":"副总理兼国防部长","name":"刘世轩","type":"WJT"},
{"username":"liujingyu","country":"罗马尼亚","identify":"外交部长","name":"刘靖宇","type":"WJT"},
{"username":"anchenming","country":"罗马尼亚","identify":"外交助理","name":"安晨铭","type":"WJT"},
{"username":"fujunting","country":"科威特国","identify":"外务助理","name":"傅钧亭","type":"WJT"},
{"username":"diaoxuchen","country":"格鲁吉亚","identify":"外交部长","name":"刁旭辰","type":"WJT"},
{"username":"pengyuqi","country":"格鲁吉亚","identify":"外交助理","name":"彭雨琦","type":"WJT"},
{"username":"zhaowenxu","country":"亚美尼亚共和国","identify":"外交部长","name":"赵文彬","type":"WJT"},
{"username":"chenbin","country":"亚美尼亚共和国","identify":"外交助理","name":"陈彬","type":"WJT"},
{"username":"wangzhaochen","country":"阿塞拜疆共和国","identify":"外交部长","name":"王兆琛","type":"WJT"},
{"username":"wangnan","country":"阿塞拜疆共和国","identify":"外交助理","name":"王楠","type":"WJT"},
{"username":"wangsirui","country":"摩尔多瓦共和国","identify":"副总理兼外交和欧洲一体化部长","name":"王思睿","type":"WJT"},
{"username":"wanghuanyu","country":"摩尔多瓦共和国","identify":"外交助理","name":"王焕昱","type":"WJT"},
{"username":"liupengyang","country":"巴林王国","identify":"外交大臣","name":"刘彤阳","type":"WJT"},
{"username":"wangfei","country":"巴林王国","identify":"外交助理","name":"王斐","type":"WJT"},
{"username":"wangsichang","country":"卡塔尔国","identify":"外交大臣","name":"王思畅","type":"WJT"},
{"username":"hutianjiao","country":"卡塔尔国","identify":"外交助理","name":"胡天骄","type":"WJT"},
{"username":"qiuhongyu","country":"也门共和国","identify":"外长","name":"仇宏宇","type":"WJT"},
{"username":"qiufangning","country":"也门共和国","identify":"外交助理","name":"邱方凝","type":"WJT"},
{"username":"yudingyi","country":"利比亚国","identify":"外交部长","name":"于丁一","type":"WJT"},
{"username":"zengjiaao","country":"利比亚国","identify":"总理","name":"曾家傲","type":"WJT"},
{"username":"zhengdongchen","country":"半岛电视台","identify":"主编","name":"郑东辰","type":"MPC"},
{"username":"liruyin","country":"半岛电视台","identify":"编辑","name":"李如荫","type":"MPC"},
{"username":"wangzeyi","country":"半岛电视台","identify":"编辑","name":"王泽一","type":"MPC"},
{"username":"huangyanran","country":"半岛电视台","identify":"编辑","name":"黄嫣然","type":"MPC"},
{"username":"kanshumeng","country":"半岛电视台","identify":"编辑","name":"阚舒萌","type":"MPC"},
{"username":"yangyuxuan","country":"半岛电视台","identify":"编辑","name":"杨雨萱","type":"MPC"},
{"username":"wangruocong","country":"华盛顿邮报","identify":"主编","name":"王若琮","type":"MPC"},
{"username":"sunmingze","country":"华盛顿邮报","identify":"编辑","name":"孙铭泽","type":"MPC"},
{"username":"zhangyunyao","country":"华盛顿邮报","identify":"编辑","name":"张蕴_","type":"MPC"},
{"username":"zhaodongyuan","country":"华盛顿邮报","identify":"编辑","name":"赵董源","type":"MPC"},
{"username":"wanghualong","country":"华盛顿邮报","identify":"编辑","name":"王骅龙","type":"MPC"},
{"username":"yuexinying","country":"华盛顿邮报","identify":"编辑","name":"岳鑫滢","type":"MPC"},
{"username":"liujingyi","country":"卫报","identify":"主编","name":"刘静怡","type":"MPC"},
{"username":"ligen","country":"卫报","identify":"编辑","name":"李根","type":"MPC"},
{"username":"wangwenqing","country":"卫报","identify":"编辑","name":"李雯清","type":"MPC"},
{"username":"gaohaoran","country":"卫报","identify":"编辑","name":"高浩然","type":"MPC"},
{"username":"wangshuo","country":"卫报","identify":"编辑","name":"王朔","type":"MPC"},
{"username":"xiongjian","country":"卫报","identify":"编辑","name":"熊剑","type":"MPC"},
{"username":"zhuhai","country":"新报","identify":"主编","name":"朱海","type":"MPC"},
{"username":"guanjun","country":"新报","identify":"编辑","name":"管军","type":"MPC"},
{"username":"hexuyang","country":"新报","identify":"编辑","name":"何旭扬","type":"MPC"},
{"username":"dumingkun","country":"新报","identify":"编辑","name":"杜明坤","type":"MPC"},
{"username":"lujunxiang","country":"新报","identify":"编辑","name":"路均翔","type":"MPC"},
{"username":"lvyanpei","country":"新报","identify":"编辑","name":"吕彦培","type":"MPC"},
{"username":"wangjiahao","country":"费加罗报","identify":"主编","name":"王家豪","type":"MPC"},
{"username":"houshumeng","country":"费加罗报","identify":"编辑","name":"侯舒萌","type":"MPC"},
{"username":"dingyutong","country":"费加罗报","identify":"编辑","name":"丁煜桐","type":"MPC"},
{"username":"lixinyu","country":"费加罗报","identify":"编辑","name":"李欣宇","type":"MPC"},
{"username":"chenjiamo","country":"费加罗报","identify":"编辑","name":"陈嘉沫","type":"MPC"},
{"username":"zhangzhihao","country":"费加罗报","identify":"编辑","name":"张智浩","type":"MPC"},
{"username":"haowang","country":"南华早报","identify":"主编","name":"郝旺","type":"MPC"},
{"username":"wangchen","country":"南华早报","identify":"编辑","name":"王晨","type":"MPC"},
{"username":"yuliyuan","country":"南华早报","identify":"编辑","name":"于丽媛","type":"MPC"},
{"username":"caowenjin","country":"南华早报","identify":"编辑","name":"蔡文锦","type":"MPC"},
{"username":"gongyi","country":"南华早报","identify":"编辑","name":"宫毅","type":"MPC"},
{"username":"wuhanxiao","country":"南华早报","identify":"编辑","name":"仵寒筱","type":"MPC"}
]

'''
data = simplejson.loads(data)

calc(data)
