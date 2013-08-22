class packages {

  $packages_to_install = [
    # for https://github.com/swordapp/Simple-Sword-Server
    'python-setuptools',
    'python-devel',
    'libxml2-devel',
    'libxslt-devel',
    # for swordpoc in Java
    'apache-maven',
    # common tools
    'unzip',
    'git',
    'vim-enhanced',
    'ack',
    'mlocate',
    # for dvn_client
    python-argparse,
    python-lxml
  ]

  package { $packages_to_install:
    ensure => installed,
  }

    exec {"install swordv2 python client":
	path	=>	"/bin:/usr/bin",
	command	=>	"git clone https://github.com/pjbull/python-client-sword2.git /swordv2 && cd /swordv2 && python setup.py install",
	provider => "shell"
  }
}
