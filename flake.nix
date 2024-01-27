{
  description = "build chatddx";

  inputs = {
    my-nixos.url = "github:ahbk/my-nixos";
    nixpkgs.follows = "my-nixos/nixpkgs";
    nixpkgs-stable.follows = "my-nixos/nixpkgs-stable";

    poetry2nix = {
      url = "github:ahbk/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, poetry2nix, ... }: 
  with nixpkgs.lib;
  let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
    inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
    mkEnv = env: pkgs.writeText "env" (
      concatStringsSep "\n" (mapAttrsToList (k: v: "${k}=${v}") env)
      );
  in {
    packages.${system}.django = rec {
      bin = pkgs.substituteAll {
        src = "${self}/backend/bin/chatddx.com";
        dir = "bin";
        isExecutable = true;
        app = app.dependencyEnv;
        inherit env static;
      };

      env = mkEnv {
        DEBUG = "true";
        STATE_DIR = "/var/lib/chatddx.com";
        HOST = "localhost";
        DJANGO_SETTINGS_MODULE = "app.settings";
      };

      app = mkPoetryApplication {
        projectDir = "${self}/backend";
        groups = [];
        checkGroups = [];
      };

      static = pkgs.stdenv.mkDerivation {
        pname = "chatddx-static";
        version = app.version;
        src = "${self}/backend";
        buildPhase = ''
          export STATIC_ROOT=$out
          export DJANGO_SETTINGS_MODULE=app.settings
          ${app.dependencyEnv}/bin/django-admin collectstatic --no-input
        '';
      };
    };
  };
}
