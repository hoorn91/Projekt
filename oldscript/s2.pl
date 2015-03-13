#!/usr/bin/perl

$bytes = 100;

# --- Initialization of environment ---
$server="10.1.2.2";
$client="10.1.2.1";
$rctrl="root\@192.168.63.160";
$sctrl="server\@192.168.63.161";

# Remove previous application instances
system("ssh $sctrl sudo killall newServerS2sctp");
system ("rm /home/client/sctp/s2_test");
system ("rm /home/client/sctp/count");

while($bytes <= 2000)
{
	$loopvar = 30;
	while($loopvar)
	{
		system("rm count");
		system("ssh -f $sctrl ./s2serv 10000");
		system("sleep 1");
		system("/home/client/_perf/s2/echo_client_s2sctp 10.1.2.2 $bytes 3 10 >> /home/client/sctp/count"); #tls_test");
		system("ssh $sctrl sudo killall newServerS2sctp");
		$loopvar--; 
	}
	$bytes += 100;
	system("ssh $sctrl sudo killall newServerS2sctp");
	system("/home/client/sctp/calc /home/client/sctp/count >> /home/client/sctp/s2_test")
}
system("ssh $sctrl sudo killall newServerS2sctp");