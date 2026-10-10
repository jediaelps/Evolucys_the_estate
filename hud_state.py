"""Projeção do HUD, preparada para futuros eventos/animações de batimento."""
def focus_icons(charges):
    return ' '.join(['⚡'] * max(0, min(2, charges)))

def indicators(state, previous_health=None):
    danger = state['in_confrontation'] or state['fear'] >= 70
    critical = state['health'] <= 25
    damaged = previous_health is not None and state['health'] < previous_health
    return {'phone': {'signal': state['phone_signal'], 'vibrating': state['phone_vibrating'],
                      'save_available': False},
            'heart': {'health': state['health'], 'fear': state['fear'], 'danger': danger,
                      'critical': critical, 'damaged': damaged,
                      'rate_hint': 110 if danger or critical else 70,
                      'color': '#d87670' if critical or damaged else '#b99b87'}}
