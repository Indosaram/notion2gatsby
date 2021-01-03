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
                ' Warning : No target directory is specified.'
                + 'Creating new repo in the current directory.'
            )

        if not os.path.exists(param['target_dir']):
            os.mkdir(param['target_dir'])

    def _get_github_username(self):
        self.username = self._execute('git config --global user.name').replace(
            '\n', ''
        )

    def _execute(self, command, shell=False):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=shell)
        stdout = process.communicate()[0]
        result = stdout.decode('cp949')

        return result

    def create_blog(self):
        repository_name = self.param['blog_title']
        target_dir = self.param['target_dir']

        path_to_repo = os.path.join(target_dir, repository_name)
        self.repository_name = repository_name

        if os.path.exists(path_to_repo):
            print('Error : This repository name already exists!')
            return

        self.target_dir = target_dir

        print(path_to_repo)
        os.mkdir(path_to_repo)
        os.chdir(path_to_repo)

        self._execute('echo "# github_page_test" >> README.md', shell=True)
        git_commands = [
            f'gh repo create -y --public {repository_name}',
            'git init',
            'git add README.md',
            'git commit -m "first commit"',
            f'git remote add origin https://github.com/{self.username}/{repository_name}.git',
            'git push -u origin master',
        ]
        for command in git_commands:
            print(command)
            self._execute(command)

        os.chdir('..')

    def initiate(self):
        self._execute("git checkout -b gh-pages")
        self._execute("git push --set-upstream origin gh-pages")
        self._set_notion_token()

    def _set_notion_token(self):
        NOTION_TOKEN = self.param['notion_token']
        NOTION_ROOT_PAGE_ID = self.param['notion_root_page_id']

        # XXX: For local run
        with open('.env', 'r+') as f:
            f.write(
                f'NOTION_TOKEN = {NOTION_TOKEN}\nNOTION_ROOT_PAGE_ID = {NOTION_ROOT_PAGE_ID}'
            )

        git_commands = [
            f'git remote add origin https://github.com/{self.username}/{self.repository_name}',
            f'gh secret set NOTION_TOKEN -b"{NOTION_TOKEN}"',
            f'gh secret set NOTION_ROOT_PAGE_ID -b"{NOTION_ROOT_PAGE_ID}"',
        ]

        for command in git_commands:
            print(command)
            self._execute(command)
