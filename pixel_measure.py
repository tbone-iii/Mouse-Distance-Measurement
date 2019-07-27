# TODO:
# Record mouse positions after each click.
# Calculate the distance after two clicks.
# ! Determine the ratio between the distances.
# Features:
# ? Freeze the screen (like Snipping Tool does)
# ? Add a toggle display for showing the click positions
# ?  (may require freezing the screen as an image)
# ? Allow zoom-in


import pynput.mouse
from pynput.keyboard import Key, Listener
import logging

# Set up the logger for info printouts
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Disable logger for live use
logger.propagate = False

# Establish the key to be held during mouse pointer location measurement.
HOTKEY = Key.shift
BREAKOUT_KEY = Key.esc

print(f"Press the '{str(BREAKOUT_KEY)[4:]}' key to break out.")

# Establish the mouse button to use for point measurement
MOUSE_KEY = pynput.mouse.Button.left


class Measurements():
    # Position list of tuples
    pos = []

    # State for whether points are being recorded
    is_active = False

    # List of distances calculated
    distances = []

    @staticmethod
    def append(point: (int, int)) -> None:
        """ Appends a point to the list of positions if appropriate. """
        if Measurements.is_active:
            Measurements.pos.append(point)
            logging.info(f"\tAdded point: ({point[0]}, {point[1]})")

    @staticmethod
    def compute_distance() -> None:
        """ Computes the distance across the list of points in "pos". """
        distance = compute_distance_list(Measurements.pos)
        if distance:
            Measurements.distances.append(distance)
            print(f"Distance: {distance: <3.2f} px")
            logging.info(f" DISTANCE: {distance: <3.2f} px")
        # Reset the "pos" list of points to empty
        Measurements.pos = []

    @staticmethod
    def compute_ratio() -> float or bool:
        """ Computes the ratio of the previous two distances. """
        distances = Measurements.distances
        if len(distances) < 2:
            return False
        else:
            ratio = distances[-2]/distances[-1]
            print(f"Ratio: {ratio: .2f}")
            return ratio


def on_click(x, y, button, pressed):
    """ When the mouse is clicked, record the cursor position. """
    global Measurements

    # Break out if a full click (down and up) does not occur
    if not pressed:
        return True
    # Break out if the button pressed is not the desired mouse button
    elif button is not MOUSE_KEY:
        return True

    logging.info(f" On-click point: ({x}, {y})")

    # Add the point to the list of positions
    Measurements.append((x, y))


def on_press(key):
    """ When the shift key is pressed and held, turn on the active recording
        of the mouse position on each click.
    """
    global Measurements
    if (key == HOTKEY and not Measurements.is_active):
        logging.info(" Shift is being pressed.")
        Measurements.is_active = True

    # Terminate listener if the specified escape key is pressed
    if (key == BREAKOUT_KEY):
        return False


def on_release(key):
    """ When the shift key is released, turn off the active recording of the
        mouse position on each click.
    """
    global Measurements
    if key == HOTKEY:
        logging.info(" Shift was released.")
        Measurements.is_active = False

        # Compute the distance of the recorded points
        Measurements.compute_distance()

        # Compute the ratio between the previous distances
        Measurements.compute_ratio()


def main():
    # Open up the mouse and keyboard event listeners
    with pynput.mouse.Listener(on_click=on_click) as listener:
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()


def compute_distance_list(pos: list) -> float or bool:
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
            logging.info(f" Distance points: ({x1}, {y1}), ({x2},{y2})")
            distance += ((y2 - y1)**2 + (x2 - x1)**2)**0.5

        return distance


if __name__ == '__main__':
    main()
