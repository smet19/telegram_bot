import telebot
import boto3
import requests
import os


BOT_TOKEN = os.getenv('BOT_TOKEN')
BUCKET_NAME = os.getenv('BUCKET_NAME')

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(content_types=["text", "audio", "document", "sticker",
                                    "video", "video_note", "voice", "location",
                                    "contact", "new_chat_members", "left_chat_member",
                                    "new_chat_title", "new_chat_photo", "delete_chat_photo",
                                    "group_chat_created", "supergroup_chat_created",
                                    "channel_chat_created", "migrate_to_chat_id",
                                    "migrate_from_chat_id", "pinned_message"])
def handle_other(message):
    bot.reply_to(message,   "                                 ...,**//////**,,...                               \n" +
                            "                       .,**///(((/**,,,,,,.           .,**,,.                      \n" +
                            "                  .,/(/,.                                   .*/*.                  \n" +
                            "               .*//,.                         .,..,/%&&&%%%%#///((/,.              \n" +
                            "           .,*/*,. ..,,*//,.                  .,***,..  ...,/(#/*/(#(*.            \n" +
                            "       .,*/*,,*/#%&&%(/,..                  .,,..             .,***/(#/.           \n" +
                            "     .*//,..*(%##(//*,.....,,,,,.          .,*,.     ,(%@@&(,    .,,,,/#(*.        \n" +
                            "   ..,***.   .,,,    ./%&%#/,..,*//*.        .,*,.    ..,,,.      .**.,/((/*.      \n" +
                            "  ,*//*,.    ,**,.  .,(&@@%(,...***.            ..***,,,.......,,**,.   ,*/(/,.    \n" +
                            " .,/((*.      .**.         .,*/*.                                        .*((/,    \n" +
                            " .,/(/,.       .,***,,,,,,*,.            ,,..,**,.                        ,*((,    \n" +
                            "  .,//.                                 .**,  ..**.                       .,**.    \n" +
                            "   .,*,.                                  .,*****,.             .,,.      ..,.     \n" +
                            "      ....                                                  .,,,,.                 \n" +
                            "                         .,,,..                     ..,,,,,..                      \n" +
                            "                               ..,,*****/**************,..                         \n" +
                            "                                         .......                                   \n" ) #Чел ты...


@bot.message_handler(content_types='photo')
def handle_photo(message):

    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    print(type(downloaded_file))

    with open("tmp.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    img_id = message.message_id
    print(img_id)

    s3 = boto3.resource('s3')
    s3.Bucket(BUCKET_NAME).upload_file('tmp.jpg', f'uploads/{img_id}.jpg', ExtraArgs={'ACL':'public-read'})

    img_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/uploads/{img_id}.jpg"

    data = {"img_url": img_url, "img_id": img_id}
    url = 'http://pikachu:5000/v1/predict'
    response = requests.post(url, json=data)
    response_json = response.json()
    print(response_json)

    prediction = response_json["prediction"]

    bot.reply_to(message, prediction)


bot.polling()