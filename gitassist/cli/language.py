"""Language selection."""

from gitassist.config import settings
from gitassist.cli.output import print_title

def choose_language():
    print_title("Language / اللغة")
    print("1. English")
    print("2. العربية")
    choice = input("Enter choice / أدخل الاختيار: ").strip()
    if choice == "2":
        settings.LANGUAGE = "ar"
    else:
        settings.LANGUAGE = "en"
    return settings.LANGUAGE