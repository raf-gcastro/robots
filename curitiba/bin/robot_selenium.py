from selenium import webdriver
from selenium.webdriver import FirefoxOptions, FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os
from sys import argv


download_dir = os.environ['HOME'] + "/Downloads"
download_timeout = 10

params = { 
    "Exercicio": "2021",
    "Mes": "Maio",
    "CodigoVerificacao": "", 
    "NumeroInicial": "", 
    "NumeroFinal": "", 
    "NumeroLote": "", 
    "NumeroRPS": ""
}


def download_wait(directory, timeout, nfiles=None):
    from time import sleep

    """
    Wait for downloads to finish with a specified timeout.

    Args
    ----
    directory : str
        The path to the folder where the files will be downloaded.
    timeout : int
        How many seconds to wait until timing out.
    nfiles : int, defaults to None
        If provided, also wait for the expected number of files.

    """
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        sleep(1)
        dl_wait = False
        files = os.listdir(directory)
        if nfiles and len(files) != nfiles:
            dl_wait = True

        for fname in files:
            if fname.endswith('.crdownload'):
                dl_wait = True

        seconds += 1
    return seconds

profile = webdriver.FirefoxProfile('selenium_profile_firefox')
options = Options()
if (len(argv) > 1 and argv[1] == '1'):
    options.headless = True

browser = webdriver.Firefox(
    firefox_profile=profile,
    options=options
)

browser.get('https://isscuritiba.curitiba.pr.gov.br/iss/default.aspx')
handles = browser.window_handles
browser.switch_to.window(handles[0])

timeout = 5
element_present = EC.presence_of_element_located((By.ID, 'btnLoginCertificado'))
WebDriverWait(browser, timeout).until(element_present)

login_button = browser.find_elements_by_xpath('//input[@id="btnLoginCertificado"]')[0]
login_button.click()

browser.get('https://isscuritiba.curitiba.pr.gov.br/iss/AcessoFrame/frmAcessoSistema.aspx?sParam=CONSULTAR_NFSE_REC')

iframe = browser.find_element_by_id('ctl00_ContentPlaceHolder1_frmObras')
browser.switch_to.frame(iframe)

for key, value in params.items():
    if value == "": continue
    try:
        element = Select(browser.find_element_by_id(key))
        element.select_by_visible_text(value)
    except:
        element = browser.find_element_by_id(key)
        browser.execute_script("arguments[0].setAttribute('value', arguments[1])", element, value);

search_button = browser.find_element_by_id('btnPesquisar')
search_button.click()

timeout = 5
element_present = EC.presence_of_element_located((By.NAME, 'tblNfse_length'))
WebDriverWait(browser, timeout).until(element_present)

#select_lenght = Select(browser.find_element_by_name('tblNfse_length'))
#select_lenght.select_by_visible_text('100')

generate_xml_button = browser.find_element_by_link_text('Gerar Arquivo XML')
generate_xml_button.click()

download_wait(download_dir, download_timeout, nfiles=None)

browser.quit()
