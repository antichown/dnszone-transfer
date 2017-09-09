#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Dns Zone Transfer by 0x94

import colorama
import dns.resolver
import dns.query
import dns.zone
import dns.exception
import optparse
import sys

from threading import Thread

success = colorama.Fore.GREEN 
error = colorama.Fore.RED   
info = colorama.Fore.YELLOW 

class Zone():
    
    def __init__(self,domain):
        self.domain=domain
    
    def nslerial(self,domain):  
        try:
            Nslist = dns.resolver.query(self.domain, 'NS')
            return Nslist
        except dns.resolver.NXDOMAIN:
            print "NS yok"
        return False
    
    def resolver(self,domain):
        dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
        dns.resolver.default_resolver.nameservers = ['8.8.8.8', '2001:4860:4860::8888',
                                                     '8.8.4.4', '2001:4860:4860::8844' ]
        try:
            r = dns.resolver.query(self.domain)
            return True
        except:
            return False
        
    def kayit(self,veri):
        print error+veri
        with open(self.domain+".txt", 'a+') as filem:
            filem.write(veri+"\n")
            
    def zonecik(self,ns):
        print "NS Bilgileri getiriliyor"
        print info+"--"+ns
        print "Zone Transfer kontrol ediliyor"
        try:
            zonecheck=dns.zone.from_xfr(dns.query.xfr(str(ns), self.domain))
            bilgi = zonecheck.nodes.keys()
            bilgi.sort()
            for gizlib in bilgi:
                kayit = zonecheck[gizlib].to_text(gizlib)
                self.kayit(kayit)            
        except:
            print "Zone Transfer Alinamadi"

    def baslat(self):
        print self.domain+" NS leri kontrol ediliyor"
  
        if self.resolver(self.domain):
            try:
                nssender=[self.zonecik(str(ns)) for ns in dns.resolver.query(self.domain, 'NS')]
            except:
                print "NS alınırken hata"
                
                
if __name__ == '__main__':
    try:           
        colorama.init(autoreset=True) #windows icin        
        parser = optparse.OptionParser()
        parser.add_option('-d',
            action = "store", 
            dest   = "domain",
            type   = "string", 
            help = "example: ./dnszone.py -d host.com")
              
        (option,args) = parser.parse_args()
        if not option.domain:
            print "example: ./dnszone.py -d host.com" 
            sys.exit(0)   
        else:
                  
            print"""
            ##############################################
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            #          DNS Zone Transfer v0.1            #
            #               Coder: 0x94                  #
            #             twitter.com/0x94               #
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            ##############################################  
            """          
            starter=Zone(option.domain)
            starter.baslat()     
    except KeyboardInterrupt:
        print('\n Exit.')
        sys.exit(0)