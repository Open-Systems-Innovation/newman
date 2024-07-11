  {
  description = "Description for the project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    custom-nixpkgs.url = "github:Open-Systems-Innovation/custom-nixpkgs";
  };

  outputs = { self, nixpkgs, custom-nixpkgs, ... }:
      let
        system = "x86_64-linux";
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ custom-nixpkgs.overlays.default ];
        };
      in
        {
          devShells.${system}.default = pkgs.mkShell {
            name = "default";
               
            packages = [
            # General packages
              # pkgs.hello-nix
              # pkgs.petsc
              # pkgs.mpich
              # pkgs.clangd
              #  # Python packages
              (pkgs.python3.withPackages (python-pkgs: [
              #  # packages for formatting/ IDE
                python-pkgs.llama-index-core
                python-pkgs.llama-index-embeddings-huggingface
                python-pkgs.llama-index-llms-ollama
                python-pkgs.llama-index-readers-file
                #python-pkgs.llama-index-llms-huggingface
                python-pkgs.langchain
                python-pkgs.faiss
                python-pkgs.ollama
              #  python-pkgs.pip
              #  python-pkgs.python-lsp-server
              #  # packages for code
              #  python-pkgs.gmsh
              #  python-pkgs.matplotlib
              #  python-pkgs.meshio
              #  python-pkgs.numpy
              #  python-pkgs.firedrake
              ]))
            ];

            # PETSC_DIR = "${pkgs.petsc}";
            NLTK_DATA = ".nltk_data";
            TIKTOKEN_CACHE_DIR = ".tiktoken";
            
            shellHook = ''
              export VIRTUAL_ENV="newman"
            '';
          };
        };
}

