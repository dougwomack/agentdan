#!/usr/bin/perl
## ---------------------------------------------------------------------------
## Elemental Technologies Inc. Company Confidential Strictly Private
##
## ---------------------------------------------------------------------------
##                           COPYRIGHT NOTICE 
## ---------------------------------------------------------------------------
## Copyright 2011 (c) Elemental Technologies Inc.
##
## Elemental Technologies owns the sole copyright to this software. Under
## international copyright laws you (1) may not make a copy of this software
## except for the purposes of maintaining a single archive copy, (2) may not
## derive works herefrom, (3) may not distribute this work to others. These
## rights are provided for information clarification, other restrictions of
## rights may apply as well.
##
## This is an unpublished work.
## ---------------------------------------------------------------------------
##                              WARRANTY 
## ---------------------------------------------------------------------------
## Elemental Technologies Inc. MAKES NO WARRANTY OF ANY KIND WITH REGARD TO THE
## USE OF THIS SOFTWARE, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
## THE IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR
## PURPOSE.
## ---------------------------------------------------------------------------
##****************************************************************************
##*************** START OF PUBLIC TYPE AND SYMBOL DEFINITIONS ****************
##****************************************************************************

use strict;
use Digest::MD5 qw(md5_hex);
use CGI;
use URI;
use Time::Local;
my $debug = 0;

sub help
{
  print "Usage:\n";
  print "auth_curl [OPTIONS]\n\n";
  
  print "OPTIONS:\n";
  print "  all regular curl options\n";
  print "  --login <login>: User login\n";
  print "  --api-key <key>: User API Key\n";
  exit(0);
}

# Arguments 
my $login;
my $key;
my @curl_args;

# Iterate through the provided arguments
my $skip_next = 0;
for (my $i=0; $i< (scalar @ARGV); $i++)
{
    if ($skip_next)
    {
        $skip_next = 0;
        next;
    }
    
    my $arg = $ARGV[$i];
    print "$i: $arg\n" if $debug;
    
    if ($arg eq '--login')
    {
        $skip_next = 1;
        $login = $ARGV[$i+1];
    }
    elsif ($arg eq '--api-key')
    {
        $skip_next = 1;
        $key = $ARGV[$i+1];
    }
    elsif ($arg eq '--help' || $arg eq '-h' || $arg eq '-?')
    {
        help();
        exit(0);
    }
    else
    {
        if ($arg =~ /^-.*/)
        {
            push @curl_args, $arg;
        }
        elsif ($arg =~ /^\s+$/)
        {
            push @curl_args, "\"$arg\"";
        }
        else
        {
            push @curl_args, $arg;
        }
    }
}

if (!defined $login)
{
    print "Login is missing\n";
    help();
}
if (!defined $key)
{
    print "API key is missing\n";
    help();
}

# Here's what was found
print "login: $login\n" if $debug;
print "key: $key\n" if $debug;
print "curl args: @curl_args\n" if $debug;


my $escaped_url = CGI::escapeHTML($curl_args[-1]);
my $url = URI->new($escaped_url);
my $expires = timegm(gmtime()) + 30;
my $path_without_api_version = $url->path();
$path_without_api_version =~ s/\/api(?:\/[^\/]*\d+(?:\.\d+)*[^\/]*)?//i;

print "escaped url: $escaped_url\n" if $debug;
print "expires: $expires\n" if $debug;
print "path_without_api_version: $path_without_api_version\n" if $debug;

my $hashed_key = md5_hex($key . md5_hex($path_without_api_version . $login . $key . $expires));

# format curl_args
for (my $i=0; $i< (scalar @curl_args); $i++)
{
    $curl_args[$i] =~ s/"/'/g;
    if (substr($curl_args[$i], 1, 1) ne '-')
    {
        $curl_args[$i] = '"' . $curl_args[$i] . '"';
    }
}
print "curl -H \"X-Auth-User: $login\" -H \"X-Auth-Expires: $expires\" -H \"X-Auth-Key: $hashed_key\" @curl_args"  if $debug;
print `curl -H \"X-Auth-User: $login\" -H \"X-Auth-Expires: $expires\" -H \"X-Auth-Key: $hashed_key\" @curl_args`;
