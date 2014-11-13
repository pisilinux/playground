package Build::Pisi;

use strict;

# Stolen from Build::Kiwi
sub parsexml {
  my ($xml) = @_;
  my @nodestack;
  my $node = {};
  my $c = '';
  $xml =~ s/^\s*\<\?.*?\?\>//s;
  while ($xml =~ /^(.*?)\</s) {
    if ($1 ne '') {
      $c .= $1;
      $xml = substr($xml, length($1));
    }
    if (substr($xml, 0, 4) eq '<!--') {
      $xml =~ s/.*?-->//s;
      next;
    }
    die("bad xml\n") unless $xml =~ /(.*?\>)/s;
    my $tag = $1;
    $xml = substr($xml, length($tag));
    my $mode = 0;
    if ($tag =~ s/^\<\///s) {
      chop $tag;
      $mode = 1;	# end
    } elsif ($tag =~ s/\/\>$//s) {
      $mode = 2;	# start & end
      $tag = substr($tag, 1);
    } else {
      $tag = substr($tag, 1);
      chop $tag;
    }
    my @tag = split(/(=(?:\"[^\"]*\"|\'[^\']*\'|[^\"\s]*))?\s+/, "$tag ");
    $tag = shift @tag;
    shift @tag;
    push @tag, undef if @tag & 1;
    my %atts = @tag;
    for (values %atts) {
      next unless defined $_;
      s/^=\"([^\"]*)\"$/=$1/s or s/^=\'([^\']*)\'$/=$1/s;
      s/^=//s;
      s/&lt;/</g;
      s/&gt;/>/g;
      s/&amp;/&/g;
      s/&apos;/\'/g;
      s/&quot;/\"/g;
    }
    if ($mode == 0 || $mode == 2) {
      my $n = {};
      push @{$node->{$tag}}, $n;
      for (sort keys %atts) {
	$n->{$_} = $atts{$_};
      }
      if ($mode == 0) {
	push @nodestack, [ $tag, $node, $c ];
	$c = '';
	$node = $n;
      }
    } else {
      die("element '$tag' closes without open\n") unless @nodestack;
      die("element '$tag' closes, but I expected '$nodestack[-1]->[0]'\n") unless $nodestack[-1]->[0] eq $tag;
      $c =~ s/^\s*//s;
      $c =~ s/\s*$//s;
      $node->{'_content'} = $c if $c ne '';
      $node = $nodestack[-1]->[1];
      $c = $nodestack[-1]->[2];
      pop @nodestack;
    }
  }
  $c .= $xml;
  $c =~ s/^\s*//s;
  $c =~ s/\s*$//s;
  $node->{'_content'} = $c if $c ne '';
  return $node;

}

sub unify {
  my %h = map {$_ => 1} @_;
  return grep(delete($h{$_}), @_);
}

use Data::Dumper;
sub pisiparse {
    my ($xml) = @_;
    my @packdeps;
    my $ret = {};
    my %hash = ("version" => "=", "versionFrom" => ">=", "versionTo" => "<=");

    # Parse XML file using internal parser
    my $pspec = parsexml($xml);
    $pspec = $pspec ->{'PISI'}->[0];
    if ($pspec->{'Source'}) {
        my $source = (($pspec->{'Source'} || [])->[0] || {});

        # Get BuildDependencies
        my @build_deps;
        @build_deps = @{$source->{'BuildDependencies'}->[0]->{'Dependency'}};

        for my $dep (@build_deps){
            # Get name of the dependency
            my $build_dep = $dep->{'_content'};

            # Get keys of each dependency (type of hash), and along with _content variable look for following:
            # versionFrom, version, versionTo
            my @attrs = keys %$dep;
            for my $attr (@attrs){
                if (($attr eq 'versionFrom') || ($attr eq 'version') || ($attr eq 'versionTo') ) {
                    $build_dep = $build_dep . " " .$hash{$attr} . " " . $dep->{$attr};
                    }
                }
            # Add dependency to the @packdeps array
            push @packdeps, $build_dep;
            }
        }
    $ret->{'deps'} = [ unify(@packdeps) ];
    return $ret;
  }


# Read xml file and parse using pisiparse subroutine
sub parse {
  my ($fn) = @_;

  local *F;
  open(F, '<', $fn) || die("$fn: $!\n");
  my $xml = '';
  1 while sysread(F, $xml, 4096, length($xml)) > 0;
  close F;
  my $d;
  eval {
    $d = pisiparse($xml);
  };
  if ($@) {
    my $err = $@;
    $err =~ s/^\n$//s;
    return {'error' => $err};
  }
  return $d;
}
# Extracts name, version, release, architecture, description, dependencies etc. from given .pisi package
sub query{
    my ($handle, %opts) = @_;
    my $name;
    my $epoch;
    my $version;
    my $release;
    my $arch;
    my $description;
    my $depends;
    my @provides;
    my $xml;
    my $x_p;
    my $p_md5;
    my $data;

    qx(unzip $handle "metadata.xml");
    local *F;
    open(F, '<', "metadata.xml") || die("metadata.xml: $!\n");
    $xml = '';
    1 while sysread(F, $xml, 4096, length($xml)) > 0;
    close F;
    $p_md5 = Digest::MD5::md5_hex($xml);
    $x_p = parsexml($xml);
    #print Dumper ($x_p);
    qx(rm metadata.xml);

    $name = $x_p->{'PISI'}->[0]->{'Package'}->[0]->{'Name'}->[0]->{'_content'};
    my @a = @{$x_p->{'PISI'}->[0]->{'Package'}->[0]->{'Description'}};
    foreach my $c (@a){
       if('en' eq $c->{'xml:lang'}){
           $description = $c->{'_content'};
        }
    }
    $arch = $x_p->{'PISI'}->[0]->{'Package'}->[0]->{'Architecture'}->[0]->{'_content'};
    $version = $x_p->{'PISI'}->[0]->{'Package'}->[0]->{'History'}->[0]->{'Update'}->[0]->{'Version'}->[0]->{'_content'};
    $release =  $x_p->{'PISI'}->[0]->{'Package'}->[0]->{'History'}->[0]->{'Update'}->[0]->{'release'};

        my @keys;
        my @values;
        my $val; 
        my @packdeps;
        my %hash = ('version' => '=', 'versionFrom' => '>=', 'versionTo' => '<=');
        my @rt_deps = @{$x_p->{'PISI'}->[0]->{'Package'}->[0]->{'RuntimeDependencies'}->[0]->{'Dependency'}};

        foreach my $deps (@rt_deps){
            while( my ($k, $v) = each %$deps) {
                if (my $opr = $hash{$k}){
                    pop @keys;
                    $val = (pop @values)." ".$opr." ".$v;
                    push @packdeps, $val;
                }
                else{
                    push @keys, $k;
                    push @values, $v;
                }
            }
        }
        foreach my $value (@values){
            push @packdeps, $value;
        }

    $depends = [unify(@packdeps)];
    $data->{'name'} = $name;
    $data->{'hdrmd5'} = $p_md5;
    $data->{'requires'} = $depends;
    $data->{'provides'} = $name;
    $data->{'source'} = $name;

    if ($opts{'evra'}) {
        $data->{'version'} = $version;
        $data->{'release'} = $release;
        $data->{'arch'} = $arch;
    }

    if ($opts{'description'}) {
        $data->{'description'} = $description;
    }

    return $data;

}

# Gives only hdrmd5 from query method
sub queryhdrmd5{
    my ($handle, %opts) = @_;
    return query($handle)->{'hdrmd5'};
}

# helper method for version compare method.
sub verscmp_part {
  my ($s1, $s2) = @_;
  if (!defined($s1)) {
    return defined($s2) ? -1 : 0;
  }
  return 1 if !defined $s2;
  return 0 if $s1 eq $s2;
  while (1) {
    $s1 =~ s/^[^a-zA-Z0-9]+//;
    $s2 =~ s/^[^a-zA-Z0-9]+//;
    my ($x1, $x2, $r);
    if ($s1 =~ /^([0-9]+)(.*?)$/) {
      $x1 = $1;
      $s1 = $2;
      $s2 =~ /^([0-9]*)(.*?)$/;
      $x2 = $1;
      $s2 = $2;
      return 1 if $x2 eq '';
      $x1 =~ s/^0+//;
      $x2 =~ s/^0+//;
      $r = length($x1) - length($x2) || $x1 cmp $x2;
    } elsif ($s1 ne '' && $s2 ne '') {
      $s1 =~ /^([a-zA-Z]*)(.*?)$/;
      $x1 = $1;
      $s1 = $2;
      $s2 =~ /^([a-zA-Z]*)(.*?)$/;
      $x2 = $1;
      $s2 = $2;
      return -1 if $x1 eq '' || $x2 eq '';
      $r = $x1 cmp $x2;
    }
    return $r > 0 ? 1 : -1 if $r;
    if ($s1 eq '') {
      return $s2 eq '' ? 0 : -1;
    }
    return 1 if $s2 eq ''
  }
}

# compares 2 given pisi packages' versions by looking at their names
sub verscmp {
  my ($s1, $s2, $dtest) = @_;

  return 0 if $s1 eq $s2;
  my ($v1, $r1) = $s1 =~ /(.*?)-((?:[^-]*)-(?:[^-]*)-(?:[^-]*))$/s;

  my ($v2, $r2) = $s2 =~ /(.*?)-((?:[^-]*)-(?:[^-]*)-(?:[^-]*))$/s;

  return 0 if $dtest && ($v1 eq '' || $v2 eq '');
  if ($v1 ne $v2) {
    my $r = verscmp_part($v1, $v2);
    return $r if $r;
  }
  $r1 = '' unless defined $r1;
  $r2 = '' unless defined $r2;
  return 0 if $dtest && ($r1 eq '' || $r2 eq '');
  if ($r1 ne $r2) {
    return verscmp_part($r1, $r2);
  }
  return 0;
}

1;
