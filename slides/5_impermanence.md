# impermanence

-v-

* während des Betriebs werden Konfigurationen sammeln sich weitere Konfigurationen an
* unbeabsichtigt (automatisch) oder beabsichtigt ("nur noch eben das eine Zertifikat runterladen")
* NixOS kann diese Konfigurationen nicht absichern, weil es diese Dateien nicht kennt

-v-

* Vorschlag von Graham Christensen [Erase your darlings](https://grahamc.com/blog/erase-your-darlings/) von 2020:
  * ausschließlich `/boot` und `/nix` zum booten benötigt
  * folglich alles andere löschen beim hochfahren
  * das Betriebssystem erlangt immer wieder einen Zustand wie nach einer kompletten Neuinstallation
  * jegliche Konfiguration wird erzwungen in nix zu hinterlegen

-v-

``` [5|8|13-14|19-20]
{
  description = "the nix config";
  inputs = {
    nixpkgs.url = "github:NixOs/nixpkgs/nixos-unstable";
    impermanence.url = "github:nix-community/impermanence";
  };

  outputs = { self, nixpkgs, impermanence, ... } @ inputs: {    
    nixosConfigurations.nixos = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [
        ./configuration.nix
        impermanence.nixosModules.impermanence
        ./impermanence.nix

        imports = [ home-manager.nixosModules.home-manager ];
        home-manager.users.username = { ... }: {
            imports = [
              impermanence.homeManagerModules.impermanence
              ./home/impermanence.nix
            ];
        };
    ];
  };
}
```

Note:

* erfordert das home-manager nicht als standalone module aktiviert ist

-v-

impermanence im System konfigurieren
``` [1|3-10|11-18]
environment.persistence."/persist" = {
  hideMounts = true;
  directories = [
    "/var/log"
    "/var/lib/bluetooth"
    "/var/lib/nixos"
    "/var/lib/systemd/coredump"
    "/etc/NetworkManager/system-connections"
    { directory = "/var/lib/colord"; user = "colord"; group = "colord"; mode = "u=rwx,g=rx,o="; }
  ];
  files = [
    "/etc/machine-id"
    "/etc/ssh/ssh_host_ed25519_key"
    "/etc/ssh/ssh_host_ed25519_key.pub"
    "/etc/ssh/ssh_host_rsa_key"
    "/etc/ssh/ssh_host_rsa_key.pub"
    { file = "/var/keys/secret_file"; parentDirectory = { mode = "u=rwx,g=,o="; }; }
  ];
};
```

-v-

impermanence in home-manager konfigurieren
```
  home.persistence."/persist/home/user" = {
    directories = [
      "Music"
      "Pictures"
      "Documents"
      "Videos"
      ".gnupg"
      ".ssh"
      ".local/share/keyrings"
      ".local/share/direnv"
    ];
    allowOther = true;
  };
```
-v-

Vor dem Boot aufräumen ([skript source](https://github.com/nix-community/impermanence?tab=readme-ov-file#btrfs-subvolumes))

```
  boot.initrd.postResumeCommands = lib.mkAfter ''
    mkdir /btrfs_tmp
    mount /dev/root_vg/root /btrfs_tmp
    if [[ -e /btrfs_tmp/root ]]; then
        mkdir -p /btrfs_tmp/old_roots
        timestamp=$(date --date="@$(stat -c %Y /btrfs_tmp/root)" "+%Y-%m-%-d_%H:%M:%S")
        mv /btrfs_tmp/root "/btrfs_tmp/old_roots/$timestamp"
    fi

    delete_subvolume_recursively() {
        IFS=$'\n'
        for i in $(btrfs subvolume list -o "$1" | cut -f 9- -d ' '); do
            delete_subvolume_recursively "/btrfs_tmp/$i"
        done
        btrfs subvolume delete "$1"
    }

    for i in $(find /btrfs_tmp/old_roots/ -maxdepth 1 -mtime +30); do
        delete_subvolume_recursively "$i"
    done

    btrfs subvolume create /btrfs_tmp/root
    umount /btrfs_tmp
  '';
```

-v-

```
{ lib, ... }: {
  boot.initrd.systemd.services.rollback = {
    description = "Rollback BTRFS root subvolume to a pristine state";
    wantedBy = [ "initrd-switch-root.target"];
    after = [ "sysroot.mount" ];
    requires = [ "cryptsetup.target" ];
    before = [ "initrd-switch-root.target" ];
    unitConfig.DefaultDependencies = "no";
    serviceConfig.Type = "oneshot";
    script = ''
      mkdir /btrfs_tmp
      # ... script source: https://github.com/nix-community/impermanence?tab=readme-ov-file#btrfs-subvolumes
      btrfs subvolume create /btrfs_tmp/root
      umount /btrfs_tmp
    '';
  };
}
```