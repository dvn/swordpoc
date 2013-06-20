class repos {

file { '/etc/yum.repos.d/epel-apache-maven.repo':
  source => 'puppet:///modules/bucket/etc/yum.repos.d/epel-apache-maven.repo',
}

#file { '/etc/yum.repos.d/CentOS-Base.repo':
#  source => 'puppet:///modules/bucket/etc/yum.repos.d/CentOS-Base.repo',
#}

}
