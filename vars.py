class vars():
	command_str = 'command'
	cat_str = 'cat'
	girl_str = 'Beauty'
	invalid_str = 'invalid'
	cat_list = ['cat', 'kitty', 'kitties', '貓', '咪', '喵']
	girl_list = ['girl', 'sister', 'woman', 'women', '女', '姐', '姊', '妹']
	ptt_url = 'https://www.ptt.cc'
	ptt_beauty_init = '/bbs/Beauty/index'
	ptt_cat_init = '/bbs/cat/index'

	init_url =\
	{
		girl_str : ptt_beauty_init,\
		cat_str : ptt_cat_init
	}

	lower_bound_dict =\
	{
		girl_str : 50,\
		cat_str : 10
	}

	popularity_excep = ('爆', 'X')

	url_ending = '.html'