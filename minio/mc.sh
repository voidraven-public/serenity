curl -o $HOME/minio-binaries/mc [^1^][1]
chmod +x $HOME/minio-binaries/mc
export PATH=$PATH:$HOME/minio-binaries/
mc --help