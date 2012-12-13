from errbot import BotPlugin, botcmd
import random

class Insulter(BotPlugin):
	""""An Err plugin that will allow users to insult each other"""
	min_err_version = '1.6.7'
	not_allowed_message = 'Plugin usage not allowed in this room'

	def activate(self):
		super(Insulter, self).activate()
		self.load_insults_list()

	def get_configuration_template(self):
		"""Defines the configuration structure this plugin supports"""
		return {'ALLOWED_ROOMS': ['room_1', 'room_2']}

	def get_room_from_message(self, mess):
		"""Get the room name from a message"""
		jid = "{}".format(mess.getFrom())
		return jid.rsplit('/')[0].rsplit('@')[0]
	
	def load_insults_list(self):
		"""Load the list of insults from the shelf"""
		if 'insults' not in self.shelf.keys():
			self.insults = [[], []]
		else:
			self.insults = self.shelf['insults']

	def is_plugin_usage_allowed(self, mess):
		"""Check whether the usage of the plugin is allowed within this room"""
		if self.config is not None and "ALLOWED_ROOMS" in self.config:
			if self.get_room_from_message(mess) not in self.config['ALLOWED_ROOMS']:
				return False
		return True

	def sync_shelf(self):
		"""Synchronise the shelf with our insults variable"""
		self.shelf['insults'] = self.insults
                self.shelf.sync()

	@botcmd(split_args_with=None)
	def insult_add_adjective(self, mess, args):
		"""Add an adjective to the list of adjectives that can be used in the random insults"""
		if len(args) > 0:
			for adjective in args:
				if adjective not in self.insults[0]:
					self.insults[0].append(adjective)
			self.sync_shelf()

	@botcmd(split_args_with=None)
	def insult_remove_adjective(self, mess, args):
		"""Remove an adjective from the list of adjectives"""
		if len(args) > 0:
			for adjective_to_remove in args:
				self.insults[0].remove(adjective_to_remove)
			self.sync_shelf()

	@botcmd(split_args_with=None)
	def insult_add_noun(self, mess, args):
		"""Add a noun to the list of nouns that can be used in the random insults"""
		if len(args) > 0:
			for noun in args:
				if noun not in self.insults[1]:
					self.insults[1].append(noun)
		self.sync_shelf()

	@botcmd(split_args_with=None)
	def insult_remove_noun(self, mess, args):
		"""Remove a noun from the list of nouns"""
		if len(args) > 0:
			for noun_to_remove in args:
				self.insults[1].remove(noun_to_remove)
			self.sync_shelf()

	@botcmd(split_args_with=None)
	def insult_send(self, mess, args):
		"""Send a random insult to the specified user or to all users"""
		if self.is_plugin_usage_allowed(mess):
			if args == []:
				args.append('all')
			if len(self.insults[0]) > 0 and len(self.insults[0]) > 0:
				return '@{0} {1} {2}'.format(args[0], random.choice(self.insults[0]), random.choice(self.insults[1]))
			return "NOOOO!! couldn't create a decent insult..."
		else:
			return self.not_allowed_message

	@botcmd()
	def insult_print_list(self, mess, args):
		"""Print a list of all adjectives & nouns"""
		if self.is_plugin_usage_allowed(mess):
			return "Adjectives: {0}\nNouns: {1}".format(self.insults[0], self.insults[1])
		else:
			return self.not_allowed_message
