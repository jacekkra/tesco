import os
import shutil
import sqlite3
import tempfile

from dotenv import load_dotenv


def load_cookies():
    load_dotenv()
    firefox_profile_dir = os.path.expanduser(os.getenv("FIREFOX_PROFILE_DIR"))
    cookies_url = os.path.join(firefox_profile_dir, "cookies.sqlite")

    dictionary = {}

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = shutil.copy(cookies_url, temp_dir)

        con = sqlite3.connect(temp_file)
        cur = con.cursor()
        cur.execute(
            "SELECT name, value FROM moz_cookies WHERE host LIKE '%tesco.pl'"
        )
        for item in cur.fetchall():
            dictionary[item[0]] = item[1]

    return dictionary
