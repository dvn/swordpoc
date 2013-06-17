class sysprep {

#file { '/etc/inittab':
#  source => 'puppet:///modules/bucket/etc/inittab',
#  owner  => 'root',
#  group  => 'root',
#  mode   => '0644',
#}

}
