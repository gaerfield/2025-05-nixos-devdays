# Lanzaboote: Secure Boot for NixOS

-v-

* UEFI secure boot nutzen um ausschließlich vertrauenswürdige Kernel zu booten
* lanzaboote signiert Treiber und Kernel während `nixos-rebuild`

Note:

BIOS Passwort muss gesetzt sein

-v-

Vorgehen hier nur angerissen:
* nutze `sbctl` zur Generierung von keys
* die erzeugten keys werden `nixos-anywhere` in extra-files zur Verfügung gestellt
* nach der Installation im BIOS Secure Boot in den Setup Mode versetzen (unterschiedlich je nach Hersteller)
* in NixOS booten und eigene erstellte keys in das TPM einspielen
* im BIOS Secure Boot wieder aktivieren

-v-

* [lanzaboote: quick start](https://github.com/nix-community/lanzaboote/blob/master/docs/QUICK_START.md)
* [secure boot on framework laptop](https://0xda.de/blog/2024/06/framework-and-nixos-secure-boot-day-three/)
