vm_name = File.basename(Dir.getwd)

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-24.04"

  config.vm.provider "libvirt" do |p|
    p.memorybacking :access, :mode => "shared"
    p.memory = 4096
    p.cpus = 2
  end

  config.vm.synced_folder ".", "/workspace", type: "virtiofs"
  config.vm.synced_folder "~/.codex", "/home/vagrant/.codex", type: "rsync", rsync__args: ["--recursive", "--include=auth.json", "--exclude=*"]
  
  config.vm.provision "shell", inline: <<-SHELL
    export DEBIAN_FRONTEND=noninteractive
    apt-get update

    # Install Codex
    apt-get install --yes npm
    npm i -g @openai/codex

    # Install dev dependencies
    apt-get install --yes git

    # Set up workspace
    chown -R vagrant:vagrant /workspace
    echo "cd /workspace" >>.bash_profile
  SHELL

  # Add lines like this to expose ports from the VM for local testing:
  #    config.vm.network "forwarded_port", guest: 3000, host: 3000
end
