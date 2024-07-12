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
                python-pkgs.python-lsp-server
               # python-pkgs.llama-index-core
               # python-pkgs.llama-index-embeddings-huggingface
               # python-pkgs.llama-index-llms-ollama
               # python-pkgs.llama-index-readers-file
               # python-pkgs.langchain
                python-pkgs.faiss
                python-pkgs.ollama
                python-pkgs.pylatexenc # to parase the LaTeX documents in RAG
                python-pkgs.chromadb  # the embedding database
                python-pkgs.sentence-transformers
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

