# coding: utf-8
from transitions import Machine


class ModeMachine(object):
	"""
	Tiny sample of python library pytransition.

	usage: https://github.com/pytransitions/transitions
	"""

	mode_states=['mode_off', 'mode_on']

	def __init__(self, name):
		"""
		Constructor.

		.
		"""
		self.name = name

		self.mode_machine = Machine(model=self,\
			states=ModeMachine.mode_states,\
			initial='mode_off')
		self.mode_machine.add_transition(trigger='start',\
			source='mode_off', dest='mode_on')
		self.mode_machine.add_transition(trigger='end',\
			source='mode_on', dest='mode_off')

"""
usage
>> machine = Machine("new machine")
>> machine.state
'mode-off'

>> machine.start()
>> machine.state
'mode-on'

>> machine.end()
>> machine.state
'mode-off'
"""
