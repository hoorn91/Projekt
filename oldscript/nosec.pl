#!/usr/bin/perl

$bytes = 100;

# --- Initialization of environment ---
$server="10.1.2.2";
$client="10.1.2.1";
$rctrl="root\@192.168.63.160";
$sctrl="server\@192.168.63.161";

# Remove previous application instances
system ("ssh $sctrl sudo killall sctp");
system ("rm nosec_test");
system ("rm count");

while($bytes <= 2000)
{
	$loopvar = 30;
	while($loopvar)
	{
		system("rm count");
		system("ssh -f $sctrl ./sctpserv no_security server $bytes");
		system("sleep 1");
		system("./sctp no_security client server >> count");#nosec_test");
		system("ssh $sctrl sudo killall sctp");
		$loopvar--; 
	}
	$bytes += 100;
	system("ssh $sctrl sudo killall sctp");
	system("./calc count >> nosec_test")
}
system("ssh $sctrl sudo killall sctp");