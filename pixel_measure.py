# TODO:
# ! Record mouse positions after each click.
# ! Calculate the distance after two clicks.
# ! Determine the ratio between the distances.
# ! Features:
# ? Freeze the screen (like Snipping Tool does)
# ? Add a toggle display for showing the click positions
# ?  (may require freezing the screen as an image)
# ? Allow zoom-in


from pynput.mouse import Listener as m_Listener
from pynput.keyboard import Listener as kb_Listener
from pynput.keyboard import Key
import logging

# Set up the logger for info printouts
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Establish the key to be held during mouse pointer location measurement.
hotkey = Key.shift


class Measurements():
    # Global position list of tuples
    pos = []

    # Global state for whether points are being recorded
    is_active = True


def on_click(x, y, button, pressed):
    """ When the mouse is clicked, record the cursor position. """
    global Measurements

    # Break out if a full click (down and up) does not occur
    if not pressed:
        return True

    # Break out if the button pressed is not the left mouse button

    logging.info(f"On-click point: ({x}, {y})")

    # Add the point to the list of positions
    Measurements.pos.append((x, y))


def on_press(key):
    """ When the shift key is pressed and held, turn on the active recording
        of the mouse position on each click.
    """
    global Measurements
    if key == hotkey and not Measurements.is_active:
        logging.info("Shift is being pressed.")
        Measurements.is_active = True


def on_release(key):
    """ When the shift key is released, turn off the active recording of the
        mouse position on each click.
    """
    global Measurements
    if key == hotkey:
        logging.info("Shift was released.")
        Measurements.is_active = False


def main():
    # Open up the mouse and keyboard event listeners
    with m_Listener(on_click=on_click) as listener:
        with kb_Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()


def compute_distance(pos: list) -> float or bool:
    """ Computes the distance between each point in the list sequentially.
        Returns the sum of the points. If the computation was not successful,
        it returns a False value.
    """
    if len(pos) <= 1:
        print("Big mistake buddy. You need TWO or more points selected.")
        return False
    else:
        # Compute distance
        distance = 0
        for ind, point in enumerate(pos):
            if ind + 1 >= len(pos):
                break
            x1, y1 = point
            x2, y2 = pos[ind + 1]
            logging.info(f"Distance points: ({x1}, {y1}), ({x2},{y2})")
            distance += ((y2 - y1)**2 + (x2 - x1)**2)**0.5

        return distance


if __name__ == '__main__':
    main()
