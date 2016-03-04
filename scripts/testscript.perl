#!/usr/bin/perl -w

use strict;
use CGI;

my $q = new CGI;
$q->charset('utf-8');
print $q->header( "application/json" );

my $task = $q->url_param("task");
my $message = $q->param("message");
my $lcmessage = lc $message;
my $from = $q->param("from");
my $ts = `date --utc '+%Y-%m-%d %H:%M:%S UTC %N'`;
chop $ts;
my $host = `hostname`;
chop $host;


open(my $fh, '>>/tmp/smssync') or die "Could not open file $!";
print $fh 'ts="' . $ts . '", task=' . $task . ', from="' . $from . '", message="' . $message . '".' . "\n";
close $fh;

if ($task eq "send") {
   print '{
    "payload": {
        "success": "true",
        "error": null,
        "secret": "secret02",
        "task": "send",
        "messages": [
        ]
    }
}
   ';

} else {
   print '{
    "payload": {
        "success": "true",
        "error": null,
        "secret": "secret02",
        "task": "send",
        "messages": [
            {
                "to": "' . $from . '",
                "message": "Si, claro! ' . $message . ".\n" . $ts . "\n" . $host . '",
                "uuid": "' . $ts . '"
            }
        ]
    }
}
   ';
}
