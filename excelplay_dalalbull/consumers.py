from channels import Group
from channels.sessions import channel_session
from channels.auth import http_session_user, channel_session_user
from django.core.serializers.json import DjangoJSONEncoder

import json
from .views import niftyData,sell_data,graph,portfolio,ticker_data
from .models import Stock_data

import redis
from channels import Channel
redis_conn = redis.Redis("localhost", 6378)

from common.decorators import isLoggedInCh


#================ Nifty channel =======================#

@http_session_user
@isLoggedInCh
def connect_to_nifty_channel(message):
	Group('nifty-channel').add(message.reply_channel)
	message.reply_channel.send({
		'text' : json.dumps({"accept": True}) #{ "close" : True }
		})
	print("New nifty listener added!")

def disconnect_from_nifty_channel(message):
	Group('nifty-channel').discard(message.reply_channel)

def niftyChannelDataPush():

	nifty_data = niftyData()
	Group('nifty-channel').send( 
		{
			'text': json.dumps(nifty_data,cls=DjangoJSONEncoder)
		})

@http_session_user
@isLoggedInCh
def connect_to_graph_channel(message):
	Group('NIFTY-50').add(message.reply_channel)
	message.reply_channel.send({
		'text' : json.dumps({"accept": True}) #{ "close" : True }
		})
	print('New graph listener!')


def disconnect_from_graph_channel(message):
	Group('NIFTY-50').discard(message.reply_channel)


def graphDataPush():
	graphData = graph('NIFTY 50')
	Group('NIFTY-50').send({
		'text': json.dumps(graphData,cls=DjangoJSONEncoder),
		})

#==================== portfolio channel ========================#


@http_session_user
@isLoggedInCh
def connect_to_portfolio_channel(message):
	userid = message.http_session['user']	
	print('Portfolio listner added!',userid)
	redis_conn.hset("online-users",
		userid,
		message.reply_channel.name)
	message.reply_channel.send({
		'text' : json.dumps({"accept": True}) #{ "close" : True }
		})


@http_session_user
def disconnect_from_portfolio_channel(message):
	try:
		userid = message.http_session['user']	
		redis_conn.hdel("online-users",userid)
	except:
		pass

def portfolioDataPush():
	for userid in redis_conn.hkeys("online-users"):
		userid = userid.decode("utf-8")
		try:
			portfolioData = portfolio(userid)
			Channel( redis_conn.hget("online-users",userid)).send(
				{
				'text': json.dumps(portfolioData,cls=DjangoJSONEncoder)
				})
		except:
			print("Error in portfolioPush")




#======================= SELL CHANNEL ==========================#


@http_session_user
@isLoggedInCh
def connect_to_sell_channel(message):
	userid = message.http_session['user']
	redis_conn.hset("online-sellers",userid,message.reply_channel.name)
	print('New seller listener added!')
	message.reply_channel.send({
		'text' : json.dumps({"accept": True}) #{ "close" : True }
		})


@http_session_user
def disconnect_from_sell_channel(message):
	try:
		userid = message.http_session['user']
		redis_conn.hdel("online-sellers",userid)
	except:
		pass

def sellDataPush():
	for userid in redis_conn.hkeys("online-sellers"):
		userid = userid.decode("utf-8")
		try:
			sellData = sell_data(userid)
			Channel( redis_conn.hget("online-sellers",userid) ).send(
				{
				'text' : json.dumps(sellData,cls=DjangoJSONEncoder)
				})
		except:
			print("sellDataPush failed!")


#================ Ticker Channel =======================#

def connect_to_ticker_channel(message):
	Group('Ticker').add(message.reply_channel)
	message.reply_channel.send({
		'text' : json.dumps({"accept": True}) #{ "close" : True }
		})
	print('New ticker listener!')

def disconnect_from_ticker_channel(message):
	Group('Ticker').discard(message.reply_channel)


def tickerDataPush():
	tickerData = ticker_data()
	Group('Ticker').send({
		'text': json.dumps(tickerData,cls=DjangoJSONEncoder),
		})

def disconnectFromDalalbullCh(user_id):
	redis_conn.hdel("online-users",userid)
	redis_conn.hdel("online-sellers",userid)