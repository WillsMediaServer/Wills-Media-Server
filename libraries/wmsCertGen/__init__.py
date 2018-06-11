import logging
import os
import random
import subprocess
import string
import sys


class CertGen:
    def __init__(self, config, SECURITY_DIR):
        self.logger = logging.getLogger("wms.cert-gen")
        try:
            data = subprocess.Popen([
                    "openssl",
                    "version"
                ], stdout=subprocess.PIPE)
            stdout, stderr = data.communicate()
            self.logger.debug(stderr)
            self.logger.debug(stdout.decode("utf-8"))
        except Exception:
            self.logger.info("openSSL Doesn't exist on the path, please install it or disable https")
            sys.exit()
        self.config = config
        self.generateList = []
        self.SECURITY_DIR = SECURITY_DIR
        self.checks()
        if self.generateList != []:
            self.generate()

    def generate(self):
        self.logger.info("Need to generate {}".format(self.generateList))
        toDoList = self.generateList
        
        if "CA-Private-Key" in toDoList:
            self.logger.info("Generating WMS Cert Auth Private Key")
            pkeygenLocation = os.path.join(self.SECURITY_DIR, "wmsCA.key")
            pkeygen = subprocess.Popen([
                    "openssl",
                    "genrsa",
                    "-out",
                    pkeygenLocation,
                    "2048"
                ], stdout=subprocess.PIPE)
            stdout, stderr = pkeygen.communicate()
        
        if "CA-Root-Cert" in toDoList:
            self.logger.info("Generating WMS Cert Auth Private Key")
            pkeygenLocation = os.path.join(self.SECURITY_DIR, "wmsCA.key")
            rootcertLocation = os.path.join(self.SECURITY_DIR, "wmsCA.pem")
            rootcertGen = subprocess.Popen([
                    "openssl",
                    "req",
                    "-x509",
                    "-new",
                    "-nodes",
                    "-key",
                    pkeygenLocation,
                    "-sha256",
                    "-days",
                    "365",
                    "-subj",
                    "/C=GB/ST=Unknown/L=Unknown/O=Wills Media Server/CN=Wills Media Server",
                    "-out",
                    rootcertLocation
                ], stdout=subprocess.PIPE)
            stdout, stderr = rootcertGen.communicate()
    
        if "Cert-Private-Key" in toDoList:
            self.logger.info("Generating WMS Certificate Private Key")
            pkeygenLocation = os.path.join(self.SECURITY_DIR, "wmsCert.key")
            pkeygen = subprocess.Popen([
                    "openssl",
                    "genrsa",
                    "-out",
                    pkeygenLocation,
                    "2048"
                ], stdout=subprocess.PIPE)
            stdout, stderr = pkeygen.communicate()

        if "Cert-Signing-Request" in toDoList:
            self.logger.info("Generating WMS Certificate Signing Request")
            pkeygenLocation = os.path.join(self.SECURITY_DIR, "wmsCert.key")
            csrLocation = os.path.join(self.SECURITY_DIR, "wmsCert.csr")
            csrGen = subprocess.Popen([
                    "openssl",
                    "req",
                    "-new",
                    "-key",
                    pkeygenLocation,
                    "-subj",
                    "/C=GB/ST=Unknown/L=Unknown/O=Wills Media Server/CN=WMS",
                    "-out",
                    csrLocation
                ], stdout=subprocess.PIPE)
            stdout, stderr = csrGen.communicate()
        
        if "Cert" in toDoList:
            self.logger.info("Generating WMS Certificate")
            csrLocation = os.path.join(self.SECURITY_DIR, "wmsCert.csr")
            caPrivateKeyLocation = os.path.join(self.SECURITY_DIR, "wmsCA.key")
            caCertificateLocation = os.path.join(self.SECURITY_DIR, "wmsCA.pem")
            certLocation = os.path.join(self.SECURITY_DIR, "wmsCert.crt")
            certConfig = os.path.join(self.SECURITY_DIR, "../", "../", "libraries", "wmsCertGen", "wmsCertConfig.ext")
            certGen = subprocess.Popen([
                    "openssl",
                    "x509",
                    "-req",
                    "-in",
                    csrLocation,
                    "-CA",
                    caCertificateLocation,
                    "-CAkey",
                    caPrivateKeyLocation,
                    "-CAcreateserial",
                    "-out",
                    certLocation,
                    "-days",
                    "365",
                    "-sha256",
                    "-extfile",
                    certConfig
                ], stdout=subprocess.PIPE)
            stdout, stderr = certGen.communicate()

    def checks(self):
        self.logger.info("Checking if certificates already exist")

        if not os.path.exists(os.path.join(self.SECURITY_DIR, "wmsCA.key")):
            self.logger.info("wms CA Private key doesn't exist. Adding to Generate list")
            self.generateList.append("CA-Private-Key")
        
        if not os.path.exists(os.path.join(self.SECURITY_DIR, "wmsCA.pem")):
            self.logger.info("wms CA Root Certificate doesn't exist. Adding to Generate list")
            self.generateList.append("CA-Root-Cert")
        
        if not os.path.exists(os.path.join(self.SECURITY_DIR, "wmsCert.key")):
            self.logger.info("wms Certificate Private Key doesn't exist. Adding to Generate list")
            self.generateList.append("Cert-Private-Key")
        
        if not os.path.exists(os.path.join(self.SECURITY_DIR, "wmsCert.csr")):
            self.logger.info("wms Certificate Signing request doesn't exist. Adding to Generate list")
            self.generateList.append("Cert-Signing-Request")
        
        if not os.path.exists(os.path.join(self.SECURITY_DIR, "wmsCert.crt")):
            self.logger.info("wms Certificate doesn't exist. Adding to Generate list")
            self.generateList.append("Cert")

        self.logger.info("Finished checking")
