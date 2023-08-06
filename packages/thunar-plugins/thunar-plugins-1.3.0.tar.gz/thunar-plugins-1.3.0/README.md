# 🖱️ 🛠️ Thunar Plugins

This Python package extends the [Thunar file manager](https://docs.xfce.org/xfce/thunar/start) and provides a way for other Python packages to do the same without worrying about Thunar finding them.

## ✨ Features Added to Thunar

- ✅ a settings menu to en-/disable plugins added by this or other Python packages

- 🔗 creating links to a file or folder

- ☑️  Calculating various checksums of files

- 🗓️ *planned*: all features from [`thunar-custom-actions`](https://gitlab.com/nobodyinperson/thunar-custom-actions)

- 🔄 Basic [Git Annex](https://git-annex.branchable.com) support (`sync`,`get`,`drop`)


## 📦 Installation

![arch-logo](https://img.shields.io/badge/Arch-Linux-success?style=for-the-badge&logo=arch-linux)
![manjaro-logo](https://img.shields.io/badge/Manjaro-Linux-success?style=for-the-badge&logo=manjaro) 

If you are on an Arch-based Linux, you can install [the `python-thunar-plugins-git` package from the AUR](https://aur.archlinux.org/packages/python-thunar-plugins-git/):

```bash
# using yay, you may of course use your favourite AUR installer
pacman -Syu yay
yay -Syu python-thunar-plugins-git
```

In this case you might only have to restart Thunar to see the new plugins:

```bash
thunar -q
```

### Other Platforms: Installation from PyPI

#### ☝️ Prerequisites

For these Thunar plugins to work, you will need to have installed:

- [Thunar](https://gitlab.xfce.org/xfce/thunar) (obviously)
- [thunarx-python](https://gitlab.xfce.org/bindings/thunarx-python)



```bash
# Install this package from PyPI:
pip install thunar-plugins

# Install the latest development version:
pip install git+https://gitlab.com/nobodyinperson/thunar-plugins

# Install from the repository root
git clone https://gitlab.com/nobodyinperson/thunar-plugins
cd thunar-plugins
pip install .
```

> If that fails, try `python3 -m pip install --user ...` instead of just `pip install ...`


#### ⚡ Troubleshooting

- try `thunar -q` or log out and back in if the plugins aren't shown in Thunar
- run `thunar -q` and then `THUNARX_PYTHON_DEBUG=all THUNAR_PLUGINS_LOGLEVEL=debug thunar` to debug
- run `thunar-plugins activate` (or `python3 -m thunar_plugins activate`) to place the activator script (should be done upon installation)
- run `thunar-plugins deactivate` to deactivate plugins


## ➕ Adding More Plugins

This `thunar_plugins` package can act as a stepping stone for other packages
that add plugins to Thunar: The activator script loads all `thunar_plugin`
entry points provided by any installed Python package. So if another package
provides a Thunar plugin (e.g. a new context menu entry) with class
`mypackage.mymodule.mysubmodule.MyThunarPlugin`, that package may adjust its
`setup.cfg` like this and stop caring about how to tell Thunar where the plugin
can be found:

```ini
[options]
install_requires = thunar_plugins

[options.entry_points]
thunar_plugin =
    my-thunar-plugin = mypackage.mymodule.mysubmodule:MyThunarPlugin
```

> For proper display in the `thunar-plugins` settings dialog, every Python Thunar
> plugin class registered like this should also have a short `name` and a
> one-sentence `description` string attribute.
