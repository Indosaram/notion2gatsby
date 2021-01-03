from create_github_page import InitGithubPage
from gatsby_helper import *

class GithubPageGenerator:
    def __init__(self):
        return


if __name__ == '__main__':
    """
    Parameters
    """

    param = {
        'blog_title' : 'TEST',
        'description' : 'Test blog for Notion2Gatsby',
        'author' : 'tester',
        'siteurl' : 'indosaram.github.io',
        'twitter' : 'twitter.com',
        'target_dir' : 'C:\code\gh-pages',
        'notion_token' : '129f1b5694a479f940d0226c4033a6d066f9970a126d7c822b3ba45f4002541ccad6704d33c7340195a16757be0fc060399fb25cde612fe8658d66f7a9c139f18fa66be9826288d444b298a6f415',
        'notion_root_page_id' : '0995f90cde434d35ab6369f46b2eaf04',
        'google_analytics' : 'U-XXX',
        'google_adsense' : 'ca-pub-xx',
    }


    """
    Create github repo and pages
    """    
    # TODO: If this is the first time to create Github pages,
    # then create username.github.io repository first.
    # TODO: Clone base directory of mine
    # initiator = InitGithubPage(param)
    # initiator.create_blog()
    # initiator.initiate()

    """
    Gatsby Build helper
    """    
    set_adsense_code(param['google_adsense'])
    set_analytics_code(param['google_analytics'])
    copy_param2config(param)


    # TODO: src/images/ 폴더 아이콘 변경 기능

