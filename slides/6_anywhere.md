# nixos-anywhere

-v-

* `nixos-rebuild` erlaubt die Trennung von Build- und Targethost
* Build auf potenter Hardware oder regelmäßig in CI/CD pipelines
* Ergebnis auf einspielen auf dem Target via ssh

-v-

* nixos-anywhere erweitert das Prinzip
* nutzt [kexec](https://en.wikipedia.org/wiki/Kexec) und [disko](https://github.com/nix-community/disko) um remote NixOS aufzusetzen

Note:

Schritt weg von der Konfiguration einer einzelnen Maschine zur Konfiguration von einer beliebigen Menge von Maschinen

-v-

* NixOS image booten
* public key hinzufügen

```
mkdir -p .ssh && echo ssh-ed25519 AAAAC... > .ssh/authorized_keys
```
-v-

* nixos-anywhere Installation durchführen lassen

```
nix run github:nix-community/nixos-anywhere -- \
  --extra-files ./extra-files \
  --disk-encryption-keys /tmp/secret.key /tmp/secret.key \
  --flake .#myHost nixos@192.168.122.27
```

-v-

```
nix run github:nix-community/nixos-anywhere -- \
  --extra-files ./extra-files \
  --disk-encryption-keys /tmp/secret.key /tmp/secret.key \
  --flake .#myHost nixos@192.168.122.27
```

* `./extra-files` Dateistruktur die 1:1 nach root des Ziels kopiert werden
  * bspw. die Passwörter für die User durch setzen der Konfiguration: <br />
    `users.users.gaerfield.hashedPasswordFile = "/persist/passwords/username";`
  * Erzeugung mit <br />
    `mkpasswd -m sha-512 thePassword > ./extra-files/persist/passwords/username`
* `/tmp/secret.key` beinhaltet den encryption-key für die Verschlüsselung der Partitionen
* `--flake .#myHost` welche Konfiguration eingespielt werden soll
* `nixos@192...` der Host auf den mittels ssh die Installation durchgeführt wird

Note:

durch "nix run" wird nixos-anywhere nicht installiert sondern einfach ausgeführt

-v-

* nixos-anywhere wird einmalig ausgeführt
* im Falle von rebuilds wir `--target-host` gesetzt
* quirks: das sudo Passwort wird drei mal abgefragt
```
nixos-rebuild --flake .#myHost --target-host 192.168.122.27 --use-remote-sudo switch
```

-v-

Partitionskonfiguration:
``` [6|10-23|30|38|42-68|72]
{
  disko.devices = {
    disk = {
      vda = {
        type = "disk";
        device = "/dev/vda";
        content = {
          type = "gpt";
          partitions = {
            ESP = {
              label = "boot";
              name = "ESP";
              size = "512M";
              type = "EF00";
              content = {
                type = "filesystem";
                format = "vfat";
                mountpoint = "/boot";
                mountOptions = [
                  "defaults"
                ];
              };
            };
            luks = {
              size = "100%";
              label = "luks";
              content = {
                type = "luks";
                name = "cryptroot";
                passwordFile = "/tmp/secret.key";
                extraOpenArgs = [
                  "--allow-discards"
                  "--perf-no_read_workqueue"
                  "--perf-no_write_workqueue"
                ];
                # https://0pointer.net/blog/unlocking-luks2-volumes-with-tpm2-fido2-pkcs11-security-hardware-on-systemd-248.html
                # settings = {crypttabExtraOpts = ["fido2-device=auto" "token-timeout=10"];};
                settings = {crypttabExtraOpts = ["tpm2-device=auto" "tpm2-measure-pcr=yes"];};
                content = {
                  type = "btrfs";
                  extraArgs = ["-L" "nixos" "-f"];
                  subvolumes = {
                    "/root" = {
                      mountpoint = "/";
                      mountOptions = ["subvol=root" "compress=zstd" "noatime"];
                    };

                    "/persist" = {
                      mountpoint = "/persist";
                      mountOptions = ["subvol=persist" "compress=zstd" "noatime"];
                    };
                    
                    "/nix" = {
                      mountpoint = "/nix";
                      mountOptions = ["subvol=nix" "compress=zstd" "noatime"];
                    };
                    
                    "/swap" = {
                      mountpoint = "/swap";
                      swap.swapfile.size = "8G";
                    };
                  };
                };
              };
            };
          };
        };
      };
    };
  };

  fileSystems."/persist".neededForBoot = true;  
}
```

