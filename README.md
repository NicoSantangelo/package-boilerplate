# Sublime Text Package Boilerplate

Template and helpers for creating sublime text packages.

## Usage

### New package

If you run `Package Boilerplate: New package` PackageBoilerplate will ask you for a command name, for example `MyFirstCommand` and then will create all the files from the skeleton placing them on the [packages path](https://github.com/NicoSantangelo/package-boilerplate#packages_path).

### Add support

This command will list a series of support options (like adding tests to your command). If you want to know more, you can choose `What's this?` on the displayed options.

## Settings

The file `PackageBoilerplate.sublime-settings` is used for configuration, you can change your user settings in `Preferences -> Package Settings -> PackageBoilerplate -> Settings - User`.

The defaults are:

````json
{
    "packages_path": "",
    "base_package_structure_path": ""
}
````

#### packages_path

Customize the location of the directory where the package files will be created. By default it uses the `Sublime` package folder (you can find it in `Preferences -> Browse packages...`).


#### base_package_structure_path

Customize the path to the skeleton to be used to generate the package files.  By default it uses the skeleton provided by this package (see it here: [skeleton](https://github.com/NicoSantangelo/package-boilerplate/tree/master/skeleton)).


## Shortcut Keys

You can use a shortcut for running a command like this:
````json
{
    "keys": ["KEYS"], "command": "package_boilerplate_new_package", 
    "keys": ["KEYS"], "command": "package_boilerplate_support" 
}
````


## Installation

### Manual

You can clone the repo in your `/Packages` (*Preferences -> Browse Packages...*) folder and start using/hacking it.
    
    cd ~/path/to/Packages
    git clone git://github.com/NicoSantangelo/package-boilerplate.git PackageBoilerplate