"""Verificação opcional com janela real: python visual_smoke.py."""
import unittest
from test_visual_commands import VisualCommandTests
import test_visual_ux
import test_inventory_window
import test_inventory_overlay
import test_phase44
import test_phase45
import test_phase451
import test_phase452


def main():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(VisualCommandTests)
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test_visual_ux.VisualUXTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test_inventory_window.InventoryWindowTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test_inventory_overlay.InventoryOverlayTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test_phase44.DocumentPanelTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test_phase45.VisualInvestigationTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test_phase451.NaturalInterfaceTests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test_phase452.SystemsInterfaceTests))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.skipped:
        raise SystemExit("Verificação gráfica não concluída: Tk/display indisponível.")
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    main()
