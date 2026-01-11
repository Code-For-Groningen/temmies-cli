# run nix-shell here to get a shell with temmies-cli installed
{ pkgs ? import <nixpkgs> {} }:

let
  temmies = pkgs.python3Packages.buildPythonPackage rec {
    pname = "temmies";
    version = "1.2.130";
    pyproject = true;

    src = pkgs.python3Packages.fetchPypi {
      inherit pname version;
      hash = "sha256-pX7xMQmtNWcLWRkvC4/m9Wr24yWgX5/MUwY+lPDpr6g=";
    };

    build-system = [ pkgs.python3Packages.setuptools ];

    dependencies = with pkgs.python3Packages; [
      requests
      beautifulsoup4
      urllib3
      selenium
    ];

    dontCheckRuntimeDeps = true;
  };

temmies-cli = pkgs.python3Packages.buildPythonPackage {
    pname = "temmies-cli";
    version = "0.1.0";
    pyproject = true;

    src = ./.;

    build-system = [ pkgs.python3Packages.setuptools ];

    dependencies = with pkgs.python3Packages; [
      pkgs.python3Packages.click
      pkgs.python3Packages.requests
      pkgs.python3Packages.lxml
      pkgs.python3Packages.beautifulsoup4
      pkgs.python3Packages.keyring
      temmies
      pkgs.python3Packages.tqdm
    ];

  };

in pkgs.mkShell {
  buildInputs = [
    (pkgs.python3.withPackages (ps: [ temmies-cli ]))
  ];
}