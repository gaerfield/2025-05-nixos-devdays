# NixOS

{{slides/1_me.md}}
{{slides/2_nixos_high_level.md}}

---

# What is NixOS?

Let's head to [nixos.org](https://nixos.org)
<iframe src="https://nixos.org" width="1500" height="550" loading="lazy" referrerpolicy="no-referrer-when-downgrade"> </iframe> 

-v-

# Wha ... ?

* NixOS
* Nix package manager
* Nix expression language

-v-

Nix* related docs are crap

---

# What is NixOS?

An operating system featuring:
* atomic upgrades
* rollbacks <!-- .element: class="fragment" -->
* a fully declarative configuration model <!-- .element: class="fragment" -->

-v-

* declaritive configuration brought me to nixos ... my dotfiles where somewhat broken
    * reproducible OS states
    * identical configuration across multiple machines

-v-

* what I got additionally
    * atomic upgrades = either an upgrade works or fails completely, no partial upgrades
    * if misconfigured something, I can rollback to any state in history
    * reproducible operating system

-v-

* how does it work? - configuration.nix

-v-

* /nix/store

-v-

* but the user directory is still broken: home-manager

---

# things I want to cover

* the basics rergarding nix store
* the relation to the doctor thesis
* flakes
* nixos-anywhere
* things I want to link
  * 