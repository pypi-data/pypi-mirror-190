from volworld_common.util.id_util import new_rand_test_user_name
from volworld_aws_api_common.test.aws.request.post__signup import act__signup
from volworld_aws_api_common.test.aws.request.post__login import act__login
from volworld_aws_api_common.api.AA import AA


class UserInfo:
    def __init__(self, name: str):
        self.name = name
        self.used_name = f"{new_rand_test_user_name()}xxxxxx{self.name}"
        self.password = None
        self.user_id = None
        self.token = None
        self.login_info = None

    def signup(self):
        login = act__signup(self.used_name)
        assert login[AA.Name] == self.used_name
        self.password = login[AA.Password]
        self.user_id = login[AA.UserId]

    def login(self):
        self.login_info = act__login(self.used_name, self.password)
        self.token = self.login_info[AA.Token]
        return self.login_info


class UserPool:
    def __init__(self):
        self.users = dict()

    def get_user(self, name: str):
        if name not in self.users:
            return None

        return self.users[name]

    def add_user(self, name: str) -> UserInfo:
        self.users[name] = UserInfo(name)
        return self.users[name]

    def add_signup_user(self, name: str) -> UserInfo:
        inf = UserInfo(name)
        self.users[name] = inf
        inf.signup()
        return inf

    def login(self, context, name):
        user = self.users[name]
        assert user is not None
        if hasattr(context, 'curr_login_user'):
            if context.curr_login_user == user:
                return
        curr_login_name = 'None'
        if hasattr(context, 'curr_login'):
            curr_login_name = context.curr_login_user.name

        print(f"Need to login [{name}], current login is [{curr_login_name}]")
        user.login()
        context.curr_login_user = user
        context.curr_login = user.login_info
