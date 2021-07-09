#/bin/bash

CERT_FILES=("AC+Secretaria+da+Receita+Federal+do+Brasil+v4.cer" "AC+VALID+RFB+v5.cer" "Autoridade+Certificadora+Raiz+Brasileira+v5.cer")
CERT_ORG="acras.pfx"
CERT_ORG_PASS="Acras1245"
CERT_DIR="./certs"
INSTALL_DIR="./selenium_profile_firefox"

pk12util -i ${CERT_DIR}/${CERT_ORG} -d ${INSTALL_DIR} -W ${CERT_ORG_PASS}

for cert_file in ${CERT_FILES[@]}; do
  certutil -A -n "${cert_file}" -t "TCu,Cuw,Tuw" -i "${CERT_DIR}/$cert_file" -d ${INSTALL_DIR}
done;
