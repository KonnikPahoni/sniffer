import telegram
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
import django.core.exceptions
from data_getter.models import User, AdminSettings
from settings import *
from utils import check_health
from telegram.constants import MESSAGEENTITY_EMAIL

AWAITING_EMAIL = 0
TIMEOUT_TIME = 3600


class TelegramBot:

    @staticmethod
    def get_superadmins(id_only=True):
        superadmins = User.objects.filter(roles_csv__contains='ROLE_SUPERADMIN')
        if id_only:
            return map(lambda admin: admin.telegram_id, superadmins)
        return superadmins

    @staticmethod
    def get_admins(id_only=True):
        admins = User.objects.filter(roles_csv__contains='ROLE_ADMIN')
        if id_only:
            return map(lambda admin: admin.telegram_id, admins)
        return admins

    @staticmethod
    def get_users(id_only=True):
        users = User.objects.filter(roles_csv__contains='ROLE_USER')
        if id_only:
            return map(lambda user: user.telegram_id, users)
        return users

    @staticmethod
    def update_admin_settings(admin_id, field_name, field_value):
        admin_settings = AdminSettings.objects.select_related('user').get(
            user__telegram_id__exact=admin_id)
        setattr(admin_settings, field_name, field_value)
        admin_settings.save()

    class Decorators(object):
        """Helper class to declare decorators inside the main class"""

        @staticmethod
        def access_denied(msg, self, update, context):
            return self.send(update.effective_chat.id, '🛑 Access denied: ' + msg)

        @classmethod
        def admins_only(cls, command):
            """Accessed by admins only"""

            def decorated(self, update, context):
                if update.message.chat.id in TelegramBot.get_admins():
                    return command(self, update, context)
                return cls.access_denied('admin role required', self, update, context)

            return decorated

        @classmethod
        def superadmins_only(cls, command):
            """Accessed by superadmins only"""

            def decorated(self, update, context):
                if update.message.chat.id in TelegramBot.get_admins():
                    return command(self, update, context)
                return cls.access_denied('are you superadmin?', self, update, context)

            return decorated

        @classmethod
        def users_only(cls, command):
            """Accessed by registered users only"""

            def decorated(self, update, context):
                if update.message.chat.id not in TelegramBot.get_users():
                    return command(self, update, context)
                return cls.access_denied('please, register using /start command first', self, update, context)

            return decorated

    def send_all_admins(self, msg):
        for admin_id in self.get_admins():
            self.updater.bot.send_message(chat_id=admin_id, text=msg,
                                          parse_mode='HTML')

    def send_all_users(self, msg):
        for admin_id in self.get_users():
            self.updater.bot.send_message(chat_id=admin_id, text=msg,
                                          parse_mode='HTML')

    def send(self, user_id, msg):
        self.updater.bot.send_message(chat_id=user_id,
                                      parse_mode='HTML',
                                      text=msg)

    def start_command(self, update, context):
        if update.effective_chat.id in self.get_users():
            self.send(update.effective_chat.id, 'You have already registered! ')
            return ConversationHandler.END

        msg = '😃 Hiya, fellow data lover. Please, send me your email to complete registration.'
        self.send(update.effective_chat.id, msg)
        return AWAITING_EMAIL

    def bad_email_message(self, update, context):
        self.send(update.effective_chat.id, 'Please, provide a valid email address. Waiting for it :)')

        return AWAITING_EMAIL

    def email_message(self, update, context):
        email = update.message.text
        name = ''
        if hasattr(update.message.from_user, 'first_name'):
            name += update.message.from_user.first_name
        if hasattr(update.message.from_user, 'last_name'):
            name += ' ' + update.message.from_user.last_name
        if hasattr(update.message.from_user, 'username'):
            name += ' (@' + update.message.from_user.username + ')'

        user = User(telegram_id=update.effective_chat.id,
                    name=name,
                    roles_csv="ROLE_USER",
                    email=email)
        try:
            user.full_clean()
        except django.core.exceptions.ValidationError as e:
            self.send(update.effective_chat.id, str(e))
            return AWAITING_EMAIL

        user.save()
        self.send(update.effective_chat.id, "Thanks! We have created your account.")
        logging.warning('New registration! Chat id: ' + str(update.effective_chat.id))

        return ConversationHandler.END

    @Decorators.superadmins_only
    def make_admin_command(self, update, context):
        user = User.objects.get(telegram_id=int(context.args[0]))
        user.roles_csv += ',ROLE_ADMIN'
        user.save()
        admin_settings = AdminSettings(user=user)
        admin_settings.save()
        logging.warning('User with telegram_id=' + context.args[0] + ' was given admin access.')

    @Decorators.admins_only
    def start_info_command(self, update, context):
        self.update_admin_settings(update.effective_chat.id, 'logging_level', logging.INFO)
        logging.info('Listening to logging at level INFO')

    @Decorators.admins_only
    def stop_info_command(self, update, context):
        logging.info('Stopped listening to logging')
        self.update_admin_settings(update.effective_chat.id, 'logging_level', logging.WARNING)

    @Decorators.admins_only
    def health_command(self, update, context):
        self.send(update.effective_chat.id, check_health(as_string=True))

    @Decorators.admins_only
    def logs(self, update, context):
        log_file = open(PATH_TO_LOGS, "rb")
        context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=log_file,
            caption="🦉 Hope you'll find something interesting!")
        log_file.close()

    def start(self):
        logging.info('Telegram bot starting')
        while True:
            try:
                self.updater.start_polling()
            except telegram.error.NetworkError:
                logging.warning('No connection')

    def stop(self):
        self.updater.stop()
        logging.info('Telegram bot stopped')

    def __init__(self):
        self.updater = Updater(token=TELEGRAM_TOKEN)
        self.admin_settings = AdminSettings.objects.select_related('user').all()
        start_handler = CommandHandler('start', self.start_command)
        registration_handler = ConversationHandler(
            entry_points=[start_handler],
            states={
                AWAITING_EMAIL: [MessageHandler(Filters.entity(MESSAGEENTITY_EMAIL), self.email_message),
                                 MessageHandler(Filters.all, self.bad_email_message)],
                ConversationHandler.TIMEOUT: [start_handler]},
            fallbacks=[start_handler],
            conversation_timeout=TIMEOUT_TIME)

        start_info_handler = CommandHandler('start_info', self.start_info_command)
        stop_info_handler = CommandHandler('stop_info', self.stop_info_command)
        health_handler = CommandHandler('health', self.health_command)
        logs_handler = CommandHandler('logs', self.logs)
        make_admin_command_handler = CommandHandler('make_admin', self.make_admin_command)

        self.updater.dispatcher.add_handler(registration_handler)
        self.updater.dispatcher.add_handler(start_info_handler)
        self.updater.dispatcher.add_handler(stop_info_handler)
        self.updater.dispatcher.add_handler(health_handler)
        self.updater.dispatcher.add_handler(logs_handler)
        self.updater.dispatcher.add_handler(make_admin_command_handler)
