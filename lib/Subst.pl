#!/usr/bin/perl -w
#Подстановка параметров в настроечные файлы
#предполагается что параметры подлежащие подстановке 
# заключены в <<>> например <<DateStr>>

use strict;

my %Prm = @ARGV;

for my $i (keys %Prm){print "$i = $Prm{$i}\n"}
while (<STDIN>){
         s/<<([^<>]+)>>/$Prm{"$1"}/g;
         s/\xd//g;
         print ;
}         
