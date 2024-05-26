{
  description = "Nix flake for mempool dev";

  inputs = {
    nixpkgs.url = "https://flakehub.com/f/NixOS/nixpkgs/0.1.*.tar.gz";
    rust-overlay.url = "github:oxalica/rust-overlay";
  };

  outputs = {
    self,
    nixpkgs,
    rust-overlay,
  }: let
    supportedSystems = ["x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin"];
    forEachSupportedSystem = nixpkgs.lib.genAttrs supportedSystems;
  in {
    devShells = forEachSupportedSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      default = (pkgs.mkShell.override { stdenv = pkgs.gcc12Stdenv; }) {

        # GCC does not compile without this
        hardeningDisable = [ "format" ];

        buildInputs = with pkgs; [
          clang
          autoconf
          automake
          pkg-config
          patchutils
          guile
          cmake
          sourceHighlight
          gawk
          bison
          help2man
        ] ++ (lib.attrsets.attrValues self.packages.${system});

        nativeBuildInputs = with pkgs; [
          (python3.withPackages
            (python-pkgs: [
              python-pkgs.numpy
              python-pkgs.pandas
              python-pkgs.pyarrow
              python-pkgs.matplotlib
            ]))

          clang-tools
          curl
          libmpc
          mpfr
          mpfr.dev
          gmp
          gmp.dev
          flex
          texinfo
          gperf
          libtool
          bc
          zlib.dev
          zlib
          dtc
          babeltrace
          m4
          elfutils
          elfutils.dev
          expat
          zstd
          ncurses.dev
        ];
      };
    });

    packages = forEachSupportedSystem (system:
      import ./nix/pkgs ((import nixpkgs) {
        inherit system;
        overlays = [(import rust-overlay)];
      }));
  };
}
