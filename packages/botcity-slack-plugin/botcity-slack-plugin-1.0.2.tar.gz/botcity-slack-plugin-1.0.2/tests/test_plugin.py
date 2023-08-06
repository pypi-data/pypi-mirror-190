import conftest
from botcity.plugins.slack import (Author, BotSlackPlugin, Color, Field,
                                   Footer, Message)


def test_send_simple_message(bot: BotSlackPlugin):
    response_message = bot.send_simple_message(text="A simple message", users=["Livia Maçon"])
    bot.delete_message(response_message)
    assert "A simple message" == (response_message.get('message').get('blocks')[0].
                                  get('elements')[0].get('elements')[1].get('text').strip)()


def test_send_message(bot: BotSlackPlugin):
    message = Message(text="A more elaborate message",
                      title="title test",
                      color=Color.RED
                      )

    # Sets author
    message.author = Author(author_name="Author test",
                            author_icon="https://placeimg.com/16/16/people",
                            author_link="http://flickr.com/bobby/")
    # Sets thumb_url
    message.thumb_url = "http://placekitten.com/g/200/200"

    # Sets Footer
    message.footer = Footer(footer="Footer test",
                            footer_icon="https://platform.slack-edge.com/img/default_application_icon.png")
    # Sets fields
    message.fields = [Field(title="Field test", value="values test", short=False),
                      Field(title="Field test 2", value="values test 2", short=True),
                      Field(title="Field test 3", value="values test 3", short=True)]

    # Send message
    response_message = bot.send_message(message=message)
    bot.delete_message(response_message)
    assert response_message.get('ok') is True


def test_send_message_without_fields_and_color(bot: BotSlackPlugin):
    message = Message(text="A more elaborate message",
                      title="title test",
                      )

    # Sets author
    message.author = Author(author_name="Author test",
                            author_icon="https://placeimg.com/16/16/people",
                            author_link="http://flickr.com/bobby/")
    # Sets thumb_url
    message.thumb_url = "http://placekitten.com/g/200/200"

    # Sets Footer
    message.footer = Footer(footer="Footer test",
                            footer_icon="https://platform.slack-edge.com/img/default_application_icon.png")

    # Send message
    response_message = bot.send_message(message=message)
    bot.delete_message(response_message)
    assert response_message.get('ok') is True


def test_update_message(bot: BotSlackPlugin):
    message_one = bot.send_simple_message(text="A simples message")
    new_message = "Edit a simple message"
    update = bot.update_message(response=message_one, text=new_message)
    bot.delete_message(update)
    assert new_message == (update.get("message").get("text")).strip()


def test_upload_file(bot: BotSlackPlugin, tmp_folder: str):
    file = conftest.create_file(path=f"{tmp_folder}/tmp_file.txt", content="file temporary")
    upload_file = bot.upload_file(file=file, text_for_file="Text accompanying the file",
                                  title_for_file="the title of file")
    bot.delete_file(upload_file)
    assert upload_file.get('ok') is True


def test_reply(bot: BotSlackPlugin):
    response_message = bot.send_simple_message(text="This is a test to reply the message in the thread")
    reply = bot.reply(response=bot.get_replies(response_message),
                      msg="This is a reply to message")

    bot.delete_message(response_message)
    bot.delete_message(reply)
    assert (reply.get('message').get('text')).strip() == "This is a reply to message"


def test_get_text_replies(bot: BotSlackPlugin):
    response_message = bot.send_simple_message(text="This is a test to reply the message in the thread")
    reply = bot.reply(response=bot.get_replies(response_message),
                      msg="This is a reply to message")

    messages = bot.get_replies(response_message)
    list_message_text = bot.get_text_replies(messages)
    text = str(list_message_text[0]).strip()
    bot.delete_message(response_message)
    bot.delete_message(reply)
    assert text == "This is a reply to message"
