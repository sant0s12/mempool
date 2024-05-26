{
  pkgs,
  makeRustPlatform,
  ...
}: let
  toolchain = pkgs.rust-bin.stable."1.63.0".default;
  rustPlatform = makeRustPlatform {
    cargo = toolchain;
    rustc = toolchain;
  };
in
  rustPlatform.buildRustPackage {
    name = "banshee";

    cargoPatches = [
      # a patch file to add/update Cargo.lock in the source code
      ./cargo.lock.patch
    ];

    cargoHash = "sha256-PGW+7cejaMVFiqBWmX2WwheCykZZ/utWDEoTcA2wPa8=";

    src = fetchGit {
      url = "https://github.com/pulp-platform/banshee";
      rev = "29607d2115f95e76fa6491145d63ece4f26059ca";
      submodules = true;
    };

    nativeBuildInputs = with pkgs; [git cmake llvm_12 llvm_12.dev libxml2];

    preBuild = ''
      export LLVM_SYS_120_PREFIX=${pkgs.llvmPackages_12.llvm.dev}
    '';
  }
