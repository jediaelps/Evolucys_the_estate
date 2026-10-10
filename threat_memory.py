"""Conhecimento narrativo por contexto, sempre confrontado com sinais atuais."""
from copy import deepcopy


class ThreatMemory:
    def __init__(self):
        self.contexts = {}
        self.visit = 0

    def observe(self, context, signals, level, discovery, reminder, changed='', explicit=False, changed_present=''):
        signature = sorted([list(signal) for signal in signals])
        record = self.contexts.setdefault(context, {
            'state': 'unknown', 'signals': [], 'visit': -1, 'reminders': 0})
        previous = record['signals']
        if not signature:
            record['signals'] = []
            if previous:
                record.update(state='altered', visit=self.visit, reminders=0)
                return changed
            return ''
        if signature != previous:
            was_known = bool(previous) or record['state'] != 'unknown'
            record.update(signals=signature, state='altered' if was_known else level,
                          visit=self.visit, reminders=0)
            return (changed_present or reminder) if was_known else discovery
        if explicit:
            record.update(state='confirmed', visit=self.visit)
            return reminder
        if record['visit'] != self.visit:
            record.update(state='known', visit=self.visit)
            if record['reminders'] == 0:
                record['reminders'] += 1
                return reminder
        return ''

    def export_state(self):
        return {'visit': self.visit, 'contexts': deepcopy(self.contexts)}

    def restore_state(self, state):
        self.visit = state.get('visit', 0)
        self.contexts = deepcopy(state.get('contexts', {}))
