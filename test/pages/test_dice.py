# pylint: disable=C

from kniffel.windows.game_window.dice import *

from unittest import TestCase

ONE_DICE = ["---------", "!       !", "!   ¤   !", "!       !", "---------"]


class DiceTest(TestCase):
    def __init__(self, method_name='runTest'):
        super().__init__(method_name)
        self.window: curses.window = None
        self.ds: DiceSet = None

    def setUp(self):
        curses.initscr()
        curses.start_color()
        common.init_colors()
        [max_y, max_x] = DiceSet.get_required_size()
        curses.resize_term(max_y, max_x)
        self.window = curses.newwin(max_y, max_x, 0, 0)
        self.ds = DiceSet(self.window)

    def tearDown(self) -> None:
        curses.endwin()

    def test_display(self):
        [max_y, max_x] = DiceSet.get_required_size()
        self.ds.set_dice([1, 1, 1, 1, 1])
        self.ds.handle_input('d')
        lines = []
        for y in range(max_y):
            chars = []
            for x in range(max_x):
                chars.append(chr(self.window.inch(y, x) & 0xFF))
            line = "".join(chars)
            if line.strip() == "":
                continue
            lines.append(line.strip())
        self.assertEqual(ONE_DICE * 5, lines)

    def test_handle_arrow_down(self):
        self.ds.handle_input(curses.KEY_DOWN)
        self.assertEqual(1, self.ds.selected,
                         "After pressing arrow down, second dice should be selected")

    def test_handle_arrow_up(self):
        self.ds.handle_input(curses.KEY_UP)
        self.assertEqual(4, self.ds.selected,
                         "After pressing arrow up 5 dice should be selected ")
        self.ds.handle_input(curses.KEY_UP)
        self.assertEqual(3, self.ds.selected,
                         "After pressing arrow up 4 dice should be selected ")

    def test_handle_roll(self):
        old_dice = self.ds.get_dice()
        self.ds.roll(8)
        new_dice = self.ds.get_dice()
        for i in range(len(old_dice)):
            if old_dice[i] != new_dice[i]:
                return
        raise AssertionError("Dice should change with re-roll")

    def lock_all_dice(self):
        self.ds.lock_dice(0, True)
        self.ds.lock_dice(1, True)
        self.ds.lock_dice(2, True)
        self.ds.lock_dice(3, True)
        self.ds.lock_dice(4, True)

    def test_handle_lock_roll(self):
        self.lock_all_dice()
        old_dice = self.ds.get_dice()
        self.ds.roll(8)
        new_dice = self.ds.get_dice()
        self.assertListEqual(old_dice, new_dice,
                             "Locked dice should not be rolled")

    def enter_and_select_next(self):
        self.ds.handle_input(curses.KEY_ENTER)
        self.ds.handle_input(curses.KEY_DOWN)

    def test_lock_functionality(self):
        for i in range(5):
            self.enter_and_select_next()
        for i in range(5):
            self.assertTrue(self.ds.is_locked(i),
                            "Dice should be locked")
        for i in range(5):
            self.enter_and_select_next()
        for i in range(5):
            self.assertFalse(self.ds.is_locked(i),
                             "Dice should not be locked")
