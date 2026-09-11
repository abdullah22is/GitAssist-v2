"""Text strings for GitAssist (English and Arabic)."""

from gitassist.config import settings

TEXTS = {
    # عام
    "welcome": {"en": "Welcome to GitAssist!", "ar": "مرحبًا بك في GitAssist!"},
    "menu_prompt": {"en": "What would you like to do?", "ar": "ماذا تريد أن تفعل؟"},
    "exit_message": {"en": "Goodbye!", "ar": "وداعًا!"},
    "not_implemented": {"en": "This feature is not implemented yet.", "ar": "هذه الميزة غير منفذة بعد."},
    "help_text": {"en": "Use menu numbers to select actions, 'm' for manual command, 'h' for help, 'q' to quit.", "ar": "استخدم أرقام القائمة للاختيار، 'm' لأمر يدوي، 'h' للمساعدة، 'q' للخروج."},
    "git_installed": {"en": "Git: Installed", "ar": "Git: مثبت"},
    "git_not_installed": {"en": "Git is not installed or not in PATH.", "ar": "Git غير مثبت أو ليس في PATH."},
    "repo_detected": {"en": "Repository: Detected", "ar": "المستودع: موجود"},
    "repo_not_detected": {"en": "Repository: Not detected (not inside a Git repo)", "ar": "المستودع: غير موجود (لست داخل مستودع Git)"},
    "current_branch": {"en": "Current branch: {branch}", "ar": "الفرع الحالي: {branch}"},
    "no_branch": {"en": "Current branch: (no branch)", "ar": "الفرع الحالي: (بدون فرع)"},
    "uncommitted_changes_yes": {"en": "Uncommitted changes: Yes", "ar": "تغييرات غير محفوظة: نعم"},
    "uncommitted_changes_no": {"en": "Uncommitted changes: No", "ar": "تغييرات غير محفوظة: لا"},
    "remote_configured": {"en": "Remote: {remote}", "ar": "المستودع البعيد: {remote}"},
    "remote_not_configured": {"en": "Remote: Not configured", "ar": "المستودع البعيد: غير مضبوط"},
    "ready_message": {"en": "GitAssist is ready. Menu coming in next stage.", "ar": "GitAssist جاهز. القائمة قادمة في المرحلة التالية."},
    "invalid_choice": {"en": "Invalid choice.", "ar": "اختيار غير صالح."},
    "please_enter_number": {"en": "Please enter a number.", "ar": "يرجى إدخال رقم."},
    "input_empty": {"en": "Input cannot be empty.", "ar": "الإدخال لا يمكن أن يكون فارغًا."},

    # القوائم
    "main_menu_title": {"en": "Main Menu", "ar": "القائمة الرئيسية"},
    "create_new_project": {"en": "Create new Git project", "ar": "إنشاء مشروع Git جديد"},
    "open_existing_project": {"en": "Open existing project", "ar": "فتح مشروع موجود"},
    "clone_repository": {"en": "Clone repository", "ar": "استنساخ مستودع"},
    "show_status": {"en": "Show status", "ar": "عرض الحالة"},
    "save_changes": {"en": "Save changes (add/commit)", "ar": "حفظ التغييرات (add/commit)"},
    "view_history": {"en": "View commit history", "ar": "عرض سجل الالتزامات"},
    "manage_branches": {"en": "Manage branches", "ar": "إدارة الفروع"},
    "stash_changes": {"en": "Stash changes", "ar": "حفظ مؤقت (stash)"},
    "manage_files": {"en": "Manage files", "ar": "إدارة الملفات"},
    "synchronize": {"en": "Synchronize with remote", "ar": "مزامنة مع البعيد"},
    "github_info": {"en": "GitHub / Remote Info", "ar": "معلومات GitHub / البعيد"},
    "manual_command": {"en": "Enter a Git command manually", "ar": "إدخال أمر Git يدويًا"},
    "voice_command": {"en": "Voice command", "ar": "أمر صوتي"},
    "exit": {"en": "Exit", "ar": "خروج"},
    "back_to_main": {"en": "Back to main menu", "ar": "العودة إلى القائمة الرئيسية"},

    # سيناريوهات
    "project_name_prompt": {"en": "Project name (repository name):", "ar": "اسم المشروع (اسم المستودع):"},
    "location_prompt": {"en": "Location (leave empty for current directory):", "ar": "الموقع (اتركه فارغًا للمجلد الحالي):"},
    "path_exists_error": {"en": "Path '{path}' already exists.", "ar": "المسار '{path}' موجود بالفعل."},
    "initialize_repo": {"en": "Initializing Git repository...", "ar": "تهيئة مستودع Git..."},
    "repo_initialized": {"en": "Git repository initialized.", "ar": "تم تهيئة مستودع Git."},
    "create_readme_prompt": {"en": "Create README.md?", "ar": "هل تريد إنشاء README.md؟"},
    "add_remote_prompt": {"en": "Add remote repository now?", "ar": "هل تريد إضافة مستودع بعيد الآن؟"},
    "remote_url_prompt": {"en": "Remote URL:", "ar": "رابط المستودع البعيد:"},
    "remote_added": {"en": "Remote 'origin' added.", "ar": "تمت إضافة المستودع البعيد 'origin'."},
    "project_path_prompt": {"en": "Project path:", "ar": "مسار المشروع:"},
    "not_git_repo_error": {"en": "Not a Git repository.", "ar": "ليس مستودع Git."},
    "opened_project": {"en": "Opened: {path}", "ar": "تم الفتح: {path}"},
    "clone_url_prompt": {"en": "Repository URL:", "ar": "رابط المستودع:"},
    "clone_dest_prompt": {"en": "Destination folder (leave empty for default):", "ar": "المجلد الوجهة (اتركه فارغًا للافتراضي):"},
    "clone_completed": {"en": "Clone completed.", "ar": "اكتمل الاستنساخ."},
    "open_cloned_prompt": {"en": "Open cloned repository now?", "ar": "هل تريد فتح المستودع المستنسخ الآن؟"},

    # المزامنة
    "fetch_completed": {"en": "Fetch completed.", "ar": "اكتمل الجلب."},
    "pull_completed": {"en": "Pull completed.", "ar": "اكتمل السحب."},
    "push_completed": {"en": "Push completed.", "ar": "اكتمل الرفع."},
    "check_updates": {"en": "Check remote updates", "ar": "فحص تحديثات البعيد"},
    "behind_remote": {"en": "You are behind the remote branch. Consider pulling changes.", "ar": "أنت متأخر عن الفرع البعيد. يُنصح بسحب التغييرات."},
    "up_to_date": {"en": "Your branch is up to date with remote.", "ar": "فرعك محدث بالنسبة للبعيد."},

    # الفروع
    "branch_management": {"en": "Branch Management", "ar": "إدارة الفروع"},
    "list_branches": {"en": "List branches", "ar": "عرض الفروع"},
    "create_branch": {"en": "Create branch", "ar": "إنشاء فرع"},
    "switch_branch": {"en": "Switch branch", "ar": "التبديل إلى فرع"},
    "delete_branch": {"en": "Delete branch", "ar": "حذف فرع"},
    "merge_branch": {"en": "Merge branch", "ar": "دمج فرع"},
    "new_branch_name": {"en": "New branch name:", "ar": "اسم الفرع الجديد:"},
    "branch_created": {"en": "Branch '{name}' created.", "ar": "تم إنشاء الفرع '{name}'."},
    "branch_to_switch": {"en": "Branch name to switch to:", "ar": "اسم الفرع للتبديل إليه:"},
    "branch_switched": {"en": "Switched to '{name}'.", "ar": "تم التبديل إلى '{name}'."},
    "branch_to_delete": {"en": "Branch name to delete:", "ar": "اسم الفرع للحذف:"},
    "branch_deleted": {"en": "Branch '{name}' deleted.", "ar": "تم حذف الفرع '{name}'."},
    "branch_to_merge": {"en": "Branch name to merge into current:", "ar": "اسم الفرع لدمجه في الحالي:"},
    "confirm_force_delete": {"en": "Force delete (unmerged branches)?", "ar": "حذف قسري (فروع غير مدمجة)؟"},
    "confirm_merge": {"en": "Merge '{name}' into current branch? This may cause conflicts.", "ar": "دمج '{name}' في الفرع الحالي؟ قد يسبب تعارضات."},

    # Stash
    "stash_management": {"en": "Stash Management", "ar": "إدارة الحفظ المؤقت (stash)"},
    "stash_save": {"en": "Save changes (stash)", "ar": "حفظ التغييرات (stash)"},
    "stash_list": {"en": "List stashes", "ar": "عرض المحفوظات"},
    "stash_apply": {"en": "Apply stash", "ar": "تطبيق stash"},
    "stash_pop": {"en": "Pop stash", "ar": "استرجاع stash"},
    "stash_drop": {"en": "Drop stash", "ar": "حذف stash"},
    "stash_message_prompt": {"en": "Stash message (optional):", "ar": "رسالة stash (اختياري):"},
    "changes_stashed": {"en": "Changes stashed.", "ar": "تم حفظ التغييرات."},
    "confirm_drop_stash": {"en": "Drop latest stash?", "ar": "حذف آخر stash؟"},

    # الملفات
    "file_management": {"en": "File Management", "ar": "إدارة الملفات"},
    "create_file": {"en": "Create file", "ar": "إنشاء ملف"},
    "edit_file": {"en": "Edit file (append line)", "ar": "تعديل ملف (إضافة سطر)"},
    "delete_file": {"en": "Delete file", "ar": "حذف ملف"},
    "create_directory": {"en": "Create directory", "ar": "إنشاء مجلد"},
    "filename_prompt": {"en": "File name (e.g., notes.txt):", "ar": "اسم الملف (مثال: notes.txt):"},
    "file_exists_error": {"en": "File '{name}' already exists.", "ar": "الملف '{name}' موجود بالفعل."},
    "file_created": {"en": "File '{name}' created.", "ar": "تم إنشاء الملف '{name}'."},
    "file_to_edit": {"en": "File name to edit:", "ar": "اسم الملف للتعديل:"},
    "file_not_found": {"en": "File '{name}' does not exist.", "ar": "الملف '{name}' غير موجود."},
    "line_to_append": {"en": "Line to append:", "ar": "السطر للإضافة:"},
    "line_appended": {"en": "Line appended to '{name}'.", "ar": "تمت إضافة السطر إلى '{name}'."},
    "file_to_delete": {"en": "File name to delete:", "ar": "اسم الملف للحذف:"},
    "delete_confirm": {"en": "Are you sure you want to delete '{name}'?", "ar": "هل أنت متأكد من حذف '{name}'؟"},
    "file_deleted": {"en": "File '{name}' deleted.", "ar": "تم حذف الملف '{name}'."},
    "dirname_prompt": {"en": "Directory name:", "ar": "اسم المجلد:"},

    # GitHub
    "github_management": {"en": "GitHub / Remote Info", "ar": "معلومات GitHub / البعيد"},
    "show_remote_details": {"en": "Show remote details", "ar": "عرض تفاصيل البعيد"},
    "open_browser": {"en": "Open repository in browser", "ar": "فتح المستودع في المتصفح"},
    "create_github_repo": {"en": "Create GitHub repository", "ar": "إنشاء مستودع GitHub"},
    "github_token_prompt": {"en": "GitHub personal access token (input hidden):", "ar": "رمز الوصول الشخصي لـ GitHub (الإدخال مخفي):"},
    "github_repo_name_prompt": {"en": "Repository name:", "ar": "اسم المستودع:"},
    "github_private_prompt": {"en": "Private repository?", "ar": "مستودع خاص؟"},
    "github_repo_created": {"en": "Repository created: {url}", "ar": "تم إنشاء المستودع: {url}"},
    "github_failed": {"en": "Failed to create repository. Check token and permissions.", "ar": "فشل إنشاء المستودع. تحقق من الرمز والصلاحيات."},

    # الأوامر اليدوية
    "manual_mode_title": {"en": "Manual Command Mode", "ar": "وضع الأوامر اليدوية"},
    "enter_git_command": {"en": "Enter a Git command (e.g., 'git status'):", "ar": "أدخل أمر Git (مثال: 'git status'):"},
    "invalid_command": {"en": "Invalid command. Must start with 'git'.", "ar": "أمر غير صالح. يجب أن يبدأ بـ 'git'."},
    "invalid_shell_syntax": {"en": "This looks like shell syntax (e.g. ; && | > <), not a single Git command. Please enter one Git command at a time.", "ar": "يبدو هذا كصياغة أوامر نظام (مثل ; && | > <) وليس أمر Git واحد. الرجاء إدخال أمر Git واحد في كل مرة."},
    "invalid_quoting": {"en": "This command has unmatched quotes and could not be parsed.", "ar": "يحتوي هذا الأمر على علامات اقتباس غير متطابقة ولم يمكن تحليله."},
    "typo_detected": {"en": "Possible typo detected.", "ar": "احتمال وجود خطأ إملائي."},
    "you_entered": {"en": "You entered: {command}", "ar": "أدخلت: {command}"},
    "did_you_mean": {"en": "Did you mean: {suggestion}", "ar": "هل كنت تقصد: {suggestion}"},
    "execute_corrected": {"en": "Execute corrected command?", "ar": "تنفيذ الأمر المصحح؟"},

    # الذكاء الاصطناعي
    "interpreting": {"en": "Interpreting...", "ar": "جارٍ التفسير..."},
    "ai_suggestion": {"en": "AI suggests: {command}", "ar": "يقترح الذكاء الاصطناعي: {command}"},
    "execute_suggested": {"en": "Execute suggested command?", "ar": "تنفيذ الأمر المقترح؟"},
    "ai_failed": {"en": "AI could not generate a Git command. Try a different phrase or check AI configuration.", "ar": "تعذر على الذكاء الاصطناعي توليد أمر Git. جرب صياغة مختلفة أو تحقق من إعدادات AI."},

    # الصوت
    "voice_unavailable": {"en": "Speech recognition libraries are not installed.", "ar": "مكتبات التعرف على الصوت غير مثبتة."},
    "voice_install_hint": {"en": "Install SpeechRecognition, sounddevice, and numpy to use voice commands.", "ar": "ثبّت SpeechRecognition و sounddevice و numpy لاستخدام الأوامر الصوتية."},
    "voice_listening": {"en": "Listening...", "ar": "جارٍ الاستماع..."},
    "voice_processing": {"en": "Processing speech...", "ar": "جارٍ معالجة الصوت..."},
    "voice_not_understood": {"en": "Could not understand audio.", "ar": "تعذر فهم الصوت."},
    "voice_heard": {"en": "Heard: {text}", "ar": "تم السماع: {text}"},
    "voice_libs_missing": {"en": "SpeechRecognition or sounddevice is missing.", "ar": "مكتبة SpeechRecognition أو sounddevice مفقودة."},

    # Security
    "risk_level": {"en": "Risk level: {level}", "ar": "مستوى الخطورة: {level}"},
    "safer_alternative": {"en": "Safer alternative: {alternative}", "ar": "البديل الأكثر أمانًا: {alternative}"},
    "confirm_continue": {"en": "Do you want to continue? (y/n)", "ar": "هل تريد المتابعة؟ (y/n)"},
    "command_cancelled": {"en": "Command cancelled.", "ar": "تم إلغاء الأمر."},
    "command_failed": {"en": "Command failed: {command}", "ar": "فشل الأمر: {command}"},
    "unexpected_error": {"en": "Unexpected error: {error}", "ar": "خطأ غير متوقع: {error}"},
    "dry_run_message": {"en": "Dry-run mode: would execute: {command}", "ar": "وضع المحاكاة: سيتم تنفيذ: {command}"},

    # Context warnings
    "warning_not_git_repo": {"en": "You are not inside a Git repository.", "ar": "أنت لست داخل مستودع Git."},
    "suggestion_init_or_clone": {"en": "Use 'git init' to create a new repository or 'git clone' to get one.", "ar": "استخدم 'git init' لإنشاء مستودع جديد أو 'git clone' لاستنساخ واحد."},
    "warning_uncommitted_changes": {"en": "You have uncommitted changes that may be overwritten.", "ar": "لديك تغييرات غير محفوظة قد تُستبدل."},
    "suggestion_commit_or_stash": {"en": "Commit or stash your changes first.", "ar": "قم بحفظ التغييرات (commit) أو تخزينها (stash) أولاً."},
    "warning_no_remote": {"en": "No remote repository is configured.", "ar": "لا يوجد مستودع بعيد مكوّن."},
    "suggestion_add_remote": {"en": "Add a remote with 'git remote add origin <url>'.", "ar": "أضف مستودعًا بعيدًا باستخدام 'git remote add origin <url>'."},

    # Error explanations
    "error_not_git_repo": {"en": "You are not inside a Git repository.", "ar": "أنت لست داخل مستودع Git."},
    "error_remote_exists": {"en": "A remote named 'origin' is already configured for this repository.", "ar": "يوجد مستودع بعيد باسم 'origin' مكوّن مسبقًا."},
    "error_push_rejected": {"en": "The remote contains commits that you do not have locally.", "ar": "يحتوي المستودع البعيد على التزامات غير موجودة محليًا."},
    "error_merge_conflict": {"en": "Merge conflict detected in file contents.", "ar": "تم اكتشاف تعارض دمج في محتوى الملفات."},
    "error_local_changes_overwritten": {"en": "You have local modifications that would be lost if you merge or pull.", "ar": "لديك تعديلات محلية ستفقد إذا قمت بالدمج أو السحب."},
    "error_auth_failed": {"en": "Authentication failed or insufficient permissions for the remote repository.", "ar": "فشلت المصادقة أو الصلاحيات غير كافية للمستودع البعيد."},
    "error_not_found": {"en": "The remote repository was not found.", "ar": "لم يتم العثور على المستودع البعيد."},
    "error_unrelated_histories": {"en": "You are trying to merge two branches with unrelated histories.", "ar": "أنت تحاول دمج فرعين لهما تاريخ غير مرتبط."},
    "error_pathspec": {"en": "The specified file or path does not exist in the repository.", "ar": "الملف أو المسار المحدد غير موجود في المستودع."},
    "error_username": {"en": "Git is asking for credentials but no interactive prompt is available.", "ar": "يطلب Git بيانات الاعتماد ولكن لا يوجد موجه تفاعلي متاح."},

    # Error suggestions (used dynamically by errors/analyzer.py)
    "suggestion_remote_set_url": {"en": "Use 'git remote set-url origin <url>' to change it, or 'git remote remove origin' first.", "ar": "استخدم 'git remote set-url origin <url>' لتغييره، أو 'git remote remove origin' أولاً."},
    "suggestion_pull_first": {"en": "Pull the latest changes first with 'git pull', then try pushing again.", "ar": "اسحب آخر التغييرات أولاً باستخدام 'git pull'، ثم حاول الرفع مرة أخرى."},
    "suggestion_resolve_conflicts": {"en": "Open the conflicted files, resolve the markers, then 'git add' and 'git commit'.", "ar": "افتح الملفات المتعارضة وقم بحل العلامات، ثم استخدم 'git add' و'git commit'."},
    "suggestion_check_credentials": {"en": "Check your GitHub token or credentials and repository permissions.", "ar": "تحقق من رمز GitHub أو بيانات الاعتماد وصلاحيات المستودع."},
    "suggestion_verify_url": {"en": "Verify the repository URL is correct and that you have access to it.", "ar": "تحقق من صحة رابط المستودع وأن لديك صلاحية الوصول إليه."},
    "suggestion_allow_unrelated": {"en": "If intentional, use 'git merge --allow-unrelated-histories'.", "ar": "إذا كان ذلك مقصودًا، استخدم 'git merge --allow-unrelated-histories'."},
    "suggestion_check_path": {"en": "Check the file name or path for typos.", "ar": "تحقق من اسم الملف أو المسار من وجود أخطاء إملائية."},
    "suggestion_credential_manager": {"en": "Configure a Git credential helper: 'git config --global credential.helper store' (or 'manager' on Windows).", "ar": "قم بإعداد مدير بيانات اعتماد Git: 'git config --global credential.helper store' (أو 'manager' على Windows)."},

    # Risk warnings & safer alternatives (used dynamically by security/analyzer.py)
    "warning_add_generic": {"en": "This stages changes in the Git index and changes repository state.", "ar": "سيؤدي هذا إلى تجهيز التغييرات في فهرس Git وتغيير حالة المستودع."},
    "warning_commit_generic": {"en": "This creates a new commit and changes repository history.", "ar": "سيؤدي هذا إلى إنشاء التزام جديد وتغيير تاريخ المستودع."},
    "warning_fetch_generic": {"en": "This contacts the configured remote and updates remote-tracking references.", "ar": "سيتصل هذا بالمستودع البعيد ويحدّث مراجع الفروع البعيدة."},
    "warning_clone_generic": {"en": "This creates a local copy of a repository and may access the network.", "ar": "سيُنشئ هذا نسخة محلية من مستودع وقد يتصل بالشبكة."},
    "warning_init_generic": {"en": "This creates Git metadata in the selected directory.", "ar": "سيُنشئ هذا بيانات Git الوصفية في المجلد المحدد."},
    "warning_branch_generic": {"en": "This may create, rename, or otherwise change local branch state.", "ar": "قد يؤدي هذا إلى إنشاء فرع محلي أو إعادة تسميته أو تغيير حالته."},
    "warning_tag_generic": {"en": "This may create or change Git tags.", "ar": "قد يؤدي هذا إلى إنشاء وسوم Git أو تغييرها."},
    "warning_stash_generic": {"en": "This changes the stash and may move working-tree changes between the stash and your files.", "ar": "سيغيّر هذا الـstash وقد ينقل تغييرات مجلد العمل بين الـstash والملفات."},
    "warning_remote_generic": {"en": "This changes remote configuration for the repository.", "ar": "سيغيّر هذا إعدادات المستودع البعيد للمستودع الحالي."},
    "warning_reset_hard": {"en": "This will permanently discard all uncommitted changes and reset history. This cannot be undone.", "ar": "سيؤدي هذا إلى حذف جميع التغييرات غير المحفوظة وإعادة ضبط التاريخ نهائيًا. لا يمكن التراجع عن هذا."},
    "alternative_reset_hard": {"en": "Consider 'git stash' to save your changes first, or 'git reset --soft' to keep them staged.", "ar": "فكّر في استخدام 'git stash' لحفظ تغييراتك أولاً، أو 'git reset --soft' للاحتفاظ بها في منطقة التحضير."},
    "warning_force_push": {"en": "Force push overwrites remote history and can permanently delete others' commits.", "ar": "الرفع القسري (force push) يستبدل تاريخ المستودع البعيد وقد يحذف التزامات الآخرين نهائيًا."},
    "alternative_force_push": {"en": "Consider 'git push --force-with-lease' which is safer, or coordinate with your team first.", "ar": "فكّر في استخدام 'git push --force-with-lease' الأكثر أمانًا، أو تنسّق مع فريقك أولاً."},
    "warning_clean_fd": {"en": "This will permanently delete all untracked files and directories. This cannot be undone.", "ar": "سيؤدي هذا إلى حذف جميع الملفات والمجلدات غير المتتبعة نهائيًا. لا يمكن التراجع عن هذا."},
    "alternative_clean_fd": {"en": "Run 'git clean -nfd' first to preview what will be deleted.", "ar": "شغّل 'git clean -nfd' أولاً لمعاينة ما سيتم حذفه."},
    "warning_checkout_discard": {"en": "This will permanently discard all uncommitted changes in the working directory.", "ar": "سيؤدي هذا إلى حذف جميع التغييرات غير المحفوظة في مجلد العمل نهائيًا."},
    "alternative_checkout_discard": {"en": "Consider 'git stash' if you might need these changes later.", "ar": "فكّر في استخدام 'git stash' إذا كنت قد تحتاج هذه التغييرات لاحقًا."},
    "warning_rebase_i": {"en": "Interactive rebase rewrites commit history. Avoid this on commits already pushed to a shared branch.", "ar": "إعادة الترتيب التفاعلي (rebase -i) يعيد كتابة تاريخ الالتزامات. تجنّب هذا على التزامات تم رفعها بالفعل إلى فرع مشترك."},
    "alternative_rebase_i": {"en": "If commits are already shared, consider 'git revert' instead.", "ar": "إذا كانت الالتزامات مشتركة بالفعل، فكّر في استخدام 'git revert' بدلاً من ذلك."},
    "warning_branch_D": {"en": "Force-deleting a branch discards any unmerged commits on it permanently.", "ar": "الحذف القسري للفرع يتخلص من أي التزامات غير مدموجة عليه نهائيًا."},
    "alternative_branch_D": {"en": "Use 'git branch -d' (safe delete) if the branch has already been merged.", "ar": "استخدم 'git branch -d' (حذف آمن) إذا كان الفرع قد تم دمجه بالفعل."},
    "warning_merge": {"en": "Merging may introduce conflicts that need manual resolution.", "ar": "قد يؤدي الدمج إلى ظهور تعارضات تحتاج إلى حل يدوي."},
    "alternative_merge": {"en": "Make sure your work is committed or stashed before merging.", "ar": "تأكد من أن عملك محفوظ (commit) أو مخزَّن مؤقتًا (stash) قبل الدمج."},
    "warning_stash_drop": {"en": "Dropping a stash permanently deletes it. It cannot be recovered easily.", "ar": "حذف الـ stash يزيله نهائيًا. لا يمكن استرجاعه بسهولة."},
    "alternative_stash_drop": {"en": "Use 'git stash apply' first to confirm you no longer need these changes.", "ar": "استخدم 'git stash apply' أولاً للتأكد من أنك لم تعد بحاجة لهذه التغييرات."},

    # Command descriptions & progress messages (core/commands.py)
    "commit_message_prompt": {"en": "Commit message:", "ar": "رسالة الالتزام (commit):"},
    "save_changes_prompt": {"en": "Stage all changes?", "ar": "هل تريد تحضير جميع التغييرات؟"},
    "file_to_stage": {"en": "File to stage:", "ar": "الملف المراد تحضيره:"},
    "staging_all": {"en": "Staging all changes...", "ar": "جارٍ تحضير جميع التغييرات..."},
    "staging_file": {"en": "Staging '{file}'...", "ar": "جارٍ تحضير '{file}'..."},
    "staging_readme": {"en": "Staging README.md...", "ar": "جارٍ تحضير README.md..."},
    "committing_changes": {"en": "Committing changes...", "ar": "جارٍ تنفيذ الالتزام (commit)..."},
    "creating_commit": {"en": "Creating initial commit...", "ar": "جارٍ إنشاء الالتزام الأول..."},
    "initial_commit_created": {"en": "Initial commit created.", "ar": "تم إنشاء الالتزام الأول."},
    "adding_remote": {"en": "Adding remote 'origin'...", "ar": "جارٍ إضافة المستودع البعيد 'origin'..."},
    "cloning_repo": {"en": "Cloning repository...", "ar": "جارٍ استنساخ المستودع..."},
    "changed_to": {"en": "Changed directory to: {path}", "ar": "تم الانتقال إلى: {path}"},
    "fetching_status": {"en": "Fetching status...", "ar": "جارٍ جلب الحالة..."},
    "fetching_history": {"en": "Fetching commit history...", "ar": "جارٍ جلب سجل الالتزامات..."},
    "merge_success": {"en": "Branch merged successfully.", "ar": "تم دمج الفرع بنجاح."},
    "stash_applied": {"en": "Stash applied.", "ar": "تم تطبيق الـ stash."},
    "stash_popped": {"en": "Stash popped.", "ar": "تم استرجاع الـ stash."},
    "stash_dropped": {"en": "Stash dropped.", "ar": "تم حذف الـ stash."},
    "conflicts_detected": {"en": "Conflicts detected in the following files:", "ar": "تم اكتشاف تعارضات في الملفات التالية:"},
    "resolve_conflicts": {"en": "Resolve the conflicts, then stage and commit the changes.", "ar": "قم بحل التعارضات، ثم قم بتحضير التغييرات والالتزام بها."},
    "executing_manual": {"en": "Executing command...", "ar": "جارٍ تنفيذ الأمر..."},
    "ahead_commits": {"en": "You are ahead of the remote by {count} commit(s).", "ar": "أنت متقدم عن البعيد بـ {count} التزام(ات)."},

    # Stash & sync progress messages (previously hardcoded in English)
    "stash_saving": {"en": "Saving changes to stash...", "ar": "جارٍ حفظ التغييرات في الـ stash..."},
    "stash_listing": {"en": "Listing stashes...", "ar": "جارٍ عرض قائمة الـ stash..."},
    "stash_popping": {"en": "Applying and removing latest stash...", "ar": "جارٍ تطبيق وحذف آخر stash..."},
    "stash_applying": {"en": "Applying latest stash...", "ar": "جارٍ تطبيق آخر stash..."},
    "stash_dropping": {"en": "Dropping latest stash...", "ar": "جارٍ حذف آخر stash..."},
    "fetching_remote": {"en": "Fetching from {remote}...", "ar": "جارٍ الجلب من {remote}..."},
    "pulling_remote": {"en": "Pulling changes from remote...", "ar": "جارٍ سحب التغييرات من البعيد..."},
    "pushing_remote": {"en": "Pushing changes to remote...", "ar": "جارٍ رفع التغييرات إلى البعيد..."},

    # --- Security policy engine: additional risk warnings ---
    "warning_tag_delete": {"en": "This will permanently delete a tag. If it was already pushed, others may still have it.", "ar": "سيؤدي هذا لحذف وسم (tag) بشكل دائم. إذا كان مرفوعًا سابقًا فقد يبقى موجودًا لدى آخرين."},
    "alternative_tag_delete": {"en": "Make sure the tag isn't needed elsewhere before deleting it.", "ar": "تأكد أن أحدًا لا يحتاج هذا الوسم قبل حذفه."},
    "warning_reflog_delete": {"en": "This permanently removes entries from the reflog, which can make some commits unrecoverable.", "ar": "سيؤدي هذا لحذف إدخالات من الـ reflog بشكل دائم، مما قد يجعل بعض الالتزامات غير قابلة للاسترجاع."},
    "alternative_reflog_delete": {"en": "Consider backing up important commit hashes before pruning the reflog.", "ar": "يُفضّل حفظ نسخة من أهم أرقام الالتزامات (hashes) قبل تنظيف الـ reflog."},
    "warning_gc_prune": {"en": "Pruning now can permanently remove unreachable objects (e.g. commits only kept via reflog).", "ar": "التنظيف الفوري قد يحذف بشكل دائم كائنات غير قابلة للوصول (مثل التزامات محفوظة فقط عبر الـ reflog)."},
    "alternative_gc_prune": {"en": "Run 'git gc' without --prune=now to use the default (safer) grace period.", "ar": "شغّل 'git gc' بدون --prune=now لاستخدام فترة الأمان الافتراضية."},
    "warning_reset_soft": {"en": "This will move the current branch pointer and may change what is staged.", "ar": "سيؤدي هذا لتحريك مؤشر الفرع الحالي وقد يغيّر ما هو مُجهّز (staged)."},
    "alternative_reset_soft": {"en": "Your working tree files are not touched by a soft/mixed reset, only the index/HEAD.", "ar": "لن تتأثر ملفات مجلد العمل بإعادة الضبط الناعمة/المختلطة، فقط الفهرس ومؤشر HEAD."},
    "warning_push_generic": {"en": "This will upload your local commits to the remote repository.", "ar": "سيؤدي هذا لرفع التزاماتك المحلية إلى المستودع البعيد."},
    "warning_pull_generic": {"en": "This will fetch and merge remote changes into your current branch.", "ar": "سيؤدي هذا لجلب التغييرات البعيدة ودمجها في فرعك الحالي."},
    "warning_revert_generic": {"en": "This creates a new commit that reverses another one; it can conflict with other changes.", "ar": "سيُنشئ هذا التزامًا جديدًا يعكس التزامًا آخر، وقد يتعارض مع تغييرات أخرى."},
    "warning_remote_remove": {"en": "This changes or removes remote repository configuration.", "ar": "سيؤدي هذا لتغيير أو حذف إعدادات المستودع البعيد."},
    "alternative_remote_remove": {"en": "You can re-add the remote later with 'git remote add' if needed.", "ar": "يمكنك إعادة إضافة المستودع البعيد لاحقًا باستخدام 'git remote add' إذا لزم الأمر."},
    "warning_config_generic": {"en": "This changes Git configuration, which can affect future commands.", "ar": "سيؤدي هذا لتغيير إعدادات Git، مما قد يؤثر على الأوامر المستقبلية."},
    "warning_checkout_branch": {"en": "This will switch your working branch.", "ar": "سيؤدي هذا لتبديل الفرع الذي تعمل عليه."},
    "warning_restore_staged": {"en": "This only changes the staged (index) version of the file(s), not your working tree.", "ar": "سيغيّر هذا فقط النسخة المُجهّزة (staged) من الملف(ات)، دون التأثير على مجلد العمل."},
    "warning_unrecognized_shape": {"en": "This command's arguments don't match a recognized safe shape, so it needs confirmation.", "ar": "شكل معاملات هذا الأمر غير معروف كأمر آمن، لذا يتطلب تأكيدًا."},
    "warning_unknown_subcommand": {"en": "This is not a recognized Git subcommand pattern, so it needs confirmation before running.", "ar": "هذا النمط غير معروف كأمر فرعي من أوامر Git، لذا يتطلب تأكيدًا قبل التنفيذ."},

    # --- Structured parser: blocked / parse-error explanations ---
    "blocked_not_git_invocation": {"en": "Refused: this is not a plain 'git ...' invocation.", "ar": "تم الرفض: هذا ليس استدعاءً مباشرًا لأمر 'git ...'."},
    "blocked_unrecognized_global_option": {"en": "Refused: an unrecognized option appears before the Git subcommand, so its effect can't be verified as safe.", "ar": "تم الرفض: يوجد خيار غير معروف قبل الأمر الفرعي لـ Git، ولا يمكن التأكد من أن تأثيره آمن."},
    "blocked_config_env": {"en": "Refused: --config-env can inject configuration through the environment and is not allowed in untrusted GitAssist commands.", "ar": "تم الرفض: الخيار --config-env يمكنه حقن إعدادات عبر البيئة ولا يُسمح به في أوامر GitAssist غير الموثوقة."},
    "blocked_exec_path": {"en": "Refused: changing Git's executable search path (--exec-path) could run a substituted binary instead of the real Git.", "ar": "تم الرفض: تغيير مسار بحث Git عن ملفاته التنفيذية (--exec-path) قد يشغّل برنامجًا مختلفًا بدل Git الحقيقي."},
    "blocked_alias_shell_escape": {"en": "Refused: this defines a Git alias that runs an external shell command ('!...'), which is a known code-execution vector.", "ar": "تم الرفض: هذا يُعرّف اسمًا مستعارًا (alias) في Git يشغّل أمر نظام خارجي ('!...')، وهذا مسار معروف لتنفيذ أوامر خطرة."},
    "blocked_exec_capable_config": {"en": "Refused: this configuration key can make Git execute an external program (e.g. pager, editor, credential helper, or a filter/diff/merge driver).", "ar": "تم الرفض: هذا المفتاح في الإعدادات قد يجعل Git يشغّل برنامجًا خارجيًا (مثل المُصفّح، المحرر، أداة بيانات الاعتماد، أو أداة فلترة/دمج)."},
    "blocked_unsafe_transport": {"en": "Refused: 'ext::' and 'fd::' transport addresses can run arbitrary external commands.", "ar": "تم الرفض: عناوين النقل من نوع 'ext::' أو 'fd::' يمكن أن تُشغّل أوامر نظام خارجية عشوائية."},
    "blocked_upload_receive_pack": {"en": "Refused: --upload-pack/--receive-pack can make Git run an arbitrary program as part of the transfer.", "ar": "تم الرفض: خياري --upload-pack أو --receive-pack قد يجعلان Git يشغّل برنامجًا عشوائيًا كجزء من عملية النقل."},
    "blocked_unknown_subcommand": {"en": "Refused: this Git subcommand is not explicitly allowed. Unknown Git names can resolve to aliases or external git-* programs, so GitAssist will not execute them.", "ar": "تم الرفض: هذا الأمر الفرعي لـ Git غير مسموح به صراحةً. أسماء أوامر Git غير المعروفة قد تُنفّذ كـ alias أو كبرنامج خارجي، لذلك لن ينفذها GitAssist."},
    "blocked_generic": {"en": "Refused: this command could not be safely understood.", "ar": "تم الرفض: تعذّر فهم هذا الأمر بشكل آمن."},
    "parse_error_malformed_config": {"en": "Refused: malformed -c configuration argument (expected key=value).", "ar": "تم الرفض: معامل الإعداد -c غير صحيح الصياغة (المتوقع مفتاح=قيمة)."},
    "parse_error_missing_value": {"en": "Refused: an option that requires a value is missing one.", "ar": "تم الرفض: أحد الخيارات يتطلب قيمة ولم تُقدَّم."},
    "parse_error_no_subcommand": {"en": "Refused: no Git subcommand was found in this input.", "ar": "تم الرفض: لم يتم العثور على أمر فرعي لـ Git في هذا الإدخال."},
    "blocked_command": {"en": "This command was blocked for security reasons and will not run. {reason}", "ar": "تم حظر هذا الأمر لأسباب أمنية ولن يتم تنفيذه. {reason}"},

    # --- GitHub API: specific error outcomes ---
    "github_error_no_token": {"en": "No access token was provided.", "ar": "لم يتم تقديم رمز وصول."},
    "github_error_invalid_repo_name": {"en": "Invalid repository name. Use only letters, numbers, dots, dashes, and underscores.", "ar": "اسم مستودع غير صالح. استخدم فقط الحروف والأرقام والنقاط والشرطات والشرطات السفلية."},
    "github_error_invalid_token": {"en": "GitHub rejected the token as invalid or expired.", "ar": "رفض GitHub الرمز باعتباره غير صالح أو منتهي الصلاحية."},
    "github_error_rate_limited_or_forbidden": {"en": "GitHub denied the request - this may be a rate limit or a token missing the required permission scope.", "ar": "رفض GitHub الطلب - قد يكون هذا بسبب تجاوز الحد المسموح أو رمز لا يملك الصلاحية اللازمة."},
    "github_error_repo_exists_or_invalid": {"en": "GitHub rejected the request - a repository with this name may already exist.", "ar": "رفض GitHub الطلب - قد يكون هناك مستودع بهذا الاسم بالفعل."},
    "github_error_api_generic": {"en": "GitHub API returned an error.", "ar": "أرجعت واجهة GitHub خطأً."},
    "github_error_timeout": {"en": "The request to GitHub timed out. Check your connection and try again.", "ar": "انتهت مهلة الطلب إلى GitHub. تحقق من اتصالك وحاول مرة أخرى."},
    "github_error_network": {"en": "Could not reach GitHub. Check your internet connection.", "ar": "تعذّر الوصول إلى GitHub. تحقق من اتصالك بالإنترنت."},
    "github_error_unexpected": {"en": "GitHub returned an unexpected response.", "ar": "أرجع GitHub استجابة غير متوقعة."},
    "command_timed_out": {"en": "The command timed out: {command}", "ar": "انتهت مهلة الأمر: {command}"},

    # --- Remote update monitor ---
    "remote_status_title": {"en": "Remote Update Status", "ar": "حالة تحديثات المستودع البعيد"},
    "remote_status_remote": {"en": "Remote", "ar": "المستودع البعيد"},
    "remote_status_branch": {"en": "Branch", "ar": "الفرع"},
    "remote_status_line": {"en": "Status", "ar": "الحالة"},
    "remote_status_up_to_date": {"en": "Up to date with {remote}/{branch}.", "ar": "محدَّث مع {remote}/{branch}."},
    "remote_status_behind": {"en": "Behind {remote}/{branch} by {behind} commit(s). Recommendation: review, then pull.", "ar": "متأخر عن {remote}/{branch} بـ {behind} التزام(ات). التوصية: راجع ثم اسحب (pull)."},
    "remote_status_ahead": {"en": "Ahead of {remote}/{branch} by {ahead} commit(s). Recommendation: push when ready.", "ar": "متقدم عن {remote}/{branch} بـ {ahead} التزام(ات). التوصية: ارفع (push) عندما تكون جاهزًا."},
    "remote_status_diverged": {"en": "Diverged from {remote}/{branch}: {ahead} ahead, {behind} behind. Recommendation: review carefully before merging or rebasing.", "ar": "تباعد عن {remote}/{branch}: {ahead} متقدم، {behind} متأخر. التوصية: راجع بعناية قبل الدمج أو إعادة الترتيب."},
    "remote_status_no_remote": {"en": "No remote configured for this repository.", "ar": "لا يوجد مستودع بعيد مُعرَّف لهذا المستودع."},
    "remote_status_offline": {"en": "Could not reach the remote (offline or timed out). Showing last known status.", "ar": "تعذّر الوصول إلى المستودع البعيد (غير متصل أو انتهت المهلة). يُعرض آخر حالة معروفة."},
    "remote_status_unsafe_remote": {"en": "Automatic remote check skipped: this remote uses an unsafe transport or custom upload helper.", "ar": "تم تخطي الفحص التلقائي: هذا المستودع البعيد يستخدم وسيلة نقل غير آمنة أو أداة رفع مخصصة."},
    "remote_status_disabled": {"en": "Remote checking is disabled in settings.", "ar": "فحص المستودع البعيد معطّل في الإعدادات."},
    "remote_status_not_a_repo": {"en": "Not inside a Git repository.", "ar": "لست داخل مستودع Git."},
    "remote_status_cached_note": {"en": "(cached result - next automatic check is throttled)", "ar": "(نتيجة مخزّنة - الفحص التلقائي التالي مُقيَّد زمنيًا)"},

    # --- Repository dashboard (section 18) ---
    "dashboard_title": {"en": "GitAssist", "ar": "GitAssist"},
    "dashboard_repository": {"en": "Repository", "ar": "المستودع"},
    "dashboard_branch": {"en": "Branch", "ar": "الفرع"},
    "dashboard_working": {"en": "Working", "ar": "حالة العمل"},
    "dashboard_working_clean": {"en": "CLEAN", "ar": "نظيف"},
    "dashboard_staged_count": {"en": "{count} staged", "ar": "{count} مُجهّز"},
    "dashboard_unstaged_count": {"en": "{count} unstaged", "ar": "{count} غير مُجهّز"},
    "dashboard_untracked_count": {"en": "{count} untracked", "ar": "{count} غير متتبَّع"},
    "dashboard_remote": {"en": "Remote", "ar": "المستودع البعيد"},
    "dashboard_upstream": {"en": "Upstream", "ar": "الفرع البعيد المرتبط"},
    "dashboard_status": {"en": "Status", "ar": "الحالة"},
    "dashboard_no_remote": {"en": "none configured", "ar": "غير مُعرَّف"},
    "dashboard_status_up_to_date": {"en": "UP TO DATE", "ar": "محدَّث"},
    "dashboard_status_behind": {"en": "BEHIND", "ar": "متأخر"},
    "dashboard_status_ahead": {"en": "AHEAD", "ar": "متقدم"},
    "dashboard_status_diverged": {"en": "DIVERGED", "ar": "متباعد"},
    "dashboard_status_offline": {"en": "UNKNOWN (offline)", "ar": "غير معروف (غير متصل)"},
    "dashboard_status_disabled": {"en": "CHECK DISABLED", "ar": "الفحص معطّل"},
    "dashboard_status_no_remote": {"en": "-", "ar": "-"},
    "dashboard_status_not_a_repo": {"en": "-", "ar": "-"},

    # --- Local project workflow (section 14) ---
    "path_not_found_error": {"en": "Path does not exist: {path}", "ar": "المسار غير موجود: {path}"},
    "path_not_a_directory_error": {"en": "Path is not a directory: {path}", "ar": "المسار ليس مجلدًا: {path}"},
    "not_git_repo_warning": {"en": "This is not a Git repository yet: {path}", "ar": "هذا ليس مستودع Git بعد: {path}"},
    "init_repo_here": {"en": "Initialize a new repository here", "ar": "تهيئة مستودع جديد هنا"},
    "clone_into_here": {"en": "Clone an existing repository here", "ar": "استنساخ مستودع موجود هنا"},
    "cancel": {"en": "Cancel", "ar": "إلغاء"},
    "cancelled": {"en": "Cancelled.", "ar": "تم الإلغاء."},
    "sync_check_updates": {"en": "Check for remote updates", "ar": "التحقق من تحديثات المستودع البعيد"},
    "continue_to_menu": {"en": "Continue to main menu", "ar": "المتابعة إلى القائمة الرئيسية"},
    "add_remote_option": {"en": "Add a remote repository", "ar": "إضافة مستودع بعيد"},

    # --- Next-step suggestion engine (section 16) ---
    "next_step_after_init": {"en": "Next: create or add some files, then stage them with 'add'.", "ar": "التالي: أنشئ أو أضف بعض الملفات، ثم جهّزها باستخدام 'add'."},
    "next_step_after_clone": {"en": "Next: check the repository status, or start making changes.", "ar": "التالي: تحقق من حالة المستودع، أو ابدأ بإجراء تغييرات."},
    "next_step_after_add": {"en": "Next: create a commit to save these staged changes.", "ar": "التالي: أنشئ التزامًا (commit) لحفظ هذه التغييرات المُجهّزة."},
    "next_step_after_commit_with_remote": {"en": "Next: push this commit to the remote when you're ready.", "ar": "التالي: ارفع (push) هذا الالتزام إلى المستودع البعيد عندما تكون جاهزًا."},
    "next_step_after_commit_no_remote": {"en": "Next: add a remote repository if you'd like to back this up or share it.", "ar": "التالي: أضف مستودعًا بعيدًا إذا أردت نسخ هذا احتياطيًا أو مشاركته."},
    "next_step_after_fetch": {"en": "Remote information updated. Check whether your branch is ahead, behind, or diverged.", "ar": "تم تحديث معلومات المستودع البعيد. تحقق ما إذا كان فرعك متقدمًا أو متأخرًا أو متباعدًا."},
    "next_step_conflicts": {"en": "Resolve the conflicts in the listed files, then stage and commit them.", "ar": "قم بحل التعارضات في الملفات المذكورة، ثم جهّزها والتزم بها."},

    # --- File operations (section 21) ---
    "create_file_failed": {"en": "Failed to create '{name}': {error}", "ar": "فشل إنشاء '{name}': {error}"},
    "edit_file_failed": {"en": "Failed to edit '{name}': {error}", "ar": "فشل تعديل '{name}': {error}"},
    "delete_file_failed": {"en": "Failed to delete '{name}': {error}", "ar": "فشل حذف '{name}': {error}"},
    "create_dir_failed": {"en": "Failed to create directory '{name}': {error}", "ar": "فشل إنشاء المجلد '{name}': {error}"},
    "permission_denied_error": {"en": "Permission denied: {path}", "ar": "تم رفض الإذن: {path}"},
    "path_outside_cwd_warning": {"en": "This path is outside your current working directory: {path}", "ar": "هذا المسار خارج مجلد العمل الحالي: {path}"},

    "error_no_upstream": {"en": "This branch has no upstream (tracking) branch set on the remote.", "ar": "لا يوجد لهذا الفرع فرع تتبّع (upstream) مُعرَّف على المستودع البعيد."},
    "suggestion_set_upstream": {"en": "Push with '-u' once to link this branch to a remote branch, e.g. git push -u origin <branch>.", "ar": "ارفع باستخدام '-u' مرة واحدة لربط هذا الفرع بفرع بعيد، مثل: git push -u origin <branch>."},
    "error_unmerged_files": {"en": "You have unresolved merge conflicts that must be fixed before continuing.", "ar": "لديك تعارضات دمج غير محلولة يجب إصلاحها قبل المتابعة."},

    # Sync menu action labels (distinct from *_completed result messages)
    "sync_fetch": {"en": "Fetch", "ar": "جلب (fetch)"},
    "sync_pull": {"en": "Pull", "ar": "سحب (pull)"},
    "sync_push": {"en": "Push", "ar": "رفع (push)"},

    # GitHub manager
    "opening_url": {"en": "Opening: {url}", "ar": "جارٍ فتح: {url}"},
    "browser_opened": {"en": "Browser opened.", "ar": "تم فتح المتصفح."},
    "browser_open_failed": {"en": "Failed to open browser: {error}", "ar": "فشل فتح المتصفح: {error}"},
    "remote_url": {"en": "Remote URL: {url}", "ar": "رابط المستودع البعيد: {url}"},
    "provider": {"en": "Provider: {provider}", "ar": "المزوّد: {provider}"},
    "owner": {"en": "Owner: {owner}", "ar": "المالك: {owner}"},
    "repo_name": {"en": "Repository: {repo}", "ar": "المستودع: {repo}"},    "cannot_delete_current_branch": {
        "en": "Cannot delete the current branch. Switch to another branch first.",
        "ar": "لا يمكن حذف الفرع الحالي. قم بالتبديل إلى فرع آخر أولاً."
    },
    "switch_first_hint": {
        "en": "Use 'Switch branch' to move to another branch, then try deleting again.",
        "ar": "استخدم 'التبديل إلى فرع' للانتقال إلى فرع آخر، ثم حاول الحذف مرة أخرى."
    },    "no_stashes": {
        "en": "No stashes found.",
        "ar": "لا توجد محفوظات (stash)."
    },    "allow_unrelated_prompt": {
        "en": "Pull failed. Try again with --allow-unrelated-histories?",
        "ar": "فشل السحب. هل تريد المحاولة مع --allow-unrelated-histories؟"
    },    "project_selection_title": {
        "en": "Project Selection",
        "ar": "اختيار المشروع"
    },
    "use_current_project": {
        "en": "Work on current directory",
        "ar": "العمل على المجلد الحالي"
    },
}

def get_text(key: str, lang: str = None, **kwargs) -> str:
    if lang is None:
        lang = settings.LANGUAGE
    if key in TEXTS:
        if lang in TEXTS[key]:
            text = TEXTS[key][lang]
        else:
            text = TEXTS[key]["en"]
    else:
        text = key
    if kwargs:
        return text.format(**kwargs)
    return text