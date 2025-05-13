# Flakes

-v-

während Installation werden zwei Dateien erstellt:

* `/etc/nixos/hardware-configuraton.nix`
* `/etc/nixos/configuration.nix`

-v-

```
{ config, lib, pkgs, modulesPath, ... }:

{
  imports =
    [ (modulesPath + "/profiles/qemu-guest.nix")
    ];

  boot.initrd.availableKernelModules = [ "ahci" "xhci_pci" "virtio_pci" "virtio_scsi" "sr_mod" "virtio_blk" ];
  boot.initrd.kernelModules = [ ];
  boot.kernelModules = [ "kvm-intel" ];
  boot.extraModulePackages = [ ];
  networking.useDHCP = lib.mkDefault true;
  nixpkgs.hostPlatform = lib.mkDefault "x86_64-linux";
}
```

Note:

`hardware-configuration.nix` ist automatisch generiert anhand der detektierten Hardware


-v-

```
{ modulesPath, lib, pkgs, ... } : {
  imports = [
    ./hardware-config.nix
  ];
  config = {
    services.openssh.enable = true;
    boot.loader.systemd-boot.enable = true;
    boot.loader.efi.canTouchEfiVariables = true;

    networking.hostName = "nixos";
    networking.networkmanager.enable = true;
    services.xserver = {
      layout = "de";
      xkbVariant = "nodeadkeys";
    };
    console.keyMap = "de-latin1-nodeadkeys";

    programs = {
      chromium.enable = true;
      fish.enable = true;
    };
    
    # https://nixos.wiki/wiki/FAQ/When_do_I_update_stateVersion
    system.stateVersion = "23.11"; # Did you read the comment?
  };
}
```

Note:

* `configuration.nix` enthält die anfängliche Default-Konfiguration von der ausgehend alles individualisiert wird

-v-

* nach Installation beide Dateien irgendwo anders hin kopieren, z.B. `~/nixos-config`
* und aktiviert flakes

-v-

* flakes sind quasi ein Standard
* wurden 2021 eingeführt
* haben noch immer experimentellen Status
* müssen daher explizit aktiviert werden

-v-

* sehr vereinfacht dargestellt: flakes sind Module
* sie erleichtern in vielen Fällen die Benutzung von NixOS (u.a. beim package pinning)
* sie haben Schwächen:
  * [flakes aren't real and cannot hurt you](https://jade.fyi/blog/flakes-arent-real/)
  * [flakes is an experiment that did too much at once](https://samuel.dionne-riel.com/blog/2023/09/06/flakes-is-an-experiment-that-did-too-much-at-once.html)

-v-

> Nix flakes provide a standard way to write Nix expressions (and therefore packages) whose dependencies are version-pinned in a lock file, improving reproducibility of Nix installations.
>
> [https://nixos.wiki/wiki/Flakes](https://nixos.wiki/wiki/Flakes)

Note:

Nix expression language ist die Sprache in der Konfigurationsfiles verfasst sind

-v-

configuration.nix anpassen:

```
nix.settings.experimental-features = [ "nix-command" "flakes" ];
```

-v-

* `flake.nix` in `~/nixos-config` anlegen

``` [4, 8, 11]
{
  description = "the nix config";
  inputs = {
    nixpkgs.url = "github:NixOs/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, ... } @ inputs: {
    nixosConfigurations.myHost = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [
        ./configuration.nix
    ];
  };
}
```

-v-

* `flake.nix` in `~/nixos-config` anlegen

``` [4, 8, 11]
{
  description = "the nix config";
  inputs = {
    nixpkgs.url = "github:NixOs/nixpkgs/nixos-24.11";
  };

  outputs = { self, nixpkgs, ... } @ inputs: {
    nixosConfigurations.myHost = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [
        ./configuration.nix
    ];
  };
}
```

-v-

* `nix flake lock` erstellt das Lockfile `flack.lock`
* `nix flake update` aktualisiert das Lockfile

```
{
  "nodes": {
    "nixpkgs": {
      "locked": {
        "lastModified": 1745234285,
        "narHash": "sha256-GfpyMzxwkfgRVN0cTGQSkTC0OHhEkv3Jf6Tcjm//qZ0=",
        "owner": "NixOs",
        "repo": "nixpkgs",
        "rev": "c11863f1e964833214b767f4a369c6e6a7aba141",
        "type": "github"
      },
      "original": {
        "owner": "NixOs",
        "ref": "nixos-unstable",
        "repo": "nixpkgs",
        "type": "github"
      }
    },
  "root": "root",
  "version": 7
}
```

-v-

`sudo nixos-rebuild --flake` ausführen

Note:

* ich würde die Konfiguration auch umgehend in git versionieren und pushen
* stolperfalle git:
  * falls kein git-repo = alles ok
  * falls git-repo und alle files geadded = alles ok
  * falls git-repo und file nicht geadded = nix IGNORIERT DAS FILE KOMPLETT
* [nix flakes explained](https://www.youtube.com/watch?v=JCeYq72Sko0)

-v-

* development environments mit `.envrc` und flakes:

``` [3, 210-217]
{
  description = "Minimal example of building Kotlin with Gradle and Nix";
  inputs = { nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable"; };
  inputs.systems.url = "github:nix-systems/default";

  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.flake-utils.inputs.systems.follows = "systems";

  outputs = { self, systems, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        updateLocks = pkgs.callPackage ./update-locks.nix { };
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pkgs.gradle_8
            pkgs.temurin-bin-21
            updateLocks
            pkgs.ktlint
          ];
        };
        packages.default = pkgs.callPackage ./build.nix { };
      });
}
```