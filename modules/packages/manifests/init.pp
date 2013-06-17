class packages {

  $packages_to_install = [
    'python-setuptools',
    #'gcc',
    'python-devel',
    'libxml2-devel',
    'libxslt-devel',
    'unzip',
    'git',
    'vim-enhanced',
    'mlocate',
  ]

  package { $packages_to_install:
    ensure => installed,
  }

}
