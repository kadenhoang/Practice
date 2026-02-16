"""
PSEUDOCODE (Auth):
  load_users: Read users file, return dict username -> password_hash (or empty)
  save_user: Append user line (tab-separated: username, hash, first, last, phone, dob, country, zip, address)
  login: Load users, if username exists and hash matches password return True else False
  create_account: If username taken return False; else save_user with all info, return True
"""
import hashlib

USERS_FILE = "users.txt"
_SEP = "\t"
_NUM_FIELDS = 9  # username, hash, first_name, last_name, phone, dob, country, zipcode, address


def _hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def _sanitize(s):
    """Replace tab and newline so one line per user is safe."""
    if s is None:
        return ""
    return str(s).strip().replace("\t", " ").replace("\r", " ").replace("\n", " ")


def load_users():
    """Return dict of username -> password_hash. Supports old 'user:hash' and new tab-separated lines."""
    users = {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if _SEP in line:
                    parts = line.split(_SEP, _NUM_FIELDS - 1)
                    if len(parts) >= 2:
                        users[parts[0].strip()] = parts[1].strip()
                elif ":" in line:
                    username, stored_hash = line.split(":", 1)
                    users[username.strip()] = stored_hash.strip()
    except FileNotFoundError:
        pass
    return users


def save_user(username, password_hash, first_name="", last_name="", phone="", date_of_birth="", country="", zipcode="", address=""):
    """Append one user line. Tab-separated: username, hash, first_name, last_name, phone, dob, country, zipcode, address."""
    parts = [
        _sanitize(username),
        password_hash,
        _sanitize(first_name),
        _sanitize(last_name),
        _sanitize(phone),
        _sanitize(date_of_birth),
        _sanitize(country),
        _sanitize(zipcode),
        _sanitize(address),
    ]
    with open(USERS_FILE, "a", encoding="utf-8") as f:
        f.write(_SEP.join(parts) + "\n")


def login(username, password):
    """Return True if username exists and password matches."""
    users = load_users()
    if username not in users:
        return False
    return users[username] == _hash_password(password)


def create_account(username, password, first_name="", last_name="", phone="", date_of_birth="", country="", zipcode="", address=""):
    """Return True if account was created; False if username already exists. Stores all user info in user file."""
    username = _sanitize(username)
    if not username:
        return False
    users = load_users()
    if username in users:
        return False
    save_user(
        username,
        _hash_password(password),
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        date_of_birth=date_of_birth,
        country=country,
        zipcode=zipcode,
        address=address,
    )
    return True


def require_auth():
    """
    Show login/create-account page (CLI). Return only after user has logged in
    or created an account successfully.
    """
    from ui import (
        title,
        section,
        prompt,
        prompt_password,
        success,
        error,
        info,
        menu,
        welcome_banner,
    )
    welcome_banner("Student & Teacher Info")

    while True:
        title("Sign in or create an account")
        choice = menu(
            ["I already have an account (Log in)", "Create a new account"],
            title_text="What would you like to do",
            hint="Enter 1 to log in, or 2 to create an account.",
        )

        if choice == "1":
            section("Log in")
            username = prompt("Username: ")
            password = prompt_password("Password: ")
            if not username:
                error("Username cannot be empty. Please try again.")
                continue
            if login(username, password):
                success(f"Welcome back, {username}!")
                return
            error("Invalid username or password. Please try again.")

        elif choice == "2":
            section("Create a new account")
            username = prompt("Choose a username: ")
            password = prompt_password("Choose a password: ")
            if not username:
                error("Username cannot be empty. Please try again.")
                continue
            if not password:
                error("Password cannot be empty. Please try again.")
                continue
            if create_account(username, password):
                success(f"Account created. Welcome, {username}!")
                return
            error("That username is already taken. Please choose another.")

        else:
            error("Please enter 1 or 2.")
