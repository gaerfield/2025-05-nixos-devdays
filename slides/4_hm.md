# home-manager

-v-

* `home-manager` erweitert die NixOS Prinzipien auf das User-profile
* erlaubt Konfiguration von:
    * dotfiles
    * shell
    * Installation von Applikationen nur für den einzelnen User

-v-

flake hinzufügen

``` [5-8|16-20]
{
  description = "the nix config";
  inputs = {
    nixpkgs.url = "github:NixOs/nixpkgs/nixos-unstable";
    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, home-manager, ... } @ inputs: {    
    nixosConfigurations.nixos = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [
        ./configuration.nix
        home-manager.nixosModules.home-manager {
            home-manager.useGlobalPkgs = true;
            home-manager.useUserPackages = true;
            home-manager.users.theUser = ./home.nix;
        }
    ];
  };
}
```

-v-

```
{ pkgs, ... }: {
  programs.fish = {
    enable = true;
    functions = {
      emo-shrug = { description = "¯\_(ツ)_/¯"; body = "echo '¯\_(ツ)_/¯' | wl-copy";};
      jwt-decode = {
        description = "cat jwtToken | jwt-decode";
        body = "jq -R 'split(\".\") | select(length > 0) | .[0],.[1] | @base64d | fromjson'";
      };
    };

    shellAbbrs = {
      scan-network = {
        expansion = "nmap -sV -open -oG scan-result.log -p %22 172.20.0.0/24";
        setCursor = true;
      };
    };
  };
}
```

-v-

[Declarative gnome configuration with NixOS](https://determinate.systems/posts/declarative-gnome-configuration-with-nixos/)

```
  dconf = {
    enable = true;

    settings = {
      # subpixel anti-aliasing (best for LCD's)
      "org/gnome/desktop/interface".font-antialiasing = "rgba";
      "org/gnome/desktop/peripherals/mouse".natural-scroll = true;
      "org/gnome/desktop/peripherals/touchpad".tap-to-click = true;

      "org/gnome/desktop/interface".enable-hot-corners = false;
      "org/gnome/mutter/keybindings" = {
        toggle-tiled-left=["<Alt><Super>Left"];
        toggle-tiled-right=["<Alt><Super>Right"];
      };
      ...
    };
  };
```

-v-

Installation von Applikationen nur für den einzelnen User
```
home.packages = with pkgs; [
    alacritty
    grc
    lazygit
    lazydocker
    zip
    unzip
]
```

Note:

* NixOS Konfiguration so schlank wie möglich halten
* Verringerung der Angriffsfl์äche

-v-

* Nachteile
  * Konfigurationen von Applikationen aus nixpkgs inkompatibel mit home-manager (Beispiel firefox)
  * nutzt man home-manager für dotfiles sind diese immutable
    * entweder akzeptieren
    * oder symlinks nutzen: [the home manager function that changes everything](https://jeancharles.quillet.org/posts/2023-02-07-The-home-manager-function-that-changes-everything.html)
    * oder dotfiles nicht mit home-manager managen (alternativ GNU Stow)

Note:

Kompletter Verzicht auf HM finde ich unsinnig:
* programmspezifische Konfiguration (firefox)
* dconf-Gnome
* userspezifische systemd services
* shell-Konfigurationen in Nix Expression Language einfacher