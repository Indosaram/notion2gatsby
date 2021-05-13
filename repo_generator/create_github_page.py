import os
import subprocess


class InitGithubPage:
    def __init__(self, param):
        self._get_github_username()
        self.param = param

        # TODO: Proper Exception control
        if 'target_dir' not in param.keys():
            param['target_dir'] = os.getcwd()

            print(
                '❗ WARNING : Target directory is not specified.'
                + 'Create new directory in this path.'
            )

        if not os.path.exists(param['target_dir']):
            os.mkdir(param['target_dir'])

    def _get_github_username(self):
        try:
            username = self._execute('git config --global user.name')
        except FileNotFoundError:
            username_ = input(
                "WARNING: You have not setup your Github username. Enter yours (ex: Indosaram): "
            )
            username = self._execute(
                f'git config --global user.name "{username_}"'
            )

        self.username = username.replace('\n', '')

    def _execute(self, command, shell=True):
        print('✔', command)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=shell)
        stdout = process.communicate()[0]
        try:
            result = stdout.decode('cp949')
        except UnicodeDecodeError:
            result = None

        return result

    def create_blog(self):
        repository_name = self.param['blog_title']
        target_dir = self.param['target_dir']
        template_repo = self.param['template_repo']

        self.path_to_repo = os.path.join(target_dir, repository_name)
        self.repository_name = repository_name

        if os.path.exists(self.path_to_repo):
            print(
                '❌ Error : This repo name already exists. Check again your `blog_title` key in the .json file.'
            )
            return False

        self.target_dir = target_dir

        os.chdir(target_dir)
        self._execute(f'git clone {template_repo}')
        template_name = template_repo.split('/')[-1].split('.')[0]
        os.rename(template_name, repository_name)
        os.chdir(self.path_to_repo)
        print(f"✔ cd {self.path_to_repo}")

        git_commands = [
            "rm -rf .git",
            "git init -q",
            f'gh repo create -y --public {repository_name}',
        ]
        for command in git_commands:
            self._execute(command)

        return True

    def _set_notion_token(self):
        NOTION_USER_ID = self.param["notion_user_id"]
        NOTION_TOKEN = self.param['notion_token']
        NOTION_ROOT_PAGE_ID = self.param['notion_root_page_id']

        # For local run
        with open('.env', 'w') as f:
            f.write(
                f'NOTION_TOKEN = {NOTION_TOKEN}\nNOTION_ROOT_PAGE_ID = {NOTION_ROOT_PAGE_ID}'
            )
        os.chdir(self.path_to_repo)
        git_commands = [
            f'gh secret set NOTION_TOKEN -b"{NOTION_USER_ID}"',
            f'gh secret set NOTION_TOKEN -b"{NOTION_TOKEN}"',
            f'gh secret set NOTION_ROOT_PAGE_ID -b"{NOTION_ROOT_PAGE_ID}"',
        ]

        for command in git_commands:
            self._execute(command)

    def finalize(self):
        git_commands = [
            'git add .',
            'git commit -m "first commit"',
            'git branch -M main',
            'git push -u origin main',
            'git checkout -b gh-pages',
            'git push -u origin gh-pages',
        ]
        for command in git_commands:
            self._execute(command)

        self._set_notion_token()
        self._execute('git push --set-upstream origin main')

        os.chdir('..')

    def _edit_js(self, file, target, code):
        if not isinstance(target, list):
            target = [target]
        if not isinstance(code, list):
            code = [code]

        with open(file, 'r') as f:
            lines = f.readlines()

        idx = 0
        with open(file, 'w') as f:
            for line in lines:
                if len(target) - idx > 0:
                    if line.startswith(target[idx]):
                        line = target[idx] + f'`{code[idx]}`,\n'
                        idx += 1
                f.write(line)

    def set_analytics_code(self, code):
        """
        Thin wrapper for analytics code
        """
        file = 'gatsby-config.js'
        target = '        trackingId: '
        self._edit_js(file, target, code)

    def set_adsense_code(self, code):
        """
        Thin wrapper for adsense code
        """
        file = 'gatsby-config.js'
        target = '        publisherId: '
        self._edit_js(file, target, code)

    def copy_param2config(self, param):
        file = 'gatsby-config.js'

        target = [
            '    title: ',
            '    description: ',
            '    author: ',
            '    siteUrl: ',
            '  pathPrefix: ',
        ]

        code = [
            param['blog_title'],
            param['description'],
            param['author'],
            param['siteUrl'],
            param['blog_title'],
        ]

        self._edit_js(file, target, code)

    def update_blog(self):
        repository_name = self.param['blog_title']
        template_repo = self.param['template_repo']

        os.chdir(os.path.join(self.param['target_dir'], repository_name))

        git_commands = [
            'git remote remove origin',
            f'git remote add origin {template_repo}',
            'git pull origin main',
            'git remote remove origin',
            f'git remote add origin https://github.com/{self.username}/{repository_name}.git',
            'git push --set-upstream origin main',
        ]
        for command in git_commands:
            self._execute(command)
