import requests

'''
1.UA 伪装
反反爬策略
'''
def user_agent(type='chrome'):
    #headers 信息
    if type == 'chrome':
        user_agent_info = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    elif type == 'firefox':
        user_agent_info = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'
    else:
        user_agent_info = ''
    return user_agent_info
def from_str_to_dict(params):
    params_list = params.split('&')
    params_dict = {}
    for p in params_list:
        index = p.find('=')
        k = p[:index]
        v = p[index+1:]
        params_dict[k] = v
    return params_dict

