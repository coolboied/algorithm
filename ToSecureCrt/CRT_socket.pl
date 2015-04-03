# $language = "PerlScript"
# $interface = "1.0"
use Win32::OLE;
use Socket;
use IO::Socket::INET;
Win32::OLE->Option(Warn => 3);

#socket(SOCKET,AF_INET,SOCK_STREAM,(getprotobyname('udp')));   
#bind(SOCKET, sockaddr_in(3344,INADDR_ANY));
my $server = IO::Socket::INET->new(LocalPort => 3344, Proto => "udp") or print "Couldn't be a udp server on port $port : $@\n";

$cmd = 'ls';

#while($server->recv($line, 1024,0))
while(1)
{
    my $line;
    #print("aaa\n");
    #sysread(SOCKET, $line , 20);
    $server->recv($line, 1024, 0);
    #print($line."squall");
    $crt->Screen->Send("$line\n");
}





