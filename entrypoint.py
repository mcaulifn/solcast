#import time
#import schedule
from solcast.rooftop import RooftopSite

if __name__ == '__main__':
    api_key = 'Pop60dEugiTVyV5yQLh36h_uoFin5eS7'
    resource_id = '4333-7f2f-6be9-5257'
    site = RooftopSite(api_key, resource_id)
    print(site.get_forecasts())
    # schedule.every(60).minutes.do(handler)
    # while True:
    #    schedule.run_pending()
    #    time.sleep(1)
