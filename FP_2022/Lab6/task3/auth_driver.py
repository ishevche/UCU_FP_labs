import auth

# Set up a test user and permission
auth.authenticator.add_user("joe", "joejoe")
auth.authorizor.add_permission("permit user")
auth.authorizor.add_permission("add permissions")
auth.authorizor.permit_user("permit user", "joe")
auth.authorizor.permit_user("add permissions", "joe")


class Editor:
    def __init__(self):
        self.username = None
        self.menu_map = {
            "login": self.login,
            "register": self.register,
            "test": self.test,
            "change": self.change,
            "permit user": self.permit_user,
            "add permissions": self.add_permissions,
            "quit": self.quit,
        }

    def login(self):
        logged_in = False
        while not logged_in:
            username = input("username: ")
            password = input("password: ")
            try:
                logged_in = auth.authenticator.login(username, password)
            except auth.InvalidUsername:
                print("Sorry, that username does not exist")
            except auth.InvalidPassword:
                print("Sorry, incorrect password")
            else:
                self.username = username

    def register(self):
        got_info = False
        while not got_info:
            username = input("username: ")
            password = input("password: ")
            password_repeat = input("repeat your password: ")
            if password != password_repeat:
                continue
            try:
                auth.authenticator.add_user(username, password)
                self.username = username
                got_info = True
            except auth.UsernameAlreadyExists:
                print("This username already exists")
            except auth.PasswordTooShort:
                print("Your password too short")

    def is_permitted(self, permission):
        try:
            auth.authorizor.check_permission(permission, self.username)
        except auth.NotLoggedInError as e:
            print("{} is not logged in".format(e.username))
            return False
        except auth.NotPermittedError as e:
            print("{} cannot {}".format(e.username, permission))
            return False
        else:
            return True

    def test(self):
        if self.is_permitted("test program"):
            print("Testing program now...")

    def change(self):
        if self.is_permitted("change program"):
            print("Changing program now...")

    def permit_user(self):
        got_info = False
        while not got_info:
            username = input("username: ")
            permission = input("permission name: ")
            if self.is_permitted("permit user"):
                try:
                    auth.authorizor.permit_user(permission, username)
                    got_info = True
                except auth.PermissionError:
                    print("Permission does not exist")
                except auth.InvalidUsername as e:
                    print(f"No such user {e.username}")

    def add_permissions(self):
        got_info = False
        while not got_info:
            permission = input("permission name: ")
            if self.is_permitted("add permissions"):
                try:
                    auth.authorizor.add_permission(permission)
                    got_info = True
                except auth.PermissionError:
                    print("Permission Exists")

    def quit(self):
        raise SystemExit()

    def menu(self):
        try:
            answer = ""
            while True:
                print(
                    """
Please enter a command:
\tlogin\t\t\t\tLogin
\tregister\t\t\tRegister
\ttest\t\t\t\tTest the program
\tchange\t\t\t\tChange the program
\tpermit user\t\t\tGrand permission to a user
\tadd permissions\t\tMake new permission
\tquit\t\t\t\tQuit
"""
                )
                answer = input("enter a command: ").lower()
                try:
                    func = self.menu_map[answer]
                except KeyError:
                    print("{} is not a valid option".format(answer))
                else:
                    func()
        finally:
            print("Thank you for testing the auth module")


Editor().menu()
