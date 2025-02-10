from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import re
import json
from datetime import datetime

now = datetime.now()
data_inicio = now.strftime("%d/%m/%Y %H:%M:%S")

# -- Selenium configs
chrome_options = Options()
chrome_options.add_argument("--log-level=3")
navegador = webdriver.Chrome(options=chrome_options)

navegador.get("") # link to acesses intelligent hub



print('Faça o login no MDM')
input('Após fazer o login, aperte ENTER para começar... ') # press enter after login

sessao = input("Continuar sessão anterior? S/N: ").lower() # input to load last session
print('')



def addToJson(dumpThisArray): # save current device status so you can load after
    checkpoint = json.dumps(dumpThisArray, ensure_ascii=False)
    with open(r'checkpoint.json', 'w', encoding='utf-8') as arquivo:
        arquivo.write(checkpoint)

if 's' in sessao: # if you want to load last session
    getCheckpoint = []
    getLog = open(r'checkpoint.json', 'r')
    getLog = getLog.read()
    getLog = eval(getLog)
    getCheckpoint = getLog

checkProducts = []
finalizados = []
AllSerialNumber = []

    

def novaSessão(): # apply the tag for each device (Apply tag, clear cache and save the device url)
    while AllSerialNumber:
        count = 0

        for sn in AllSerialNumber:
            count = count +1

            def AddTag(sn):
                try:
                    print(f'=================================|  {sn}  |=================================') # style
                    print(f"                                                                           Falta: {len(AllSerialNumber)}")

                    # Search device
                    sleep(3)
                    navegador.get('https://cn259.awmdm.com/AirWatch/#/Device/List')
                    sleep(1)
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="SearchText"]'))).send_keys(Keys.CONTROL, 'A') # search Device: select search bar
                    sleep(1)
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="SearchText"]'))).send_keys(Keys.BACKSPACE) # search Device: clear search bar
                    sleep(1)
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="SearchText"]'))).send_keys(sn) # search Device: paste device SN
                    sleep(1)
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="SearchText"]'))).send_keys(Keys.RETURN) # search Device: enter
                    sleep(1)
                    link_device = WebDriverWait(navegador, 25).until(EC.presence_of_element_located(('xpath', f'//*[@id="airwatchdevicelistsearch"]/section[3]/section[1]/table/tbody/tr//span[text()="{sn}"]'))) # locate device TR
                    sleep(2)
                    link_device.find_element(By.XPATH, './ancestor::a').click() # Open the device url

                    # Device: Clear App Data
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="device-details-apps"]'))).click() # Open "apps" window
                    sleep(0.5)
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="SearchText"]'))).send_keys('chrome') # search "chrome" in apps

                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="SearchText"]'))).send_keys(Keys.RETURN) # Enter
                    sleep(1.5)
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="airwatchdevicesdeviceapplicationsearch"]/section[3]/section[1]/table/tbody/tr[1]/td[1]/span/input'))).click() # checbox chrome
                    sleep(0.5)
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '/html/body/main/div/div/div[3]/section/section/div/div/div/div[4]/section[1]/div[2]/div/a'))).click() # "More Actions" chrome
                    sleep(0.5) 
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="grid_actions_more"]/section/div/ul/li[4]/a'))).click() # clear app data
                    sleep(0.5)
                    navegador.switch_to.alert.accept() # accpet alert
                    print(">> Limpeza do AppData")

                    #Device -> Add tag
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '/html/body/main/div/div/hgroup/div[2]/div/a[5]'))).click() # more actions add tag
                    sleep(0.5)
                    # locate manage tags
                    try:
                        WebDriverWait(navegador, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="maincolumn"]/hgroup/div[2]/div/section[2]/div[4]/ul/li[2]/a'))).click()
                    except TimeoutException:
                        WebDriverWait(navegador, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="maincolumn"]/hgroup/div/div/section[2]/div[4]/ul/li[2]/a'))).click()
                    sleep(0.5)
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="search_available_tags"]/input'))).send_keys('Ct60 - Android 13') # search "android 13"
                    sleep(0.5)
                    
                    # Condição "se a tag estiver em "available tags" ele adiciona, se não, se ela estiver em "assigned Tags" ele só salva
                    try:
                        WebDriverWait(navegador, 3).until(EC.presence_of_element_located(('xpath', '//*[@id="available_tags"]//span[text()="CT60 - Android 13 Update"]'))).click() # ADD Tag andorid 13
                        sleep(0.5)
                        WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="DeviceTagManagementModal"]/form/section/div/button[text()="Save"]'))).click() # save button
                        print(">> Tag foi adicionada")
                    except TimeoutException: # if the tag already applied
                        WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="DeviceTagManagementModal"]/form/section/div/button[text()="Save"]'))).click() # save button
                        print(">> Já possui a Tag")


                    geturl = navegador.current_url # copy the device url
                    currentURL = geturl.replace('Apps', "Products")

                    checkProducts.append({
                        "sn":sn,
                        "url":currentURL,
                    })
                    AllSerialNumber.remove(sn)
                    print(f'==================================================================================')

                except Exception as erro:
                    print(f"Erro ao procurar o Device {sn}. Erro encontrado:")
                    print(erro)
                    print(f'==================================================================================')   

            AddTag(sn)
    
    addToJson(checkProducts)
    check_steps()


# after applyng all the tags, check uptade status
def check_steps():
    while checkProducts:
        
        for device in checkProducts:
            print(f'=================================|  {device['sn']}  |=================================') # apenas frufru
            print(f'    {device["url"]}        Falta: {len(checkProducts)}')
            print(' ')


            def stepOne():
                try:
                    navegador.get(device["url"]) # Device url
                    navegador.refresh()
                    
                    step1_textName = WebDriverWait(navegador,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="airwatchprovisioningpoliciessearchdevicepolicies"]//a[text()="1 - Clear previous Update Files - Honeywell"]'))) # procura o step1
                    sleep(0.5)
                    try:
                        step1_textName.find_element(By.XPATH,'./ancestor::tr//td[text()="Compliant"]') # If status is "compliant"
                        print("Step 1 - Compliant")
                        return True
                    except:
                        try:
                            step1_textName.find_element(By.XPATH,'./ancestor::tr//td[text()="Non-Compliant - Waiting For Dependencies"]') # If status is "Waiting For Dependencies"
                            print("   Step 1 - Waiting For Dependencies")
                            return False

                        except:
                            step1_textName.find_element(By.XPATH,'./ancestor::tr//td[text()="Non-Compliant - In Progress"]') # If status is "in progress"
                            print("   Step 1 - In Progress")
                            return False

                except TimeoutException:
                    print("Não foi encontrado Step 1 Próximo passo...")
                except Exception as erro:
                    print(f'ainda atualizando - {device['sn']} - {erro}')

                    
            def stepTwo():
                try:

                    step2_textName = WebDriverWait(navegador,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="airwatchprovisioningpoliciessearchdevicepolicies"]//a[text()="CT60 - Android 13 - Step 2 - Allow Wipe Update"]'))) # procura o step2
                    sleep(0.5)
                    try:
                        step2_textName.find_element(By.XPATH,'./ancestor::tr//td[text()="Compliant"]') # If status is "compliant"
                        print("Step 2 - Compliant")
                        return True
                    except:
                        try:
                            step2_textName.find_element(By.XPATH,'./ancestor::tr//td[text()="Non-Compliant - Waiting For Dependencies"]') # If status is Waiting For Dependencies
                            print("   Step 2 - Waiting For Dependencies")
                            return False

                        except:
                            step2_textName.find_element(By.XPATH,'./ancestor::tr//td[text()="Non-Compliant - In Progress"]') # If status is in progress
                            print("   Step 2 - In Progress")
                            return False

                except TimeoutException:
                    print("Não foi encontrado Step 2 Próximo passo...")
                except Exception as erro:
                    print(f'step2 atualizando - {device['sn']} - {erro}')


            def stepThree():
                try:

                    step3_textName = WebDriverWait(navegador,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="airwatchprovisioningpoliciessearchdevicepolicies"]//a[text()="CT60 - Android 13 - Step 3 - Send File"]'))) # procura o step2
                    sleep(0.5)

                    try:
                        step3_textName.find_element(By.XPATH,'./ancestor::tr//td[text()="Compliant"]') # If status is "compliant"
                        print("Step 3 - Compliant")
                        return True
                    except:
                        try:
                            step3_textName.find_element(By.XPATH,'./ancestor::tr//td[text()="Non-Compliant - Waiting For Dependencies"]') # If status is Waiting For Dependencies
                            print("   Step 3 - Waiting For Dependencies")
                            return False

                        except:
                            step3_textName.find_element(By.XPATH,'./ancestor::tr//td[text()="Non-Compliant - In Progress"]') # If status is in progress
                            print("   Step 3 - In Progress")
                            return False

                except TimeoutException:
                    print("Não foi encontrado Step 3 Próximo passo...")
                except Exception as erro:
                    print(f'step3 atualizando - {device['sn']} - {erro}')
                
            def applyDeviceConfig():
                try:
                    # apply Device config
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="SearchText"]'))).send_keys(Keys.CONTROL, 'A') # select all
                    sleep(0.5)
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="SearchText"]'))).send_keys(Keys.BACKSPACE) # clear search bar
                    sleep(0.5)
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="SearchText"]'))).send_keys("Honeywell CT60 Device Config Regional") # search product
                    sleep(0.5)
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="SearchText"]'))).send_keys(Keys.RETURN) # Enter
                    sleep(2)
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '/html/body/main/div/div/div[3]/section/section/div/div/section/div/section[3]/section[1]/table/tbody/tr/td[1]/span/input'))).click() # checkbox device regional
                    sleep(0.5)
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="top_actions_container"]/a[2]'))).click() # checkbox device regional
                    sleep(0.5)
                    navegador.switch_to.alert.accept()
                    print('-Device config aplicado')
                    return True
                except:
                    print(f'Não foi possivel aplicar o Device config regional (validar manualmente)')
                    return False
            

            return_StepOne = stepOne()
            return_StepTwo = stepTwo()
            return_StepThree = stepThree()
            if return_StepOne and return_StepTwo and return_StepThree:
                return_DeviceConfig = applyDeviceConfig()

            print(' ')
            # if all the uptdates and device config is true, then remove the tag and
            if return_StepOne and return_StepTwo and return_StepThree and return_DeviceConfig:

                try:
                    # Remove Tag
                    sleep(0.5)
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="MoreActionsPopup"]'))).click() # more actions add tag
                    sleep(0.5)
                    try:
                        WebDriverWait(navegador, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="maincolumn"]/hgroup/div[2]/div/section[2]/div[4]/ul/li[2]/a'))).click()
                    except TimeoutException:
                        WebDriverWait(navegador, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="maincolumn"]/hgroup/div/div/section[2]/div[4]/ul/li[2]/a'))).click()
                    sleep(0.5)
                    element_tag = WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="assigned_tags"]//span[text()="CT60 - Android 13 Update"]'))) # Locate the tag
                    sleep(0.5)
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="DeviceTagManagementModal"]/form/section/div/button[text()="Save"]'))).click() # save button
                    print('>> Tag Removida')
                except Exception as erro:
                    print(f'Não foi possivel remover a tag: Erro {erro}')


                try:
                    # active Admin mode
                    WebDriverWait(navegador, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="MoreActionsPopup"]'))).click()
                    sleep(0.5)
                    try:
                        WebDriverWait(navegador, 3).until(EC.presence_of_element_located(('xpath', '//*[@id="maincolumn"]/hgroup/div[2]/div/section[2]/div[5]/ul/li[1]/a'))).click()
                    except:
                        WebDriverWait(navegador, 3).until(EC.presence_of_element_located(('xpath', '//*[@id="maincolumn"]/hgroup/div/div/section[2]/div[5]/ul/li[1]/a'))).click()
                    navegador.switch_to.alert.accept()
                    sleep(0.5)
                    navegador.switch_to.alert.accept()
                    print(">> Está em modo ADMIN")
                except Exception as erro:
                    print(f'Não foi possivel entrar no modo Admin')


                finalizados.append(device)
                checkProducts.remove(device)
                addToJson(checkProducts)

            print(' ')
            print(f'==================================================================================')

if "n" in sessao:
    raw_sn = input('Digite os SN, separando por virgula: ')
    AllSerialNumber = re.split(r'\s*,\s*', raw_sn)
    novaSessão()
else:
    checkProducts = getCheckpoint
    print(checkProducts)
    check_steps()

# Finalizados
def print_finalizados():
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|  Finalizados  |=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    print('')
    for device in finalizados:
        print(f"Serial: {device['sn']} | URL: {device['url']}")
    print('')
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=--=-')

print_finalizados()
print('--Tudo finalizado--')
now = datetime.now()
data_final = now.strftime("%d/%m/%Y %H:%M:%S")

print(f'O script teve inicio as {data_inicio} e finalizou as {data_final}')

while True:
    sleep(3000)


