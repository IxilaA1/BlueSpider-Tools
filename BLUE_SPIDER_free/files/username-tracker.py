import requests
from bs4 import BeautifulSoup
import re
import time
import os

   
logo_ascii = """
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                   >|a@@@@@@@@@|                                                
                                              }@@@@@@@@@@@@@@@@| 000M|                                          
                                          ;@@@@@@O  @@@@@@@@@@@|  j000000_                                      
                                       }@@@@@v   |@@@@@@@@@@@@@| 00J  |00000j                                   
                                     @@@@@_     @@@@@@@@@@@@@@@| 0000    ;00000^                                
                                  ;@@@@v       _@@@@@@@     >@@| 0000v      }0000_                              
                                ^@@@@_         @@@@@@@      ^O@| 00000        ;0000_                            
                                 @@@@;         @@@@@@@      ;p@| 00000         0000^                            
                                   @@@@p       >@@@@@@@^    >@@| 0000v      J0000;                              
                                     O@@@@|     M@@@@@@@@@@@@@@| 0000    >00000                                 
                                       ;@@@@@J^  }@@@@@@@@@@@@@| 00v  j00000}                                   
                                          >@@@@@@@_;@@@@@@@@@@@| ;M000000_                                      
                                              >@@@@@@@@@@@@@@@@| 00000}                                          
                                                   ^jpM@@@@@@@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|    
"""


os.system('cls' if os.name == 'nt' else 'clear')


print(logo_ascii)


time.sleep(2)



def Title(title_str):
    print(f"\n--- {title_str} ---\n")

def Error(e):
    print(f"[!] AN ERROR OCCURRED: {e}")


white = ""
red = ""
reset = ""
BEFORE = ""
AFTER = ""
INFO = "[*]"
WAIT = "[...]"
INPUT_SYM = "[>]"
GEN_VALID = "[+]"
GEN_INVALID = "[-]"
ADD = "[+]"

def current_time_hour():
    return time.strftime("%H:%M:%S")

def ChoiceUserAgent():
   
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"




Title("Username Tracker")

try:
    user_agent = ChoiceUserAgent()
    headers = {"User-Agent": user_agent}
    number_site = 0
    number_found = 0
    sites_and_urls_found = []

    print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO} Selected User-Agent: {white}{user_agent}{reset}")
    
    
    username = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT_SYM} Enter Username -> {reset}").lower()
    


    sites = {
        "Steam": {
            "url": f"https://steamcommunity.com/id/{username}", "method": "get", "verification": "username", "except": None
        },
        "Telegram": {
            "url": f"https://t.me/{username}", "method": "get", "verification": "username",
            "except": [f"if you have telegram, you can contact @{username} right away.", f"resolve?domain={username}", f"telegram: contact @{username}"]
        },
        "TikTok": {
            "url": f"https://www.tiktok.com/@{username}", "method": "get", "verification": "username",
            "except": [f"\\u002f@{username}\""]
        },
        "Instagram": {
            "url": f"https://www.instagram.com/{username}", "method": "get", "verification": "username", "except": None
        },
        "Paypal": {
            "url": f"https://www.paypal.com/paypalme/{username}", "method": "get", "verification": "username",
            "except": [f"slug_name={username}", f"\"slug\":\"{username}\"", f"2F{username}&"]
        },
        "GitHub": {
            "url": f"https://github.com/{username}", "method": "get", "verification": "status", "except": None
        },
        "Pinterest": {
            "url": f"https://www.pinterest.com/{username}", "method": "get", "verification": "username",
            "except": [f"[\\\"username\\\",\\\"{username}\\\"]"]
        },
        "Snapchat": {
            "url": f"https://www.snapchat.com/add/{username}", "method": "get", "verification": "status", "except": None
        },
        "Blogger": {
            "url": f"https://{username}.blogspot.com", "method": "get", "verification": "status", "except": None
        },
        "Tumblr": {
            "url": f"https://{username}.tumblr.com", "method": "get", "verification": "status", "except": None
        },
        "SoundCloud": {
            "url": f"https://soundcloud.com/{username}", "method": "get", "verification": "status", "except": None
        },
        "About.me": {
            "url": f"https://about.me/{username}", "method": "get", "verification": "status", "except": None
        },
        "Flickr": {
            "url": f"https://www.flickr.com/people/{username}", "method": "get", "verification": "status", "except": None
        },
        "Keybase": {
            "url": f"https://keybase.io/{username}", "method": "get", "verification": "status", "except": None
        },
        "Last.fm": {
            "url": f"https://www.last.fm/user/{username}", "method": "get", "verification": "status", "except": None
        },
        "Behance": {
            "url": f"https://www.behance.net/{username}", "method": "get", "verification": "status", "except": None
        },
        "Quora": {
            "url": f"https://www.quora.com/profile/{username}", "method": "get", "verification": "status", "except": None
        },
        "Patreon": {
            "url": f"https://www.patreon.com/{username}", "method": "get", "verification": "status", "except": None
        },
        "Myspace": {
            "url": f"https://myspace.com/{username}", "method": "get", "verification": "username", "except": None
        },
        "Kaggle": {
            "url": f"https://www.kaggle.com/{username}", "method": "get", "verification": "username", "except": None
        },
        "Periscope": {
            "url": f"https://www.pscp.tv/{username}", "method": "get", "verification": "username", "except": None
        },
        "Disqus": {
            "url": f"https://disqus.com/by/{username}", "method": "get", "verification": "username", "except": None
        },
        "Mastodon": {
            "url": f"https://mastodon.social/@{username}", "method": "get", "verification": "username", "except": None
        },
        "GitLab": {
            "url": f"https://gitlab.com/{username}", "method": "get", "verification": "username", "except": None
        },
        "LiveJournal": {
            "url": f"https://{username}.livejournal.com", "method": "get", "verification": "username", "except": None
        },
        "CodeWars": {
            "url": f"https://www.codewars.com/users/{username}", "method": "get", "verification": "username", "except": None
        },
        "Spotify": {
            "url": f"https://open.spotify.com/user/{username}", "method": "get", "verification": "status", "except": None # Corrected Spotify URL and check
        },
        "Weebly": {
            "url": f"https://{username}.weebly.com", "method": "get", "verification": "username", "except": None
        },
        "YouTube": {
            "url": f"https://www.youtube.com/@{username}", "method": "get", "verification": "status", "except": ["This channel does not exist."]
        },
        "ProductHunt": {
            "url": f"https://www.producthunt.com/@{username}", "method": "get", "verification": "username", "except": None
        },
        "Mix": {
            "url": f"https://mix.com/{username}", "method": "get", "verification": "username", "except": None
        },
        "Facebook": {
            "url": f"https://www.facebook.com/{username}", "method": "get", "verification": "status", "except": None
        },
        "Strava": {
            "url": f"https://www.strava.com/athletes/{username}", "method": "get", "verification": "username", "except": None
        },
        "Linktree": {
            "url": f"https://linktr.ee/{username}", "method": "get", "verification": "status", "except": ["404 page not found"]
        },
        "Xbox": {
            "url": f"https://www.xboxgamertag.com/search/{username}", "method": "get", "verification": "status", "except": ["No results found"]
        },
        "Twitch": {
            "url": f"https://www.twitch.tv/{username}", "method": "get", "verification": "username", "except": None
        },
        "Goodreads": {
            "url": f"https://www.goodreads.com/{username}", "method": "get", "verification": "status", "except": None
        },
        "500px": {
            "url": f"https://500px.com/{username}", "method": "get", "verification": "username", "except": None
        },
        "LinkedIn": {
            "url": f"https://www.linkedin.com/in/{username}", "method": "get", "verification": "status", "except": None
        },
        "Weibo": {
            "url": f"https://weibo.com/{username}", "method": "get", "verification": "username", "except": None
        },
        "OKCupid": {
            "url": f"https://www.okcupid.com/profile/{username}", "method": "get", "verification": "status", "except": None
        },
        "Meetup": {
            "url": f"https://www.meetup.com/members/{username}", "method": "get", "verification": "username", "except": None
        },
        "CodePen": {
            "url": f"https://codepen.io/{username}", "method": "get", "verification": "status", "except": None
        },
        "StackOverflow": {
            "url": f"https://stackoverflow.com/users/{username}", "method": "get", "verification": "status", "except": None
        },
        "HackerRank": {
            "url": f"https://www.hackerrank.com/{username}", "method": "get", "verification": "username", "except": None
        },
        "Xing": {
            "url": f"https://www.xing.com/profile/{username}", "method": "get", "verification": "status", "except": None
        },
        "Deezer": {
            "url": f"https://www.deezer.com/en/user/{username}", "method": "get", "verification": "status", "except": None
        },
        "Ravelry": {
            "url": f"https://www.ravelry.com/people/{username}", "method": "get", "verification": "username", "except": None
        },
        "Vine": {
            "url": f"https://vine.co/u/{username}", "method": "get", "verification": "status", "except": None
        },
        "Foursquare": {
            "url": f"https://foursquare.com/user/{username}", "method": "get", "verification": "status", "except": None
        },
        "Ello": {
            "url": f"https://ello.co/{username}", "method": "get", "verification": "username", "except": None
        },
        "Hootsuite": {
            "url": f"https://hootsuite.com/{username}", "method": "get", "verification": "status", "except": None
        },
        "Prezi": {
            "url": f"https://prezi.com/{username}", "method": "get", "verification": "status", "except": None
        },
        "Groupon": {
            "url": f"https://www.groupon.com/profile/{username}", "method": "get", "verification": "status", "except": None
        },
        "Joomla": {
            "url": f"https://www.joomla.org/user/{username}", "method": "get", "verification": "status", "except": None
        },
        "StackExchange": {
            "url": f"https://stackexchange.com/users/{username}", "method": "get", "verification": "status", "except": None
        },
        "Taringa": {
            "url": f"https://www.taringa.net/{username}", "method": "get", "verification": "username", "except": None
        },
        "Shopify": {
            "url": f"https://{username}.myshopify.com", "method": "get", "verification": "status", "except": None
        },
        "8tracks": {
            "url": f"https://8tracks.com/{username}", "method": "get", "verification": "status", "except": None
        },
        "Couchsurfing": {
            "url": f"https://www.couchsurfing.com/people/{username}", "method": "get", "verification": "status", "except": None
        },
        "OpenSea": {
            "url": f"https://opensea.io/{username}", "method": "get", "verification": "status", "except": None
        },
        "Trello": {
            "url": f"https://trello.com/{username}", "method": "get", "verification": "username", "except": None
        },
        "Fiverr": {
            "url": f"https://www.fiverr.com/{username}", "method": "get", "verification": "status", "except": None
        },
        "Badoo": {
            "url": f"https://badoo.com/profile/{username}", "method": "get", "verification": "username", "except": None
        },
        "Rumble": {
            "url": f"https://rumble.com/user/{username}", "method": "get", "verification": "status", "except": None
        },
        "Wix": {
            "url": f"https://www.wix.com/website/{username}", "method": "get", "verification": "status", "except": None
        },
        "allmylinks": {
            "url": f"https://allmylinks.com/{username}", "method": "get", "verification": "status", "except": ["This page is missing"]
        },
        "Medium": {
            "url": f"https://medium.com/@{username}", "method": "get", "verification": "status", "except": ["Out of nothing, something."]
        },
        "Reddit": {
            "url": f"https://reddit.com/user/{username}", "method": "get", "verification": "status", "except": ["Sorry, nobody on Reddit goes by that name."]
        },
        "Twitter/X": {
            "url": f"https://x.com/{username}", "method": "get", "verification": "status", "except": None
        },
        "Fosstodon": {
            "url": f"https://fosstodon.org/@{username}", "method": "get", "verification": "status", "except": ["The user could not be found"]
        },
        "Bugcrowd": {
            "url": f"https://bugcrowd.com/{username}", "method": "get", "verification": "status", "except": ["The requested page was not found"]
        },
        "HackerOne": {
            "url": f"https://hackerone.com/{username}", "method": "get", "verification": "status", "except": ["User does not exist"] # Changed method to 'get' for simplicity
        },
        "HackTheBox": {
            "url": f"https://app.hackthebox.com/profile/{username}", "method": "get", "verification": "status", "except": ["User not found"]
        },
        "Apple Developer": {
            "url": f"https://developer.apple.com/forums/profile/{username}", "method": "get", "verification": "status", "except": ["The page you’re looking for can’t be found"]
        },
        "Apple Discussions": {
            "url": f"https://discussions.apple.com/profile/{username}", "method": "get", "verification": "status", "except": ["The page you tried was not found. You may have used an outdated link or may have typed the address (URL) incorrectly."]
        },
        "Hacker News": {
            "url": f"https://news.ycombinator.com/user?id={username}", "method": "get", "verification": "status", "except": ["No such user."]
        },
        "Bitbucket": {
            "url": f"https://bitbucket.org/{username}", "method": "get", "verification": "status", "except": ["Repository not found"]
        },
        "Slack": {
            "url": f"https://{username}.slack.com", "method": "get", "verification": "status", "except": ["This workspace doesn’t exist"]
        },
        "Slide Share": {
            "url": f"https://www.slideshare.net/{username}", "method": "get", "verification": "status", "except": ["This username"]
        },
        "Wattpad": {
            "url": f"https://www.wattpad.com/user/{username}", "method": "get", "verification": "status", "except": ["Oops! That page can’t be found."]
        },
        "Codecademy": {
            "url": f"https://www.codecademy.com/profiles/{username}", "method": "get", "verification": "status", "except": ["This profile could not be found"]
        },
        "Gravatar": {
            "url": f"https://gravatar.com/{username}", "method": "get", "verification": "status", "except": ["Uh oh. Page not found"]
        },
        "Dev To": {
            "url": f"https://dev.to/{username}", "method": "get", "verification": "status", "except": ["This page does not exist"]
        },
        "Kaskus": {
            "url": f"https://www.kaskus.co.id/profile/@{username}", "method": "get", "verification": "status", "except": ["We can't find the page you are looking for"]
        },
        "Crunchbase": {
            "url": f"https://www.crunchbase.com/person/{username}", "method": "get", "verification": "status", "except": ["Page Not Found"]
        }
    }

    print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT} Scanning **{len(sites)}** websites for username: **{username}**...")

    session = requests.Session()

    for site, data in sites.items():
        number_site += 1
        url = data["url"]
        method = data["method"]
        verification = data["verification"]
        page_except = data["except"]
        found = False
        response = None

        try:
            
            if method == "get":
                response = session.get(url, timeout=10, headers=headers, allow_redirects=True)
            elif method == "post":
                
                print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT} {site}: Using POST method (unverified in this version).")
                continue

            
            if response is not None and response.status_code == 200:
                
                page_text_lower = response.text.lower()
                
                
                if verification == "status":
                    found = True
                   
                    if page_except:
                        for exception_text in page_except:
                            if exception_text.lower() in page_text_lower:
                                found = False
                                break

                
                elif verification == "username":
                    found = False
                    
                    
                    temp_page_text = page_text_lower
                    if page_except:
                        for exception_text in page_except:
                            temp_page_text = temp_page_text.replace(exception_text.lower(), ' ')

                   
                    if username in temp_page_text:
                        found = True


            elif response is not None and (300 <= response.status_code < 400):

                 if verification == "status" and response.status_code not in (404, 410, 403):
                    
                     found = True 


            
            if found:
                number_found += 1
                sites_and_urls_found.append({site: url})
                print(f"**[{current_time_hour()}] [+] FOUND | {site}:** {url}")
            else:
                print(f"**[{current_time_hour()}] [-] NOT FOUND | {site}:** Not Found (Status: {response.status_code if response else 'N/A'})")

        except requests.exceptions.Timeout:
            print(f"**[{current_time_hour()}] [!] ERROR | {site}:** Request timed out.")
        except requests.exceptions.RequestException as e:
            
            print(f"**[{current_time_hour()}] [!] ERROR | {site}:** Request error: {e}")
        except Exception as e:
            
            print(f"**[{current_time_hour()}] [!] ERROR | {site}:** An unexpected error occurred: {e}")



    if number_found > 0:
        print(f"\n{red}*** RESULTS FOUND: {number_found} out of {number_site} sites ***{reset}")
        for site_and_url_found in sites_and_urls_found:
            for site, url in site_and_url_found.items():
                time.sleep(0.1)
                print(f"{white}----------------------------------------------------------------------------------------------------{reset}")
                print(f"{ADD} Site: {white}{site}{reset}")
                print(f"{ADD} Link: {white}{url}{reset}")
        print(f"{white}----------------------------------------------------------------------------------------------------{reset}")
    else:
        print(f"\n{red}*** No results found for username: {username} ***{reset}")


    print(f"\n{BEFORE}{current_time_hour()}{AFTER} {INFO} **Scan Complete.** Total Websites: {white}{number_site}{reset} | Total Found: {white}{number_found}{reset}")


except Exception as e:
    Error(e)