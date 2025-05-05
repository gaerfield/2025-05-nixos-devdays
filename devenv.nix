{ pkgs, lib, config, inputs, ... }:

{
  # https://devenv.sh/packages/
  packages = [ pkgs.git ];

  enterShell = ''
    git --version
  '';

  # https://devenv.sh/git-hooks/
  # git-hooks.hooks.shellcheck.enable = true;

  # See full reference at https://devenv.sh/reference/options/
  languages.python = {
    enable = true;
    venv.enable = true;
    venv.requirements = ''
      mkSlides
    '';
  };

  cachix.enable = false;
}
