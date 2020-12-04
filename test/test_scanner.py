#!/usr/bin/env python3
import pytest
from scanner import *


def test_nmap_scan_host():
    input = ['www.synacktiv.com']
    report = nmap_scan(input)
    assert any('www.synacktiv.com' in host.hostnames for host in report.hosts)

def test_nmap_scan_ipv4():
    input = ['8.8.8.8']
    report = nmap_scan(input)
    assert any('dns.google' in host.hostnames for host in report.hosts)

def test_nmap_scan_ipv6():
    input = ['2001:4860:4860::8888']
    with pytest.raises(SystemExit):
        report = nmap_scan(input)    # No report if source doesn't use IPv6
        if report:
            assert any('dns.google' in host.hostnames for host in report.hosts)

def test_nmap_scan_cidr():
    input = ['91.209.35.0/24']
    report = nmap_scan(input)
    assert report.hosts_total > 1

def test_nmap_scan_misc():
    input = ['www.synacktiv.com', '8.8.8.8']
    report = nmap_scan(input)
    assert report.hosts_total == 2

def test_nmap_scan_bad():  
    input = ['blabla']
    with pytest.raises(SystemExit):
        report = nmap_scan(input)
        assert report == null
