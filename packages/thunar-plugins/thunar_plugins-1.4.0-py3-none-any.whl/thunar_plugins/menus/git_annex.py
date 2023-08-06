# system modules
import logging
import os
import subprocess
import shutil
import shlex
import pathlib
import re
import json
from collections import defaultdict, Counter
import threading
import time
import pkg_resources
import functools
import itertools

# internal modules
from thunar_plugins import l10n
from thunar_plugins.log import console, Notify
from thunar_plugins.version import __version__

# external modules
from rich.pretty import Pretty
from rich.syntax import Syntax
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import GObject, Gtk, GLib, Thunarx

logger = logging.getLogger(__name__)


METADATA_CACHE = defaultdict(lambda: defaultdict(set))


class GitAnnexHelper:
    @functools.lru_cache(maxsize=1)
    def git_annex_executable(self):
        return shutil.which("git-annex")

    @functools.lru_cache(maxsize=1)
    def git_annex_version(self):
        version = self.subprocess(
            subprocess.check_output, ["git", "annex", "version", "--raw"]
        )
        logger.info(f"Git Annex version: {version}")
        return version

    @functools.lru_cache(maxsize=1)
    def git_annex_capabilities(self):
        caps = set()
        view_help = self.subprocess(
            subprocess.check_output, ["git", "annex", "view", "--help"]
        )
        if re.search(r"FIELD\?=", view_help, flags=re.IGNORECASE):
            caps.add("view-show-valueless")
        logger.info(
            f"This git-annex ({self.git_annex_version()}) "
            f"{'can' if 'view-show-valueless' in caps else 'can´t'} "
            f"show unvalued fields in a view."
        )
        logger.debug(f"git annex capabilities: {caps}")
        return caps

    @classmethod
    def debug_cmdline(cls, cmdparts, comment="📋 Copy-pastable:"):
        if logger.getEffectiveLevel() <= logging.DEBUG:
            console.print(
                Syntax(
                    f"\n# {comment}\n\n{shlex.join(cmdparts)}\n",
                    "bash",
                    word_wrap=True,
                )
            )

    @classmethod
    def flush_gtk(cls):
        while Gtk.events_pending():
            Gtk.main_iteration()

    @classmethod
    def not_in_parallel(cls, decorated_fun):
        if not hasattr(cls, "locks"):
            cls.locks = dict()

        cls.locks[decorated_fun] = threading.Lock()

        @functools.wraps(decorated_fun)
        def wrapper(*args, **kwargs):
            if (lock := cls.locks[decorated_fun]).locked():
                logger.debug(
                    f"Not running {decorated_fun}(*{args!r},**{kwargs!r}) as it is already running!"
                )
            else:
                with lock:
                    decorated_fun(*args, **kwargs)

        return wrapper

    @classmethod
    def run_in_thread(cls, decorated_fun):
        @functools.wraps(decorated_fun)
        def wrapper(*args, **kwargs):
            thread = threading.Thread(
                target=decorated_fun, args=args, kwargs=kwargs
            )
            logger.debug(
                f"Starting {decorated_fun}(*{args!r}, **{kwargs!r}) in thread"
            )
            thread.start()
            # logger.debug(
            #     f"Waiting for {decorated_fun}(*{args!r}, **{kwargs!r}) thread to exit..."
            # )
            # thread.join()

        return wrapper

    @classmethod
    def only_for_unique_git_annex_repo(cls, decorated_fun):
        @functools.wraps(decorated_fun)
        def wrapper(*args, **kwargs):
            items = args[-1]
            logger.debug(
                f"only_for_unique_git_annex_repo: {args = }, {kwargs = }, {items = }"
            )
            folders = set(
                (
                    f.get_location().get_path()
                    if f.is_directory()
                    else os.path.dirname(f.get_location().get_path())
                )
                for f in items
            )
            folder_uuids = {d: cls.get_git_annex_uuid(d) for d in folders}
            uuids = set(folder_uuids.values())
            if not (len(uuids) == 1 and all(uuids)):
                logger.info(
                    f"Not exactly ONE unique git-annex repo selected: "
                    f"{folder_uuids = }"
                )
                return []
            info = dict(
                cwd=(cwd := next(iter(folder_uuids))),
                repo=cls.get_git_repo(cwd),
                uuid=next(iter(uuids), None),
            )
            return decorated_fun(*args, info=info, **kwargs)

        return wrapper

    @classmethod
    def make_metadata_cache(cls, path, cache=None):
        """
        Make/Update a ``dict[file][field] = {'val3','val2'}``
        """
        notification = Notify.Notification.new(
            _("Git Annex Thunar Plugin"), None, "git-annex"
        )
        cls.notification = notification
        if cache is None:
            cache = defaultdict(lambda: defaultdict(set))
        notification.update(
            _("Git Annex Thunar Plugin"),
            "⏳ "
            + _("Determining amount of annexed files in {repo}").format(
                repo=pathlib.Path(path).name
            ),
            "git-annex",
        )
        notification.show()
        n_files = 0
        for n_files, f in enumerate(
            cls.subprocess(
                subprocess.Popen,
                ["git", "-C", path, "annex", "find", "--copies=0"],
                stdout=subprocess.PIPE,
            ).stdout,
            start=1,
        ):
            cls.flush_gtk()
        try:
            git_annex = cls.subprocess(
                subprocess.Popen,
                ["git", "-C", path, "annex", "metadata", "--json"],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
            )

            time_last_notification_update = 0
            time_begin = time.time()
            i = 0
            for i, line in enumerate(git_annex.stdout, start=1):
                cls.flush_gtk()
                if time.time() - time_last_notification_update > 1:
                    # couldn't get a stop button to work, callback was never
                    # called, don't know why 🤷
                    notification.update(
                        _("Git Annex Thunar Plugin"),
                        "⏳ "
                        + _(
                            "Reading metadata from Git Annex... ({n}/{n_files} files in {path})"
                        ).format(
                            n=i, n_files=n_files, path=pathlib.Path(path).name
                        )
                        + (
                            "\n\n{}".format(
                                _("This currently can't be interrupted") + "🙂 "
                            )
                            if time.time() - time_begin > 5
                            else ""
                        ),
                        "git-annex",
                    )
                    notification.show()
                    time_last_notification_update = time.time()
                try:
                    m = json.loads(line)
                    cache.pop(m["file"], None)
                    for k, v in m["fields"].items():
                        for x in v:
                            if not k.endswith("lastchanged"):
                                # file-specific field
                                cache[m["file"]][k].add(x)
                                # overall list of fields
                                cache["/"][k].add(x)
                except Exception as e:
                    logger.error(
                        f"Something didn't work while reading metadata: "
                        f"{type(e).__name__}: {e}"
                    )
        except subprocess.CalledProcessError as e:
            logger.error(f"Couldn't get annex metadata from {path!r}: {e}")
            return cache
        finally:
            if git_annex.poll():
                logger.warning(f"Killing {git_annex}")
                git_annex.kill()
        notification.update(
            _("Git Annex Thunar Plugin"),
            "✅ "
            + _("Read metadata from {n} files in {path}").format(
                n=i, path=pathlib.Path(path).name
            )
            + "\n\n"
            + _("There are {n_fields} unique metadata fields.").format(
                n_fields=len(cache["/"])
            ),
            "git-annex",
        )
        notification.show()
        if logger.getEffectiveLevel() <= logging.DEBUG:
            console.print(f"cache: ")
            console.print(Pretty(dict(cache), max_length=20))
        return cache

    @classmethod
    def rebuild_metadata_cache(cls, path):
        uuid = cls.get_git_annex_uuid(path)
        if not uuid:
            return METADATA_CACHE[uuid]
        METADATA_CACHE[uuid] = cls.make_metadata_cache(path=path)

    @classmethod
    def subprocess(cls, fun, cmd, *args, **kwargs):
        logger.info(f"🚀 Running {cmd}")
        cls.debug_cmdline(cmd)
        return fun(
            cmd, *args, **{**dict(encoding="utf-8", errors="ignore"), **kwargs}
        )

    @classmethod
    def run_cmd(
        cls,
        cmdparts,
        cwd=None,
        terminal=True,
        notify=False,
        title=None,
        keep_open_on_success=False,
        keep_open_on_failure=True,
        dry_run=False,
    ):
        if not shutil.which("xfce4-terminal"):
            logger.warning(
                f"xfce4-terminal not found. Currently, "
                f"this is the only terminal our git-annex integration supports. "
                f"Continuing without showing commands in terminal."
            )
            terminal = False
        if terminal:

            def close_cmd(text, timeout=None):
                return ";".join(
                    map(
                        shlex.join,
                        [["echo"], ["echo", text]]
                        + (
                            [
                                ["echo", "This window will auto-close soon."],
                                ["sleep", str(int(timeout))],
                                ["exit"],
                            ]
                            if isinstance(timeout, int)
                            else [
                                ["echo", "You can close this window now."],
                                ["sleep", "infinity"],
                            ]
                        ),
                    )
                )

            cmdparts = [
                "sh",
                "-c",
                f"(set -x;{shlex.join(cmdparts)}) "
                f"&& ({close_cmd('✅ Success!',timeout=None if keep_open_on_success else 10)}) "
                f"|| ({close_cmd('💥 Failure!',timeout=None if keep_open_on_failure else 10)})",
            ]
            logger.debug(f"What the terminal will be given: {cmdparts = }")
            cls.debug_cmdline(
                cmdparts,
                comment="What the Terminal will be given, 📋 copy-pastable:",
            )
            cmdparts = (
                [
                    "xfce4-terminal",  # TODO: Hard-coded terminal emulator is bad
                    "--icon",
                    "git-annex",
                    "--hide-menubar",
                    "--hide-toolbar",
                ]
                + (["--title", title] if title else [])
                + [
                    "--command",
                    shlex.join(cmdparts),
                ]
            )
        cls.debug_cmdline(
            cmdparts,
            comment="The entire command-line to run, 📋 copy-pastable:",
        )
        if dry_run:
            logger.info(f"🚀 Would now run {cmdparts = }")
            return cmdparts
        else:
            if notify:
                notification = Notify.Notification.new(
                    _("Git Annex Thunar Plugin"), None, "git-annex"
                )
                notification.update(
                    _("Git Annex Thunar Plugin"),
                    "⏳ "
                    + (title or _("Running {cmd}...").format(cmd=cmdparts)),
                    "git-annex",
                )
                notification.show()
            result = cls.subprocess(subprocess.run, cmdparts, cwd=cwd)
            if notify:
                notification.update(
                    _("Git Annex Thunar Plugin"),
                    "✅ " + (title or _("Ran {cmd}").format(cmd=cmdparts)),
                    "git-annex",
                )
                notification.show()
            return result

    @classmethod
    def run_git_annex(
        cls,
        subcmd,
        paths=None,
        add_before=False,
        commit_before=False,
        reset_before=True,
        args=None,
        cwd=None,
        **kwargs,
    ):
        args = args or []
        paths = paths or []
        cmdparts = ["git", "annex", subcmd] + args + paths
        logger.debug(f"Bare {cmdparts = }")
        cls.debug_cmdline(cmdparts)
        if reset_before:
            cmdparts = [
                "sh",
                "-xc",
                ";".join(
                    shlex.join(p) for p in (["git", "reset"] + paths, cmdparts)
                ),
            ]
            logger.debug(f"With git resetting: {cmdparts = }")
            cls.debug_cmdline(cmdparts)
        repo_description = cls.get_git_annex_description(cwd or ".")
        if commit_before:
            cmdparts = [
                "sh",
                "-xc",
                ";".join(
                    shlex.join(p)
                    for p in (
                        [
                            "git",
                            "commit",
                            "-m",
                            f"thunar-plugins v{__version__}"
                            + (
                                " in {}".format(repo_description)
                                if repo_description
                                else ""
                            ),
                        ],
                        cmdparts,
                    )
                ),
            ]
            logger.debug(f"With git add: {cmdparts = }")
            cls.debug_cmdline(cmdparts)
        if add_before:
            cmdparts = [
                "sh",
                "-xc",
                ";".join(
                    shlex.join(p)
                    for p in (
                        ["git", "add"]
                        + (["-A"] if add_before == "all" else paths),
                        cmdparts,
                    )
                ),
            ]
            logger.debug(f"With git add: {cmdparts = }")
            cls.debug_cmdline(cmdparts)
        return cls.run_cmd(cmdparts=cmdparts, cwd=cwd, **kwargs)

    @classmethod
    def get_git_annex_uuid(cls, folder):
        try:
            return cls.subprocess(
                subprocess.check_output,
                ["git", "-C", folder, "config", "annex.uuid"],
            ).strip()
        except subprocess.CalledProcessError as e:
            logger.info(f"{folder!r} is apparently no git repository: {e}")

    @classmethod
    def get_git_annex_description(cls, folder):
        try:
            infojson = json.loads(
                cls.subprocess(
                    subprocess.check_output,
                    [
                        "git",
                        "-C",
                        str(folder),
                        "annex",
                        "info",
                        "here",
                        "--fast",
                        "--json",
                    ],
                )
            )
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            logger.info(
                f"Couldn't determine git annex repo description for {folder!r}: {type(e).__name__} {e}"
            )
            return None
        return (
            re.sub(r"\s*\[here\]\s*$", "", infojson.get("description", ""))
            or None
        )

    @classmethod
    def get_git_branch(cls, folder="."):
        return cls.subprocess(
            subprocess.check_output,
            [
                "git",
                "-C",
                str(folder),
                "rev-parse",
                "--abbrev-ref",
                "HEAD",
            ],
        ).rstrip("\r\n")

    @classmethod
    def get_git_branches(cls, folder=".", all=False, sensible=True):
        git_branch_output = (
            cls.subprocess(
                subprocess.check_output,
                [
                    "git",
                    "-C",
                    str(folder),
                    "branch",
                ]
                + (["-a"] if all else []),
            )
            .rstrip("\r\n")
            .splitlines()
        )
        branches = [re.sub(r"^\W+", r"", L) for L in git_branch_output]
        if sensible:
            branches = [
                b
                for b in branches
                if not (
                    re.search(r"(^|/)views/", b)
                    or re.search(r"(^|/)synced/", b)
                    or re.search(r"(^|/)git-annex$", b)
                )
            ]
        return branches

    @classmethod
    def get_git_repo(cls, folder):
        return cls.subprocess(
            subprocess.check_output,
            [
                "git",
                "-C",
                str(folder),
                "rev-parse",
                "--show-toplevel",
            ],
        ).rstrip("\r\n")


class GitAnnexSubmenu(GObject.GObject, Thunarx.MenuProvider, GitAnnexHelper):
    def __init__(self):
        logger.debug(f"{type(self).__name__} is initialized")

    @property
    def counter(self):
        try:
            return self._counter
        except AttributeError:
            self._counter = collections.Counter()
        return self._counter

    @classmethod
    def name(cls):
        s = _("Git Annex Context-Menu")
        if not shutil.which("git-annex"):
            s = _("[Unavailable]") + " " + s
        return s

    @classmethod
    def description(cls):
        s = _(
            "This plugin adds a context menu item "
            "for managing Git Annex repositories."
        )
        if not shutil.which("git-annex"):
            s += " " + _(
                "Install Git Annex to use this plugin: "
                "https://git-annex.branchable.com"
            )
        return s

    @GitAnnexHelper.only_for_unique_git_annex_repo
    def get_file_menu_items(self, window, items, info):
        uuid = info["uuid"]
        cwd = info["cwd"]
        logger.debug(f"Will operate in {cwd = }")
        repo = info["repo"]
        branch = self.get_git_branch(repo)
        branches = self.get_git_branches(folder=repo, all=False, sensible=True)
        in_view = re.search(r"^views/.+", branch, flags=re.IGNORECASE)
        logger.debug(f"{repo = }, {branch = }, {branches = }, {in_view = }")

        # Note: Using a relative path to the repo is necessary as git-annex/git
        # doesn't see paths behind symlinks in the repo as tracked. So we need
        # to give it the actual absolute path in the repo
        # (see https://git-annex.branchable.com/bugs/Paths_behind_relative_symlinks_in_repo_don__39__t_work/)
        def path_for_git(path, repo=repo):
            repo = pathlib.Path(repo)
            objects_dir = (repo / ".git" / "annex" / "objects").resolve()
            p = pathlib.Path(path)
            # find the last link in the chain pointing to the actual annex
            while p.is_symlink():
                logger.debug(
                    f"{str(p)!r} is a symlink to {str(p.readlink())!r}"
                )
                if objects_dir in p.resolve().parents:
                    logger.debug(
                        f"{str(p)!r} is a git annex symlink "
                        f"pointing within {str(objects_dir)!r}"
                    )
                    # something dir in the path can still be a link, so we resolve the parent
                    return str(p.parent.resolve() / p.name)
                logger.debug(
                    f"following {str(p)!r} symlink to {str(p.readlink())!r}"
                )
                p = p.readlink()
            logger.debug(
                f"{str(p)!r} is no symlink, resolved path for git is {str(p.resolve())!r}"
            )
            return str(p.resolve())

        paths = [str(path_for_git(f.get_location().get_path())) for f in items]

        notify_flags = ["--notify-start", "--notify-finish"]
        if any(i.is_directory() for i in items) or len(items) > 10:
            logger.debug(
                f"Directory or too many files selected, "
                f"won't show desktop notifications"
            )
            notify_flags = []

        def on_click(menuitem, func=self.run_git_annex, **kwargs):
            kwargs = {
                **dict(
                    cwd=cwd,
                    title="{title} @ {repo}".format(
                        title=kwargs.get(
                            "title",
                            shlex.join(
                                ["git", "annex", kwargs.get("subcmd", "")]
                                + kwargs.get("args", [])
                            ),
                        ),
                        repo=pathlib.Path(repo).name,
                    ),
                ),
                **kwargs,
            }
            menuitem.connect(
                "activate",
                lambda item, *a, **kw: func(**kwargs),
            )

        # top-level Git Annex context menu entry
        git_annex_menuitem = Thunarx.MenuItem(
            name="ContextMenu::GitAnnex",
            label=_("Git Annex")
            + (" {}".format(_("(in view)")) if in_view else ""),
            tooltip=_("Git Annex File Synchronization"),
            icon="git-annex",
        )

        git_annex_sync_menuitem = Thunarx.MenuItem(
            name="ContextMenu::GitAnnexSync",
            label=_("Sync"),
            tooltip=_("Synchronize Git Annex state with other repos")
            + " (git annex sync{})".format(
                " {}".format("--only-annex") if in_view else ""
            ),
            icon="emblem-synchronizing",
        )
        on_click(
            git_annex_sync_menuitem,
            subcmd="sync",
            reset_before=False,
            add_before="all" if in_view else False,
            commit_before=in_view,
            args=["--only-annex"] if in_view else [],
        )

        git_switch_menuitem = Thunarx.MenuItem(
            name="ContextMenu::GitSwitch",
            label=_("Switch to Branch"),
            tooltip=_("Switch to different git branch"),
            icon="emblem-shared",
        )
        git_switch_submenu = Thunarx.Menu()
        git_switch_menuitem.set_menu(git_switch_submenu)
        for b in branches:
            if b == branch:
                continue
            menuitem = Thunarx.MenuItem(
                name="ContextMenu::GitSwitch",
                label=b,
                tooltip=_("Switch to git branch {!r}").format(b),
            )
            on_click(
                menuitem,
                func=self.run_cmd,
                cmdparts=(c := ["git", "switch", "--force", b]),
                terminal=False,
                notify=True,
                title=f"{shlex.join(c)} @ {pathlib.Path(repo).name}",
            )
            git_switch_submenu.append_item(menuitem)

        git_annex_add_menuitem = Thunarx.MenuItem(
            name="ContextMenu::GitAnnexAdd",
            label=_("Add"),
            tooltip=_("Add untracked files to Git Annex") + " (git annex add)",
            icon="list-add",
        )
        on_click(
            git_annex_add_menuitem,
            subcmd="add",
            paths=paths,
            reset_before=False,
            args=notify_flags,
        )

        git_annex_get_menuitem = Thunarx.MenuItem(
            name="ContextMenu::GitAnnexGet",
            label=_("Get"),
            tooltip=_("Retreve files with Git Annex") + " (git annex get)",
            icon="edit-download",
        )
        on_click(
            git_annex_get_menuitem,
            subcmd="get",
            paths=paths,
            reset_before=True,
            args=notify_flags,
        )

        git_annex_drop_menuitem = Thunarx.MenuItem(
            name="ContextMenu::GitAnnexDrop",
            label=_("Drop"),
            tooltip=_("Drop files safely with Git Annex")
            + " (git annex drop)",
            icon="edit-delete",
        )
        on_click(
            git_annex_drop_menuitem,
            subcmd="drop",
            paths=paths,
            reset_before=True,
            args=notify_flags,
        )

        git_annex_lock_menuitem = Thunarx.MenuItem(
            name="ContextMenu::GitAnnexLock",
            label=_("Lock"),
            tooltip=_(
                "Lock files with Git Annex. "
                "This saves disk space and is faster but makes them read-only."
            )
            + " (git annex lock)",
            icon="object-locked",
        )
        on_click(
            git_annex_lock_menuitem,
            subcmd="lock",
            paths=paths,
            reset_before=True,
        )

        git_annex_unlock_menuitem = Thunarx.MenuItem(
            name="ContextMenu::GitAnnexUnlock",
            label=_("Unlock"),
            tooltip=_(
                "Unlock files with Git Annex to make them editable. "
                "Increases disk usage and is slower."
            )
            + " (git annex unlock)",
            icon="object-unlocked",
        )
        on_click(
            git_annex_unlock_menuitem,
            subcmd="unlock",
            paths=paths,
            reset_before=True,
        )

        # Metadata submenu
        git_annex_metadata_menuitem = Thunarx.MenuItem(
            name="ContextMenu::GitAnnexMetadata",
            label=_("Metadata"),
            tooltip=_("Manipulate Git Annex Metadata"),
            icon="dialog-information",
        )
        git_annex_metadata_submenu = Thunarx.Menu()
        git_annex_metadata_menuitem.set_menu(git_annex_metadata_submenu)

        # cache rebuilding
        git_annex_metadata_rebuild_cache_menuitem = Thunarx.MenuItem(
            name="ContextMenu::GitAnnexMetadata::CacheRebuild",
            label=_("Build Metadata List"),
            tooltip=_(
                "Rebuild cache of Git Annex metadata to enable switching to views."
            ),
            icon="database-index",
        )
        git_annex_metadata_submenu.append_item(
            git_annex_metadata_rebuild_cache_menuitem
        )
        git_annex_metadata_rebuild_cache_menuitem.connect(
            "activate",
            lambda item, *a, **kw: self.rebuild_metadata_cache(path=cwd, **kw),
        )

        if in_view:
            menuitem = Thunarx.MenuItem(
                name=f"ContextMenu::GitAnnexMetadata::Vcycle",
                label=_("Cycle View"),
                tooltip=_("Cycle the view layers"),
                icon="object-rotate-left",
            )
            git_annex_metadata_submenu.append_item(menuitem)
            on_click(
                menuitem,
                subcmd="vcycle",
                terminal=False,
                notify=True,
            )
            menuitem = Thunarx.MenuItem(
                name=f"ContextMenu::GitAnnexMetadata::Vpop",
                label=_("Back to previous view"),
                tooltip=_("Go back to last view"),
                icon="edit-undo",
            )
            git_annex_metadata_submenu.append_item(menuitem)
            on_click(
                menuitem,
                subcmd="vpop",
                terminal=False,
                notify=True,
            )

        git_annex_metadata_view_menuitem = Thunarx.MenuItem(
            name="ContextMenu::GitAnnexMetadata::View",
            label=_("Add to View") if in_view else _("View"),
            tooltip=_("Modify current metadata-driven view")
            if in_view
            else _("Switch to a metadata-driven view"),
            icon="view-hidden",
        )
        git_annex_metadata_view_submenu = Thunarx.Menu()
        git_annex_metadata_view_menuitem.set_menu(
            git_annex_metadata_view_submenu
        )
        menuitem = Thunarx.MenuItem(
            name=f"ContextMenu::GitAnnexMetadata::View::**Folder**",
            label=_("Path"),
            tooltip=_(
                "Add the file's folder structure to the current metadata-driven view"
            )
            if in_view
            else _("Switch to a view that has the current folder structure."),
            icon="folder",
        )
        git_annex_metadata_view_submenu.append_item(menuitem)
        on_click(
            menuitem,
            subcmd=(c := "vadd" if in_view else "view"),
            args=(a := [f"/=*"]),
            terminal=False,
            notify=True,
        )
        if len(METADATA_CACHE[uuid]["/"]) > 0 or in_view:
            git_annex_metadata_submenu.append_item(
                git_annex_metadata_view_menuitem
            )

        if len(METADATA_CACHE[uuid]["/"]) > 0:
            for i, field in enumerate(METADATA_CACHE[uuid]["/"], start=1):
                logger.debug(f"{i = }, {field = }")
                menuitem = Thunarx.MenuItem(
                    name=f"ContextMenu::GitAnnexMetadata::View::{i}",
                    label=field,
                    tooltip=(
                        _(
                            "Add a {field} level to the current metadata-driven view"
                        ).format(field=field)
                        if in_view
                        else _(
                            "Switch to a metadata-driven view over field {field}"
                        )
                    ).format(field=repr(field)),
                    icon="view-hidden",
                )
                git_annex_metadata_view_submenu.append_item(menuitem)
                on_click(
                    menuitem,
                    subcmd=(c := "vadd" if in_view else "view"),
                    args=(
                        a := [
                            f"{field}?=*"
                            if "view-show-valueless"
                            in self.git_annex_capabilities()
                            else f"{field}=*"
                        ]
                    ),
                    terminal=False,
                    notify=True,
                )

        logger.debug(f"Assembling menus...")
        git_annex_submenu = Thunarx.Menu()
        git_annex_submenu.append_item(git_annex_sync_menuitem)
        if git_switch_submenu.get_items():
            git_annex_submenu.append_item(git_switch_menuitem)
        git_annex_submenu.append_item(git_annex_add_menuitem)
        git_annex_submenu.append_item(git_annex_get_menuitem)
        git_annex_submenu.append_item(git_annex_drop_menuitem)
        git_annex_submenu.append_item(git_annex_lock_menuitem)
        git_annex_submenu.append_item(git_annex_unlock_menuitem)
        git_annex_submenu.append_item(git_annex_metadata_menuitem)
        git_annex_menuitem.set_menu(git_annex_submenu)

        return (git_annex_menuitem,)

    def get_folder_menu_items(self, window, folder):
        return self.get_file_menu_items(window, [folder])


class GitAnnexProperties(
    GObject.GObject, Thunarx.PropertyPageProvider, GitAnnexHelper
):
    def __init__(self):
        logger.debug(f"{type(self).__name__} is initialized")

    @classmethod
    def name(cls):
        s = _("Git Annex Properties Page")
        if not shutil.which("git-annex"):
            s = _("[Unavailable]") + " " + s
        return s

    @classmethod
    def description(cls):
        s = _(
            "This plugin adds a properties page "
            "for managing Git Annex metadata."
        )
        if not shutil.which("git-annex"):
            s += " " + _(
                "Install Git Annex to use this plugin: "
                "https://git-annex.branchable.com"
            )
        return s

    @property
    def ui(self):
        try:
            return self._ui
        except AttributeError:
            self._ui = Gtk.Builder()
            self._ui.set_translation_domain(l10n.GETTEXT_DOMAIN)
            self._ui.add_from_file(
                pkg_resources.resource_filename(
                    "thunar_plugins.ui", "git-annex-properties.glade"
                )
            )

            handlers = {
                "readMetadata": self.readMetadata,
                "editMetadata": self.editMetadata,
                "metadataTextChanged": self.metadataTextChanged,
                "stopReadMetadata": self.stopReadMetadata,
            }
            self._ui.connect_signals(handlers)
        return self._ui

    def stopReadMetadata(self, *args, **kwargs):
        self._stopReadMetadata = True

    def editMetadata(self, widget, *args, **kwargs):
        field_entry = self.ui.get_object("git_annex_metadata_field_entry")
        value_entry = self.ui.get_object("git_annex_metadata_value_entry")
        if not (field := field_entry.props.text):
            return
        if not (value := value_entry.props.text):
            return
        optmakers = dict(
            git_metadata_set_button=lambda f, v: ["--set", f"{f}={v}"],
            git_metadata_add_button=lambda f, v: ["--set", f"{f}+={v}"],
            git_metadata_setdefault_button=lambda f, v: ["--set", f"{f}?={v}"],
            git_metadata_remove_button=lambda f, v: ["--set", f"{f}-={v}"],
            git_metadata_clear_button=lambda f, v: ["--remove", f],
        )
        for btnid, optmaker in optmakers.items():
            if widget is self.ui.get_object(btnid):
                cmdparts = (
                    [
                        "git",
                        "-C",
                        self.info["cwd"],
                        "annex",
                        "metadata",
                        "--force",
                    ]
                    + optmaker(field, value)
                    + self.paths
                )
                break
        if not cmdparts:
            logger.error(
                f"Don't know what to do with metadata {field = !r} {value = !r} from {widget = }"
            )
            return
        self.ui.get_object(
            "git_annex_metadata_edit_spinner"
        ).props.active = True
        with self.subprocess(subprocess.Popen, cmdparts) as proc:
            while (returncode := proc.poll()) is None:
                self.flush_gtk()
        image = self.ui.get_object("git_annex_metadata_edit_image")
        self.ui.get_object(
            "git_annex_metadata_edit_spinner"
        ).props.active = False
        if returncode == 0:
            image.props.icon_name = "dialog-ok"
            image.props.tooltip_text = None
        else:
            image.props.icon_name = "dialog-error"
            image.props.tooltip_text = _(
                "Error setting Git Annex metadata. "
                "The following command returned code {returncode}:\n\n{cmdline}"
            ).format(returncode=returncode, cmdline=shlex.join(cmdline))

    def metadataTextChanged(self, *args, **kwargs):
        """Make button sensitive iff text is set"""
        field_entry = self.ui.get_object("git_annex_metadata_field_entry")
        value_entry = self.ui.get_object("git_annex_metadata_value_entry")
        logger.debug(
            f"metadataTextChanged(): {field_entry.props.text = !r}, {value_entry.props.text = !r}"
        )
        field_ok = re.search(
            r"^[A-Z0-9_.-]+$", field_entry.props.text, flags=re.IGNORECASE
        )
        field_entry.props.primary_icon_name = (
            "gtk-dialog-error"
            if not field_ok and field_entry.props.text
            else None
        )
        for button in map(
            self.ui.get_object,
            (
                "git_metadata_set_button",
                "git_metadata_add_button",
                "git_metadata_setdefault_button",
                "git_metadata_remove_button",
                "git_metadata_clear_button",
            ),
        ):
            button.props.sensitive = value_entry.props.text and field_ok
        self.ui.get_object(
            "git_annex_metadata_edit_image"
        ).props.icon_name = None
        self.ui.get_object(
            "git_annex_metadata_edit_spinner"
        ).props.active = False

    @GitAnnexHelper.not_in_parallel
    def readMetadata(self, widget, *args, **kwargs):
        treestore = self.ui.get_object("git_annex_metadata_treestore")
        liststore = self.ui.get_object("git_annex_metadata_paths_liststore")
        treestore_filled = bool(treestore.iter_children(None))
        if treestore_filled and widget is not self.ui.get_object(
            "git_annex_read_metadata_button"
        ):
            # logger.debug(
            #     f"Not updating metadata because treestore is "
            #     "already filled and button was not clicked."
            # )
            return
        self._stopReadMetadata = False
        button = self.ui.get_object("git_annex_read_metadata_button")
        button.props.sensitive = False
        pbar = self.ui.get_object("git_annex_metadata_read_progressbar")
        treeview = self.ui.get_object("git_annex_metadata_treeview")
        treeview.props.sensitive = False
        metadata = defaultdict(Counter)
        n_files = 0
        with self.subprocess(
            subprocess.Popen,
            ["git", "-C", self.info["cwd"], "annex", "metadata", "--json"]
            + self.paths,
            stdout=subprocess.PIPE,
        ) as git_annex:
            for n_files, metadata_json_line in enumerate(
                git_annex.stdout, start=1
            ):
                if self._stopReadMetadata:
                    logger.info(f"🛑 Stop reading metadata")
                    git_annex.terminate()
                    break
                pbar.props.text = _("read metadata from {n} files").format(
                    n=n_files
                )
                pbar.pulse()
                self.flush_gtk()
                try:
                    metadata_json = json.loads(metadata_json_line)
                except json.JSONDecodeError as e:
                    logger.error(
                        f"git-annex returned weird JSON {metadata_json_line!r}: {e}"
                    )
                    continue
                if path := metadata_json.get("file"):
                    liststore.append([path])
                for field, values in metadata_json.get("fields", {}).items():
                    if not field.endswith("lastchanged"):
                        for value in values:
                            metadata[field][value] += 1

        pbar.props.fraction = 1
        self.flush_gtk()
        with console.status("Filling treeview..."):
            treestore.clear()
            for field, values in sorted(metadata.items()):
                fielditer = treestore.append(None, (field, None))
                for value, count in sorted(values.items()):
                    valueiter = treestore.append(
                        fielditer,
                        (_("{n} files").format(n=count) + " ⮕ ", value),
                    )
            treeview.expand_all()
        if logger.getEffectiveLevel() <= logging.DEBUG:
            logger.debug(f"metadata from {n_files} selected files: ")
            console.log(dict(metadata))
        button.props.sensitive = True
        treeview.props.sensitive = True

    @GitAnnexHelper.only_for_unique_git_annex_repo
    def get_property_pages(self, files, info):
        if hasattr(self, "_ui"):
            # necessary for some reason as the properties page is empty
            # otherwise 🤷
            del self._ui
        self.paths = [str(f.get_location().get_path()) for f in files]
        self.info = info
        if logger.getEffectiveLevel() <= logging.DEBUG:
            logger.debug(f"paths for git annex properties page:")
            console.log(self.paths)

        page_toplevel_box = self.ui.get_object(
            "git_annex_metadata_properties_page"
        )

        git_annex_page = Thunarx.PropertyPage.new(_("Git Annex"))
        git_annex_page.add(page_toplevel_box)
        return [git_annex_page]
