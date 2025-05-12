Note:

stellt euch vor, ihr könntet das gesamte OS konfigurieren

-v-

```
environment.systemPackages = with pkgs; [
    neovim
    git
    python314
    jq
    digikam
];
```

Note:

Programme

-v-

```
programs.firefox = {
    enable = true;
    policies = {
        DisableTelemetry = true;
        ExtensionSettings = {
        "uBlock0@raymondhill.net" = {
            install_url = "https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/latest.xpi";
            installation_mode = "force_installed";
        };
        };
        Preferences = { 
        "browser.contentblocking.category" = { Value = "strict"; Status = "locked"; };
        "extensions.pocket.enabled" = { Value = false; Status = "locked"; };
        };
    };
};
```

Note:

Einstellungen der Programme

-v-

```
{
  services.avahi.enable = false;
  networking.nameservers = [ "1.1.1.1#cloudflare-dns.com" "2606:4700:4700::1111#cloudflare-dns.com" ];
  services.resolved = {
    enable = true;
    dnssec = "allow-downgrade";
    domains = [ "~." ];
    fallbackDns = [
      "1.0.0.1#cloudflare-dns.com"  "2606:4700:4700::1001#cloudflare-dns.com"
    ];
    dnsovertls = "opportunistic"; # allow fallback for corporate machines
    llmnr = "false";
    extraConfig = ''
      MulticastDNS=true
    '';
  };
}
```

Note:

Systemkonfigurationen

-v-

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

Note:

Konfiguration der UI-Shell

-v-

```
environment.systemPackages = with pkgs; [
    neovim
    git
    python314
    jq
    digikam
];
```

Notes:

Änderungen an der Konfiguration würden nie vergessen werden, denn sie sind dokumentiert.


-v-

```
environment.systemPackages = with pkgs; [
    neovim
    git
    jq
    digikam
];
```

Notes:

Das Entfernen einer Einstellung wäre schlicht das Anpassen eines Textes

-v-

* 💻 Laptops    
* 📂 NAS <!-- .element: class="fragment" -->
* 🖥️ Daddel-Maschine <!-- .element: class="fragment" -->

Notes:

Die Einstellungen könnten einfach auf verschiedene Rechner verteilt und synchron gehalten werden.
Überall das gleiche Setup

-v-

![](./img/1/nixos.svg)

-v-

NixOS ist eine Linux Distribution mit folgenden Eigenschaften:
* rein deklarative Konfiguration <!-- .element: class="fragment" -->
* Immutability <!-- .element: class="fragment" -->
* atomare Upgrades <!-- .element: class="fragment"  -->
* Rollbacks <!-- .element: class="fragment" -->

-v-

```language-plantuml
skinparam {
  backgroundColor #002b36
  ArrowColor #93a1a1
  ArrowFontColor #93a1a1
  sequenceLifeLineBorderColor #93a1a1
  stateBodyBackgroundColor #93a1a1
}
hide empty description
scale 2
state "NixOS" as os
```

-v-

```language-plantuml
skinparam {
  backgroundColor #002b36
  ArrowColor #93a1a1
  ArrowFontColor #93a1a1
  sequenceLifeLineBorderColor #93a1a1
  stateBodyBackgroundColor #93a1a1
}
hide empty description
scale 2
state "NixOS 🔒" as os #line.bold;line:red
```

Note:

Das Betriebssystem ist immutable:
Heisst: im Gegensatz zum user profile ist das Basissystem nur über die Konfiguration veränderbar

-v-

<div class="multicolumn">

<div>

```language-plantuml
skinparam {
  backgroundColor #002b36
  ArrowColor #93a1a1
  ArrowFontColor #93a1a1
  sequenceLifeLineBorderColor #93a1a1
  stateBodyBackgroundColor #93a1a1
}
hide empty description
scale 2
state "NixOS 🔒" as os #line.bold;line:red
```

</div>

<div>

```
environment.systemPackages = with pkgs; [
    neovim
    git
    jq
    digikam
];
```

</div>

</div>

-v-

<div class="multicolumn">

<div>

```language-plantuml
skinparam {
  backgroundColor #002b36
  ArrowColor #93a1a1
  ArrowFontColor #93a1a1
  sequenceLifeLineBorderColor #93a1a1
  stateBodyBackgroundColor #93a1a1
}
hide empty description
scale 2
state "NixOS 🔒" as os #line.bold;line:red
```

</div>

<div>

```
environment.systemPackages = with pkgs; [
    neovim
    git
    pyton314
    jq
    digikam
];
```

`sudo nixos-rebuild switch` <!-- .element: class="fragment" -->

</div>

</div>

-v-

<div class="multicolumn">

<div>

```language-plantuml
skinparam {
  backgroundColor #002b36
  ArrowColor #93a1a1
  ArrowFontColor #93a1a1
  sequenceLifeLineBorderColor #93a1a1
  stateBodyBackgroundColor #93a1a1
}
hide empty description
scale 2
state "NixOS Generation 1" as os1
state "NixOS Generation 2 🔒" as os2 #line.bold;line:red

os1 --> os2
```

</div>

<div>

```
environment.systemPackages = with pkgs; [
    neovim
    git
    pyton314
    jq
    digikam
];
```

</div>

</div>

Note:

erzeugt eine neue Generation des Betriebssystems anhand der vorhanden Konfiguration

-v-

<div class="multicolumn">

<div>

```language-plantuml
skinparam {
  backgroundColor #002b36
  ArrowColor #93a1a1
  ArrowFontColor #93a1a1
  sequenceLifeLineBorderColor #93a1a1
  stateBodyBackgroundColor #93a1a1
}
hide empty description
scale 2
state "NixOS Generation 1" as os1
state "NixOS Generation 2 🔒" as os2 #line.bold;line:red
state "NixOS Generation 3 💀" as os3


os1 --> os2
os2 -[hidden]-> os3
```

</div>

<div>

```
environment.systemPackages = with pkgs; [
    neovim
    git
    pyton314
    jibbereish
    jq
    digikam
];
```

`sudo nixos-rebuild switch`

</div>

</div>

Note:

die Operation ist atomar, erfolgt vollständig oder gar nicht

-v-

<div class="multicolumn">

<div>

```language-plantuml
skinparam {
  backgroundColor #002b36
  ArrowColor #93a1a1
  ArrowFontColor #93a1a1
  sequenceLifeLineBorderColor #93a1a1
  stateBodyBackgroundColor #93a1a1
}
hide empty description
scale 2
state "NixOS Generation 1" as os1
state "NixOS Generation 2 🔒" as os2 #line.bold;line:red

os1 --> os2
```

</div>

<div>

```
environment.systemPackages = with pkgs; [
    neovim
    git
    pyton314
    jibbereish
    jq
    digikam
];
```

</div>

</div>

Note:

die neue Generation wird einfach verworfen

-v-

<div class="multicolumn">

<div>

```language-plantuml
skinparam {
  backgroundColor #002b36
  ArrowColor #93a1a1
  ArrowFontColor #93a1a1
  sequenceLifeLineBorderColor #93a1a1
  stateBodyBackgroundColor #93a1a1
}
hide empty description
scale 2
state "NixOS Generation 1" as os1
state "NixOS Generation 2" as os2
state "NixOS Generation 3 🔒" as os3 #line.bold;line:red

os1 --> os2
os2 --> os3
```

</div>

<div>

```
environment.systemPackages = with pkgs; [
    neovim
    git
    pyton314
    ejabberd
    jq
    digikam
];
```

`sudo nixos-rebuild switch`

</div>

</div>

Note:

schützt vor halben upgrades
durch stromausfall oder fehlgeschlagener Konfiguration
eine fehlerhafte Generation wird schlicht verworfen
nach Behebung des Fehlers wird eine neue Generation erzeugt

-v-

<div class="multicolumn">

<div>

```language-plantuml
skinparam {
  backgroundColor #002b36
  ArrowColor #93a1a1
  ArrowFontColor #93a1a1
  sequenceLifeLineBorderColor #93a1a1
  stateBodyBackgroundColor #93a1a1
}
hide empty description
scale 2
state "NixOS Generation 1" as os1
state "NixOS Generation 2" as os2
state "NixOS Generation 3 🔒" as os3 #line.bold;line:red

os1 --> os2
os2 --> os3
```

</div>

<div>

<img src="./img/1/gen7.png" />

</div>

</div>

Note: 

* und dem Bootloader hinzugefügt
* hat die Änderung nicht den gewünschten Effekt, kann einfach
* ein Rollback durch die Auswahl einer älteren Generation erfolgen

-v-

<div class="multicolumn">

<div>

```language-plantuml
skinparam {
  backgroundColor #002b36
  ArrowColor #93a1a1
  ArrowFontColor #93a1a1
  sequenceLifeLineBorderColor #93a1a1
  stateBodyBackgroundColor #93a1a1
}
hide empty description
scale 2
state "NixOS Generation 1" as os1
state "NixOS Generation 2" as os2
state "NixOS Generation 3" as os3
state "NixOS Generation 4 +200MB 🔒" as os4 #line.bold;line:red

os1 --> os2
os2 --> os3
os3 --> os4
```

</div>

<div>

```
environment.systemPackages = with pkgs; [
    neovim
    git
    pyton314
    ejabberd
    jq
    digikam
    vscode
];
```

</div>

</div>

Note:

jede neue Generation entspricht einer Änderung der Konfiguration
und jede neue Generation nimmt nur soviel Platz ein, wie es erforderlich ist

-v-

<div class="multicolumn">

<div>

```language-plantuml
skinparam {
  backgroundColor #002b36
  ArrowColor #93a1a1
  ArrowFontColor #93a1a1
  sequenceLifeLineBorderColor #93a1a1
  stateBodyBackgroundColor #93a1a1
}
hide empty description
scale 2
state "NixOS Generation 1" as os1
state "NixOS Generation 2" as os2
state "NixOS Generation 3" as os3
state "NixOS Generation 4 +200MB 🔒" as os4
state "NixOS Generation 5 +0MB 🔒" as os5 #line.bold;line:red

os1 --> os2
os2 --> os3
os3 --> os4
os4 --> os5
```

</div>

<div>

```
environment.systemPackages = with pkgs; [
    neovim
    git
    pyton314
    ejabberd
    jq
    digikam
];
```

</div>

</div>

Note:

* aber weniger wird Speicherbedarf wird es nicht
* garbage-collection

-v-

<div class="multicolumn">

<div>

```language-plantuml
skinparam {
  backgroundColor #002b36
  ArrowColor #93a1a1
  ArrowFontColor #93a1a1
  sequenceLifeLineBorderColor #93a1a1
  stateBodyBackgroundColor #93a1a1
}
hide empty description
scale 2
state "NixOS Generation 4 +200MB 🔒" as os4
state "NixOS Generation 5 +0MB 🔒" as os5 #line.bold;line:red

os4 --> os5
```

</div>

<div>

```
environment.systemPackages = with pkgs; [
    neovim
    git
    pyton314
    ejabberd
    jq
    digikam
];
```

</div>

</div>

Note:

die Liste installierbaren und konfigurierbaren Pakete ist nixpkgs
