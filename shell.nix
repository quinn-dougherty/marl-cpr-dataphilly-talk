{ pkgs ? import <nixpkgs> {} }:

with pkgs;
let
  pythonOnNix = import (pkgs.fetchFromGitHub {
    owner = "kamadorueda";
    repo = "python-on-nix";
    rev = "50eb084be288012628a89fa9ddd0cc8a875df6e8";
    sha256 = "1cj2r93faaff8rqsr0kp1zy11shpkb01dc3w5qb3b41b3g9k309w";
  });
  env = pythonOnNix.python39Env {
    name = "dataphilly-talk";
    projects = {
      torch = "1.9.0";
      gym = "0.19.0";
      ray = "1.6.0";
      dm-tree = "0.1.6";  # needed for rllib
      pandas = "1.3.3";  # needed for rllib
      tabulate = "0.8.9";  # needed for tune or rllib
      scikit-image = "0.18.3";  # needed for rllib
      requests = "2.25.1";  # needed for tune
      lz4 = "3.1.3";  # silences a suggestion in rllib
      flake8 = "latest";
      pytest = "latest";
      hypothesis = "latest";
      black = "latest";
      # pytype = "latest";  # still can't get it to work
      # ninja = "1.10.2.2";  # needed for pytype
      mypy = "latest";
    };
  };
  dataphillyTalkDev = stdenv.mkDerivation {
    name = "dataphilly-talk";
    src = ./.;
    buildInputs = [ env ];
    buildPhase = ''
      python --version >> out.txt
      python -c 'import torch; print("torch version: ", torch.__version__)' >> out.txt
      python -c 'import numpy as np; print("numpy version: ", np.__version__)' >> out.txt
      python -c 'import ray; print("ray version: ", ray.__version__)' >> out.txt
      python -c 'import ray.rllib' >> out.txt
      python -c "import ray; ray.init(); ray.shutdown()" >> out.txt
      python -c 'import gym; print("gym version: ", gym.__version__)' >> out.txt
    '';
    installPhase = ''
      mkdir -p $out
      cp out.txt $out/out.txt
      (mypy . || echo "mypy failed") >> $out/validate.txt
      (flake8 . --ignore F401 --max-line-length=111 || echo "flake8 failed") >> $out/validate.txt
      (pytest || echo "pytest failed") >> $out/validate.txt
      cat $out/out.txt
      cat $stdenv/setup >> $out/setup
      cat $out/validate.txt
    '';
  };
in
mkShell {
  buildInputs = [
    dataphillyTalkDev env
  ];
}
