# Definition of spreadsheet column names, default data and other attributes
OUTPUT_HEADERS_DEFAULTS = {
    "name": {
        "default": "",
        "type": str,
        "label": "Name"
    },
    "owner": {
        "default": "",
        "type": str,
        "label": "Owner"
    },
    "pull_y_n": {
        "default": "",
        "type": str,
        "label": "Pull (Y/N)"
    },
    "pull_target": {
        "default": "",
        "type": str,
        "label": "Pull Target"
    },
    "notes": {
        "default": "",
        "type": str,
        "label": "Notes"
    },
    "empty": {
        "default": False,
        "type": bool,
        "label": "Empty"
    },
    "archived": {
        "default": False,
        "type": bool,
        "label": "Archived"
    },
    "fork": {
        "default": False,
        "type": bool,
        "label": "Fork"
    },
    "description": {
        "default": "",
        "type": str,
        "label": "Description"
    },
    "fork_count": {
        "default": 0,
        "type": int,
        "label": "Forks"
    },
    "open_issues": {
        "default": 0,
        "type": int,
        "label": "Open Issues"
    },
    "last_updated": {
        "default": "",
        "type": str,
        "label": "Last Updated"
    },
    "url": {
        "default": "",
        "type": str,
        "label": "URL"
    },
    "default_branch": {
        "default": "",
        "type": str,
        "label": "Default Branch"
    },
    "branch_list": {
        "default": "",
        "type": str,
        "label": "Branch List"
    },
    "release_tags": {
        "default": 0,
        "type": int,
        "label": "Release Tags"
    },
    "latest_tag": {
        "default": "",
        "type": str,
        "label": "Latest Tag"
    }
}