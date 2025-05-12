# Schatten

-v-

* miserable Dokumentation
* miserable Namenswahl: nix, NixOS, nixpkgs, flakes <!-- .element: class="fragment" -->
* Zersplitterung in der Community zu einzelnen Themen erschwert Dokumentation <!-- .element: class="fragment" -->
* keine best-practices oder Richtlinien wie die Konfiguration zu organisieren ist <!-- .element: class="fragment" -->
* NixOS/Nix kapselt Implementationsdetails nur mangelhaft <!-- .element: class="fragment" -->
* nixos-rebuild Fehler sind sehr schwer zu interpretieren  <!-- .element: class="fragment" -->
* wenn die Aktualisierung eines Pakets scheitert, scheitert die Aktualisierung des Gesamtsystems <!-- .element: class="fragment" -->  
* package pinning ist unnötig schwierig <!-- .element: class="fragment" -->

---

# Anhang

-v-

## Einstieg ins Thema

1) [yt: NixOS explained](https://www.youtube.com/watch?v=9OMDnZWXjn4)
2) [yt: nix flakes explained](https://www.youtube.com/watch?v=JCeYq72Sko0)
3) [yt: nix from the ground up](https://www.youtube.com/watch?v=5D3nUU1OVx8)

-v-

## Hilfe bei der ersten Installation

* [NixOS & Flakes Book](https://nixos-and-flakes.thiscute.world/preface)
  * [NixOS Wiki Flakes](https://nixos.wiki/wiki/Flakes)
* [Declarative gnome configuration with NixOS](https://determinate.systems/posts/declarative-gnome-configuration-with-nixos/)
* [nix package/options/flakes search](https://search.nixos.org)
* [home-manager](https://github.com/mipmip/home-manager-option-search)
  * [Home manager options search](https://home-manager-options.extranix.com/)

-v-

## Addons

* [nixos-hardware](https://github.com/NixOS/nixos-hardware): Sammlung von hardware quirks Einstellungen
* [impermanence](https://github.com/nix-community/impermanence)
  * [Erase your darlings](https://grahamc.com/blog/erase-your-darlings/): Artikel zur ursprünglichen Idee
  * [Nixos wiki: impermanence](https://nixos.wiki/wiki/Impermanence)
* [nixos-anywhere](https://github.com/nix-community/nixos-anywhere/): NixOS Installation via ssh
* [disko](https://github.com/nix-community/disko): deklarative Partionierung
* [lanzaboote](https://github.com/nix-community/lanzaboote): Secure Boot für NixOS

-v-

## NixOS Kritik

* Flakes:
  * [flakes aren't real and cannot hurt you](https://jade.fyi/blog/flakes-arent-real/)
  * [flakes is an experiment that did too much at once](https://samuel.dionne-riel.com/blog/2023/09/06/flakes-is-an-experiment-that-did-too-much-at-once.html)
* home-manager:
  * [dropping home manager](https://ayats.org/blog/no-home-manager): Artikel bzgl. der nervigen Eigenheiten von home-manager und Alternativen
  * [you may not need home manager](https://www.zaynetro.com/post/2024-you-dont-need-home-manager-nix#home-manager-pros): Abwägung der Vor- und Nachteile
* [NixOS is a good server OS, except when it isn’t](https://sidhion.com/blog/nixos_server_issues/): Artikel warum die minimale NixOS Größe bereits 900MB beträgt
* [Minimal containers using Nix](https://tmp.bearblog.dev/minimal-containers-using-nix/): NixOS als base image layer verglichen mit alpine
  * https://xeiaso.net/blog/i-was-wrong-about-nix-2020-02-10/

-v-

## Vertiefung

* theoretische Grundlagen von Eelco Dolstra
    * [Paper zur Motivation des Forschungsthemas](https://edolstra.github.io/pubs/iscsd-scm11-final.pdf) (2003)
    * [Doktorarbeit von Eelco Dolstra](https://edolstra.github.io/pubs/phd-thesis.pdf) (2006)
* vimjoyer's videos zum Thema NixOs:
  * [Modularisierung der NixOS Konfiguration](https://www.youtube.com/watch?v=vYc6IzKvAJQ)
  * [Gaming in NixOS](https://www.youtube.com/watch?v=qlfm3MEbqYA)
  * [NixOS mit Flakes und Home Manager](https://www.youtube.com/watch?v=a67Sv4Mbxmc)
* [nix-direnv](https://determinate.systems/posts/nix-direnv/) (determinate.systems hat noch weitere sehr interessante Artikel zum Thema Nix)
* [Secure Boot & Full Disk Encryption on NixOS with TPM2 unlock](https://jnsgr.uk/2024/04/nixos-secure-boot-tpm-fde/)
  * [Bypassing disk encryption on systems with automatic TPM2 unlock](https://oddlama.org/blog/bypassing-disk-encryption-with-tpm2-unlock/)
* kuratierte Link Liste: [awesome-nix](https://github.com/nix-community/awesome-nix)