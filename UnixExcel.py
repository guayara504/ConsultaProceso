import msvcrt
from re import L
import shutil
import sys
import time
import os
from datetime import datetime
from webbrowser import Chrome
import pyexcel
import xlwt
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class Extractor(object):
    def __init__(self):

        #Escoger Chrome como Navegador
        op = webdriver.ChromeOptions()
        op.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=op)
        #Escoger preferencias del WebDriver
        self.base_url = "https://consultaprocesos.ramajudicial.gov.co/Procesos/NumeroRadicacion/"
        self.delay = 5
        self.driver.wait = WebDriverWait(self.driver, self.delay)
        self.driver.set_window_size(1024, 768)
        self.load_page()
    
    #Cargar la pagina solicitada
    def load_page(self):
        self.driver.get(self.base_url)
        def page_loaded(driver):
            path = '//*[@id="mainContent"]/div/div/div/div[1]/div/div[2]/span'
            return driver.find_element(By.XPATH, path)
        wait = WebDriverWait(self.driver, self.delay)
        os.system ("cls")
        try:
            wait.until(page_loaded)
        except TimeoutException:
            print('line: 38 error: No se cargo la pagina, TimeoutException')

   

    #Ingresar al proceso en la pagina
    def iniciar_busqueda(self):
        #Click en arrojar todas las actuaciones
        self.driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div/div/div[1]/div/form/div[1]/div[1]/div/div/div/div[1]/div/div[2]/div').click()
    
    def ingresar_radicado(self):
        #Pegar Radicado
        self.driver.find_element(By.XPATH,"//input[@maxlength='23']").clear()
        self.driver.find_element(By.XPATH,"//input[@maxlength='23']").send_keys("76001333300120210015600")
        #Click en boton 'Consulta'
        self.driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div/div/div[1]/div/form/div[2]/button[1]/span').click()
        #Ingresar a datos del proceso
        if WaitForElement(self, '//*[@id="mainContent"]/div/div/div/div[2]/div/div/div[2]'):
            self.driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div/div/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]').click()

    #Extrae los datos del proceso
    def extraer_datos(self,datos):
        if WaitForElement(self, '//*[@id="mainContent"]/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/div/table/tbody/div/tr/th/tr[1]/th'):
            datos["fecha"] = (self.driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/div/table/tbody/div/tr/th[1]/tr[1]/td').text)
            datos["despacho"] = (self.driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/div/table/tbody/div/tr/th/tr[2]/td').text)
            datos["ponente"] = (self.driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/div/table/tbody/div/tr/th/tr[3]/td').text)
            datos["tipo_proceso"] = (self.driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/div/table/tbody/div/tr/th/tr[4]/td').text)
            datos["clase_proceso"] = (self.driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/div/table/tbody/div/tr/th/tr[5]/td').text)
    def extraer_partes(self,datos):
        self.driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[3]').click()
        if WaitForElement(self, '//*[@id="input-131"]'):
            datos["demandante"] = (self.driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div/div[2]/div/table/tbody/tr[1]/td[2]').text)
            datos["demandado"] = (self.driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div/div[2]/div/table/tbody/tr[2]/td[2]').text)    
    
    def extraer_actuaciones(self,actuaciones):
        pass

#Espera por el elemento
def WaitForElement(self, path):
    demora = 3
    limit = demora
    inc = 1
    c = 0
    while c < limit:
        try:
            self.driver.find_element(By.XPATH,path)
            return 1
        except:
            time.sleep(inc)
            c+=inc
    return 0

#Clase principal   
if __name__ == "__main__": 
    datos = {"fecha": "","despacho":"","ponente":"","tipo_proceso":"","clase_proceso":"","demandante":"","demandado":""}
    actuaciones = []
    buscador = Extractor()
    buscador.iniciar_busqueda()
    buscador.ingresar_radicado()
    buscador.extraer_datos(datos)
    buscador.extraer_partes(datos)
    
    for dato in datos:

        print(dato+":",datos[dato])
