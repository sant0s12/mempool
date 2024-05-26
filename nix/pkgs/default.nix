{pkgs, ...}: {
  banshee = pkgs.callPackage ./banshee {};
  bender = pkgs.callPackage ./bender.nix {};
}
