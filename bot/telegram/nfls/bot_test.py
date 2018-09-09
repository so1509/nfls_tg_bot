from telegram.ext import Updater
import logging
import nfls
import json
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler


updater = Updater(token='673002179:AAGgdFL11tzJvH9uQ06JY3vKuBss11ksj-I')

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Welcome to NFL SCORES!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)

caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)

def inline_caps(bot, update):

    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)

def fantasy_team(bot, update, args):
    team_name = args
    with open('registered_fantasy_teams.json') as f:
        team_string = 'POS' + '\t' + 'NAME' + '\t' + 'TEAM'  + '\t' + '?' 
        for team in json.load(f)['teams']:
            if team_name == team['name']:
                for player in team['lineup']:
                    team_string += player['position'] + '\t' + player['name'] + '\t'+ player['team'] + '\t' + player['rosterStatus'] + '\n'
            bot.send_message(chat_id=update.nessage.chat_id, text=team_string)
            #else:
            #bot.send_message(chat_id=update.nessage.chat_id, text='Sorry, team not found for name ' + args)

#fantasy_teams_handler = CommandHandler('fantasyTeams', fantasy_team, pass_args=True)
#dispatcher.add_handler(fantasy_teams_handler)
#def teams(bot, update):
#    teams_string=""
#    for team in nfls.getTeams()["NFLTeams"]:
#        teams_string += team["fullName"] + ", " + team["code"] + ", "+ team["shortName"] + "\n"
#    bot.send_message(chat_id=update.message.chat_id, text=teams_string)


def teams(bot, update):
    teams_string = ""
    for team in nfls.getTeams()["NFLTeams"]:
        img_src = 'opt/bot/telegram/nfls/nfl_png/' + team['code'] + '.png'
        #teams_string += '<a  href="file:///' + img_src + '">&#8205;</a>' + team["fullName"] + ", " + team["code"] + ", "+ team["shortName"] + "\n"
        teams_string += team["fullName"] + ", " + '<b>' + team["code"] + "</b>, "+ team["shortName"] + "\n"
    bot.send_message(chat_id=update.message.chat_id, parse_mode='HTML', text=teams_string)


teams_handler = CommandHandler('teams', teams)
dispatcher.add_handler(teams_handler)

def convertTZ(date, timeET):
    conv_date = ""
    conv_time = ""
    time_array=timeET.split()
    hour = time_array[0].split(':')[0]
    minute = time_array[0].split(':')[1]
    if time_array[1] == 'PM':
        conv_time += str(int(hour) + 12)
    else:
        conv_time += hour

    conv_time = str(int(conv_time) + 6)
    if int(conv_time) >= 24:
        conv_time = str(int(conv_time) - 24)

    conv_time += ':' + minute
    return date + ' ' + conv_time
        
def schedule(bot,update):
    schedule=nfls.getSchedule()
    current_week=schedule["currentWeek"]
    schedule_string='CURRENT_WEEK: [ ' + current_week + ' ]\n'
    for game in schedule["Schedule"]:
        if game["gameWeek"] == current_week:
            schedule_string += convertTZ(game["gameDate"], game["gameTimeET"]) + ': <b>' +  game["awayTeam"] + ' @ ' + game["homeTeam"] + '</b>\n'  
    
    bot.send_message(chat_id=update.message.chat_id, parse_mode='html', text=schedule_string)

schedule_handler = CommandHandler('schedule', schedule)
dispatcher.add_handler(schedule_handler)

def league_settings(bot,update):
    settings_string=''
    settings_json = nfls.getScoringSettings()
    for settings in settings_json:
        settings_string += '<b> ### ' + settings[0]  + ' ### </b>'
        for category in settings:
            settings_string += '<b>' + category[0] + '</b>'
            for rule in category:
                settings_string +=  category[0] + '<i>' + category[1] + '</i>'

    bot.send_message(chat_id=update.message.chat_id, parse_mode='html', text=settings_string)

league_settings_handler = CommandHandler('league_settings', league_settings)
dispatcher.add_handler(league_settings_handler)


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")




unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)
