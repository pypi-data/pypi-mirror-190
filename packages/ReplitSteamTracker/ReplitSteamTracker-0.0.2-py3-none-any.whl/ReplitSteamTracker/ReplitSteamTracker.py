import requests
from bs4 import BeautifulSoup as bs
from time import sleep


def checkDiscount(divPrice, divPercent):
  newPrice = divPrice[(divPrice.find('$') + 1):(divPrice.find('</div>'))]
  percent = divPercent[(divPercent.find('pct">-') + 6):(divPercent.find('%'))]
  price_percent = newPrice + '#' + percent
  return price_percent


def Steamscrap(url):
  #send requests
  try:
    r = requests.get(url)
  except:
    raise Exception("HTTP Error 429")
  sleep(0.25)
  if r.ok:
    soup = bs(r.text, 'html.parser')
  else:
    raise Exception("HTTP Error 429")
  #check Name
  divName = soup.find('div', {
    'class': 'apphub_HomeHeaderContent'
  }).find('div', {'id': 'appHubAppName'})
  divName = str(divName)
  gameName = divName[(divName.find('id="appHubAppName">') +
                      19):divName.find('</div>')]
  #if there is a '&'
  if gameName.find('&amp;') >= 0:
    gameName.replace('&amp;', '&')
    #if game is comming soon
  try:
    divPrice = soup.find('div',
                         {'class': 'game_area_comingsoon game_area_bubble'}).find('a',{'class' : 'btn_green_steamui btn_medium'})
    return 0, gameName
  except:
    pass
  #check Price
  divPrice = soup.find('div', {
    'class': 'game_area_purchase_game'
  }).find('div', {'class': 'game_purchase_price price'})
  divPrice = str(divPrice)

  #if game is free
  isFree = divPrice.find('Free')
  if divPrice != 'None':
    if isFree >= 0:
      free = 'free'
      return free, gameName

    else:
      #if there is no discount + not free
      price = divPrice[(divPrice.find('$') + 1):(divPrice.find('</div>') - 1)]
      try:
        float(price)
        return price, gameName
      except:
        return 'demo', gameName

  else:
    divPrice = soup.find('div', {
      'class': 'discount_block game_purchase_discount'
    }).find('div', {'class': 'discount_final_price'})
    divPercent = soup.find('div', {
      'class': 'discount_block game_purchase_discount'
    }).find('div', {'class': 'discount_pct'})
    divPrice = str(divPrice)
    divPercent = str(divPercent)

    #checking diff of discount
    discount = checkDiscount(divPrice, divPercent)
    return discount, gameName
