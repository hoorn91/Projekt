#!/usr/bin/perl

$bytes = 100;

# --- Initialization of environment ---
$server="10.1.2.2";
$client="10.1.2.1";
$rctrl="root\@192.168.63.160";
$sctrl="server\@192.168.63.161";

# Remove previous application instances
system("ssh $sctrl sudo killall perfServerS2sctp");
system ("rm /home/client/sctp/s2nosec_test");
system ("rm /home/client/sctp/count");
system ("rm /home/client/sctp/s2nosec_spread/*");
while($bytes <= 2000)
{
	system("rm /home/client/sctp/count");
	$loopvar = 30;
	while($loopvar)
	{
		system("ssh -f $sctrl ./s2serv");
		system("sleep 1");
		system("/home/client/_perf/s2/echo_client_s2sctp 10.1.2.2 $bytes 0 10000 1 $bytes >> /home/client/sctp/count"); #tls_test");
		system("ssh $sctrl sudo killall perfServerS2sctp");
		$loopvar--;
	}
	system("ssh $sctrl sudo killall perfServerS2sctp");
	system("/home/client/sctp/calc /home/client/sctp/count >> /home/client/sctp/s2nosec_test");
	system("cat /home/client/sctp/count >> /home/client/sctp/s2nosec_spread/s2nosec".$bytes."bytes");
	$bytes += 100;
}
system("ssh $sctrl sudo killall perfServerS2sctp");
