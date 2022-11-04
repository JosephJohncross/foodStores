from datetime import datetime
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        if user.last_login is None:
             login_timestamp = '' 
        else:
            user_l = tuple_to_list(user.last_login)
            user_l[0] = datetime.now(tz=None)
            login_timestamp = user.last_login[0]
            user.last_login = tuple(user_l)
        return str(user.pk) + user.password + str(login_timestamp) + str(timestamp)
    
account_activation_token = AccountActivationTokenGenerator()

def tuple_to_list(t):
    return [*t]