#All keys stored as env variables on replit.
#Some variables stored as database variables on replit hence the syntax db['var_name']

import discord
import os
from discord_webhook import DiscordWebhook
import time
from replit import db
import requests
from keepalive import keep_alive
from operator import itemgetter
from web3 import Web3
from threading import Timer

#ENV VAR
bot_token = os.environ['BOT_TOKEN']
etherscan_key = os.environ['etherscan_key']
infura_project_id = os.environ['INFURA_PROJECT_ID']

infura_url = f'https://mainnet.infura.io/v3/{infura_project_id}'

web3 = Web3(Web3.HTTPProvider(infura_url))
is_connected = web3.isConnected()

latest_block_number = int(web3.eth.get_block('latest')['number'])
start_block = latest_block_number - 55

#A database of wallets I wish to track
db['wallets'] = {
    'Andre': '0x431e81e5dfb5a24541b5ff8762bdef3f32f96354',
    'Tetra': '0x9c5083dd4838e120dbeac44c052179692aa5dac5',
    'Messi': '0xca86d57519dbfe34a25eef0923b259ab07986b71',
    'Sifu': '0x5dd596c901987a2b28c38a9c1dfbf86fffc15d77',
    'Skull Wallet1': '0x23b922a832b63831fbf04c7a1941943b88b3d0d6',
    'Skull Wallet2': '0x60965f808e23722abd465e5c9e3f2b21ff6ed803', 
    'Skull Wallet3': '0x1FafD34DDc10BE3B4c3eE4007712C701F87A95aa',
    'Skull Wallet4':  '0x6530ebc94E114898171Df384c17566E1A2cBC9e3',
    'Skull Wallet5':  '0xbA7EEBcfbC6FA219F54Ae8c435dcF848FadDE13d',
    'Random Task': '0x313acece2b6ae4e65259b7c76f34e60512cfb95b',
    'Gainzy': '0x20B95125f3C5e487C9cad47107431C2089355b17',
    'Gainzy2': '0x333345727be2ec482baf99a25cb1765cb7b78de6'
}
name_list = list(db['wallets'].keys())
db['hashes'] = []


async def get_transactions():
    webhook = os.environ['WEBHOOK']
    latest_block_number = int(web3.eth.get_block('latest')['number'])
    start_block = latest_block_number - 100
    for i in range(len(db['wallets'])):
        wallet = db['wallets'][name_list[i]]
        print(wallet)

        #API URL's Below
        normal_txns_url = f'https://api.etherscan.io/api?module=account&action=txlist&address={wallet}&startblock={start_block}&endblock={latest_block_number}&sort=asc&apikey={etherscan_key}'
        
        avax_normal_url = f'https://api.snowtrace.io/api?module=account&action=txlist&address={wallet}&startblock=9558000&endblock=99999999999&sort=asc&apikey={snowtrace_key}'

        ftm_normal_url = f'https://api.ftmscan.com/api?module=account&action=txlist&address={wallet}&startblock=27000000&endblock=99999999&sort=asc&apikey={ftm_key}'
        #Fetch Etherscan Data
        response = requests.get(url=normal_txns_url)
        data = response.json()
        sorted_result = sorted(data['result'], key=itemgetter('timeStamp'))

        #Fetch AVAX Data
        response_avax = requests.get(url=avax_normal_url)
        data_avax = response_avax.json()

        try:
            print(wallet)
            txn_hash = (sorted_result[-1]['hash'])
            print(txn_hash)
            if txn_hash not in db['hashes']:
                webhook = DiscordWebhook(
                    url=
                    f'https://discord.com/api/webhooks/{webhook}',
                    rate_limit_retry=True,
                    content=
                    f"Hey @everyone! A new txn on {list(db['wallets'].keys())[i]}'s wallet! https://etherscan.io/tx/{txn_hash}"
                )
                response = webhook.execute()
                db['hashes'].append(txn_hash)
            else:
                print("else")
        except:
            print("passed over except")
        
        
        try:
          print(wallet)
          txn_hash_avax = data_avax['result'][-1]['hash']
          if txn_hash_avax not in db['hashes']:
              webhook = DiscordWebhook(
                    url=
                    f'https://discord.com/api/webhooks/{webhook}',
                    rate_limit_retry=True,
                    content=
                    f"Hey @everyone! A new txn on {list(db['wallets'].keys())[i]}'s wallet! https://snowtrace.io/tx/{txn_hash_avax}"
                )
              response = webhook.execute()
              db['hashes'].append(txn_hash_avax)
          else:
            pass
        except:
          print("avax except")

        #Fetch FTM data
        response_ftm = requests.get(url=ftm_normal_url)
        data_ftm = response_ftm.json()
        try:
          print(wallet)
          txn_hash_ftm = data_ftm['result'][-1]['hash']
          print(txn_hash_ftm)
          if txn_hash_ftm not in db['hashes']:
              webhook = DiscordWebhook(
                    url=
                    f'https://discord.com/api/webhooks/{webhook}',
                    rate_limit_retry=True,
                    content=
                    f"Hey @everyone! A new txn on {list(db['wallets'].keys())[i]}'s wallet! https://ftmscan.com/tx/{txn_hash_ftm}"
                )
              response = webhook.execute()
              db['hashes'].append(txn_hash_ftm)
          else:
            print("ftm else")
        except:
          print("ftm except") 
        time.sleep(5)     
        
    Timer(5.0, await get_transactions()).start()
            

client = discord.Client()
@client.event
async def on_ready():
    print(f"You have logged in as {client}")
    await get_transactions()
    time.sleep(120)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/wallets'):
        await message.channel.send(
            f"Current Wallets being tracked: {db['wallets']}")


keep_alive()
client.run(bot_token)
