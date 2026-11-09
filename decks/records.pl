# records.pl -- what each deck reads, recorded after every build, so that the CI rebuilds only the decks a push
# touches (beamer-almamater/ci/impact.py). Called from the END block of a deck repository's .latexmkrc:
#
#     my $records = './.style/decks/records.pl';
#     do $records if -e $records;
#
# Run from the repository's root, after latexmk. Each file is rewritten only when its list changes.
#
# bib/cites/<deck>.keys -- the keys the deck cites, from aux/<deck>.aux: a change to bib/apice.bib rebuilds only the
#     decks citing a changed entry (Andrea, 2026-10-30; moved here from each .latexmkrc on 2026-11-09).
# deps/<deck>.files -- every file of the repository the deck reads, from aux/<deck>.fls, plus the .bst named in its .aux;
#     a link is listed with the file it points to (sty/beamerthemealmamater.sty and .style/beamerthemealmamater.sty).
#     The .bib files are left out: bib/cites decides for them, entry by entry (Andrea, 2026-11-09).

use strict;
use warnings;
use Cwd qw(getcwd realpath);
use File::Spec;

my $root = realpath(getcwd());

sub write_if_changed {
	my ( $file, $text ) = @_;
	my $old = '';
	if ( open( my $fh, '<', $file ) ) { local $/; $old = <$fh> // ''; close $fh; }
	return if -e $file && $old eq $text;
	my ($dir) = $file =~ m{^(.*)/};
	mkdir $dir unless -d $dir;
	if ( open( my $fh, '>', $file ) ) { print $fh $text; close $fh; }
}

# a path as the repository sees it, or undef when it lies outside (TeX Live, the home folder)
sub in_repo {
	my ($p) = @_;
	my $abs = File::Spec->rel2abs( $p, $root );
	$abs = File::Spec->canonpath($abs);
	return undef unless index( $abs, "$root/" ) == 0;
	return substr( $abs, length($root) + 1 );
}

foreach my $auxfile ( glob 'aux/*.aux' ) {
	my ($base) = $auxfile =~ m{([^/]+)\.aux$};
	next unless -e "tex/$base.tex";   # a probe jobname is no deck

	# bib/cites/<deck>.keys
	my ( %keys, @bst );
	if ( open( my $in, '<', $auxfile ) ) {
		while ( my $line = <$in> ) {
			while ( $line =~ /\\citation\{([^}]*)\}/g ) {
				$keys{$_} = 1 foreach grep { $_ ne '' } map { s/^\s+|\s+$//gr } split /,/, $1;
			}
			push @bst, $1 if $line =~ /\\bibstyle\{([^}]*)\}/;
		}
		close $in;
	}
	write_if_changed( "bib/cites/$base.keys", join '', map { "$_\n" } sort keys %keys );

	# deps/<deck>.files
	my $fls = "aux/$base.fls";
	next unless -e $fls;
	my %files;
	my @read;
	if ( open( my $in, '<', $fls ) ) {
		while ( my $line = <$in> ) {
			push @read, $1 if $line =~ /^INPUT (.+?)\s*$/;
		}
		close $in;
	}
	foreach my $b (@bst) {
		push @read, "bst/$b.bst" if -e "bst/$b.bst";
	}
	foreach my $p (@read) {
		my $rel = in_repo($p);
		next unless defined $rel;
		next if $rel =~ m{^(aux|pdf)/} || $rel =~ /\.bib$/;
		$files{$rel} = 1;
		my $real = realpath( File::Spec->rel2abs( $rel, $root ) );   # through every link on the way
		next unless defined $real;
		my $target = in_repo($real);
		$files{$target} = 1 if defined $target && $target ne $rel;
	}
	write_if_changed( "deps/$base.files", join '', map { "$_\n" } sort keys %files );
}

1;
