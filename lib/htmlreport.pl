#!/usr/bin/perl -w
#формирования запроса на вывод отчетов от МСМ

use strict;
use locale;
use File::Basename;

use lHtmlBusLib ;

my @Now = (localtime)[3,4,5]; $Now[1]++; $Now[2] -= 100;


my %cgi=GetCGIParam();
my $CallMe=basename($0);
my $Dir = ( exists $cgi{dir} ? $cgi{dir} : dirname($0) );
my $ReportList = "$Dir/report.list";

opendir(DATA,$Dir) || MsgToWebmaster("Can't open DataBase","$Dir $!");
my @files = readdir(DATA); 
closedir(DATA);
my %files;
for my $i (@files) {         #поиск описаний вариантов запросов
    if ( $i =~ /\.report$/ ) {
        $files{basename($i)} = '' ;
        open(DATA,"<$Dir/$i") || MsgToWebmaster("Can't open :","$i $!");
        while(<DATA>){
            $files{basename($i)} .= ' ' . $1 if /\#;(.+)/g;
        }
    }
}

my %list;
open(DATA,"<$ReportList") || MsgToWebmaster("Can't open reportlist :","$ReportList $!");
my $stat = '';
while(<DATA>){
    if ( /AS=.+$/ ){
        $stat = $. ;
    } 
    next unless $stat;
    $list{$stat}->{$1} = $2 if /^([^=]+)=(.*)$/
}



print "Content-type: text/html; charset=koi8-r\n\n";    

if (not exists $cgi{Go}){
    print "$ENV{'SERVER_NAME'}<br>" ;
    print "<form ACTION=\"$CallMe\" method=\"post\">";
    
    print 'Дата начала периода :';     print Date4Select('s',$cgi{sd},$cgi{sm},$cgi{sy});
    print ' &nbsp; ';
    print 'Дата конца периода  :'; print Date4Select('e',$cgi{ed},$cgi{em},$cgi{ey});

    for my $i (sort keys %list){
        my $sel = 'checked'; 
        $sel = '' if exists $list{$i}->{'select'} && $list{$i}->{'select'} eq 'off';
        print "<br><input type=checkbox name=\"key$i\"  $sel> &nbsp; $list{$i}->{AS}";
    }
    
    print '<p><table>';
    for my $i (sort keys %files){
	my $txt = $files{$i}; $i =~ s/\.report//;
        print "<tr><td align=right> <i>$txt</i> &nbsp;
		</td><td> <input name=\"Go\" type=\"submit\" value=\"$i\"></td></tr>"
    }
    print '<table>';
    print "<input name=\"dir\" type=\"hidden\" value=\"$Dir\">";
    
    print '</form>';
} else {
    $cgi{Go} .= '.report';
    print "<br><a href=\"$CallMe?dir=$Dir\">Новый запрос </a><br>
	<b>$cgi{sd}.$cgi{sm}.$cgi{sy} - $cgi{ed}.$cgi{em}.$cgi{ey}</b> &nbsp;<b>$cgi{Go}</b> <i>$files{$cgi{Go}}</i>";

#    for my $i (keys %cgi) {print "<br>$i = $cgi{$i}"}
    for my $i (sort keys %list){
        if ( $cgi{ "key$i" } ){
            print "<br>$list{$i}->{AS} ";
            if ($list{$i}->{ask} eq 'local'){        #запрос к локальной машине
                if (open(DATA,"/usr/lib/perl5/Avtobus/Subst.pl DateStr $cgi{sd}.$cgi{sm}.$cgi{sy} DateEnd $cgi{ed}.$cgi{em}.$cgi{ey} <$Dir/$cgi{Go} | /usr/lib/perl5/Avtobus/Report.pl -I |") ){
                    HtmlRecuest($i,*DATA); sleep 1;
                } else {
                    MsgToWebmaster("Can't open pipe :",$!);
                }
            } elsif ($list{$i}->{ask} =~ /^mail/i ){ #запрос по почте
                if (open(DATA,"/usr/lib/perl5/Avtobus/Subst.pl DateStr $cgi{sd}.$cgi{sm}.$cgi{sy} DateEnd $cgi{ed}.$cgi{em}.$cgi{ey} FormNam $cgi{Go} <$Dir/$cgi{Go} | $list{$i}->{ask} |") ){
                    while(<DATA>){print}; print " $list{$i}->{ask}";
                }else{
                    MsgToWebmaster("Can't open pipe :",$!);print " Error!";next;
                }
            } elsif ($list{$i}->{ask} =~ /^remote:(.+):(.+)$/i ){     #запрос к удаленной машине
                my $ask = $1; my $dir = $2;
                if (open(DATA,"/usr/lib/perl5/Avtobus/Subst.pl DateStr $cgi{sd}.$cgi{sm}.$cgi{sy} DateEnd $cgi{ed}.$cgi{em}.$cgi{ey} <$Dir/$cgi{Go} | ssh $ask $/usr/lib/perl5/Avtobus/Report.pl -I |") ){
                    HtmlRecuest($i,*DATA);
                } else {
                    MsgToWebmaster("Can't open pipe :",$!);
                }
            }
        }
    }
}

exit 1;

#=======================   ======================================
sub HtmlRecuest{
my $i = shift;
my $fil= shift;
                print " * <br>";
                my $table = '';
                while(<$fil>){
		    chomp; s/[\x0d\x0a]//g; s/;\s+;/;;/g;
                    if ($list{$i}->{answer} eq 'html'){
                        if ( /^ ([^;]+);\x2!/ ){
                            print '</table>' if $table;
                            $table = $1 ;
                            print "<p>$table<table border=1>";
                        }
                        s/\x2/+/g; print '<tr>';
			for my $j ((split(';'))){
                            $j =~ s/</&lt;/g; s/>/&gt;/g; 
			    print '<td>&nbsp;</td>' unless $j;
			    print "<td>$j</td>" if $j;
			}
			print '</tr>';
                    } else { print;}
                }
                print '</table>' if $table;
}


sub Date4Select{
my $pref = shift || '';
my @dt = @_ ;
return (Arr4select("${pref}d",1,31,$dt[0] ? $dt[0] : $Now[0]),
        Arr4select("${pref}m",1,12,$dt[1] ? $dt[1] : $Now[1]),
        Arr4select("${pref}y",$Now[2]-1,$Now[2]+1,$dt[2] ? $dt[2] : $Now[2])
        )
}

sub Arr4select{
my $nm = shift || 0;
my $bg = shift || 1;
my $en = shift || 31;
my $sl = shift || 1;
my @ret = ("<select name=\"$nm\">");
        for my $i ($bg..$en){
                my $a = sprintf("%02d",$i);
                push (@ret, '<option' . ($i == $sl ? ' selected':'') . ">$a</option>");
        }
return (@ret,'</select>');                
}

__END__
$cgi{from} = sub {'01.'. sprintf("%02d",$_[4]+1). '-' .($_[5]+1900)}->(localtime) unless $cgi{from};
$cgi{to} = sub {sprintf("%02d",$_[3]).'-'.sprintf("%02d",$_[4]+1).'-'.($_[5]+1900)}->(localtime)
    unless $cgi{to};


    print "<select name=\"p\" size=$sizedate >";
    for $i (@point){
        print "<option value=\"$i->[0]\"",$i->[0] eq $cgi{p} ? ' selected':'';
        print ">$i->[1]</option>";
    }
    print '</select>';          #ТНПЛХПНБЮМХЕ ДНЯРСОМНЦН ЙНКХВЕЯРБЮ ЛЕЯР ДКЪ ГЮЙЮГЮ

