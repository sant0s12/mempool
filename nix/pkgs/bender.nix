{
  rustPlatform,
  ...
}:
rustPlatform.buildRustPackage {
  name = "bender";

  cargoHash = "sha256-qe2xEQ2gIWtyVuhXZW3rMVpT4TjZ7xVKMPFGW37j13w=";

  src = fetchGit {
    url = "https://github.com/pulp-platform/bender";
    rev = "818a779933f3f735f99f4868feadcbfad886bc4b";
  };
}
