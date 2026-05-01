from subprocess import run
from typing import List

from gi.repository import GObject, Nautilus

# TODO: Multi-monitor support

SUPPORTED_FORMATS = "image/jpeg", "image/png", "image/jxl"
BACKGROUND_KEY = "picture-uri"

wall_cmd = "qs -c noctalia-shell ipc call wallpaper set -- "

# wall_cmd = "noctalia msg wallpaper set -- "


class BackgroundImageExtension(GObject.GObject, Nautilus.MenuProvider):
    def menu_activate_cb(
        self,
        menu: Nautilus.MenuItem,
        file: Nautilus.FileInfo,
    ) -> None:
        if file.is_gone():
            return
        run(wall_cmd + file.get_uri()[7:], shell=True)

    def get_file_items(
        self,
        files: List[Nautilus.FileInfo],
    ) -> List[Nautilus.MenuItem]:

        if len(files) != 1:
            return []

        file = files[0]

        if not file.get_mime_type() in SUPPORTED_FORMATS:
            return []

        if file.get_uri_scheme() != "file":
            return []

        item = Nautilus.MenuItem(
            name="Nautilus::set_background_image",
            label="Set as Wallpaper...",
        )
        item.connect("activate", self.menu_activate_cb, file)

        return [
            item,
        ]

    def get_background_items(
        self,
        current_folder: Nautilus.FileInfo,
    ) -> List[Nautilus.MenuItem]:
        return []
