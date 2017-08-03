# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.header import Header
import time

def spiderWord2(email, urlProcesso):
    url = urlProcesso
    response = requests.get(url, verify=False)
    texto = response.text
    soup = BeautifulSoup(texto)

    options = Options()
    #options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=os.path.abspath("/Users/edsonsoares/PycharmProjects/WebSpider/chromedriver"),   chrome_options=options)
    driver.implicitly_wait(40)
    driver.get(url)

    contrasena = driver.find_element_by_name('senhaProcesso')
    contrasena.send_keys('kagheh')

    boton = driver.find_element_by_id('btEnviarSenha')
    boton.click()

    data = driver.find_element_by_xpath('//*[@id="tabelaUltimasMovimentacoes"]/tbody/tr[1]/td[1]')
    movimento = driver.find_element_by_xpath('//*[@id="tabelaUltimasMovimentacoes"]/tbody/tr[1]/td[3]')

    atualizado = False

    if os.path.isfile('dataText.txt'):
        file = open("dataText.txt", "r+")
        dtTmp = file.read()
        if data.text > dtTmp:
            atualizado = True
            file.seek(0)
            file.truncate()
            file.write(data.text)
    else:
        file = open("dataText.txt", "w")
        file.write(data.text)
        atualizado = True

    if atualizado:
        msg = 'Foi encontrada uma alteração no Processo: ' + data.text + '\n\n' + movimento.text + ' \n\nPágina TSJ: ' + '( ' + url + ' )'
        print(msg)
        dataAtual = data.text
        sendEmail(msg, email)
    else:
        print('*** Não foram encontradas alterações no Processo ***')

    file.close()
    driver.close()

def spiderWord(email, nuProcesso, codigo):
    url = 'http://www.tjsp.jus.br/'
    response = requests.get(url, verify=False)
    texto = response.text
    soup = BeautifulSoup(texto)

    options = Options()
    #options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=os.path.abspath("/Users/edsonsoares/PycharmProjects/WebSpider/chromedriver"),   chrome_options=options)
    driver.get(url)

    nuProcessoTxt = driver.find_element_by_xpath('//*[@id="Processo"]')
    nuProcessoTxt.send_keys(nuProcesso)

    boton = driver.find_element_by_xpath('//*[@id="ConsultarProcessoButton"]')
    boton.click()

    #Muda para a nova janela do processo para entrar a senha
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[-1])

    contrasena = driver.find_element_by_xpath('//*[@id="popupSenha"]/table/tbody/tr[5]/td[2]/input[1]')
    contrasena.send_keys(codigo)

    boton = driver.find_element_by_xpath('//*[@id="btEnviarSenha"]')
    boton.click()

    data = driver.find_element_by_xpath('//*[@id="tabelaUltimasMovimentacoes"]/tbody/tr[1]/td[1]')
    movimento = driver.find_element_by_xpath('//*[@id="tabelaUltimasMovimentacoes"]/tbody/tr[1]/td[3]')

    atualizado = False

    if os.path.isfile('dataText.txt'):
        file = open("dataText.txt", "r+")
        dtTmp = file.read()
        if data.text > dtTmp:
            atualizado = True
            file.seek(0)
            file.truncate()
            file.write(data.text)
    else:
        file = open("dataText.txt", "w")
        file.write(data.text)
        atualizado = True

    if atualizado:
        msg = 'Foi encontrada uma alteração no Processo: ' + data.text + '\n\n' + movimento.text + ' \n\nPágina TSJ: ' + '( ' + url + ' )'
        print(msg)
        dataAtual = data.text
        sendEmail(msg, email)
    else:
        print('*** Não foram encontradas alterações no Processo ***')

    file.close()
    driver.close()


def sendEmail(mensagem, email):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    sender = 'r3im0z@gmail.com'
    password = "50p#1414"
    recipient = email
    subject = 'Alteração no Processo'

    msg = MIMEText(mensagem.encode('utf-8'), 'plain', 'utf-8')

    msg['Subject'] = Header(subject, 'ISO-8859-1')
    msg['To'] = recipient
    msg['From'] = sender

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(sender, password)

    session.sendmail(sender, recipient, msg.as_string())
    session.quit()

#spiderWord2('edson.soares.r@gmail.com', 'https://esaj.tjsp.jus.br/cpopg/show.do?processo.foro=477&processo.codigo=D90003CRD0000')
spiderWord('edson.soares.r@gmail.com', '10195165720168260477', 'kagheh')