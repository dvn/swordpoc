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
    'mlocate',
  ]

  package { $packages_to_install:
    ensure => installed,
  }

}
