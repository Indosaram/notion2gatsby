def _edit_js(file, target, code):
    if not isinstance(target, list):
        target = [target]
    if not isinstance(code, list):
        code = [code]

    with open(file,'r') as f:
        lines = f.readlines()

    idx = 0
    with open(file,'w') as f:
        for line in lines:
            if len(target) - idx > 0:
                if line.startswith(target[idx]):
                    line = target[idx] + f'`{code[idx]}`,\n'
                    idx += 1
            f.write(line)

def set_analytics_code(code):
    """
    Thin wrapper for analytics code
    """
    file = 'gatsby-config.js'
    target = '        trackingId: '
    _edit_js(file, target, code)

def set_adsense_code(code):
    """
    Thin wrapper for adsense code
    """
    file = 'gatsby-config.js'
    target = '        publisherId: '
    _edit_js(file, target, code)

def copy_param2config(param):
    file = 'gatsby-config.js'
    
    target = [
        '    title: ',
        '    description: ',
        '    author: ',
        '    siteUrl: ',
        '      twitter: ',
    ]

    code = [
        param['blog_title'],
        param['description'],
        param['author'],
        param['siteurl'],        
        param['twitter']
    ]

    _edit_js(file, target, code)
