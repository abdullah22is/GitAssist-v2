"""Rule-based fallback intent parser for common Git commands."""


def _contains_phrase(text: str, phrases) -> bool:
    return any(p in text for p in phrases)


def _has_negative_intent(text: str, phrases) -> bool:
    negative = (
        "don't", "do not", "dont", "no ", "never", "لا ", "لا تعمل", "لا تسوي",
        "لا تنفذ", "عدم", "ليس", "مو "
    )
    return _contains_phrase(text, negative) and _contains_phrase(text, phrases)


def rule_based_intent(text: str, repo_state: str = ""):
    """Convert common natural-language requests into complete Git commands.

    Ambiguous/destructive requests are deliberately returned as ``None`` so
    the interactive workflow can ask for the missing information. The final
    executor still performs the authoritative security check for every result.
    """
    text_lower = text.lower().strip()

    if _contains_phrase(text_lower, ["انشاء مستودع", "إنشاء مستودع", "مستودع جديد", "init repo", "create repo", "git init"]):
        return "git init"

    if _contains_phrase(text_lower, ["عرض الحالة", "الحالة", "status", "show status"]):
        return "git status"

    # Staging is the only safe, complete interpretation when the user asks
    # generally to save changes but supplies no commit message.
    if _contains_phrase(text_lower, ["حفظ التغييرات", "احفظ", "stage changes", "staging", "git add"]):
        if _has_negative_intent(text_lower, ["حفظ التغييرات", "احفظ", "stage changes", "staging"]):
            return None
        return "git add ."

    if _contains_phrase(text_lower, ["السجل", "تاريخ", "log", "history"]):
        return "git log --oneline --graph --decorate --all"

    if _contains_phrase(text_lower, ["رفع", "push", "ارفع"]):
        if _has_negative_intent(text_lower, ["push", "رفع", "ارفع"]):
            return None
        return "git push"

    if _contains_phrase(text_lower, ["سحب", "pull", "اسحب"]):
        if _has_negative_intent(text_lower, ["pull", "سحب", "اسحب"]):
            return None
        return "git pull"

    if _contains_phrase(text_lower, [
        "انشاء فرع", "إنشاء فرع", "فرع جديد", "create branch", "new branch",
        "استنساخ", "clone", "نسخ مستودع", "حذف فرع", "delete branch", "remove branch",
        "دمج فرع", "merge branch", "ادمج", "إضافة ملف", "اضف ملف", "add file", "stage file",
    ]):
        return None

    # Never translate "revert/undo" into checkout -- ., because that silently
    # discards working-tree changes and is not semantically a Git revert.
    if _contains_phrase(text_lower, ["استرجاع", "تراجع", "undo", "revert"]):
        return None

    # A bare "commit" needs a message; the interactive commit workflow asks
    # for it instead of silently staging or inventing a message.
    if _contains_phrase(text_lower, ["commit", "اعمل commit", "سوي commit", "التزام"]):
        return None

    return None
