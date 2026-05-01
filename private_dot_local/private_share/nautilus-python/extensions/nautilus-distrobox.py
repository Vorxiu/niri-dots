from gi.repository import Nautilus, GObject
from typing import List
from subprocess import run, check_output
from shutil import which

if not which("distrobox"):
    raise ImportError("distrobox not found")

preferred_terminal = "kitty"
Terminal = ""
Terminals = ["ghostty", "kitty", "alacritty", "ptyxis", "wezterm", "foot"]

if which(preferred_terminal) is not None:
    Terminal = preferred_terminal
else:
    for terminal in Terminals:
        if which(terminal) is not None:
            Terminal = terminal
            break

def get_distroboxes() -> List[str]:
    try:
        out = check_output(["distrobox", "list", "--no-color"], text=True)
        lines = out.strip().splitlines()[1:]
        return [line.split("|")[1].strip() for line in lines if "|" in line]
    except Exception:
        return []

class DistroboxExtension(GObject.GObject, Nautilus.MenuProvider):
    """Opens selected directory in a distrobox container."""
    def _open_in_box(self, menu: Nautilus.MenuItem, box: str, path: str) -> None:
        run(
            [Terminal, "--", "distrobox", "enter", box, "--",
             "bash", "-c", f"cd {path!r} && exec $SHELL"],
            shell=False,
        )

    def get_background_items(
        self,
        current_folder: Nautilus.FileInfo,
    ) -> List[Nautilus.MenuItem]:
        if current_folder.get_uri_scheme() != "file":
            return []

        path = current_folder.get_uri()[len("file://"):]
        boxes = get_distroboxes()

        items = []
        for box in boxes:
            item = Nautilus.MenuItem(
                name=f"Nautilus::open_in_distrobox_{box}",
                label=f"Open in {box}",
            )
            item.connect("activate", self._open_in_box, box, path)
            items.append(item)

        return items

    def get_file_items(
        self,
        files: List[Nautilus.FileInfo],
    ) -> List[Nautilus.MenuItem]:
        return []