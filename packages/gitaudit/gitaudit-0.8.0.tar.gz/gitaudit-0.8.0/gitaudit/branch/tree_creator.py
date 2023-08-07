"""Tree Creator
"""

import os
from typing import Optional, List, Callable

from pydantic import BaseModel

from gitaudit.git.controller import Git
from gitaudit.git.change_log_entry import ChangeLogEntry
from .serialization import load_log_from_file, save_log_to_file
from .tree import Tree
from .hierarchy import linear_log_to_hierarchy_log


class TreeCreatorConfig(BaseModel):
    """Tree Creator Config
    """
    consider_local_branches: bool = False
    consider_remote_branches: bool = True
    consider_tags: bool = True
    local_branch_filter_func: Callable[[str], bool] = lambda x: True
    remote_branch_filter_func: Callable[[str], bool] = lambda x: True
    tag_filter_func: Callable[[str], bool] = lambda x: True
    root_ref: Optional[str] = None


CACHE_PARENT_LOG_FOLDER_NAME = 'parent_log'
CACHE_CHANGE_LOG_FOLDER_NAME = 'change_log'


class TreeCreatorCache:  # pylint: disable=too-few-public-methods
    """Tree Creator Cache
    """

    def __init__(self, root_location: str) -> None:
        self.root_location = root_location
        self.parent_log_location = os.path.join(
            self.root_location, CACHE_PARENT_LOG_FOLDER_NAME)
        self.change_log_location = os.path.join(
            self.root_location, CACHE_CHANGE_LOG_FOLDER_NAME)

        os.makedirs(self.parent_log_location, exist_ok=True)
        os.makedirs(self.change_log_location, exist_ok=True)

    def get_parent_log(self, ref: str, git: Git) -> List[ChangeLogEntry]:
        """Get the parent log

        Args:
            ref (str): reference name
            git (Git): git controller

        Returns:
            _type_: _description_
        """
        head_sha = git.show_parentlog_entry(ref)
        ref_file_path = os.path.join(
            self.parent_log_location, f"{ref}...{head_sha}")

        if os.path.isfile(ref_file_path):
            log = load_log_from_file(ref_file_path)
            if log[0].sha == head_sha:
                return log

        # if we are here we need to call git
        log = linear_log_to_hierarchy_log(git.log_parentlog(ref))
        save_log_to_file(log, ref_file_path)

        return log


class TreeCreator:  # pylint: disable=too-few-public-methods
    """Tree Creator
    """

    def __init__(self, git: Git, config: TreeCreatorConfig, cache: TreeCreatorCache = None) -> None:
        self.git = git
        self.config = config
        self.cache = cache

    def _get_refs(self):
        refs = []

        refs.extend(filter(
            self.config.local_branch_filter_func,
            self.git.local_branch_names(),
        ))
        refs.extend(filter(
            self.config.remote_branch_filter_func,
            self.git.remote_branch_names(),
        ))
        refs.extend(filter(
            self.config.tag_filter_func,
            self.git.tags(),
        ))

        return refs

    def create_tree(self) -> Tree:
        """Create the tree

        Returns:
            Tree: Created Tree
        """
        refs = self._get_refs()

        if self.config.root_ref:
            assert self.config.root_ref in refs
            refs.pop(self.config.root_ref)
            refs.insert(0, self.config.root_ref)

        tree = Tree()

        for ref in refs:
            log = self.cache.get_parent_log(ref)
            tree.append_log(log, ref)

        return tree
