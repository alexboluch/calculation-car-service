import math

def create_logic(new):
    commission_price = calc_commission(new.validated_data['auction_price'])
    swift_price = calc_swift(new, commission_price)
    registration_price = calc_registration(new, commission_price)
    delivery_land_price, delivery_all_price = calc_delivery_price(new)
    customs_clearance_price = calc_customs_clearance(new, commission_price, swift_price)
    end_price = calc_end_price(new, delivery_all_price, customs_clearance_price, commission_price, swift_price, registration_price)
    return commission_price, swift_price, registration_price, delivery_land_price, delivery_all_price, customs_clearance_price, end_price

def calc_commission(auction_price):
    if(auction_price >= 500 and auction_price < 550):
        commission_price = 233
    elif(auction_price >= 550 and auction_price < 600):
        commission_price = 238
    elif(auction_price >= 600 and auction_price < 700):
        commission_price = 248
    elif(auction_price >= 700 and auction_price < 800):
        commission_price = 263
    elif(auction_price >= 800 and auction_price < 900):
        commission_price = 278
    elif(auction_price >= 900 and auction_price < 1000):
        commission_price = 293
    elif(auction_price >= 1000 and auction_price < 1200):
        commission_price = 328
    elif(auction_price >= 1200 and auction_price < 1300):
        commission_price = 353
    elif(auction_price >= 1300 and auction_price < 1400):
        commission_price = 368
    elif(auction_price >= 1400 and auction_price < 1500):
        commission_price = 378
    elif(auction_price >= 1500 and auction_price < 1600):
        commission_price = 398
    elif(auction_price >= 1600 and auction_price < 1700):
        commission_price = 413
    elif(auction_price >= 1700 and auction_price < 1800):
        commission_price = 423
    elif(auction_price >= 1800 and auction_price < 2000):
        commission_price = 438
    elif(auction_price >= 2000 and auction_price < 2400):
        commission_price = 473
    elif(auction_price >= 2400 and auction_price < 2500):
        commission_price = 483
    elif(auction_price >= 2500 and auction_price < 3000):
        commission_price = 498
    elif(auction_price >= 3000 and auction_price < 3500):
        commission_price = 548
    elif(auction_price >= 3500 and auction_price < 4000):
        commission_price = 598
    elif(auction_price >= 4000 and auction_price < 4500):
        commission_price = 633
    elif(auction_price >= 4500 and auction_price < 5000):
        commission_price = 658
    elif(auction_price >= 5000 and auction_price < 6000):
        commission_price = 683
    elif(auction_price >= 6000 and auction_price < 7500):
        commission_price = 718
    elif(auction_price >= 7500 and auction_price < 8000):
        commission_price = 743
    elif(auction_price >= 8000 and auction_price < 10000):
        commission_price = 763
    elif(auction_price >= 10000 and auction_price < 15000):
        commission_price = 788
    elif(auction_price >= 15000):
         commission_price = ((auction_price / 100) * 4) + 118
    return commission_price

def calc_delivery_price(new):
    delivery_land_price = new.validated_data["distance_to_port"] + 100
    delivery_all_price = math.ceil(delivery_land_price + new.validated_data['delivery_sea_price']
    + 0.01 * (delivery_land_price + new.validated_data['delivery_sea_price']) + 30)
    return delivery_land_price, delivery_all_price

def calc_customs_clearance(new, commission_price, swift_price):
    customs_clearance_price = math.ceil(57 * new.validated_data['engine'] / 1000 * (2021 - new.validated_data['year'])
    + 0.1*(new.validated_data['auction_price'] + commission_price + swift_price)
    + 0.2 * ((new.validated_data['auction_price'] + commission_price + swift_price)
    + 57 * new.validated_data['engine'] / 1000 * (2021 - new.validated_data['year'])+0.1 *
    (new.validated_data['auction_price'] + commission_price + swift_price))
    + 0.05 * (new.validated_data['auction_price'] + commission_price + swift_price))
    return customs_clearance_price

def calc_end_price(new, delivery_all_price, customs_clearance_price, commission_price, swift_price, registration_price):
    end_price = math.ceil(delivery_all_price + customs_clearance_price + new.validated_data['auction_price']
    + commission_price + swift_price + new.validated_data['broker_forwarding_price']
    + new.validated_data['certification_price'] + new.validated_data['company_services_price'] + registration_price)
    return end_price

def calc_swift(new, commission_price):
    swift_price = math.ceil(0.01 * (new.validated_data['auction_price'] + commission_price) + 90)
    return swift_price

def calc_registration(new, commission_price):
    registration_price = math.ceil(0.04 * (new.validated_data['auction_price'] + commission_price + 500) + 30)
    return registration_price