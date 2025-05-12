# Theorie

-v-

Eelco Dolstra veröffentlichte 2006 seine PhD Thesis

[The Purely Functional Software
Deployment Model](https://edolstra.github.io/pubs/phd-thesis.pdf) 

Note:

Grundlage für nix, nixpkgs und letztendlich NixOS

-v-

verteilen einer Applikation **ohne Quellcode** ist fragil / fehleranfällig:
* Applikation häufig nur als Binary verfügbar
* kompiliert ausschließlich für eine konkrete Architektur
* sind sehr häufig abhängig von dynamische gelinkten Bibliotheken in einer konkreten Version

-v-

verteilen einer Applikation **bei vorhanden Quellcode** ist fragil / fehleranfällig:
* robuster dank der verfügbaren Buildskripte
* aber:
  * Versionen der Compiler können sich unterscheiden
  * dynamisches Linking ist immer noch ein Problem
  * jede Maschine muss für sich den Quellcode kompilieren

-v-

* Eelco entwickelte eine DSL, die "Nix expression language"
  * Turingvollständige funktionale Sprache
  * erlaubt die Definition der Build-Instruktionen
  * sind Betriebssystem und Architektur identisch, <br/>dann garantiert nix die Erstellung desselben binaries

-v-

* die erste Besonderheit dieser DSL liegt in der Auflösung der Dateipfade: 
  * der Pfad `/run/current-system/sw/bin/curl`
  * ist am Ende tatsächlich: 
```
nix-repl> builtins.toString "${/run/current-system/sw/bin/curl}"
"/nix/store/1d41jki2y57slqw72zcvbkvg5bfrvi9f-curl"
```

-v-

```
> builtins.toString "${/run/current-system/sw/bin/curl}"
"/nix/store/1d41jki2y57slqw72zcvbkvg5bfrvi9f-curl"
```

* jede Datei einer nix expression wird:
  * in den `/nix/store` kopiert
    * wird read-only gesetzt
    * erhält einen sha-256 hash prefix
    * und einen lesbaren Namen
  * `/nix/store` ist dadurch ein assoziativer unveränderlicher Speicher
  * Details in: chapter 5 - the extensional model

Note:

content addressable immutable store
ähnlich .git/objects: für beliebigen content bekommt man eine eindeutige Adresse geliefert

-v-

die zweite Besonderheit sind "derivations" (chapter 6 - the intensional model):

```
derivation {
  name = "my-hello-world";
  system = "aarch64-darwin";
  src = ./main.c;
  builder = "/bin/bash";
  args = ["-c" ''
    /usr/bin/clang $src -o $out
  '']
}
```

-v-

<div class="multicolumn">

<div>

``` [7]
derivation {
  name = "my-hello-world";
  system = "aarch64-darwin";
  src = ./main.c;
  builder = "/bin/bash";
  args = ["-c" ''
    /usr/bin/clang $src -o $out
  '']
}
```

* die Derivation ist "impure" da externe Abhängigkeiten notwendig sind <!-- .element: class="fragment" -->

</div>

<div>

```language-plantuml
scale 2
rectangle "build machine" {
  folder "nix store" {
    component "my-hello-world" as mhw
  }
  component clang as clang

  mhw -> clang
}
```

</div>

</div>

-v-

<div class="multicolumn">

<div>

```
derivation {
  name = "clang-16"
  system = "aarch64-darwin"
  src = builtins.fetchTarball {
      url = "https://github.com/.../clang-16.0.0.src.tar.gz"
      sha256 = "..."
  }
  builder = "/bin/bash"
  args = ["-c" ''
    # ... build script to build clang
  '']
}
```

```
derivation {
  name = "my-hello-world";
  system = "aarch64-darwin";
  src = ./main.c;
  builder = "/bin/bash";
  clang = import ./clang.nix
  args = ["-c" ''
    /usr/bin/clang $src -o $out
  '']
}
```

</div>

<div>

```language-plantuml
scale 2
rectangle "build machine" {
  folder "nix store" {
    component "my-hello-world" as mhw
    component clang as clang
  }
  
  clang <-- mhw
}
```

* einbetten weiterer derivations um "pure"ness zu erreichen <!-- .element: class="fragment" -->

</div>

</div>

Note:

* Einbettung der derivations baut sog. Merkle Tree auf, ein Hash Tree
* Änderung eines Knotens im Tree resultiert in veränderten hash des Rootknotens
* im Ergebnis laufen derivations in ihrer eigenen sandbox mit exakt definierten Abhängigkeiten 

-v-

* in der Folge enthält der nix store verschiedene Versionen derselben Applikation:

```bash
> ls /nix/store | grep "curl.*bin" | head
0x15walkqqqqghryk1fh5aq8bq93kf26-curl-8.11.0-bin
16g6gyg131k8vgna13ilb4v9msh5fmi9-curl-8.12.1-bin
2sahizqb40sc224kyavf56v9i1zxcmvi-curl-8.9.0-bin
6isq33b7wqwwq1jarzs39nmxx3w5ii4m-curl-8.8.0-bin
9is21wm88vjn60iz883y06b8smv6ayjw-curl-8.8.0-bin
```

-v-


<div class="multicolumn">

<div>

``` [4]
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

</div>

<div>

* nixpkgs ist eine Sammlung solcher derivations
* die Binaries dieser derivations werden in "cache.nixos.org" geteilt
* i.d.R wird ein Binary von dort runtergeladen
* detaillierter: [yt: nix from the ground up](https://www.youtube.com/watch?v=5D3nUU1OVx8)


</div>

</div>

