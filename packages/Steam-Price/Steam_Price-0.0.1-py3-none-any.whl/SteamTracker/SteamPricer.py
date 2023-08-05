import requests
from bs4 import BeautifulSoup as bs
from time import sleep


def checkDiscount(divPrice,divPercent) :
  newPrice = divPrice[(divPrice.find('$') + 1):(divPrice.find('USD') - 1)]
  percent = divPercent[(divPercent.find('pct">-') + 6):(divPercent.find('%'))]
  price_percent = newPrice + '/' + percent
  return price_percent


def Steamscrap(url) :
  #send requests
  try :
    r=requests.get(url)
  except : raise Exception("HTTP Error 429")
  sleep(0.25)
  if r.ok :
    soup = bs(r.text,'html.parser')
  else : 
    raise Exception("HTTP Error 429")
  
  #check Price + Name
  divPrice = soup.find('div',{'class': 'game_area_purchase_game'}).find('div',{'class': 'game_purchase_price price'})
  divPrice = str(divPrice)
  #if game is free
  isFree = divPrice.find('Free')
  if divPrice != 'None' :
    if isFree >= 0 :
      free = 'free'
      return free
    else :
      #if there is no discount + not free
      price = divPrice[(divPrice.find('$') + 1):(divPrice.find('USD') - 1)]
      return price
  else :
    divPrice = soup.find('div',{'class': 'discount_block game_purchase_discount'}).find('div',{'class': 'discount_final_price'})
    divPercent = soup.find('div',{'class': 'discount_block game_purchase_discount'}).find('div',{'class': 'discount_pct'})
    divPrice = str(divPrice) 
    divPercent = str(divPercent)
    #checking diff of discount
    discount = checkDiscount(divPrice,divPercent)
    return discount
  


  

  
  
  
